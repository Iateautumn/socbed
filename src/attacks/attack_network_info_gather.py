from attacks import Attack, AttackInfo, AttackOptions


class NetworkInfoGatherAttackOptions(AttackOptions):
    network = "Target Network"
    hosts = "Target Hosts"
    ports = "Target Ports"
    tool = "Network Information Gathering Tool Path"

    def _set_defaults(self):
        self.network = "172.18.0.0/16"
        self.hosts = "172.18.0.2"
        self.ports = "1-10000"
        self.tool = "/root/fscan"


class NetworkInfoGatherAttack(Attack):
    info = AttackInfo(
        name="info_network_gather",
        description="network information gather")
    options_class = NetworkInfoGatherAttackOptions

    def run(self):
        with self.wrap_ssh_exceptions():
            self.exec_commands_on_target(self.network_info_gather_commands())

    def network_info_gather_commands(self):
        tool = self.options.tool
        hosts = self.options.hosts
        ports = self.options.ports
        network = self.options.network
        return [
            "ip addr",
            f"chmod +x {tool}",
            f"{tool} -h {network} -m findnet",
            # f"{tool} -h {hosts} -m all -nobr -nopoc -noredis -p {ports}"
            f"{tool} -h {hosts} -m portscan -nobr -nopoc -noredis -p {ports}"
        ]
