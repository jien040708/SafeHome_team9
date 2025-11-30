class Siren:
    def __init__(self, device_id):
        self.device_id = device_id
        self.is_active = False

    def activate(self):
        if not self.is_active:
            self.is_active = True
            siren_message = f"🚨 [SIREN] {self.device_id} WEE-WOO-WEE-WOO! 🚨"
            print(siren_message)

    def deactivate(self):
        if self.is_active:
            self.is_active = False
            silence_message = f"[SIREN] {self.device_id} Silenced."
            print(silence_message)