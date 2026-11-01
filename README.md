# PS / Xbox Controller Adapter

A free Windows app that turns a PlayStation or Xbox controller into keyboard keys. Plug in a controller, click a button, and choose the key or key combination it should press.

Download [GamepadAdapter.exe](GamepadAdapter.exe), double-click it, and the mapping window opens. Nothing else needs to be installed.

## Map a button

1. Click the key chip next to a control.
2. Press a key, or hold Ctrl, Alt, or Shift and then press a key. For example, hold Ctrl and press C to bind Ctrl+C.
3. Click **Apply Changes**.

The profile is saved as `controller_mapping.json` in the same folder as the exe. **Reset to Default** restores the original keys. **Clear All** empties every binding. **Pause** stops the keys from being sent until you resume.

## Which controller you see

- A PlayStation controller shows the PlayStation image, with Share, Options, the touchpad, and the PlayStation button.
- An Xbox controller shows the Xbox image. The labels switch to View, Menu, LB, RB, LT, RT, and A, B, X, Y. The D-pad and left stick trade places, matching an Xbox pad.

## Source code

The Python source is in [GamepadAdapter-source.zip](GamepadAdapter-source.zip). It includes `ps3_adapter.py`, the mapping window, and the controller images. This is for Windows. Unzip it, install the libraries, and start the app:

```bat
pip install pywebview pyinstaller
run_adapter.bat
```

`build_app.bat` builds a new `dist\GamepadAdapter.exe`.

## License

The application is released under the [MIT License](LICENSE).

For a closer look at what each control does, read [How it works](HOW-IT-WORKS.md).
