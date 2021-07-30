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
import tempfile
import random
import shutil
import os
import subprocess
import urllib.request as request
from ..base import Runner
from ..config import *
from ..log import *
from ..persist import Persist, create_data_dir, load


class Sync(Runner):
    name = "sync"

    def __init__(self):
        self.persist: Persist = load()
        self.path = self.persist.path


    def arg(self, parser: argparse.ArgumentParser) -> None:
        subparser = parser.add_parser("sync")
        subparser.add_argument("--ring", "-r", nargs=1, help="Specify the ring level to use", type=int, default=RING_LEVEL)

    def create_tmp_dir(self) -> str:
        return tempfile.mkdtemp()

    def remove_tmp_dir(self, dir: str) -> None:
        info("Cleaning up")
        shutil.rmtree(dir)
        info("Done Cleaning up")
    
    def fetch_upstream_url(self, ring: int) -> str:
        info("Fetching upstream server")
        # Ring one should never sync (As it is the root)
        # Ring two should sync from repo.odex.be (The root)
        if ring == 2:
            info("Upstream ring {} server is {}".format(ring - 1, "https://repo.odex.be"))
            return "https://repo.odex.be"
        
        # in all other cases we should sync from a ring two repo
        ring_url = RING_DATA_URL + str(ring)

        # fetch the data from the url
        response = request.urlopen(ring_url)
        servers = response.read().decode('utf-8').splitlines()

        # return a random server (Primitive loadbalancer) from ring 2
        picked = random.choices(servers).strip()
        info("Upstream ring {} server is {}".format(ring - 1, picked))
        return picked


    def __download_db_file(self, tmp_dir:str, base_url: str, name: str) -> str:
        response = request.urlopen(base_url + '/' + name)
        db_data = response.read()

        file = open(tmp_dir + '/' + name, 'wb')
        file.write(db_data)
        file.close()

        response_sig = request.urlopen(base_url + '/' + name + '.sig')
        db_data_sig = response_sig.read()

        file_sig = open(tmp_dir + '/' + name + '.sig', 'wb')
        file_sig.write(db_data_sig)
        file_sig.close()

        return tmp_dir + '/' + name


    def download_database(self, tmp_dir:str, base_url: str) -> str:
        info("Downloading upstream database")
        self.__download_db_file(tmp_dir, base_url, "tos.files.tar.gz")
        
        return self.__download_db_file(tmp_dir, base_url, 'tos.db.tar.gz')

    def generate_download_list(self, database: str) -> list:
        info("Extracting database {}".format(database))
        result = subprocess.run(["tar", "-ztvf", database], capture_output=True).stdout.decode("utf-8").splitlines()

        items = []
        for line in result:
            ln = line.split()
            items.append(ln[-1])

        info("Generating packages")

        return filter(lambda item: not item.endswith("/desc"), items)

    def __download_from_arch(self, package: str, path: str, base_url: str, arch:str) -> None:
        name = "{}-{}.pkg.tar.{}".format(package.replace('/',''), arch, COMPRESSION)
        name_sig = name + '.sig'

        info("Downloading: {}".format(name))


        response = request.urlopen("{}/{}".format(base_url, name))
        data = response.read()

        file = open(path + name, 'wb')
        file.write(data)
        file.close()

        response_sig = request.urlopen("{}/{}".format(base_url, name_sig))
        data_sig = response_sig.read()

        file_sig = open(path + name_sig, 'wb')
        file_sig.write(data_sig)
        file_sig.close()

    def download_from_package(self, package: str, path: str, base_url: str) -> None:
        try:
            self.__download_from_arch(package, path, base_url, ARCH)
        except:
            self.__download_from_arch(package, path, base_url, "any")

    def download_from_packages(self, packages: list, path: str, base_url: str) -> None:
        for package in packages:
            self.download_from_package(package, path, base_url)

    def symlink(self, src: str, dst: str) -> None:
        try:
            os.symlink(src, dst)
        except FileExistsError:
            pass
    
    def run_command(self, namespace: argparse.Namespace) -> None:

        if not namespace.ring in VALID_RING_LEVELS:
            error("{} is not a valid ring level".format(namespace.ring))
            error("Choose one of the following: {} ring levels".format(VALID_RING_LEVELS))
            exit(1)

        tmp = self.create_tmp_dir()

        base_url = self.fetch_upstream_url(namespace.ring)
        
        db = self.download_database(tmp, base_url)
        packages = self.generate_download_list(db)

        self.download_from_packages(packages, self.path + '/', base_url)

        shutil.move(db, self.path + '/tos.db.tar.gz')
        shutil.move(db + '.sig', self.path + '/tos.db.tar.gz.sig')

        info("Resolving symlinks")

        self.symlink(self.path + '/tos.db.tar.gz', self.path + '/tos.db')
        self.symlink(self.path + '/tos.db.tar.gz.sig', self.path + '/tos.db.sig')
        self.symlink(self.path + '/tos.files.tar.gz', self.path + '/tos.files')
        self.symlink(self.path + '/tos.files.tar.gz.sig', self.path + '/tos.files.sig')

        self.remove_tmp_dir(tmp)