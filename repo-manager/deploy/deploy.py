#MIT License
#
#Copyright (c) 2020 Meyers Tom
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import argparse
import subprocess
from ..base import Runner
from ..config import *
from ..log import *
from ..persist import save, create_data_dir, Persist

from ..sync.sync import Sync


class Deploy(Runner):
    name = "deploy"

    def arg(self, parser: argparse.ArgumentParser) -> None:
        subparser = parser.add_parser("deploy")

        subparser.add_argument('--type','-t', help='The type of deployment', choices=["docker", "host"], default=DEPLOY_TYPE)
        subparser.add_argument('--path','-p', help='Where on the host to store the repo', type=str, default=DEPLOY_PATH)
        subparser.add_argument('--backend','-b', help='The type of software to use to host the repository', choices=["nginx", "traefik"], default=DEPLOY_BACKEND)
        subparser.add_argument('--domain','-d', help='The domain to use to generate a TLS certificate for', type=str, default=DEPLOY_DOMAIN)
        subparser.add_argument('--external-traefik','-e', help='The docker network name in case traefik is selected', type=str)
        subparser.add_argument('--ring','-r', help='The ring level to use', type=int, default=RING_LEVEL)

    def run_command(self, namespace: argparse.Namespace) -> None:
        # verify that if traefik is selected that the --external-traefik exists
        if namespace.backend == "traefik":
            if namespace.external_traefik == None:
                error("Specify the --external-traefik option")
                exit(1)

        # backend should be nginx if the type is host
        if namespace.backend != "nginx" and  namespace.type == "host":
            error("Only nginx is supported when using the host type")
            exit(1)

        if namespace.type == "host" and namespace.path == None:
            error("Please specify using the --path flag where to save the data")
            exit(1)

        if not namespace.ring in VALID_RING_LEVELS:
            error("{} is not a valid ring level".format(namespace.ring))
            error("Choose one of the following: {} ring levels".format(VALID_RING_LEVELS))
            exit(1)

        if namespace.type == "host":
            self.__host(namespace)
        elif namespace.type == "docker":
            self.__docker(namespace)

    def save(self, namespace: argparse.Namespace) -> None:
        persist = Persist()

        persist.type = namespace.type
        persist.ring = RING_LEVEL
        persist.domain = namespace.domain
        persist.backend = namespace.backend
        persist.path = namespace.path

        persist.update_time()

        save(persist)

    def sync(self, namespace: argparse.Namespace) -> None:
        # now we should sync the repository data using the sync command
        sync = Sync()
        sync.path = namespace.path

        # let's create a mock to sync to the host dir
        mock = argparse.Namespace(ring=RING_LEVEL)
        
        # sync the database
        sync.run_command(mock)

        self.save(namespace)

    def __host(self, namespace: argparse.Namespace) -> None:
        info("You are responsible for generating tls certificates and renewing them")
        create_data_dir(namespace.path)
        self.sync(namespace)

    def __docker_traefik(self, namespace: argparse.Namespace) -> None:
        info("You are responsible for generating tls certificates and renewing them")
        info("See https://doc.traefik.io/traefik/https/tls/")

        compose = """version: '3'

services:
 repo:
  image: nginx:alpine
  volumes:
    - {}:/usr/share/nginx/html
  labels:
      - "traefik.enable=true"
      # HTTPS Rules
      - "traefik.http.routers.tos_repo_SSL.rule=Host(`{}`)"
      - "traefik.http.routers.tos_repo_SSL.entrypoints=https"
      - "traefik.http.routers.tos_repo_SSL.tls.certresolver=letsencrypt"
      - "traefik.http.routers.tos_repo_SSL.tls=true"
      - "traefik.http.services.tos_repo_SSL.loadbalancer.server.port=80"
      # HTTP
      - "traefik.http.routers.tos_repo.rule=Host(`{}`)"
      - "traefik.http.routers.tos_repo.entrypoints=http"
      - "traefik.http.middlewares.https-redirect.redirectscheme.scheme=https"
      - "traefik.http.routers.tos_repo.middlewares=https-redirect"

  networks:
    - {}
  restart: unless-stopped

networks:
  {}:
     external: true
""".format(namespace.path, namespace.domain, namespace.domain, namespace.external_traefik)

        # Let's create the file
        file = DOCKER_COMPOSE_DIR + '/docker-compose.yml'
        compose_file = open(file, 'w')
        compose_file.write(compose)
        compose_file.close()

        # start the container :-)
        subprocess.run(["docker-compose", "-f", file, "up", "-d"])

        warn("The traefik labels might not be what you want, if that is the case, modify them here: {} and restart the containers".format(file))

        # now that it is up and running, start the sync
        self.sync(namespace)

    def __docker_nginx(self, namespace: argparse.Namespace) -> None:
        info("Nginx will automatically refresh tls certificates")

        compose = """
version: "3"
services:
  repo:
    restart: unless-stopped
    image: jwilder/nginx-proxy:latest
    volumes:
     - ./certs:/etc/nginx/certs
     - /var/run/docker.sock:/tmp/docker.sock:ro
     - ./conf.d:/etc/nginx/conf.d
     - vhost:/etc/nginx/vhost.d
     - {}:/usr/share/nginx/html
    environment:
      - VIRTUAL_HOST={}
      - LETSENCRYPT_HOST={}
    ports:
     - "80:80"
     - "443:443"
    networks:
     - nginx-proxy
    labels:
      - com.github.jrcs.letsencrypt_nginx_proxy_companion.nginx_proxy

  letsencrypt:
    restart: always
    image: jrcs/letsencrypt-nginx-proxy-companion:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./certs:/etc/nginx/certs
      - vhost:/etc/nginx/vhost.d
      - {}:/usr/share/nginx/html
volumes:
  vhost:
networks:
  nginx-proxy:
""".format(namespace.path, namespace.domain,namespace.domain, namespace.path)

        # Let's create the file
        file = DOCKER_COMPOSE_DIR + '/docker-compose.yml'
        compose_file = open(file, 'w')
        compose_file.write(compose)
        compose_file.close()

        # start the container :-)
        subprocess.run(["docker-compose", "-f", file, "up", "-d"])

        # now that it is up and running, start the sync
        self.sync(namespace)

    def __docker(self, namespace: argparse.Namespace) -> None:
        create_data_dir(DOCKER_COMPOSE_DIR)
        if namespace.backend == "traefik":
            self.__docker_traefik(namespace)
        elif namespace.backend == "nginx":
            self.__docker_nginx(namespace)