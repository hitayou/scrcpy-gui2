> [!WARNING]
> **Official GitHub repo: https://github.com/Genymobile/scrcpy, scrcpy-gui2 it is fork**

# scrcpy-gui

[English](README.md) | [Русский](README_RU.md)

A modern GUI for scrcpy with Material Design 3 styling.

## Features

- **Material Design 3** - Beautiful, modern interface
- **Multi-language Support** - English and Russian localization
- **Easy Device Connection** - USB and WiFi (TCP/IP) support
- **Full scrcpy Settings** - All video, audio, recording, and control options
- **Tabbed Interface** - Organized settings by category
- **Built-in Tutorials** - Step-by-step connection guides
- **Configuration Save/Load** - Save your preferred settings
- **Dark/Light Themes** - Choose your preferred appearance

## Requirements

- Python 3.8+
- PySide6
- scrcpy (installed separately)
- adb (Android Debug Bridge)

## Installation

### Windows

1. Install Python from https://python.org
2. Run `build.bat` to build the application
3. Run `dist\run.bat` to start the application

Or manually:
```bash
pip install PySide6
python scrcpy_gui.py
```

### Linux/macOS

```bash
chmod +x build.sh
./build.sh
./dist/run.sh
```

Or manually:
```bash
pip3 install PySide6
python3 scrcpy_gui.py
```

## Usage

### Connecting via USB

1. Enable Developer Options on your Android device
   - Go to Settings → About phone
   - Tap "Build number" 7 times
2. Enable USB debugging
   - Go to Settings → System → Developer options
   - Enable "USB debugging"
3. Connect your device via USB cable
4. Accept the USB debugging prompt on your device
5. Click "Refresh Devices" in scrcpy-gui
6. Select your device and click "Connect"
7. Click "Start Mirroring"

### Connecting via WiFi

1. First complete USB setup above
2. Connect device and computer to the same WiFi network
3. Get device IP address:
   - Settings → About phone → Status
   - Or run: `adb shell ip route | awk '{print $9}'`
4. Enable TCP/IP mode: `adb tcpip 5555`
5. Disconnect USB cable
6. Enter IP address in scrcpy-gui and click "Connect"
7. Click "Start Mirroring"

## Settings

### Video Tab
- Max Resolution (0 = unlimited)
- Bit Rate (Mbps)
- Max FPS
- Display ID
- Video Codec (h264, h265, av1)
- Crop Video

### Audio Tab
- Enable/Disable Audio
- Audio Bit Rate
- Audio Codec (opus, aac, flac, raw)
- Audio Source (output, playback, mic)

### Recording Tab
- Enable Recording
- Record Format (mp4, mkv)
- Record File Path
- No Video Playback (record only)
- No Audio Playback (record only)

### Control Tab
- Prefer Text Input
- Raw Key Events
- Gamepad Support
- Mouse Binding Mode

### Window Tab
- Window Title
- Always on Top
- Borderless Window
- Start Fullscreen
- Window Position (X, Y)
- Window Size (Width, Height)
- Background Color
- Disable Screensaver

### Advanced Tab
- Time Limit
- Turn Screen Off
- Power Off on Close
- Don't Power On
- Kill ADB on Close
- Force ADB Forward
- Tunnel Host/Port

## Keyboard Shortcuts (in scrcpy window)

- `Alt+F` - Toggle fullscreen
- `Right-click` - Back button
- `Middle-click` - Home button
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste

For more shortcuts, see scrcpy documentation.

## Configuration

Settings are automatically saved to `~/.scrcpy-gui/config.json`

You can also manually save/load configurations from the Advanced tab.

## License

This GUI is provided as-is. Original scrcpy by Genymobile.

## Troubleshooting

### "No devices found"
- Make sure USB debugging is enabled
- Try a different USB cable
- Install proper USB drivers (Windows)
- Run `adb devices` to verify detection

### "Failed to connect"
- Check that device and computer are on same network
- Verify IP address is correct
- Make sure port 5555 is not blocked by firewall
- Try `adb kill-server` and reconnect

### "scrcpy not found"
- Install scrcpy from https://github.com/Genymobile/scrcpy
- Make sure scrcpy is in your system PATH


## Resources official scrcpy dev

 - [FAQ](FAQ.md)
 - [Translations][wiki] (not necessarily up to date)
 - [Build instructions](doc/build.md)
 - [Developers](doc/develop.md)
 - [Verify release signatures](doc/verify-release.md)

[wiki]: https://github.com/Genymobile/scrcpy/wiki


## Articles official scrcpy dev

- [Introducing scrcpy][article-intro]
- [Scrcpy now works wirelessly][article-tcpip]
- [Scrcpy 2.0, with audio][article-scrcpy2]

[article-intro]: https://blog.rom1v.com/2018/03/introducing-scrcpy/
[article-tcpip]: https://www.genymotion.com/blog/open-source-project-scrcpy-now-works-wirelessly/
[article-scrcpy2]: https://blog.rom1v.com/2023/03/scrcpy-2-0-with-audio/

## Contact official scrcpy dev

You can open an [issue] for bug reports, feature requests or general questions.

For bug reports, please read the [FAQ](FAQ.md) first, you might find a solution
to your problem immediately.

[issue]: https://github.com/Genymobile/scrcpy/issues

You can also use:

 - Reddit: [`r/scrcpy`](https://www.reddit.com/r/scrcpy)
 - BlueSky: [`@scrcpy.bsky.social`](https://bsky.app/profile/scrcpy.bsky.social)
 - Twitter: [`@scrcpy_app`](https://twitter.com/scrcpy_app)


## Donate official scrcpy dev

I'm [@rom1v](https://github.com/rom1v), the author and maintainer of _scrcpy_.

If you appreciate this application, you can [support my open source
work][donate]:
 - [GitHub Sponsors](https://github.com/sponsors/rom1v)
 - [Liberapay](https://liberapay.com/rom1v/)
 - [PayPal](https://paypal.me/rom2v)

[donate]: https://blog.rom1v.com/about/#support-my-open-source-work

## License

    Copyright (C) 2018 Genymobile
    Copyright (C) 2018-2026 Romain Vimont

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
