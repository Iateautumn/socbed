from attacks import Attack, AttackInfo, AttackOptions


class FingerprintAttackOptions(AttackOptions):
    target: str = "Target URL"
    aggression: str = "Whatweb Search Aggression"

    def _set_defaults(self):
        self.target = "http://172.18.0.2/laravel/"
        self.aggression = "3"


class FingerprintAttack(Attack):
    info = AttackInfo(
        name="info_url_fingerprint",
        description="Web fingerprint information gather")
    options_class = FingerprintAttackOptions

    def run(self):
        with self.wrap_ssh_exceptions():
            self.exec_commands_on_target(([
                f"curl {self.options.target}",
                f"whatweb --aggression {self.options.aggression} {self.options.target}",
            ]))
