# scrcpy-gui

Modern GUI for scrcpy with Material Design 3 support.

## Features

- **Material Design 3** - Beautiful modern interface
- **Dark/Light Theme** - Switch between themes seamlessly
- **Multi-language** - English and Russian support
- **USB & WiFi Connection** - Connect via USB or TCP/IP
- **All scrcpy Options** - Full access to video, audio, recording, control settings
- **Built-in Tutorials** - Step-by-step guides for USB and WiFi connection
- **Single Button Control** - Start/Stop mirroring with one button
- **Responsive Design** - UI adapts to screen size
- **Config Saving** - Save and load your preferences

## Requirements

- Python 3.8+
- PySide6
- scrcpy installed on your system
- ADB (Android Debug Bridge)

## Installation

### Windows

1. Install Python 3.8+ from https://python.org
2. Open Command Prompt in the project folder
3. Run: `build.bat`
4. The executable will be created in the `dist` folder

### Linux/macOS

```bash
chmod +x build.sh
./build.sh
```

### Manual Installation

```bash
pip install PySide6
python scrcpy_gui.py
```

## Usage

1. **Connect Device**:
   - USB Mode: Connect via USB cable, click Refresh
   - WiFi Mode: Enter IP address and port, click Connect

2. **Configure Settings**:
   - Video: Resolution, bitrate, FPS, orientation
   - Audio: Bitrate, forwarding options
   - Recording: Format (MP4/MKV), save path
   - Control: Text input, gamepad, touches
   - Window: Fullscreen, always on top, borderless
   - Advanced: ADB/scrcpy paths, log level, language, theme

3. **Start Mirroring**: Click "Start Mirror" button

4. **Stop Mirroring**: Click "Stop Mirror" button

## Keyboard Shortcuts (in scrcpy window)

- `Ctrl+G` - Toggle fullscreen
- `Ctrl+H` - Home
- `Ctrl+B` - Back
- `Ctrl+S` - Screenshot
- `Ctrl+O` - Turn screen off
- `Ctrl+N` - Expand notification panel

## Configuration

Settings are saved automatically to `~/.scrcpy-gui/config.json`

## License

Apache 2.0
