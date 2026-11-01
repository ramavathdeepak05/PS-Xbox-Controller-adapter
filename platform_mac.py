"""macOS controller reading and keystrokes. Imported only on a Mac."""
import ctypes
import subprocess

# macOS virtual key codes from Events.h. Ctrl stays Control; Cmd is Command.
KEY_CODES = {
    "A": 0x00, "S": 0x01, "D": 0x02, "F": 0x03, "H": 0x04, "G": 0x05,
    "Z": 0x06, "X": 0x07, "C": 0x08, "V": 0x09, "B": 0x0B, "Q": 0x0C,
    "W": 0x0D, "E": 0x0E, "R": 0x0F, "Y": 0x10, "T": 0x11,
    "1": 0x12, "2": 0x13, "3": 0x14, "4": 0x15, "6": 0x16, "5": 0x17,
    "9": 0x19, "7": 0x1A, "8": 0x1C, "0": 0x1D,
    "O": 0x1F, "U": 0x20, "I": 0x22, "P": 0x23, "L": 0x25, "J": 0x26,
    "K": 0x28, "N": 0x2D, "M": 0x2E,
    "SPACE": 0x31, "ENTER": 0x24, "RETURN": 0x24, "TAB": 0x30,
    "BACKSPACE": 0x33, "ESC": 0x35, "ESCAPE": 0x35,
    "CMD": 0x37, "SHIFT": 0x38, "ALT": 0x3A, "CTRL": 0x3B,
    "LEFT": 0x7B, "RIGHT": 0x7C, "DOWN": 0x7D, "UP": 0x7E,
}

# SDL game-controller buttons, mapped onto the names the Windows backend already uses.
_SDL_BUTTONS = {
    0: "BUTTON_1",   # A / Cross
    1: "BUTTON_2",   # B / Circle
    2: "BUTTON_0",   # X / Square
    3: "BUTTON_3",   # Y / Triangle
    4: "BUTTON_8",   # Back / View / Share
    5: "BUTTON_12",  # Guide / PlayStation
    6: "BUTTON_9",   # Start / Menu / Options
    7: "BUTTON_10",  # Left stick click
    8: "BUTTON_11",  # Right stick click
    9: "BUTTON_4",   # LB / L1
    10: "BUTTON_5",  # RB / R1
    11: "DPAD_UP",
    12: "DPAD_DOWN",
    13: "DPAD_LEFT",
    14: "DPAD_RIGHT",
    20: "BUTTON_13",  # Touchpad
}

_AXIS_LEFT_X = 0
_AXIS_LEFT_Y = 1
_AXIS_RIGHT_X = 2
_AXIS_RIGHT_Y = 3
_AXIS_TRIGGER_LEFT = 4
_AXIS_TRIGGER_RIGHT = 5
_TRIGGER_THRESHOLD = 8000

try:
    import pygame
    from pygame._sdl2.controller import Controller
except ImportError:
    pygame = None
    Controller = None

_core_graphics = None
_core_foundation = None


def _load_quartz():
    global _core_graphics, _core_foundation
    if _core_graphics is not None:
        return
    _core_graphics = ctypes.cdll.LoadLibrary(
        "/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics"
    )
    _core_foundation = ctypes.cdll.LoadLibrary(
        "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
    )
    _core_graphics.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
    _core_graphics.CGEventCreateKeyboardEvent.argtypes = [ctypes.c_void_p, ctypes.c_uint16, ctypes.c_bool]
    _core_graphics.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
    _core_foundation.CFRelease.argtypes = [ctypes.c_void_p]


def send_key_event(key_code, is_down):
    """Post a key down or key up through Quartz. macOS delivers it only after Accessibility access."""
    if not key_code and key_code != 0:
        return
    _load_quartz()
    event = _core_graphics.CGEventCreateKeyboardEvent(None, key_code, bool(is_down))
    if not event:
        return
    _core_graphics.CGEventPost(0, event)  # kCGHIDEventTap
    _core_foundation.CFRelease(event)


def ensure_keyboard_access():
    """Open Accessibility settings when this process is not trusted to post keystrokes."""
    services = ctypes.cdll.LoadLibrary(
        "/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices"
    )
    services.AXIsProcessTrusted.restype = ctypes.c_bool
    if services.AXIsProcessTrusted():
        return
    print("Allow GamepadAdapter under System Settings -> Privacy & Security -> Accessibility.")
    print("Keys are not sent until that switch is on. Then quit the app and open it again.")
    subprocess.run(
        ["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"],
        check=False,
    )


def _family_from_name(name):
    lowered = (name or "").lower()
    if any(token in lowered for token in ("dualsense", "dualshock", "playstation", "sony", "ps5", "ps4", "ps3")):
        return "playstation"
    if any(token in lowered for token in ("xbox", "xinput", "x-box")):
        return "xbox"
    return "playstation"


class ControllerReader:
    """Reads Xbox and PlayStation pads through SDL's game-controller mapping."""

    def __init__(self):
        self.mode = None
        self.active_id = None
        self.device_name = "Detecting controller..."
        self._controller = None
        self._sdl_ready = False

    def _ensure_sdl(self):
        if pygame is None:
            return False
        if self._sdl_ready:
            return True
        import os
        os.environ.setdefault("SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS", "1")
        pygame.init()
        Controller.init()
        self._sdl_ready = True
        return True

    def _close_controller(self):
        if self._controller is not None:
            try:
                self._controller.quit()
            except Exception:
                pass
            self._controller = None

    def check_connection(self):
        if not self._ensure_sdl():
            self.mode = None
            self.device_name = "pygame is not installed, so controllers cannot be read"
            return False

        pygame.event.pump()
        chosen = None
        for index in range(Controller.get_count()):
            if Controller.is_controller(index):
                chosen = index
                break

        if chosen is None:
            self._close_controller()
            self.mode = None
            self.active_id = None
            self.device_name = "Disconnected: Please plug in an Xbox, PlayStation, or USB controller"
            return False

        if self._controller is None or self.active_id != chosen:
            self._close_controller()
            self._controller = Controller(chosen)
            self.active_id = chosen

        self.mode = "sdl"
        self.device_name = self._controller.name or f"Controller {chosen + 1}"
        return True

    def is_connected(self):
        return self.check_connection()

    def get_device_name(self):
        return self.device_name

    def get_family(self):
        return _family_from_name(self.device_name)

    def _stick(self, active_inputs, x_axis, y_axis, prefix, deadzone):
        # SDL stick Y is positive downward. Windows XInput Y is positive upward.
        x_value = self._controller.get_axis(x_axis)
        y_value = self._controller.get_axis(y_axis)
        if x_value < -deadzone:
            active_inputs.add(f"{prefix}_LEFT")
        elif x_value > deadzone:
            active_inputs.add(f"{prefix}_RIGHT")
        if y_value < -deadzone:
            active_inputs.add(f"{prefix}_UP")
        elif y_value > deadzone:
            active_inputs.add(f"{prefix}_DOWN")

    def read_inputs(self, deadzone=14000):
        if self.mode != "sdl" or self._controller is None:
            if not self.check_connection():
                return None
        else:
            pygame.event.pump()
            attached = getattr(self._controller, "attached", lambda: True)
            if not attached():
                if not self.check_connection():
                    return None

        active_inputs = set()
        for button, name in _SDL_BUTTONS.items():
            try:
                held = self._controller.get_button(button)
            except Exception:
                held = False
            if held:
                active_inputs.add(name)

        if self._controller.get_axis(_AXIS_TRIGGER_LEFT) > _TRIGGER_THRESHOLD:
            active_inputs.add("BUTTON_6")
        if self._controller.get_axis(_AXIS_TRIGGER_RIGHT) > _TRIGGER_THRESHOLD:
            active_inputs.add("BUTTON_7")

        self._stick(active_inputs, _AXIS_LEFT_X, _AXIS_LEFT_Y, "STICK", deadzone)
        self._stick(active_inputs, _AXIS_RIGHT_X, _AXIS_RIGHT_Y, "RSTICK", deadzone)
        return active_inputs
