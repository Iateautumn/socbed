from attacks import Attack, AttackInfo, AttackOptions


class DirectoryDiscoveryAttackOptions(AttackOptions):
    target = "Target URL"

    def _set_defaults(self):
        self.target = "http://172.18.0.2/"


class DirectoryDiscoveryAttack(Attack):
    info = AttackInfo(
        name="info_directory_discovery",
        description="Web directory information discovery")
    options_class = DirectoryDiscoveryAttackOptions

    def run(self):
        with self.wrap_ssh_exceptions():
            self.exec_command_on_target(f"dirb {self.options.target} -r")
