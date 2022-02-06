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
from ..base import Runner
from ..persist import Persist, load
from ..log import *
from ..config import *
import urllib
import urllib.request
import json
import base64
from getpass import getpass


class Commit(Runner):
    name = "commit"

    def __init__(self):
        self.persist: Persist = load()

    def arg(self, parser: argparse.ArgumentParser) -> None:
        subparser = parser.add_parser("commit")


    def send_api_request(self, title, body, username, password) -> None:
        url = 'https://api.github.com/repos/{}/{}/issues'.format(ORG, REPO)
        data = {'title': title, body: 'body', 'labels': ["ring"]}
        login = base64.b64encode('{}:{}'.format(username, password).encode('utf-8'))

        jsondata = json.dumps(data).encode('utf-8')

        req = urllib.request.Request(url, data=jsondata)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header("Authorization", "Basic {}".format(login))   

        print(url)

        response = urllib.request.urlopen(req)

        print(response)

    def run_command(self, namespace: argparse.Namespace) -> None:
        info("Creating issue in {}".format(GITHUB_REPO))

        title = "Add ring level {} server for domain {}".format(self.persist.ring, self.persist.domain)
        description = "Verify that my server '{}' contains all requirements for the ring {}\nThus adding it as an official mirror".format(self.persist.domain, self.persist.ring)

        info("Title: {}".format(title))
        info("Description: {}".format(description))
        

        print('Please give your github credentials so we can create the issue')
        print("Username: ", end="")
        username = input()
        password = getpass()

        self.send_api_request(title, description, username, password)
