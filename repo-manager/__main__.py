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

from .commit.commit import Commit
from .info.info import Info
from .sync.sync import Sync
from .systemctl.systemctl import Systemctl
from .deploy.deploy import Deploy

runners = {
    Commit.name: Commit(),
    Info.name: Info(),
    Sync.name: Sync(),
    Systemctl.name: Systemctl(),
    Deploy.name: Deploy()
}

parser = argparse.ArgumentParser("repo-manager", description="Manage your tos repository")

sub_parser = parser.add_subparsers(dest="command")

for name, runner in runners.items():
    runner.arg(sub_parser)

args = parser.parse_args()

if args.command == None:
    parser.print_help()
    exit(0)

runners[args.command].run_command(args)