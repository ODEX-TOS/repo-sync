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
import time
from ..base import Runner
from ..persist import Persist, load
from ..log import *
from ..config import *


class Info(Runner):
    name = "info"

    def __init__(self):
        self.persist: Persist = load()


    def arg(self, parser: argparse.ArgumentParser) -> None:
        parser.add_parser("info")

    
    def run_command(self, namespace: argparse.Namespace) -> None:
        local_time = time.ctime(self.persist.modification_time)

        time_left = time.strftime('%H:%M:%S', time.gmtime(RING_LEVEL_TIMINGS[self.persist.ring]))

        info("Repository ring {}".format(self.persist.ring))
        print("")
        info("\tLast sync: \t\t\t{}".format(local_time))
        info("\tRing {} max sync timeout:\t{}".format(self.persist.ring, time_left))