"""Windows controller reading and keystrokes. Imported only on Windows."""
import sys

if sys.platform != "win32":
    KEY_CODES = {}
    ControllerReader = None

    def send_key_event(key_code, is_down):
        return None
else:
    import ctypes
    from ctypes import wintypes

    # --- Native Windows Libraries ---
    winmm = ctypes.windll.winmm
    user32 = ctypes.windll.user32

    # Load XInput (Xbox Controllers)
    xinput_dll = None
    for dll_name in ['xinput1_4.dll', 'xinput1_3.dll', 'xinput9_1_0.dll']:
        try:
            xinput_dll = ctypes.windll.LoadLibrary(dll_name)
            break
        except Exception:
            pass

    # --- XInput Structures ---
    class XINPUT_GAMEPAD(ctypes.Structure):
        _fields_ = [
            ('wButtons', wintypes.WORD),
            ('bLeftTrigger', ctypes.c_ubyte),
            ('bRightTrigger', ctypes.c_ubyte),
            ('sThumbLX', ctypes.c_short),
            ('sThumbLY', ctypes.c_short),
            ('sThumbRX', ctypes.c_short),
            ('sThumbRY', ctypes.c_short)
        ]

    class XINPUT_STATE(ctypes.Structure):
        _fields_ = [
            ('dwPacketNumber', wintypes.DWORD),
            ('Gamepad', XINPUT_GAMEPAD)
        ]

    # XInput Button Constants
    XINPUT_GAMEPAD_DPAD_UP = 0x0001
    XINPUT_GAMEPAD_DPAD_DOWN = 0x0002
    XINPUT_GAMEPAD_DPAD_LEFT = 0x0004
    XINPUT_GAMEPAD_DPAD_RIGHT = 0x0008
    XINPUT_GAMEPAD_START = 0x0010
    XINPUT_GAMEPAD_BACK = 0x0020
    XINPUT_GAMEPAD_LEFT_THUMB = 0x0040
    XINPUT_GAMEPAD_RIGHT_THUMB = 0x0080
    XINPUT_GAMEPAD_LEFT_SHOULDER = 0x0100
    XINPUT_GAMEPAD_RIGHT_SHOULDER = 0x0200
    XINPUT_GAMEPAD_A = 0x1000
    XINPUT_GAMEPAD_B = 0x2000
    XINPUT_GAMEPAD_X = 0x4000
    XINPUT_GAMEPAD_Y = 0x8000

    # --- WinMM / DirectInput Structures (PlayStation & Generic USB Gamepads) ---
    class JOYINFOEX(ctypes.Structure):
        _fields_ = [
            ('dwSize', wintypes.DWORD),
            ('dwFlags', wintypes.DWORD),
            ('dwXpos', wintypes.DWORD),
            ('dwYpos', wintypes.DWORD),
            ('dwZpos', wintypes.DWORD),
            ('dwRpos', wintypes.DWORD),
            ('dwUpos', wintypes.DWORD),
            ('dwVpos', wintypes.DWORD),
            ('dwButtons', wintypes.DWORD),
            ('dwButtonNumber', wintypes.DWORD),
            ('dwPOV', wintypes.DWORD),
            ('dwReserved1', wintypes.DWORD),
            ('dwReserved2', wintypes.DWORD)
        ]

    class JOYCAPSW(ctypes.Structure):
        _fields_ = [
            ('wMid', wintypes.WORD),
            ('wPid', wintypes.WORD),
            ('szPname', wintypes.WCHAR * 32),
            ('wXmin', wintypes.UINT),
            ('wXmax', wintypes.UINT),
            ('wYmin', wintypes.UINT),
            ('wYmax', wintypes.UINT),
            ('wZmin', wintypes.UINT),
            ('wZmax', wintypes.UINT),
            ('wNumButtons', wintypes.UINT),
            ('wPeriodMin', wintypes.UINT),
            ('wPeriodMax', wintypes.UINT),
            ('wRmin', wintypes.UINT),
            ('wRmax', wintypes.UINT),
            ('wUmin', wintypes.UINT),
            ('wUmax', wintypes.UINT),
            ('wVmin', wintypes.UINT),
            ('wVmax', wintypes.UINT),
            ('wCaps', wintypes.UINT),
            ('wMaxAxes', wintypes.UINT),
            ('wNumAxes', wintypes.UINT),
            ('wMaxButtons', wintypes.UINT),
            ('szRegKey', wintypes.WCHAR * 32),
            ('szOEMVxD', wintypes.WCHAR * 260)
        ]

    # --- Keyboard Input Structs for SendInput (Exact 40-byte 64-bit alignment) ---
    INPUT_KEYBOARD = 1
    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_SCANCODE = 0x0008
    KEYEVENTF_EXTENDEDKEY = 0x0001

    ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong

    class MOUSEINPUT(ctypes.Structure):
        _fields_ = [
            ('dx', wintypes.LONG),
            ('dy', wintypes.LONG),
            ('mouseData', wintypes.DWORD),
            ('dwFlags', wintypes.DWORD),
            ('time', wintypes.DWORD),
            ('dwExtraInfo', ULONG_PTR)
        ]

    class KEYBDINPUT(ctypes.Structure):
        _fields_ = [
            ('wVk', wintypes.WORD),
            ('wScan', wintypes.WORD),
            ('dwFlags', wintypes.DWORD),
            ('time', wintypes.DWORD),
            ('dwExtraInfo', ULONG_PTR)
        ]

    class HARDWAREINPUT(ctypes.Structure):
        _fields_ = [
            ('uMsg', wintypes.DWORD),
            ('wParamL', wintypes.WORD),
            ('wParamH', wintypes.WORD)
        ]

    class INPUT(ctypes.Structure):
        class _INPUT(ctypes.Union):
            _fields_ = [
                ('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT)
            ]
        _anonymous_ = ('_input',)
        _fields_ = [
            ('type', wintypes.DWORD),
            ('_input', _INPUT)
        ]

    # Virtual Key Codes
    VK_MAP = {
        'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
        'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
        'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F,
        'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
        'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59,
        'Z': 0x5A,
        '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
        '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
        'SPACE': 0x20, 'ENTER': 0x0D, 'RETURN': 0x0D, 'ESC': 0x1B,
        'ESCAPE': 0x1B, 'TAB': 0x09, 'SHIFT': 0x10, 'CTRL': 0x11,
        'ALT': 0x12, 'BACKSPACE': 0x08,
        'UP': 0x26, 'DOWN': 0x28, 'LEFT': 0x25, 'RIGHT': 0x27
    }

    EXTENDED_KEYS = {0x26, 0x28, 0x25, 0x27} # Up, Down, Left, Right arrow keys

    def send_key_event(vk_code, is_down):
        """Sends a hardware scancode keyboard event via Windows SendInput for browser game compatibility."""
        if not vk_code:
            return
        scan = user32.MapVirtualKeyW(vk_code, 0)
        flags = KEYEVENTF_SCANCODE
        if not is_down:
            flags |= KEYEVENTF_KEYUP
        if vk_code in EXTENDED_KEYS:
            flags |= KEYEVENTF_EXTENDEDKEY

        inp = INPUT()
        inp.type = INPUT_KEYBOARD
        inp.ki.wVk = 0 # wVk must be 0 when using KEYEVENTF_SCANCODE
        inp.ki.wScan = scan
        inp.ki.dwFlags = flags
        inp.ki.time = 0
        inp.ki.dwExtraInfo = 0

        user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))

    MODIFIER_NAMES = ("CTRL", "ALT", "SHIFT")

    def binding_key_names(key_str):
        """Split a binding such as 'CTRL+C' into known keys, modifiers first."""
        if not isinstance(key_str, str) or not key_str.strip():
            return []
        parts = []
        for raw in key_str.upper().split("+"):
            name = raw.strip()
            if name in VK_MAP and name not in parts:
                parts.append(name)
        mods = [name for name in MODIFIER_NAMES if name in parts]
        rest = [name for name in parts if name not in mods]
        return mods + rest

    # Default game mapping (Optimized for fighting & arcade games)
    DEFAULT_MAPPING = {
        # Movement
        "DPAD_UP": "W",          # Jump
        "DPAD_DOWN": "S",        # Crouch
        "DPAD_LEFT": "A",        # Move Left
        "DPAD_RIGHT": "D",       # Move Right
        "STICK_UP": "W",         # Analog Jump
        "STICK_DOWN": "S",       # Analog Crouch
        "STICK_LEFT": "A",       # Analog Move Left
        "STICK_RIGHT": "D",      # Analog Move Right
        "RSTICK_UP": "T",        # Right stick up -> Triangle
        "RSTICK_LEFT": "J",      # Right stick left -> Square
        "RSTICK_DOWN": "K",      # Right stick down -> Cross
        "RSTICK_RIGHT": "I",     # Right stick right -> Circle

        # Face Buttons
        "BUTTON_0": "J",         # Square [□] / Xbox X -> Punch
        "BUTTON_1": "K",         # Cross [X] / Xbox A -> Kick
        "BUTTON_2": "I",         # Circle [O] / Xbox B -> Grab
        "BUTTON_3": "T",         # Triangle [△] / Xbox Y -> Stage Select

        # Shoulder Buttons / Triggers
        "BUTTON_4": "M",         # L1 / LB -> Music
        "BUTTON_5": "L",         # R1 / RB -> Super
        "BUTTON_6": "SPACE",     # L2 / LT -> Super Alt / Space
        "BUTTON_7": "ENTER",     # R2 / RT -> Fight / Start Match

        # Center Buttons
        "BUTTON_8": "N",         # Select / Back / View -> Mute
        "BUTTON_9": "ESC",       # Start / Menu -> Pause Game

        # Stick Clicks
        "BUTTON_10": "1",        # L3 (Left Stick Click)
        "BUTTON_11": "2",        # R3 (Right Stick Click)
        "BUTTON_12": "",
        "BUTTON_13": ""
    }

    CONTROLLER_LABELS = {
        "STICK_UP": "Left Stick Up (Move / Jump)",
        "STICK_DOWN": "Left Stick Down (Crouch)",
        "STICK_LEFT": "Left Stick Left (Move Back)",
        "STICK_RIGHT": "Left Stick Right (Move Forward)",
        "RSTICK_UP": "Right Stick Up (Triangle / Y)",
        "RSTICK_LEFT": "Right Stick Left (Square / X)",
        "RSTICK_DOWN": "Right Stick Down (Cross / A)",
        "RSTICK_RIGHT": "Right Stick Right (Circle / B)",
        "DPAD_UP": "D-Pad Up (Jump)",
        "DPAD_DOWN": "D-Pad Down (Crouch)",
        "DPAD_LEFT": "D-Pad Left (Move Back/Block)",
        "DPAD_RIGHT": "D-Pad Right (Move Forward)",
        "BUTTON_0": "Square [□] / Xbox X (Punch)",
        "BUTTON_1": "Cross [X] / Xbox A (Kick)",
        "BUTTON_2": "Circle [O] / Xbox B (Grab)",
        "BUTTON_3": "Triangle [△] / Xbox Y (Stage)",
        "BUTTON_4": "L1 / LB (Target / Music)",
        "BUTTON_5": "R1 / RB (Super Attack)",
        "BUTTON_6": "L2 / LT (Super Alt)",
        "BUTTON_7": "R2 / RT (Fight / Enter)",
        "BUTTON_8": "Select / Back / View (Mute)",
        "BUTTON_9": "Start / Menu (Pause Combat)",
        "BUTTON_10": "L3 / Left Stick Click",
        "BUTTON_11": "R3 / Right Stick Click",
        "BUTTON_12": "PS / Guide Button",
        "BUTTON_13": "Button 13"
    }


    class UniversalControllerReader:
        """
        Seamlessly polls any connected controller:
        - Xbox 360, Xbox One, Xbox Series X/S via native Windows XInput.
        - PlayStation (PS3, PS4, PS5) and Generic USB gamepads via native Windows DirectInput (WinMM).
        """
        def __init__(self):
            self.mode = None # 'xinput' or 'winmm'
            self.active_id = 0
            self.device_name = "Detecting controller..."
            self.right_axes = ("dwZpos", "dwRpos")
            self._right_axes_id = None

            # WinMM Structures
            self.joy_info = JOYINFOEX()
            self.joy_info.dwSize = ctypes.sizeof(JOYINFOEX)
            self.joy_info.dwFlags = 0xFF # JOY_RETURNALL

            # XInput Structures
            self.xinput_state = XINPUT_STATE()

        def check_connection(self):
            # 1. Check XInput (Xbox Controllers, Ports 0-3)
            if xinput_dll is not None:
                for user_index in range(4):
                    if xinput_dll.XInputGetState(user_index, ctypes.byref(self.xinput_state)) == 0:
                        self.mode = 'xinput'
                        self.active_id = user_index
                        self.device_name = f"Xbox / XInput Controller (Player {user_index + 1})"
                        return True

            # 2. Check WinMM (PlayStation & Generic USB Gamepads, Devices 0-15)
            num_devs = winmm.joyGetNumDevs()
            for dev_id in range(min(num_devs, 16)):
                if winmm.joyGetPosEx(dev_id, ctypes.byref(self.joy_info)) == 0:
                    same_pad = self.mode == 'winmm' and self.active_id == dev_id and self._right_axes_id == dev_id
                    self.mode = 'winmm'
                    self.active_id = dev_id
                    caps = JOYCAPSW()
                    if winmm.joyGetDevCapsW(dev_id, ctypes.byref(caps), ctypes.sizeof(JOYCAPSW)) == 0 and caps.szPname:
                        name = caps.szPname.strip()
                        self.device_name = f"Gamepad: {name} (Device {dev_id})"
                    else:
                        self.device_name = f"PlayStation / Generic Gamepad (Device {dev_id})"
                    if not same_pad:
                        self._detect_right_axes()
                        self._right_axes_id = dev_id
                    return True

            self.mode = None
            self._right_axes_id = None
            self.device_name = "Disconnected: Please plug in an Xbox, PlayStation, or USB controller"
            return False

        def _detect_right_axes(self):
            """Pick the two axes that rest at center. Triggers usually rest at an end."""
            centered = []
            for name in ("dwZpos", "dwRpos", "dwUpos", "dwVpos"):
                value = getattr(self.joy_info, name)
                if 12000 <= value <= 52000:
                    centered.append(name)
            self.right_axes = tuple(centered[:2]) if len(centered) >= 2 else ("dwZpos", "dwRpos")

        def is_connected(self):
            return self.check_connection()

        def get_device_name(self):
            return self.device_name

        def get_family(self):
            """Which controller picture to show. XInput is Xbox; DirectInput names decide the rest."""
            name = (self.device_name or "").lower()
            if any(token in name for token in ("dualsense", "dualshock", "playstation", "sony", "ps5", "ps4", "ps3")):
                return "playstation"
            if any(token in name for token in ("xbox", "xinput", "x-box")):
                return "xbox"
            if self.mode == "xinput":
                return "xbox"
            return "playstation"

        def read_inputs(self, deadzone=14000):
            # Verify active connection
            if self.mode == 'xinput':
                if xinput_dll.XInputGetState(self.active_id, ctypes.byref(self.xinput_state)) != 0:
                    if not self.check_connection():
                        return None
            elif self.mode == 'winmm':
                if winmm.joyGetPosEx(self.active_id, ctypes.byref(self.joy_info)) != 0:
                    if not self.check_connection():
                        return None
            else:
                if not self.check_connection():
                    return None

            active_inputs = set()

            # Handle Xbox / XInput Controllers
            if self.mode == 'xinput':
                gp = self.xinput_state.Gamepad
                btns = gp.wButtons

                # Face buttons
                if btns & XINPUT_GAMEPAD_X: active_inputs.add("BUTTON_0") # Square / X
                if btns & XINPUT_GAMEPAD_A: active_inputs.add("BUTTON_1") # Cross / A
                if btns & XINPUT_GAMEPAD_B: active_inputs.add("BUTTON_2") # Circle / B
                if btns & XINPUT_GAMEPAD_Y: active_inputs.add("BUTTON_3") # Triangle / Y

                # Bumpers & Triggers
                if btns & XINPUT_GAMEPAD_LEFT_SHOULDER: active_inputs.add("BUTTON_4")  # LB
                if btns & XINPUT_GAMEPAD_RIGHT_SHOULDER: active_inputs.add("BUTTON_5") # RB
                if gp.bLeftTrigger > 30: active_inputs.add("BUTTON_6")                 # LT
                if gp.bRightTrigger > 30: active_inputs.add("BUTTON_7")                # RT

                # Center Buttons
                if btns & XINPUT_GAMEPAD_BACK: active_inputs.add("BUTTON_8")  # View / Back
                if btns & XINPUT_GAMEPAD_START: active_inputs.add("BUTTON_9") # Menu / Start

                # Stick Clicks
                if btns & XINPUT_GAMEPAD_LEFT_THUMB: active_inputs.add("BUTTON_10")
                if btns & XINPUT_GAMEPAD_RIGHT_THUMB: active_inputs.add("BUTTON_11")

                # D-Pad
                if btns & XINPUT_GAMEPAD_DPAD_UP: active_inputs.add("DPAD_UP")
                if btns & XINPUT_GAMEPAD_DPAD_DOWN: active_inputs.add("DPAD_DOWN")
                if btns & XINPUT_GAMEPAD_DPAD_LEFT: active_inputs.add("DPAD_LEFT")
                if btns & XINPUT_GAMEPAD_DPAD_RIGHT: active_inputs.add("DPAD_RIGHT")

                # Left Analog Stick (XInput ranges -32768 to 32767; positive Y is UP)
                lx = gp.sThumbLX
                ly = gp.sThumbLY
                if lx < -deadzone: active_inputs.add("STICK_LEFT")
                elif lx > deadzone: active_inputs.add("STICK_RIGHT")

                if ly > deadzone: active_inputs.add("STICK_UP")
                elif ly < -deadzone: active_inputs.add("STICK_DOWN")

                rx = gp.sThumbRX
                ry = gp.sThumbRY
                if rx < -deadzone: active_inputs.add("RSTICK_LEFT")
                elif rx > deadzone: active_inputs.add("RSTICK_RIGHT")
                if ry > deadzone: active_inputs.add("RSTICK_UP")
                elif ry < -deadzone: active_inputs.add("RSTICK_DOWN")

                return active_inputs

            # Handle PlayStation & Generic USB Gamepads (WinMM)
            elif self.mode == 'winmm':
                # Buttons (bitmask)
                buttons = self.joy_info.dwButtons
                for b in range(14):
                    if buttons & (1 << b):
                        active_inputs.add(f"BUTTON_{b}")

                # Left Stick (Centered at 32767; positive Y is DOWN)
                x = self.joy_info.dwXpos - 32767
                y = self.joy_info.dwYpos - 32767
                if x < -deadzone: active_inputs.add("STICK_LEFT")
                elif x > deadzone: active_inputs.add("STICK_RIGHT")

                if y < -deadzone: active_inputs.add("STICK_UP")
                elif y > deadzone: active_inputs.add("STICK_DOWN")

                rx = getattr(self.joy_info, self.right_axes[0]) - 32767
                ry = getattr(self.joy_info, self.right_axes[1]) - 32767
                if rx < -deadzone: active_inputs.add("RSTICK_LEFT")
                elif rx > deadzone: active_inputs.add("RSTICK_RIGHT")
                if ry < -deadzone: active_inputs.add("RSTICK_UP")
                elif ry > deadzone: active_inputs.add("RSTICK_DOWN")

                # D-Pad (dwPOV)
                pov = self.joy_info.dwPOV
                if pov != 65535:
                    if pov in (31500, 0, 4500): active_inputs.add("DPAD_UP")
                    if pov in (4500, 9000, 13500): active_inputs.add("DPAD_RIGHT")
                    if pov in (13500, 18000, 22500): active_inputs.add("DPAD_DOWN")
                    if pov in (22500, 27000, 31500): active_inputs.add("DPAD_LEFT")

                return active_inputs

            return None

    ControllerReader = UniversalControllerReader
    KEY_CODES = VK_MAP
