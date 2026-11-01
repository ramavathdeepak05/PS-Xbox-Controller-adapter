# How it works

GamepadAdapter watches the controller you have plugged in and, while a control is held, sends the keyboard keys you assigned to it. When you let go, those keys are released.

It runs on Windows and macOS. On Windows, Xbox controllers are read through XInput, and PlayStation and other USB controllers are read through the Windows joystick interface. Keystrokes are sent with `SendInput`. On a Mac, both brands are read through SDL, and keystrokes are sent with Quartz. macOS delivers those keystrokes only after the app is allowed under **System Settings → Privacy & Security → Accessibility**. Quit the app and open it again after turning that on. The downloaded Mac app is not signed: the first time, right-click `GamepadAdapter.app`, choose **Open**, then choose **Open** again. That download is built for Apple Silicon.

## Using the window

The controller picture sits in the middle. Each control has a glass chip showing its current key.

- Click a chip and press one key to bind that key.
- Hold Ctrl, Alt, or Shift, then press another key, to bind a combination such as Ctrl+C. On a Mac, Command is a separate modifier, shown as Cmd. The modifier is held first and released last.
- Press only Ctrl, Alt, or Shift, then release it, to bind that modifier by itself.
- Click the × on a chip to clear it.
- Click **Apply Changes** to save. Until you do, the window shows **Not saved yet**.

**Pause** keeps the window open but stops sending keys. **Resume** turns sending back on.

Only one profile is stored. On Windows it is `controller_mapping.json` next to `GamepadAdapter.exe`. On a Mac it is saved next to the app or next to `ps3_adapter.py` when you run the source.

## Default keys

Directions are listed in the same order as the chips: up, left, down, right.

| Control | Default keys |
| --- | --- |
| D-pad | W, A, S, D |
| Left stick | W, A, S, D |
| Right stick | T, J, K, I |
| Triangle / Y | T |
| Square / X | J |
| Circle / B | I |
| Cross / A | K |
| L1 / LB | M |
| R1 / RB | L |
| L2 / LT | Space |
| R2 / RT | Enter |
| Share / Create, or View | N |
| Options / Menu | Esc |
| L3 | 1 |
| R3 | 2 |
| PlayStation / Xbox button | Not set |
| Touchpad | Not set |

The right stick follows the face buttons: up is Triangle, left is Square, down is Cross, and right is Circle. On an Xbox pad those same keys are Y, X, A, and B. L3 and R3 are the stick clicks. Tilting a stick is separate from clicking it.

You can change any of these, including the ones that start empty.

## What the app is doing

About once a millisecond, the app checks which controls are held. For each one, it looks up the saved binding and holds those keys down. A binding of `CTRL+C` holds Ctrl, then C. A binding of `CMD+C` holds Command, then C, which is copy on a Mac. Keys that no held control still needs are released, with the main key released before the modifier.

The picture switches from the connected controller. An Xbox name, or an XInput controller, uses the Xbox picture. A name that mentions PlayStation, DualSense, DualShock, or Sony uses the PlayStation picture. Other USB gamepads use the PlayStation layout.

Closing the window closes the app.
