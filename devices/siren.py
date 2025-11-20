class Siren:
    def __init__(self, device_id):
        self.device_id = device_id
        self.is_active = False

    def activate(self):
        if not self.is_active:
            self.is_active = True
            print(f"🚨 [SIREN] {self.device_id} WEE-WOO-WEE-WOO! 🚨")

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            print(f"[SIREN] {self.device_id} Silenced.")