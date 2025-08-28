# 👁️ GazeAway - Eye Strain Reminder

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)](https://windows.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

> **Take care of your eyes with intelligent screen break reminders**

GazeAway is a smart Windows application that helps reduce eye strain by reminding you to take regular breaks from your screen. Perfect for developers, office workers, students, and anyone who spends long hours in front of a computer.

> **⚠️ Note**: Windows Defender may flag the executable as a false positive during development. This is common with PyInstaller-created applications. See [ANTIVIRUS-FALSE-POSITIVE.md](ANTIVIRUS-FALSE-POSITIVE.md) for solutions.

## ✨ Features

### 🕐 Smart Timer System

- **Customizable intervals**: Set reminder intervals from 1 minute to several hours
- **Flexible break duration**: Choose how long your breaks should last (5-60 seconds)
- **Pause/Resume**: Temporarily pause reminders when you need to focus

### 🖥️ Multi-Monitor Support

- **Full-screen reminders**: Covers all connected monitors simultaneously
- **Adaptive positioning**: Automatically detects and adapts to your monitor setup
- **Consistent experience**: Same reminder experience across all screens

### 🎨 Beautiful Interface

- **Dark theme**: Easy on the eyes with a modern dark interface
- **Large, clear text**: Easy to read countdown timer and instructions
- **Professional design**: Clean, minimalist interface that doesn't distract

### 🔔 Smart Notifications

- **System tray integration**: Runs quietly in the background
- **Audio alerts**: Custom notification sounds for break reminders
- **Visual notifications**: Full-screen overlay with countdown timer

### ⚙️ Advanced Features

- **Startup integration**: Automatically start with Windows
- **Settings persistence**: Remembers your preferences between sessions
- **Professional installer**: Easy installation with NSIS installer
- **Registry integration**: Proper Windows application registration

## 🚀 Quick Start

### Option 1: Download Pre-built Installer

1. Download `GazeAway-Setup.exe` from the [Releases](https://github.com/utkvishwas/GazeAway/releases) page
2. Run the installer and follow the setup wizard
3. Launch GazeAway from the Start Menu or Desktop shortcut

### Option 2: Build from Source

#### Prerequisites

- Python 3.7 or higher
- Windows 10/11
- NSIS (for creating installer)

#### Installation Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/utkvishwas/GazeAway.git
   cd GazeAway
   ```

2. **Complete build process (one command)**

   ```bash
   build.bat
   ```

   This single command will:

   - Install all Python dependencies
   - Build the GazeAway.exe executable
   - Create the professional Windows installer
   - Provide status updates throughout the process

## 📖 Usage Guide

### First Launch

1. **Configure Settings**: Set your preferred reminder interval and break duration
2. **Start Timer**: Click "Start Timer" to begin receiving reminders
3. **Minimize**: The app will run in the system tray

### During Use

- **Break reminders**: Full-screen overlay appears with countdown timer
- **Skip option**: Click "Skip Break" if you need to continue working
- **System tray**: Right-click the tray icon for quick access to settings

### Settings

- **Reminder Interval**: How often you want reminders (default: 20 minutes)
- **Break Duration**: How long each break should last (default: 20 seconds)
- **Start with Windows**: Automatically launch on system startup

## 🛠️ Development

### Project Structure

```
GazeAway/
├── main.py              # Main application code
├── build-script.py      # PyInstaller build script
├── build.bat           # Complete build automation script
├── installer.nsi        # NSIS installer script
├── requirements.txt     # Python dependencies
├── LICENSE.txt          # License agreement
├── icon.ico            # Application icon
└── notification.wav    # Notification sound
```

### Building from Source

```bash
# Complete build process (one command)
build.bat
```

This will automatically:

- Install all required dependencies
- Build the GazeAway.exe executable
- Create the Windows installer (if NSIS is available)
- Provide detailed progress feedback

### Dependencies

- **pystray**: System tray functionality
- **Pillow**: Image processing for icons
- **pywin32**: Windows API access
- **PyInstaller**: Executable creation

## 🎯 Why GazeAway?

### Health Benefits

- **Reduces eye strain**: Regular breaks help prevent digital eye strain
- **Improves focus**: Short breaks can actually improve productivity
- **Prevents headaches**: Reduces screen-related headaches and fatigue
- **Better posture**: Encourages movement and stretching

### User Experience

- **Non-intrusive**: Runs quietly in the background
- **Customizable**: Adapt to your work schedule and preferences
- **Professional**: Clean, modern interface
- **Reliable**: Stable performance with proper error handling

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🙏 Acknowledgments

- **20-20-20 Rule**: Inspired by the eye care principle of looking at something 20 feet away for 20 seconds every 20 minutes
- **Open Source Community**: Built with amazing open-source libraries
- **Users**: For feedback and suggestions that help improve the application

## 📞 Support

- **Issues**: Report bugs and request features on [GitHub Issues](https://github.com/utkvishwas/GazeAway/issues)
- **Discussions**: Join the conversation on [GitHub Discussions](https://github.com/utkvishwas/GazeAway/discussions)
- **Email**: Contact us at support@gazeaway.app

## 🔄 Version History

### v1.0.0 (Current)

- ✅ Multi-monitor support
- ✅ System tray integration
- ✅ Customizable timer settings
- ✅ Professional installer
- ✅ Audio notifications

### Planned Features

- 🔄 Cross-platform support (macOS, Linux)
- 🔄 Cloud sync for settings
- 🔄 Statistics and usage tracking
- 🔄 Custom themes
- 🔄 Integration with productivity tools

---

<div align="center">

**Made with ❤️ for better eye health**

[⭐ Star this repo](https://github.com/utkvishwas/GazeAway) | [🐛 Report an issue](https://github.com/utkvishwas/GazeAway/issues)

</div>
