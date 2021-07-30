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
from ..persist import Persist, load

class Systemctl(Runner):
    name = "systemctl"

    def __init__(self):
        self.persist: Persist = load()

    def __create_timer_str(self) -> str:
        lookup_timer = {
            1: "1", # ring one should always sync
            2: "6h", # ring two should sync every 6 hours
            3: "1d" # ring three should sync daily
        }

        lookup_random_timer = {
            1: "1", # ring one should always sync
            2: "30m", # Randomly sync every 30 minutes (To decrease peak loads)
            3: "1h" # Randomly sync every hour
        }
        return """[Unit]
Description=Run tos repo sync

[Timer]
OnBootSec=15min
OnUnitActiveSec={}
RandomizedDelaySec={}
Persistent=true

[Install]
WantedBy=timers.target
        """.format(lookup_timer[self.persist.ring], lookup_random_timer[self.persist.ring])

    def __create_service_sync(self) -> str:
        return """[Unit]
Description=Sync the tos repo
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/repo-manager sync
"""

    def arg(self, parser: argparse.ArgumentParser) -> None:
        subparser = parser.add_parser("systemctl")

    def run_command(self, namespace: argparse.Namespace) -> None:
        
        timer_payload = self.__create_timer_str()
        timer_service = self.__create_service_sync()

        # let's update the systemctl data
        service = open("/usr/lib/systemd/system/tos-repo.service", "w")
        service.write(timer_service)
        service.close()

        timer = open("/usr/lib/systemd/system/tos-repo.timer", "w")
        timer.write(timer_payload)
        timer.close()

        # now let's reload the daemon
        subprocess.call(["systemctl", "daemon-reload"])

        # finally enable the system timer
        subprocess.call(["systemctl", "enable", "--now", "tos-repo.timer"])
