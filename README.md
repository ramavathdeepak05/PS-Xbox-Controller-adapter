# PS / Xbox Controller Adapter

A free app that turns a PlayStation or Xbox controller into keyboard keys. Plug in a controller, click a button, and choose the key or key combination it should press.

On Windows, download [GamepadAdapter.exe](GamepadAdapter.exe), double-click it, and the mapping window opens. Nothing else needs to be installed.

On an Apple Silicon Mac, download `GamepadAdapter-mac.zip` from the [latest release](https://github.com/ramavathdeepak05/PS-Xbox-Controller-adapter/releases). Unzip it and open `GamepadAdapter.app`. The app is not signed, so the first time right-click it, choose **Open**, then choose **Open** again. Intel Macs can run the source below instead of this app.

## Map a button

1. Click the key chip next to a control.
2. Press a key, or hold Ctrl, Alt, or Shift and then press a key. For example, hold Ctrl and press C to bind Ctrl+C. On a Mac, hold Command and then a letter to bind a shortcut such as Cmd+C. Control is still the Control key.
3. Click **Apply Changes**.

The profile is saved as `controller_mapping.json` in the same folder as the exe. **Reset to Default** restores the original keys. **Clear All** empties every binding. **Pause** stops the keys from being sent until you resume.

## Which controller you see

- A PlayStation controller shows the PlayStation image, with Share, Options, the touchpad, and the PlayStation button.
- An Xbox controller shows the Xbox image. The labels switch to View, Menu, LB, RB, LT, RT, and A, B, X, Y. The D-pad and left stick trade places, matching an Xbox pad.

## Mac permissions

macOS does not type keys until GamepadAdapter is allowed under **System Settings → Privacy & Security → Accessibility**. Turn the switch on, quit the app, and open it again.

## Source code

The Python source is in [GamepadAdapter-source.zip](GamepadAdapter-source.zip). It includes `ps3_adapter.py`, the Mac and Windows backends, the mapping window, and the controller images.

On Windows:

```bat
pip install pywebview pyinstaller
run_adapter.bat
```

`build_app.bat` builds a new `dist\GamepadAdapter.exe`.

On a Mac:

```bash
python3 -m pip install --user pywebview pygame
python3 ps3_adapter.py
```

`run_adapter.command` does those two steps. The same Accessibility permission is required.

## License

The application is released under the [MIT License](LICENSE).

For a closer look at what each control does, read [How it works](HOW-IT-WORKS.md).
