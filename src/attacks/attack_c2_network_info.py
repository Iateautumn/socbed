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


class C2WindowsNetworkInfoAttackOptions(C2AttackOptions):
    pass


class C2WindowsNetworkInfoAttack(C2Attack):
    info = AttackInfo(
        name="c2_network_info",
        description="Collect windows network information")
    options_class = C2WindowsNetworkInfoAttackOptions
    handler = None

    def run(self):
        with self.check_printed("172.16.1.1"):
            with self.wrap_ssh_exceptions():
                self.ssh_client.connect_to_target()
                self.exec_commands_on_shell(self.commands)
                time.sleep(1)
                self.ssh_client.close()

    def _append_command(self):
        self.commands.extend([
            "shell",
            "ipconfig /all",
            "arp -a",
            "exit",
            "background"
        ])
