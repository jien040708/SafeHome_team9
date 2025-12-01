"""
Adapter that wires the virtual SafeHome control panel keypad into the
application login flow.  The teaching staff provided a Tkinter
implementation (`DeviceControlPanelAbstract`) that emulates the
physical keypad, LEDs, and small text display.  This wrapper owns the
keypad interactions (digits, `*`, `#`) and translates them into
Control-Panel login attempts via the existing presenters.
"""

from __future__ import annotations

from typing import Optional

try:
    from virtual_device_v4.device.device_control_panel_abstract import (
        DeviceControlPanelAbstract,
    )
except ModuleNotFoundError:  # pragma: no cover - fallback when v4 is absent
    from virtual_device_v3.device.device_control_panel_abstract import (  # type: ignore
        DeviceControlPanelAbstract,
    )


class SafeHomeControlPanelDevice(DeviceControlPanelAbstract):
    """Bridge between the keypad device and the ControlPanel login view."""

    # Telephone multi-tap style mapping so that alphabetic user IDs (e.g. admin)
    # can be entered with a numeric keypad.
    LETTER_MAP = {
        "1": ["1"],
        "2": ["a", "b", "c", "2"],
        "3": ["d", "e", "f", "3"],
        "4": ["g", "h", "i", "4"],
        "5": ["j", "k", "l", "5"],
        "6": ["m", "n", "o", "6"],
        "7": ["p", "q", "r", "s", "7"],
        "8": ["t", "u", "v", "8"],
        "9": ["w", "x", "y", "z", "9"],
        "0": ["0"],
    }

    def __init__(self, master, login_view):
        super().__init__(master=master)
        self.login_view = login_view
        self.mode: str = "user"  # "user" or "password"
        self.user_buffer: str = ""
        self.password_buffer: str = ""
        self.last_digit: Optional[str] = None
        self.locked: bool = False

        self.set_security_zone_number(1)
        self.set_powered_led(True)
        self.set_armed_led(False)
        self.set_display_not_ready(False)
        self._update_display()

        # Keep device window focused near the root window
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self._ignore_close)
        self.lift()

    # ------------------------------------------------------------------ #
    # Public helpers invoked by the LoginView
    # ------------------------------------------------------------------ #
    def notify_lock(self):
        self.locked = True
        self.set_display_not_ready(True)
        self.set_display_short_message1("CONTROL PANEL LOCKED")
        self.set_display_short_message2("Wait for admin")

    def notify_unlock(self):
        self.locked = False
        self.set_display_not_ready(False)
        self.user_buffer = ""
        self.password_buffer = ""
        self.mode = "user"
        self.last_digit = None
        self._update_display()

    # ------------------------------------------------------------------ #
    # Button handlers
    # ------------------------------------------------------------------ #
    def button0(self):
        self._handle_digit("0")

    def button1(self):
        self._handle_digit("1")

    def button2(self):
        self._handle_digit("2")

    def button3(self):
        self._handle_digit("3")

    def button4(self):
        self._handle_digit("4")

    def button5(self):
        self._handle_digit("5")

    def button6(self):
        self._handle_digit("6")

    def button7(self):
        self._handle_digit("7")

    def button8(self):
        self._handle_digit("8")

    def button9(self):
        self._handle_digit("9")

    def button_star(self):
        if self.locked:
            return
        if self.mode == "user":
            if self.user_buffer:
                self.user_buffer = self.user_buffer[:-1]
        else:
            if self.password_buffer:
                self.password_buffer = self.password_buffer[:-1]
        self.last_digit = None
        self._sync_entries()
        self._update_display()

    def button_sharp(self):
        if self.locked:
            return

        if self.mode == "user":
            if not self.user_buffer:
                self.set_display_short_message2("User ID required")
                return
            self.mode = "password"
            self.last_digit = None
            self.set_display_short_message1("Enter Password (# to submit)")
            self.set_display_short_message2("")
        else:
            if not self.password_buffer:
                self.set_display_short_message2("Password required")
                return
            self._attempt_login()

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _handle_digit(self, digit: str):
        if self.locked:
            return

        if self.mode == "user":
            self._handle_user_digit(digit)
        else:
            self._handle_password_digit(digit)

        self._sync_entries()
        self._update_display()

    def _handle_user_digit(self, digit: str):
        options = self.LETTER_MAP.get(digit)
        if not options:
            return

        if self.last_digit == digit and self.user_buffer:
            current_char = self.user_buffer[-1]
            try:
                idx = options.index(current_char)
            except ValueError:
                idx = -1
            next_char = options[(idx + 1) % len(options)]
            self.user_buffer = f"{self.user_buffer[:-1]}{next_char}"
        else:
            self.user_buffer += options[0]
        self.last_digit = digit

    def _handle_password_digit(self, digit: str):
        if len(self.password_buffer) >= 16:
            return
        self.password_buffer += digit
        self.last_digit = digit

    def _attempt_login(self):
        outcome = self.login_view.submit_login_from_device(
            self.user_buffer.lower(),
            self.password_buffer,
        )
        if outcome.success:
            self.set_display_short_message1("Access granted")
            self.set_display_short_message2("Welcome to SafeHome")
            self.set_armed_led(True)
            self.mode = "user"
            self.user_buffer = ""
            self.password_buffer = ""
        else:
            self.set_armed_led(False)
            primary = outcome.alert_title or "Login failed"
            secondary = (
                outcome.alert_message
                or outcome.status_text
                or "Please try again"
            )
            self.set_display_short_message1(primary[:32])
            self.set_display_short_message2(secondary[:32])
            self.password_buffer = ""
            # stay in password mode so the user can retry quickly
        self.last_digit = None
        self._sync_entries()
        self._update_display()

    def _sync_entries(self):
        # Reflect the keypad input in the disabled text fields for clarity
        self.login_view.update_user_input(self.user_buffer.lower())
        self.login_view.update_password_input(self.password_buffer)

    def _update_display(self):
        if self.mode == "user":
            label = "Enter User ID (# to confirm)"
            content = self.user_buffer.upper() or "(blank)"
        else:
            label = "Enter Password (# to submit)"
            content = "*" * len(self.password_buffer) or "(blank)"

        if self.locked:
            self.set_display_short_message1("CONTROL PANEL LOCKED")
            self.set_display_short_message2("Wait for admin")
            return

        self.set_display_short_message1(label)
        self.set_display_short_message2(content)

    def _ignore_close(self):
        """Keep the device window alive; lift it instead of destroying."""
        self.deiconify()
        self.lift()
