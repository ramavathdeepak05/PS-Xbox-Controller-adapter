#!/usr/bin/env python3
"""
Universal Gamepad to Keyboard Adapter
Supports PlayStation (PS3, PS4, PS5), Xbox (360, One, Series X/S), and Generic USB Controllers.
Windows uses XInput, WinMM, and SendInput. macOS uses SDL and Quartz.
"""

import sys
import os

# Configure stdout/stderr encoding for Windows console compatibility
if sys.platform == 'win32':
    try:
        if sys.stdout is not None:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if sys.stderr is not None:
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import json
import time
import threading
import http.server
import socketserver
import webbrowser

try:
    import webview
except ImportError:
    webview = None

# --- Determine Base Path & UI Assets (Supports standalone PyInstaller .exe) ---
if getattr(sys, 'frozen', False):
    if sys.platform == "darwin":
        # The executable lives at GamepadAdapter.app/Contents/MacOS/<name>.
        # Keep the profile beside the .app, not inside the bundle.
        APP_DIR = sys.executable
        for _ in range(4):
            APP_DIR = os.path.dirname(APP_DIR)
    else:
        APP_DIR = os.path.dirname(sys.executable)
    if hasattr(sys, '_MEIPASS') and os.path.exists(os.path.join(sys._MEIPASS, "ui")):
        UI_DIR = os.path.join(sys._MEIPASS, "ui")
    else:
        UI_DIR = os.path.join(APP_DIR, "ui")
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    UI_DIR = os.path.join(APP_DIR, "ui")

CONFIG_FILE = os.path.join(APP_DIR, "controller_mapping.json")
LEGACY_CONFIG = os.path.join(APP_DIR, "ps3_mapping.json")

if sys.platform == "win32":
    from platform_win import ControllerReader as UniversalControllerReader, send_key_event, KEY_CODES

    def ensure_keyboard_access():
        return None
elif sys.platform == "darwin":
    from platform_mac import ControllerReader as UniversalControllerReader, send_key_event, KEY_CODES, ensure_keyboard_access
else:
    raise SystemExit("GamepadAdapter supports Windows and macOS.")


MODIFIER_NAMES = ("CMD", "CTRL", "ALT", "SHIFT")

def binding_key_names(key_str):
    """Split a binding such as 'CTRL+C' into known keys, modifiers first."""
    if not isinstance(key_str, str) or not key_str.strip():
        return []
    parts = []
    for raw in key_str.upper().split("+"):
        name = raw.strip()
        if name in KEY_CODES and name not in parts:
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



class AdapterEngine:
    """Background engine translating gamepad inputs into hardware SendInput keystrokes."""
    def __init__(self, mapping):
        self.mapping = dict(mapping)
        self.reader = UniversalControllerReader()
        self.is_running = False
        self.is_active = True
        self.thread = None
        self.pressed_order = []
        self.current_active_inputs = set()
        self.lock = threading.Lock()

    def update_mapping(self, new_mapping):
        with self.lock:
            self.mapping = dict(new_mapping)

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False
        self._release_all()

    def _release_all(self):
        for vk in reversed(self.pressed_order):
            send_key_event(vk, False)
        self.pressed_order.clear()

    def _loop(self):
        while self.is_running:
            active_inputs = self.reader.read_inputs()
            if active_inputs is None:
                self._release_all()
                self.current_active_inputs = set()
                time.sleep(0.4)
                continue

            self.current_active_inputs = active_inputs

            if not self.is_active:
                self._release_all()
                time.sleep(0.005)
                continue

            names = []
            with self.lock:
                for inp in active_inputs:
                    names.extend(binding_key_names(self.mapping.get(inp, "")))

            desired = []
            seen = set()
            ordered_names = [name for name in MODIFIER_NAMES if name in names]
            for name in names:
                if name not in MODIFIER_NAMES and name not in ordered_names:
                    ordered_names.append(name)
            for name in ordered_names:
                vk = KEY_CODES[name]
                if vk not in seen:
                    seen.add(vk)
                    desired.append(vk)

            modifier_vks = {KEY_CODES[name] for name in MODIFIER_NAMES if name in KEY_CODES}
            releasing = [vk for vk in self.pressed_order if vk not in seen]
            releasing.sort(key=lambda vk: vk in modifier_vks)
            for vk in releasing:
                send_key_event(vk, False)
                self.pressed_order.remove(vk)

            for vk in desired:
                if vk not in self.pressed_order:
                    send_key_event(vk, True)
                    self.pressed_order.append(vk)

            time.sleep(0.001) # Ultra-fast 1ms polling rate for lag-free fighting game response


GLOBAL_ENGINE = None

class AdapterHTTPHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = http.server.SimpleHTTPRequestHandler.extensions_map.copy()
    extensions_map.update({
        '.js': 'text/javascript',
        '.mjs': 'text/javascript',
        '.gltf': 'model/gltf+json',
        '.bin': 'application/octet-stream'
    })
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_DIR, **kwargs)

    def log_message(self, format, *args):
        # Suppress noisy HTTP console logs
        pass

    def do_GET(self):
        global GLOBAL_ENGINE
        if self.path == '/api/mapping':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = {
                "mapping": GLOBAL_ENGINE.mapping,
                "labels": CONTROLLER_LABELS
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return
        elif self.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = {
                "connected": GLOBAL_ENGINE.reader.is_connected(),
                "device_name": GLOBAL_ENGINE.reader.get_device_name(),
                "family": GLOBAL_ENGINE.reader.get_family(),
                "active_inputs": list(GLOBAL_ENGINE.current_active_inputs),
                "is_active": GLOBAL_ENGINE.is_active
            }
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        super().do_GET()

    def do_POST(self):
        global GLOBAL_ENGINE
        if self.path == '/api/toggle':
            GLOBAL_ENGINE.is_active = not GLOBAL_ENGINE.is_active
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"is_active": GLOBAL_ENGINE.is_active}).encode('utf-8'))
            return
        elif self.path == '/api/save':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            new_mapping = json.loads(body.decode('utf-8'))
            GLOBAL_ENGINE.update_mapping(new_mapping)
            try:
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(new_mapping, f, indent=4)
            except Exception:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            return
        elif self.path == '/api/reset':
            GLOBAL_ENGINE.update_mapping(DEFAULT_MAPPING)
            try:
                with open(CONFIG_FILE, 'w') as f:
                    json.dump(DEFAULT_MAPPING, f, indent=4)
            except Exception:
                pass
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"mapping": DEFAULT_MAPPING}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()


def load_saved_mapping():
    for path in [CONFIG_FILE, LEGACY_CONFIG]:
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    res = dict(DEFAULT_MAPPING)
                    res.update(data)
                    return res
            except Exception:
                pass
    return dict(DEFAULT_MAPPING)


def run_cli():
    """Headless CLI mode for lightweight or background usage."""
    mapping = load_saved_mapping()
    engine = AdapterEngine(mapping)
    print("=" * 65)
    print("[*] Universal Gamepad to Keyboard Adapter (CLI Mode)")
    print("Supports: Xbox (One / Series / 360), PlayStation (PS3 / PS4 / PS5)")
    print("=" * 65)
    ensure_keyboard_access()
    if engine.reader.is_connected():
        print(f"Status: Connected ({engine.reader.get_device_name()})")
    else:
        print("Status: Waiting for controller to connect...")

    print("\nActive Mappings:")
    for inp, key in mapping.items():
        if key:
            label = CONTROLLER_LABELS.get(inp, inp)
            print(f"  {label:<38} -> [{key}]")

    print("\nAdapter running! Press Ctrl+C in this console to exit.")
    engine.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping adapter...")
        engine.stop()
        print("Adapter stopped.")


def run_web_gui(port=8080):
    """Launches the Liquid Glass UI in a standalone desktop window via pywebview."""
    global GLOBAL_ENGINE
    mapping = load_saved_mapping()
    GLOBAL_ENGINE = AdapterEngine(mapping)
    GLOBAL_ENGINE.start()

    server = None
    for p in range(port, port + 20):
        try:
            server = socketserver.TCPServer(("127.0.0.1", p), AdapterHTTPHandler)
            port = p
            break
        except OSError:
            continue

    if not server:
        print("[ERROR] Could not find an open port for the Web UI.")
        return

    # Start the HTTP server on a daemon thread
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    url = f"http://127.0.0.1:{port}/"
    print("=" * 65)
    print("[*] Universal Gamepad Adapter (Desktop Application)")
    print(f"Internal API running at: {url}")
    print("=" * 65)
    ensure_keyboard_access()

    try:
        import webview
        # Open in a dedicated native desktop window
        webview.create_window(
            title="Controller Mapping",
            url=url,
            width=1440,
            height=900,
            resizable=True,
            min_size=(1100, 720)
        )
        webview.start()
    except ImportError:
        print("[INFO] pywebview not detected. Opening in browser as fallback...")
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    finally:
        print("\nShutting down adapter...")
        GLOBAL_ENGINE.stop()
        server.shutdown()
        print("Adapter stopped.")


if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_web_gui()
