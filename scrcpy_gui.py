#!/usr/bin/env python3
"""
scrcpy-gui - A modern GUI for scrcpy with Material Design 3 styling
Features: Device connection, settings management, multi-language support
"""

import sys
import os
import subprocess
import json
import re
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QCheckBox, QSpinBox, QDoubleSpinBox, QLineEdit,
    QPushButton, QLabel, QComboBox, QGroupBox, QScrollArea,
    QFrame, QSplitter, QTextEdit, QStackedWidget, QRadioButton,
    QButtonGroup, QMessageBox, QDialog, QProgressBar, QSystemTrayIcon,
    QMenu, QFileDialog, QSizePolicy
)
from PySide6.QtCore import (
    Qt, QThread, Signal, Slot, QTimer, QProcess, QSize, QPropertyAnimation,
    QEasingCurve, QPoint, QParallelAnimationGroup, QSequentialAnimationGroup
)
from PySide6.QtGui import (
    QFont, QColor, QPalette, QIcon, QPainter, QBrush, QPen,
    QLinearGradient, QRadialGradient, QFontDatabase, QAction
)


class LanguageManager:
    """Manages application localization"""

    TRANSLATIONS = {
        'en': {
            'app_title': 'scrcpy-gui',
            'connect_tab': 'Connect',
            'video_tab': 'Video',
            'audio_tab': 'Audio',
            'recording_tab': 'Recording',
            'control_tab': 'Control',
            'window_tab': 'Window',
            'advanced_tab': 'Advanced',

            'connection_type': 'Connection Type',
            'usb_connection': 'USB',
            'wifi_connection': 'WiFi (TCP/IP)',
            'device_serial': 'Device Serial',
            'device_ip': 'Device IP Address',
            'port': 'Port',
            'connect_btn': 'Connect',
            'disconnect_btn': 'Disconnect',
            'refresh_btn': 'Refresh Devices',
            'no_devices': 'No devices found',

            'usb_tutorial_title': 'USB Connection Tutorial',
            'usb_step1': 'Enable Developer Options on your Android device',
            'usb_step2': 'Go to Settings → About phone and tap "Build number" 7 times',
            'usb_step3': 'Go to Settings → System → Developer options',
            'usb_step4': 'Enable "USB debugging"',
            'usb_step5': 'Connect your device via USB cable',
            'usb_step6': 'Accept the USB debugging prompt on your device',
            'usb_step7': 'Click "Refresh Devices" to see your device',

            'wifi_tutorial_title': 'WiFi Connection Tutorial',
            'wifi_step1': 'First connect via USB and complete USB setup',
            'wifi_step2': 'Connect device and computer to the same WiFi network',
            'wifi_step3': 'Get device IP: Settings → About phone → Status',
            'wifi_step4': 'Run: adb tcpip 5555 (in terminal)',
            'wifi_step5': 'Disconnect USB cable',
            'wifi_step6': 'Enter IP address above and click Connect',

            'video_settings': 'Video Settings',
            'resolution': 'Max Resolution',
            'resolution_desc': 'Set maximum dimension (width or height)',
            'unlimited': 'Unlimited',
            'bitrate': 'Bit Rate',
            'bitrate_unit': 'Mbps',
            'max_fps': 'Max FPS',
            'display_id': 'Display ID',
            'video_codec': 'Video Codec',
            'crop_video': 'Crop Video',
            'crop_format': 'WIDTH:HEIGHT:X:Y',

            'audio_settings': 'Audio Settings',
            'enable_audio': 'Enable Audio',
            'audio_bitrate': 'Audio Bit Rate',
            'audio_codec': 'Audio Codec',
            'audio_source': 'Audio Source',
            'audio_output': 'Output',
            'audio_playback': 'Playback',
            'audio_mic': 'Microphone',

            'recording_settings': 'Recording Settings',
            'enable_recording': 'Enable Recording',
            'record_format': 'Record Format',
            'record_file': 'Record File Path',
            'browse': 'Browse...',
            'no_video_playback': 'No Video Playback (record only)',
            'no_audio_playback': 'No Audio Playback (record only)',

            'control_settings': 'Control Settings',
            'prefer_text': 'Prefer Text Input',
            'raw_key_events': 'Raw Key Events',
            'gamepad_support': 'Gamepad Support',
            'mouse_bind': 'Mouse Binding Mode',
            'mouse_bind_off': 'Off',
            'mouse_bind_left': 'Left Click',
            'mouse_bind_right': 'Right Click',

            'window_settings': 'Window Settings',
            'window_title': 'Window Title',
            'always_on_top': 'Always on Top',
            'borderless': 'Borderless Window',
            'fullscreen': 'Start Fullscreen',
            'window_x': 'Window X Position',
            'window_y': 'Window Y Position',
            'window_width': 'Window Width',
            'window_height': 'Window Height',
            'background_color': 'Background Color',
            'disable_screensaver': 'Disable Screensaver',

            'advanced_settings': 'Advanced Settings',
            'time_limit': 'Time Limit (seconds)',
            'screen_off_timeout': 'Screen Off Timeout',
            'turn_screen_off': 'Turn Device Screen Off',
            'power_off_on_close': 'Power Off on Close',
            'no_power_on': "Don't Power On",
            'kill_adb_on_close': 'Kill ADB on Close',
            'force_adb_forward': 'Force ADB Forward',
            'tunnel_host': 'Tunnel Host',
            'tunnel_port': 'Tunnel Port',

            'start_mirror': 'Start Mirroring',
            'stop_mirror': 'Stop Mirroring',
            'status_connected': 'Connected',
            'status_disconnected': 'Disconnected',
            'status_mirroring': 'Mirroring Active',
            'status_stopped': 'Stopped',

            'language': 'Language',
            'theme': 'Theme',
            'light_theme': 'Light',
            'dark_theme': 'Dark',

            'error_title': 'Error',
            'success_title': 'Success',
            'warning_title': 'Warning',

            'connecting': 'Connecting...',
            'starting': 'Starting mirror...',
            'stopping': 'Stopping...',

            'device_name': 'Device Name',
            'select_device': 'Select Device',

            'help': 'Help',
            'about': 'About',
            'about_text': 'scrcpy-gui v1.0\n\nA modern GUI for scrcpy with Material Design 3 styling.\n\nOriginal scrcpy by Genymobile\nGUI by scrcpy-gui Team',

            'apply': 'Apply',
            'reset': 'Reset Defaults',
            'save_config': 'Save Config',
            'load_config': 'Load Config',
        },
        'ru': {
            'app_title': 'scrcpy-gui',
            'connect_tab': 'Подключение',
            'video_tab': 'Видео',
            'audio_tab': 'Аудио',
            'recording_tab': 'Запись',
            'control_tab': 'Управление',
            'window_tab': 'Окно',
            'advanced_tab': 'Дополнительно',

            'connection_type': 'Тип подключения',
            'usb_connection': 'USB',
            'wifi_connection': 'WiFi (TCP/IP)',
            'device_serial': 'Серийный номер устройства',
            'device_ip': 'IP адрес устройства',
            'port': 'Порт',
            'connect_btn': 'Подключить',
            'disconnect_btn': 'Отключить',
            'refresh_btn': 'Обновить устройства',
            'no_devices': 'Устройства не найдены',

            'usb_tutorial_title': 'Инструкция по USB подключению',
            'usb_step1': 'Включите опции разработчика на вашем Android устройстве',
            'usb_step2': 'Перейдите в Настройки → О телефоне и нажмите 7 раз на "Номер сборки"',
            'usb_step3': 'Перейдите в Настройки → Система → Для разработчиков',
            'usb_step4': 'Включите "Отладка по USB"',
            'usb_step5': 'Подключите устройство через USB кабель',
            'usb_step6': 'Примите запрос отладки по USB на устройстве',
            'usb_step7': 'Нажмите "Обновить устройства" чтобы увидеть ваше устройство',

            'wifi_tutorial_title': 'Инструкция по WiFi подключению',
            'wifi_step1': 'Сначала подключитесь через USB и завершите настройку USB',
            'wifi_step2': 'Подключите устройство и компьютер к одной WiFi сети',
            'wifi_step3': 'Узнайте IP устройства: Настройки → О телефоне → Статус',
            'wifi_step4': 'Выполните: adb tcpip 5555 (в терминале)',
            'wifi_step5': 'Отсоедините USB кабель',
            'wifi_step6': 'Введите IP адрес выше и нажмите Подключить',

            'video_settings': 'Настройки видео',
            'resolution': 'Максимальное разрешение',
            'resolution_desc': 'Установить максимальный размер (ширина или высота)',
            'unlimited': 'Без ограничений',
            'bitrate': 'Битрейт',
            'bitrate_unit': 'Мбит/с',
            'max_fps': 'Максимум FPS',
            'display_id': 'ID дисплея',
            'video_codec': 'Видео кодек',
            'crop_video': 'Обрезать видео',
            'crop_format': 'ШИРИНА:ВЫСОТА:X:Y',

            'audio_settings': 'Настройки аудио',
            'enable_audio': 'Включить аудио',
            'audio_bitrate': 'Битрейт аудио',
            'audio_codec': 'Аудио кодек',
            'audio_source': 'Источник аудио',
            'audio_output': 'Выход',
            'audio_playback': 'Воспроизведение',
            'audio_mic': 'Микрофон',

            'recording_settings': 'Настройки записи',
            'enable_recording': 'Включить запись',
            'record_format': 'Формат записи',
            'record_file': 'Путь к файлу записи',
            'browse': 'Обзор...',
            'no_video_playback': 'Без воспроизведения видео (только запись)',
            'no_audio_playback': 'Без воспроизведения аудио (только запись)',

            'control_settings': 'Настройки управления',
            'prefer_text': 'Предпочитать текстовый ввод',
            'raw_key_events': 'Сырые события клавиш',
            'gamepad_support': 'Поддержка геймпада',
            'mouse_bind': 'Режим привязки мыши',
            'mouse_bind_off': 'Выкл',
            'mouse_bind_left': 'Левый клик',
            'mouse_bind_right': 'Правый клик',

            'window_settings': 'Настройки окна',
            'window_title': 'Заголовок окна',
            'always_on_top': 'Всегда сверху',
            'borderless': 'Без рамок',
            'fullscreen': 'Запуск в полноэкранном режиме',
            'window_x': 'Позиция окна X',
            'window_y': 'Позиция окна Y',
            'window_width': 'Ширина окна',
            'window_height': 'Высота окна',
            'background_color': 'Цвет фона',
            'disable_screensaver': 'Отключить скринсейвер',

            'advanced_settings': 'Дополнительные настройки',
            'time_limit': 'Ограничение по времени (секунды)',
            'screen_off_timeout': 'Таймаут отключения экрана',
            'turn_screen_off': 'Выключить экран устройства',
            'power_off_on_close': 'Выключить при закрытии',
            'no_power_on': 'Не включать',
            'kill_adb_on_close': 'Завершить ADB при закрытии',
            'force_adb_forward': 'Принудительная переадресация ADB',
            'tunnel_host': 'Хост туннеля',
            'tunnel_port': 'Порт туннеля',

            'start_mirror': 'Запустить зеркалирование',
            'stop_mirror': 'Остановить зеркалирование',
            'status_connected': 'Подключено',
            'status_disconnected': 'Отключено',
            'status_mirroring': 'Зеркалирование активно',
            'status_stopped': 'Остановлено',

            'language': 'Язык',
            'theme': 'Тема',
            'light_theme': 'Светлая',
            'dark_theme': 'Тёмная',

            'error_title': 'Ошибка',
            'success_title': 'Успех',
            'warning_title': 'Предупреждение',

            'connecting': 'Подключение...',
            'starting': 'Запуск зеркалирования...',
            'stopping': 'Остановка...',

            'device_name': 'Имя устройства',
            'select_device': 'Выбрать устройство',

            'help': 'Помощь',
            'about': 'О программе',
            'about_text': 'scrcpy-gui v1.0\n\nСовременный GUI для scrcpy со стилем Material Design 3.\n\nОригинальный scrcpy от Genymobile\nGUI от команды scrcpy-gui',

            'apply': 'Применить',
            'reset': 'Сбросить',
            'save_config': 'Сохранить конфиг',
            'load_config': 'Загрузить конфиг',
        }
    }

    def __init__(self, language='en'):
        self.current_language = language

    def set_language(self, language):
        if language in self.TRANSLATIONS:
            self.current_language = language

    def get(self, key):
        return self.TRANSLATIONS[self.current_language].get(key, key)


class MaterialColor:
    """Material Design 3 color palette"""

    PRIMARY = "#6750A4"
    ON_PRIMARY = "#FFFFFF"
    PRIMARY_CONTAINER = "#EADDFF"
    ON_PRIMARY_CONTAINER = "#21005D"
    SECONDARY = "#625B71"
    ON_SECONDARY = "#FFFFFF"
    SECONDARY_CONTAINER = "#E8DEF8"
    ON_SECONDARY_CONTAINER = "#1D192B"
    TERTIARY = "#7D5260"
    ON_TERTIARY = "#FFFFFF"
    TERTIARY_CONTAINER = "#FFD8E4"
    ON_TERTIARY_CONTAINER = "#31111D"
    ERROR = "#B3261E"
    ON_ERROR = "#FFFFFF"
    ERROR_CONTAINER = "#F9DEDC"
    ON_ERROR_CONTAINER = "#410E0B"
    OUTLINE = "#79747E"
    BACKGROUND = "#FFFBFE"
    ON_BACKGROUND = "#1C1B1F"
    SURFACE = "#FFFBFE"
    ON_SURFACE = "#1C1B1F"
    SURFACE_VARIANT = "#E7E0EC"
    ON_SURFACE_VARIANT = "#49454F"

    @classmethod
    def dark(cls):
        return {
            'PRIMARY': "#D0BCFF",
            'ON_PRIMARY': "#381E72",
            'PRIMARY_CONTAINER': "#4F378B",
            'ON_PRIMARY_CONTAINER': "#EADDFF",
            'SECONDARY': "#CCC2DC",
            'ON_SECONDARY': "#332D41",
            'SECONDARY_CONTAINER': "#4A4458",
            'ON_SECONDARY_CONTAINER': "#E8DEF8",
            'TERTIARY': "#EFB8C8",
            'ON_TERTIARY': "#492532",
            'TERTIARY_CONTAINER': "#633B48",
            'ON_TERTIARY_CONTAINER': "#FFD8E4",
            'ERROR': "#F2B8B5",
            'ON_ERROR': "#601410",
            'ERROR_CONTAINER': "#8C1D18",
            'ON_ERROR_CONTAINER': "#F9DEDC",
            'OUTLINE': "#938F99",
            'BACKGROUND': "#1C1B1F",
            'ON_BACKGROUND': "#E6E1E5",
            'SURFACE': "#1C1B1F",
            'ON_SURFACE': "#E6E1E5",
            'SURFACE_VARIANT': "#49454F",
            'ON_SURFACE_VARIANT': "#CAC4D0",
        }


class ScrcpyWorker(QThread):
    """Worker thread for running scrcpy"""

    started = Signal()
    finished = Signal(int)
    error = Signal(str)
    output = Signal(str)

    def __init__(self, command_args):
        super().__init__()
        self.command_args = command_args
        self.process = None

    def run(self):
        try:
            cmd = ['scrcpy'] + self.command_args

            self.process = QProcess()
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            self.process.readyReadStandardOutput.connect(
                lambda: self.output.emit(self.process.readAllStandardOutput().data().decode('utf-8', errors='ignore'))
            )
            self.process.finished.connect(lambda code, status: self.finished.emit(code))

            self.started.emit()

            program = cmd[0]
            args = cmd[1:] if len(cmd) > 1 else []

            self.process.start(program, args)

            if not self.process.waitForStarted(5000):
                self.error.emit(f"Failed to start scrcpy: {self.process.errorString()}")
                return

            self.process.waitForFinished(-1)

        except Exception as e:
            self.error.emit(str(e))

    def stop(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.terminate()
            self.process.waitForFinished(3000)
            if self.process.state() == QProcess.Running:
                self.process.kill()


class AdbWorker(QThread):
    """Worker thread for ADB commands"""

    devices_updated = Signal(list)
    command_finished = Signal(bool, str)

    def __init__(self):
        super().__init__()
        self.command = None
        self.args = []

    def set_command(self, command, args=None):
        self.command = command
        self.args = args or []

    def run(self):
        try:
            if self.command == 'devices':
                result = subprocess.run(
                    ['adb', 'devices'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                devices = []
                lines = result.stdout.strip().split('\n')[1:]
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            devices.append({
                                'serial': parts[0],
                                'status': parts[1]
                            })
                self.devices_updated.emit(devices)

            elif self.command == 'connect':
                result = subprocess.run(
                    ['adb', 'connect'] + self.args,
                    capture_output=True,
                    text=True,
                    timeout=15
                )
                success = 'connected' in result.stdout.lower() or 'already connected' in result.stdout.lower()
                self.command_finished.emit(success, result.stdout + result.stderr)

            elif self.command == 'disconnect':
                result = subprocess.run(
                    ['adb', 'disconnect'] + self.args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                self.command_finished.emit(True, result.stdout + result.stderr)

            elif self.command == 'tcpip':
                result = subprocess.run(
                    ['adb', 'tcpip'] + self.args,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                success = result.returncode == 0
                self.command_finished.emit(success, result.stdout + result.stderr)

            elif self.command == 'shell_ip':
                result = subprocess.run(
                    ['adb', 'shell', 'ip', 'route'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                ip = ''
                for line in result.stdout.split('\n'):
                    if 'default' in line:
                        parts = line.split()
                        if len(parts) >= 9:
                            ip = parts[8]
                            break
                self.command_finished.emit(bool(ip), ip)

        except subprocess.TimeoutExpired:
            self.command_finished.emit(False, "Command timed out")
        except Exception as e:
            self.command_finished.emit(False, str(e))


class MaterialButton(QPushButton):
    """Material Design styled button"""

    def __init__(self, text, parent=None, variant='filled'):
        super().__init__(text, parent)
        self.variant = variant
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))

        if variant == 'filled':
            self.setStyleSheet("""
                QPushButton {
                    background-color: #6750A4;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #7F67BE;
                }
                QPushButton:pressed {
                    background-color: #4F378B;
                }
                QPushButton:disabled {
                    background-color: #BDBDBD;
                    color: #757575;
                }
            """)
        elif variant == 'outlined':
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #6750A4;
                    border: 1px solid #6750A4;
                    border-radius: 20px;
                    padding: 10px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: rgba(103, 80, 164, 0.08);
                }
                QPushButton:pressed {
                    background-color: rgba(103, 80, 164, 0.12);
                }
            """)
        elif variant == 'tonal':
            self.setStyleSheet("""
                QPushButton {
                    background-color: #E8DEF8;
                    color: #1D192B;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 24px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #CCC2DC;
                }
                QPushButton:pressed {
                    background-color: #4A4458;
                }
            """)


class MaterialCard(QFrame):
    """Material Design card widget"""

    def __init__(self, parent=None, elevation=1):
        super().__init__(parent)
        self.setObjectName("materialCard")
        self.setStyleSheet("""
            QFrame#materialCard {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)

        if elevation > 0:
            self.setGraphicsEffect(None)


class MaterialCheckBox(QCheckBox):
    """Material Design checkbox"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setStyleSheet("""
            QCheckBox {
                color: #1C1B1F;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #79747E;
                background-color: transparent;
            }
            QCheckBox::indicator:checked {
                background-color: #6750A4;
                border-color: #6750A4;
            }
            QCheckBox::indicator:hover {
                border-color: #6750A4;
            }
        """)


class MaterialLineEdit(QLineEdit):
    """Material Design text input"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 16px;
                color: #1C1B1F;
            }
            QLineEdit:focus {
                border: 2px solid #6750A4;
                background-color: #FFFFFF;
            }
            QLineEdit:hover {
                background-color: #EEEEEE;
            }
        """)


class MaterialComboBox(QComboBox):
    """Material Design combo box"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QComboBox {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 16px;
                color: #1C1B1F;
            }
            QComboBox:focus {
                border: 2px solid #6750A4;
                background-color: #FFFFFF;
            }
            QComboBox:hover {
                background-color: #EEEEEE;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6750A4;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                selection-background-color: #E8DEF8;
                selection-color: #1D192B;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                height: 40px;
                padding: 5px 16px;
            }
        """)


class MaterialSpinBox(QSpinBox):
    """Material Design spin box"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QSpinBox {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 16px;
                color: #1C1B1F;
            }
            QSpinBox:focus {
                border: 2px solid #6750A4;
                background-color: #FFFFFF;
            }
            QSpinBox:hover {
                background-color: #EEEEEE;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                width: 20px;
            }
        """)


class MaterialDoubleSpinBox(QDoubleSpinBox):
    """Material Design double spin box"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Segoe UI", 10))
        self.setMinimumHeight(40)
        self.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px 16px;
                color: #1C1B1F;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #6750A4;
                background-color: #FFFFFF;
            }
            QDoubleSpinBox:hover {
                background-color: #EEEEEE;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                border: none;
                width: 20px;
            }
        """)


class TutorialDialog(QDialog):
    """Tutorial dialog for connection instructions"""

    def __init__(self, tutorial_type, lang_manager, parent=None):
        super().__init__(parent)
        self.lang = lang_manager
        self.setWindowTitle("Tutorial" if lang_manager.current_language == 'en' else "Инструкция")
        self.setMinimumSize(500, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        if tutorial_type == 'usb':
            title = self.lang.get('usb_tutorial_title')
            steps = [
                self.lang.get('usb_step1'),
                self.lang.get('usb_step2'),
                self.lang.get('usb_step3'),
                self.lang.get('usb_step4'),
                self.lang.get('usb_step5'),
                self.lang.get('usb_step6'),
                self.lang.get('usb_step7'),
            ]
        else:
            title = self.lang.get('wifi_tutorial_title')
            steps = [
                self.lang.get('wifi_step1'),
                self.lang.get('wifi_step2'),
                self.lang.get('wifi_step3'),
                self.lang.get('wifi_step4'),
                self.lang.get('wifi_step5'),
                self.lang.get('wifi_step6'),
            ]

        titleLabel = QLabel(title)
        titleLabel.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        titleLabel.setStyleSheet("color: #6750A4;")
        layout.addWidget(titleLabel)

        for i, step in enumerate(steps, 1):
            stepLayout = QHBoxLayout()
            stepNum = QLabel(f"{i}")
            stepNum.setFixedSize(30, 30)
            stepNum.setStyleSheet("""
                background-color: #E8DEF8;
                color: #1D192B;
                border-radius: 15px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            """)
            stepNum.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

            stepText = QLabel(step)
            stepText.setFont(QFont("Segoe UI", 10))
            stepText.setWordWrap(True)
            stepText.setStyleSheet("color: #1C1B1F; padding: 5px;")

            stepLayout.addWidget(stepNum)
            stepLayout.addWidget(stepText, 1)
            layout.addLayout(stepLayout)

        closeBtn = MaterialButton(self.lang.get('connect_btn') if lang_manager.current_language == 'en' else "Понятно")
        closeBtn.clicked.connect(self.accept)
        layout.addWidget(closeBtn)


class ScrcpyGUI(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.lang = LanguageManager('en')
        self.dark_mode = False
        self.scrcpy_process = None
        self.adb_worker = AdbWorker()
        self.devices = []
        self.current_device = None

        self.setup_ui()
        self.apply_theme()
        self.load_config()

        self.refresh_devices()

    def setup_ui(self):
        self.setWindowTitle(self.lang.get('app_title'))
        self.setMinimumSize(1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        splitter.setSizes([400, 800])

        main_layout.addWidget(splitter)

        self.create_menu_bar()

    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("leftPanel")
        panel.setMinimumWidth(350)
        panel.setMaximumWidth(450)

        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        header_label = QLabel(self.lang.get('app_title'))
        header_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        header_label.setStyleSheet("color: #6750A4; padding: 10px 0;")
        layout.addWidget(header_label)

        status_card = MaterialCard()
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(20, 20, 20, 20)

        self.status_label = QLabel(self.lang.get('status_disconnected'))
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #79747E;")
        status_layout.addWidget(self.status_label)

        self.device_label = QLabel("")
        self.device_label.setFont(QFont("Segoe UI", 11))
        self.device_label.setStyleSheet("color: #6750A4;")
        status_layout.addWidget(self.device_label)

        layout.addWidget(status_card)

        connection_group = QGroupBox(self.lang.get('connection_type'))
        connection_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        connection_layout = QVBoxLayout(connection_group)

        self.connection_type_group = QButtonGroup(self)

        usb_radio = QRadioButton(self.lang.get('usb_connection'))
        usb_radio.setFont(QFont("Segoe UI", 10))
        usb_radio.setChecked(True)
        usb_radio.toggled.connect(self.on_connection_type_changed)
        self.connection_type_group.addButton(usb_radio, 0)
        connection_layout.addWidget(usb_radio)

        wifi_radio = QRadioButton(self.lang.get('wifi_connection'))
        wifi_radio.setFont(QFont("Segoe UI", 10))
        wifi_radio.toggled.connect(self.on_connection_type_changed)
        self.connection_type_group.addButton(wifi_radio, 1)
        connection_layout.addWidget(wifi_radio)

        layout.addWidget(connection_group)

        device_card = MaterialCard()
        device_layout = QVBoxLayout(device_card)
        device_layout.setContentsMargins(20, 20, 20, 20)
        device_layout.setSpacing(12)

        self.device_combo = MaterialComboBox()
        self.device_combo.addItem(self.lang.get('select_device'), "")
        self.device_combo.currentIndexChanged.connect(self.on_device_selected)
        device_layout.addWidget(QLabel(self.lang.get('device_serial')))
        device_layout.addWidget(self.device_combo)

        self.ip_input = MaterialLineEdit()
        self.ip_input.setPlaceholderText("192.168.1.100")
        self.ip_input.setVisible(False)
        device_layout.addWidget(QLabel(self.lang.get('device_ip')))
        device_layout.addWidget(self.ip_input)

        self.port_input = MaterialSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(5555)
        self.port_input.setVisible(False)
        device_layout.addWidget(QLabel(self.lang.get('port')))
        device_layout.addWidget(self.port_input)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.refresh_btn = MaterialButton(self.lang.get('refresh_btn'), variant='tonal')
        self.refresh_btn.clicked.connect(self.refresh_devices)
        self.refresh_btn.setMinimumHeight(36)
        btn_layout.addWidget(self.refresh_btn)

        self.tutorial_btn = MaterialButton("?", variant='outlined')
        self.tutorial_btn.setFixedSize(36, 36)
        self.tutorial_btn.clicked.connect(self.show_tutorial)
        btn_layout.addWidget(self.tutorial_btn)

        device_layout.addLayout(btn_layout)

        self.connect_btn = MaterialButton(self.lang.get('connect_btn'))
        self.connect_btn.clicked.connect(self.connect_device)
        device_layout.addWidget(self.connect_btn)

        layout.addWidget(device_card)

        action_card = MaterialCard()
        action_layout = QVBoxLayout(action_card)
        action_layout.setContentsMargins(20, 20, 20, 20)
        action_layout.setSpacing(12)

        self.mirror_btn = MaterialButton(self.lang.get('start_mirror'))
        self.mirror_btn.clicked.connect(self.toggle_mirror)
        self.mirror_btn.setEnabled(False)
        action_layout.addWidget(self.mirror_btn)

        self.stop_btn = MaterialButton(self.lang.get('stop_mirror'), variant='outlined')
        self.stop_btn.clicked.connect(self.stop_mirror)
        self.stop_btn.setEnabled(False)
        action_layout.addWidget(self.stop_btn)

        layout.addWidget(action_card)

        layout.addStretch()

        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel(self.lang.get('language')))
        self.lang_combo = MaterialComboBox()
        self.lang_combo.addItem("English", "en")
        self.lang_combo.addItem("Русский", "ru")
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        lang_layout.addWidget(self.lang_combo)
        layout.addLayout(lang_layout)

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel(self.lang.get('theme')))
        self.theme_combo = MaterialComboBox()
        self.theme_combo.addItem(self.lang.get('light_theme'), "light")
        self.theme_combo.addItem(self.lang.get('dark_theme'), "dark")
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        return panel

    def create_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Segoe UI", 11))
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(False)

        self.tabs.addTab(self.create_connect_tab(), self.lang.get('connect_tab'))
        self.tabs.addTab(self.create_video_tab(), self.lang.get('video_tab'))
        self.tabs.addTab(self.create_audio_tab(), self.lang.get('audio_tab'))
        self.tabs.addTab(self.create_recording_tab(), self.lang.get('recording_tab'))
        self.tabs.addTab(self.create_control_tab(), self.lang.get('control_tab'))
        self.tabs.addTab(self.create_window_tab(), self.lang.get('window_tab'))
        self.tabs.addTab(self.create_advanced_tab(), self.lang.get('advanced_tab'))

        layout.addWidget(self.tabs)

        return panel

    def create_connect_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        info_label = QLabel(
            "<h3 style='color: #6750A4;'>" +
            "Quick Start Guide / Быстрый старт" +
            "</h3>"
            "<p style='color: #1C1B1F;'>"
            "1. Connect device via USB / Подключите устройство через USB<br>"
            "2. Enable USB debugging / Включите отладку по USB<br>"
            "3. Click Refresh / Нажмите Обновить<br>"
            "4. Select device and connect / Выберите устройство и подключитесь<br>"
            "5. Start mirroring / Запустите зеркалирование"
            "</p>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def create_video_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        video_group = QGroupBox(self.lang.get('video_settings'))
        video_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        video_layout = QVBoxLayout(video_group)
        video_layout.setSpacing(15)

        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel(self.lang.get('resolution')))
        self.resolution_spin = MaterialSpinBox()
        self.resolution_spin.setRange(0, 4096)
        self.resolution_spin.setValue(0)
        self.resolution_spin.setSpecialValueText(self.lang.get('unlimited'))
        res_layout.addWidget(self.resolution_spin)
        video_layout.addLayout(res_layout)

        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel(self.lang.get('bitrate')))
        self.bitrate_spin = MaterialDoubleSpinBox()
        self.bitrate_spin.setRange(0.1, 100)
        self.bitrate_spin.setValue(8)
        self.bitrate_spin.setSuffix(" " + self.lang.get('bitrate_unit'))
        bitrate_layout.addWidget(self.bitrate_spin)
        video_layout.addLayout(bitrate_layout)

        fps_layout = QHBoxLayout()
        fps_layout.addWidget(QLabel(self.lang.get('max_fps')))
        self.fps_spin = MaterialSpinBox()
        self.fps_spin.setRange(1, 120)
        self.fps_spin.setValue(60)
        fps_layout.addWidget(self.fps_spin)
        video_layout.addLayout(fps_layout)

        display_layout = QHBoxLayout()
        display_layout.addWidget(QLabel(self.lang.get('display_id')))
        self.display_spin = MaterialSpinBox()
        self.display_spin.setRange(0, 10)
        self.display_spin.setValue(0)
        display_layout.addWidget(self.display_spin)
        video_layout.addLayout(display_layout)

        codec_layout = QHBoxLayout()
        codec_layout.addWidget(QLabel(self.lang.get('video_codec')))
        self.codec_combo = MaterialComboBox()
        self.codec_combo.addItems(['h264', 'h265', 'av1'])
        codec_layout.addWidget(self.codec_combo)
        video_layout.addLayout(codec_layout)

        crop_layout = QHBoxLayout()
        crop_layout.addWidget(QLabel(self.lang.get('crop_video')))
        self.crop_input = MaterialLineEdit()
        self.crop_input.setPlaceholderText(self.lang.get('crop_format'))
        crop_layout.addWidget(self.crop_input)
        video_layout.addLayout(crop_layout)

        layout.addWidget(video_group)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def create_audio_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        audio_group = QGroupBox(self.lang.get('audio_settings'))
        audio_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        audio_layout = QVBoxLayout(audio_group)
        audio_layout.setSpacing(15)

        self.audio_check = MaterialCheckBox(self.lang.get('enable_audio'))
        self.audio_check.setChecked(True)
        audio_layout.addWidget(self.audio_check)

        bitrate_layout = QHBoxLayout()
        bitrate_layout.addWidget(QLabel(self.lang.get('audio_bitrate')))
        self.audio_bitrate_spin = MaterialSpinBox()
        self.audio_bitrate_spin.setRange(8, 320)
        self.audio_bitrate_spin.setValue(128)
        self.audio_bitrate_spin.setSuffix(" Kbps")
        bitrate_layout.addWidget(self.audio_bitrate_spin)
        audio_layout.addLayout(bitrate_layout)

        codec_layout = QHBoxLayout()
        codec_layout.addWidget(QLabel(self.lang.get('audio_codec')))
        self.audio_codec_combo = MaterialComboBox()
        self.audio_codec_combo.addItems(['opus', 'aac', 'flac', 'raw'])
        codec_layout.addWidget(self.audio_codec_combo)
        audio_layout.addLayout(codec_layout)

        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel(self.lang.get('audio_source')))
        self.audio_source_combo = MaterialComboBox()
        self.audio_source_combo.addItems([
            self.lang.get('audio_output'),
            self.lang.get('audio_playback'),
            self.lang.get('audio_mic')
        ])
        source_layout.addWidget(self.audio_source_combo)
        audio_layout.addLayout(source_layout)

        layout.addWidget(audio_group)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def create_recording_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        record_group = QGroupBox(self.lang.get('recording_settings'))
        record_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        record_layout = QVBoxLayout(record_group)
        record_layout.setSpacing(15)

        self.record_check = MaterialCheckBox(self.lang.get('enable_recording'))
        record_layout.addWidget(self.record_check)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel(self.lang.get('record_format')))
        self.record_format_combo = MaterialComboBox()
        self.record_format_combo.addItems(['mp4', 'mkv'])
        format_layout.addWidget(self.record_format_combo)
        record_layout.addLayout(format_layout)

        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel(self.lang.get('record_file')))
        self.record_file_input = MaterialLineEdit()
        self.record_file_input.setPlaceholderText("scrcpy.mp4")
        file_layout.addWidget(self.record_file_input)
        browse_btn = MaterialButton(self.lang.get('browse'), variant='tonal')
        browse_btn.setFixedHeight(40)
        browse_btn.clicked.connect(self.browse_record_file)
        file_layout.addWidget(browse_btn)
        record_layout.addLayout(file_layout)

        self.no_video_playback_check = MaterialCheckBox(self.lang.get('no_video_playback'))
        record_layout.addWidget(self.no_video_playback_check)

        self.no_audio_playback_check = MaterialCheckBox(self.lang.get('no_audio_playback'))
        record_layout.addWidget(self.no_audio_playback_check)

        layout.addWidget(record_group)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def create_control_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        control_group = QGroupBox(self.lang.get('control_settings'))
        control_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        control_layout = QVBoxLayout(control_group)
        control_layout.setSpacing(15)

        self.prefer_text_check = MaterialCheckBox(self.lang.get('prefer_text'))
        control_layout.addWidget(self.prefer_text_check)

        self.raw_key_check = MaterialCheckBox(self.lang.get('raw_key_events'))
        control_layout.addWidget(self.raw_key_check)

        self.gamepad_check = MaterialCheckBox(self.lang.get('gamepad_support'))
        control_layout.addWidget(self.gamepad_check)

        bind_layout = QHBoxLayout()
        bind_layout.addWidget(QLabel(self.lang.get('mouse_bind')))
        self.mouse_bind_combo = MaterialComboBox()
        self.mouse_bind_combo.addItems([
            self.lang.get('mouse_bind_off'),
            self.lang.get('mouse_bind_left'),
            self.lang.get('mouse_bind_right')
        ])
        bind_layout.addWidget(self.mouse_bind_combo)
        control_layout.addLayout(bind_layout)

        layout.addWidget(control_group)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def create_window_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        window_group = QGroupBox(self.lang.get('window_settings'))
        window_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        window_layout = QVBoxLayout(window_group)
        window_layout.setSpacing(15)

        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel(self.lang.get('window_title')))
        self.window_title_input = MaterialLineEdit()
        self.window_title_input.setPlaceholderText("scrcpy")
        title_layout.addWidget(self.window_title_input)
        window_layout.addLayout(title_layout)

        self.always_on_top_check = MaterialCheckBox(self.lang.get('always_on_top'))
        window_layout.addWidget(self.always_on_top_check)

        self.borderless_check = MaterialCheckBox(self.lang.get('borderless'))
        window_layout.addWidget(self.borderless_check)

        self.fullscreen_check = MaterialCheckBox(self.lang.get('fullscreen'))
        window_layout.addWidget(self.fullscreen_check)

        pos_layout = QHBoxLayout()
        pos_layout.addWidget(QLabel(self.lang.get('window_x')))
        self.window_x_spin = MaterialSpinBox()
        self.window_x_spin.setRange(-10000, 10000)
        self.window_x_spin.setValue(-1)
        pos_layout.addWidget(self.window_x_spin)
        pos_layout.addWidget(QLabel(self.lang.get('window_y')))
        self.window_y_spin = MaterialSpinBox()
        self.window_y_spin.setRange(-10000, 10000)
        self.window_y_spin.setValue(-1)
        pos_layout.addWidget(self.window_y_spin)
        window_layout.addLayout(pos_layout)

        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel(self.lang.get('window_width')))
        self.window_w_spin = MaterialSpinBox()
        self.window_w_spin.setRange(100, 10000)
        self.window_w_spin.setValue(-1)
        size_layout.addWidget(self.window_w_spin)
        size_layout.addWidget(QLabel(self.lang.get('window_height')))
        self.window_h_spin = MaterialSpinBox()
        self.window_h_spin.setRange(100, 10000)
        self.window_h_spin.setValue(-1)
        size_layout.addWidget(self.window_h_spin)
        window_layout.addLayout(size_layout)

        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel(self.lang.get('background_color')))
        self.bg_color_input = MaterialLineEdit()
        self.bg_color_input.setPlaceholderText("#222")
        color_layout.addWidget(self.bg_color_input)
        window_layout.addLayout(color_layout)

        self.disable_screensaver_check = MaterialCheckBox(self.lang.get('disable_screensaver'))
        window_layout.addWidget(self.disable_screensaver_check)

        layout.addWidget(window_group)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def create_advanced_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        advanced_group = QGroupBox(self.lang.get('advanced_settings'))
        advanced_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        advanced_layout = QVBoxLayout(advanced_group)
        advanced_layout.setSpacing(15)

        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel(self.lang.get('time_limit')))
        self.time_limit_spin = MaterialSpinBox()
        self.time_limit_spin.setRange(0, 3600)
        self.time_limit_spin.setValue(0)
        self.time_limit_spin.setSpecialValueText("∞")
        time_layout.addWidget(self.time_limit_spin)
        advanced_layout.addLayout(time_layout)

        self.screen_off_check = MaterialCheckBox(self.lang.get('turn_screen_off'))
        advanced_layout.addWidget(self.screen_off_check)

        self.power_off_check = MaterialCheckBox(self.lang.get('power_off_on_close'))
        advanced_layout.addWidget(self.power_off_check)

        self.no_power_on_check = MaterialCheckBox(self.lang.get('no_power_on'))
        advanced_layout.addWidget(self.no_power_on_check)

        self.kill_adb_check = MaterialCheckBox(self.lang.get('kill_adb_on_close'))
        advanced_layout.addWidget(self.kill_adb_check)

        self.force_adb_check = MaterialCheckBox(self.lang.get('force_adb_forward'))
        advanced_layout.addWidget(self.force_adb_check)

        tunnel_layout = QHBoxLayout()
        tunnel_layout.addWidget(QLabel(self.lang.get('tunnel_host')))
        self.tunnel_host_input = MaterialLineEdit()
        tunnel_layout.addWidget(self.tunnel_host_input)
        tunnel_layout.addWidget(QLabel(self.lang.get('tunnel_port')))
        self.tunnel_port_spin = MaterialSpinBox()
        self.tunnel_port_spin.setRange(1, 65535)
        self.tunnel_port_spin.setValue(22)
        tunnel_layout.addWidget(self.tunnel_port_spin)
        advanced_layout.addLayout(tunnel_layout)

        layout.addWidget(advanced_group)

        config_layout = QHBoxLayout()
        config_layout.setSpacing(10)

        save_btn = MaterialButton(self.lang.get('save_config'), variant='tonal')
        save_btn.clicked.connect(self.save_config)
        config_layout.addWidget(save_btn)

        load_btn = MaterialButton(self.lang.get('load_config'), variant='tonal')
        load_btn.clicked.connect(self.load_config_dialog)
        config_layout.addWidget(load_btn)

        reset_btn = MaterialButton(self.lang.get('reset'), variant='outlined')
        reset_btn.clicked.connect(self.reset_settings)
        config_layout.addWidget(reset_btn)

        layout.addLayout(config_layout)
        layout.addStretch()
        scroll.setWidget(content)
        return scroll

    def create_menu_bar(self):
        menubar = self.menuBar()

        help_menu = menubar.addMenu(self.lang.get('help'))

        about_action = QAction(self.lang.get('about'), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.about(self, self.lang.get('about'), self.lang.get('about_text'))

    def show_tutorial(self):
        conn_type = self.connection_type_group.checkedId()
        tutorial_type = 'usb' if conn_type == 0 else 'wifi'
        dialog = TutorialDialog(tutorial_type, self.lang, self)
        dialog.exec()

    def on_connection_type_changed(self):
        conn_type = self.connection_type_group.checkedId()
        is_wifi = conn_type == 1

        self.ip_input.setVisible(is_wifi)
        self.port_input.setVisible(is_wifi)
        self.device_combo.setVisible(not is_wifi)

        tutorial_type = 'usb' if conn_type == 0 else 'wifi'
        self.tutorial_btn.clicked.disconnect()
        self.tutorial_btn.clicked.connect(
            lambda t=tutorial_type: self.show_tutorial_dialog(t)
        )

    def show_tutorial_dialog(self, tutorial_type):
        dialog = TutorialDialog(tutorial_type, self.lang, self)
        dialog.exec()

    def refresh_devices(self):
        self.adb_worker.set_command('devices')
        self.adb_worker.start()

    def on_device_selected(self, index):
        if index > 0:
            serial = self.device_combo.currentData()
            self.current_device = serial
            self.mirror_btn.setEnabled(True)

    def connect_device(self):
        conn_type = self.connection_type_group.checkedId()

        if conn_type == 0:
            serial = self.device_combo.currentData()
            if serial:
                self.current_device = serial
                self.on_connection_success(f"Device {serial} selected")
            else:
                QMessageBox.warning(self, self.lang.get('warning_title'),
                                   self.lang.get('no_devices'))
        else:
            ip = self.ip_input.text().strip()
            port = self.port_input.value()

            if not ip:
                QMessageBox.warning(self, self.lang.get('warning_title'),
                                   "Please enter IP address")
                return

            self.adb_worker.set_command('connect', [f"{ip}:{port}"])
            self.adb_worker.command_finished.connect(self.on_connection_result)
            self.adb_worker.start()

    def on_connection_result(self, success, message):
        self.adb_worker.command_finished.disconnect(self.on_connection_result)
        if success:
            self.on_connection_success(message)
        else:
            QMessageBox.critical(self, self.lang.get('error_title'), message)

    def on_connection_success(self, message):
        self.status_label.setText(self.lang.get('status_connected'))
        self.status_label.setStyleSheet("color: #4CAF50;")

        if self.current_device:
            self.device_label.setText(f"Device: {self.current_device}")

        self.mirror_btn.setEnabled(True)
        QMessageBox.information(self, self.lang.get('success_title'), message)

    def toggle_mirror(self):
        if self.scrcpy_process and self.scrcpy_process.isRunning():
            self.stop_mirror()
        else:
            self.start_mirror()

    def start_mirror(self):
        args = self.build_scrcpy_args()

        if self.current_device:
            args.extend(['-s', self.current_device])

        self.scrcpy_process = ScrcpyWorker(args)
        self.scrcpy_process.started.connect(self.on_mirror_started)
        self.scrcpy_process.finished.connect(self.on_mirror_finished)
        self.scrcpy_process.error.connect(self.on_mirror_error)
        self.scrcpy_process.start()

    def build_scrcpy_args(self):
        args = []

        resolution = self.resolution_spin.value()
        if resolution > 0:
            args.extend(['-m', str(resolution)])

        bitrate = self.bitrate_spin.value()
        if bitrate > 0:
            args.extend(['-b', f'{int(bitrate * 1000000)}'])

        fps = self.fps_spin.value()
        if fps < 60:
            args.extend(['--max-fps', str(fps)])

        display = self.display_spin.value()
        if display > 0:
            args.extend(['--display-id', str(display)])

        codec = self.codec_combo.currentText()
        if codec != 'h264':
            args.extend(['--video-codec', codec])

        crop = self.crop_input.text().strip()
        if crop:
            args.extend(['--crop', crop])

        if self.audio_check.isChecked():
            args.append('--audio')
            audio_bitrate = self.audio_bitrate_spin.value()
            args.extend(['--audio-bit-rate', f'{audio_bitrate}K'])

            audio_codec = self.audio_codec_combo.currentText()
            if audio_codec != 'opus':
                args.extend(['--audio-codec', audio_codec])

            audio_source = self.audio_source_combo.currentText()
            source_map = {
                self.lang.get('audio_output'): 'output',
                self.lang.get('audio_playback'): 'playback',
                self.lang.get('audio_mic'): 'mic'
            }
            args.extend(['--audio-source', source_map.get(audio_source, 'output')])
        else:
            args.append('--no-audio')

        if self.record_check.isChecked():
            record_format = self.record_format_combo.currentText()
            record_file = self.record_file_input.text().strip()
            if record_file:
                args.extend(['-r', f'{record_file}.{record_format}'])
            else:
                args.extend(['-r', f'scrcpy.{record_format}'])

            if self.no_video_playback_check.isChecked():
                args.append('--no-video-playback')
            if self.no_audio_playback_check.isChecked():
                args.append('--no-audio-playback')

        if self.prefer_text_check.isChecked():
            args.append('--prefer-text')

        if self.raw_key_check.isChecked():
            args.append('--raw-key-events')

        if self.gamepad_check.isChecked():
            args.append('--gamepad')

        mouse_bind = self.mouse_bind_combo.currentIndex()
        if mouse_bind == 1:
            args.extend(['--mouse-bind', '1'])
        elif mouse_bind == 2:
            args.extend(['--mouse-bind', '2'])

        window_title = self.window_title_input.text().strip()
        if window_title:
            args.extend(['--window-title', window_title])

        if self.always_on_top_check.isChecked():
            args.append('--always-on-top')

        if self.borderless_check.isChecked():
            args.append('--window-borderless')

        if self.fullscreen_check.isChecked():
            args.append('--fullscreen')

        window_x = self.window_x_spin.value()
        window_y = self.window_y_spin.value()
        if window_x >= 0 and window_y >= 0:
            args.extend(['--window-x', str(window_x), '--window-y', str(window_y)])

        window_w = self.window_w_spin.value()
        window_h = self.window_h_spin.value()
        if window_w > 0 and window_h > 0:
            args.extend(['--window-width', str(window_w), '--window-height', str(window_h)])

        bg_color = self.bg_color_input.text().strip()
        if bg_color:
            args.extend(['--background-color', bg_color])

        if self.disable_screensaver_check.isChecked():
            args.append('--disable-screensaver')

        time_limit = self.time_limit_spin.value()
        if time_limit > 0:
            args.extend(['--time-limit', str(time_limit)])

        if self.screen_off_check.isChecked():
            args.append('--turn-screen-off')

        if self.power_off_check.isChecked():
            args.append('--power-off-on-close')

        if self.no_power_on_check.isChecked():
            args.append('--no-power-on')

        if self.kill_adb_check.isChecked():
            args.append('--kill-adb-on-close')

        if self.force_adb_check.isChecked():
            args.append('--force-adb-forward')

        tunnel_host = self.tunnel_host_input.text().strip()
        if tunnel_host:
            tunnel_port = self.tunnel_port_spin.value()
            args.extend(['--tunnel-host', tunnel_host, '--tunnel-port', str(tunnel_port)])

        return args

    def on_mirror_started(self):
        self.status_label.setText(self.lang.get('status_mirroring'))
        self.status_label.setStyleSheet("color: #6750A4;")
        self.mirror_btn.setText(self.lang.get('stop_mirror'))
        self.stop_btn.setEnabled(True)
        self.tabs.setEnabled(False)

    def on_mirror_finished(self, code):
        self.status_label.setText(self.lang.get('status_stopped'))
        self.status_label.setStyleSheet("color: #79747E;")
        self.mirror_btn.setText(self.lang.get('start_mirror'))
        self.stop_btn.setEnabled(False)
        self.tabs.setEnabled(True)

        if code != 0:
            QMessageBox.warning(self, self.lang.get('warning_title'),
                               f"scrcpy exited with code {code}")

    def on_mirror_error(self, error):
        QMessageBox.critical(self, self.lang.get('error_title'), error)
        self.stop_mirror()

    def stop_mirror(self):
        if self.scrcpy_process:
            self.scrcpy_process.stop()

    def browse_record_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Record File",
            "",
            "Video Files (*.mp4 *.mkv);;All Files (*)"
        )
        if file_path:
            self.record_file_input.setText(file_path)

    def on_language_changed(self, index):
        lang_code = self.lang_combo.itemData(index)
        self.lang.set_language(lang_code)
        self.update_ui_texts()

    def on_theme_changed(self, index):
        theme = self.theme_combo.itemData(index)
        self.dark_mode = theme == 'dark'
        self.apply_theme()

    def update_ui_texts(self):
        self.setWindowTitle(self.lang.get('app_title'))

        for i in range(self.tabs.count()):
            tab_names = [
                'connect_tab', 'video_tab', 'audio_tab',
                'recording_tab', 'control_tab', 'window_tab', 'advanced_tab'
            ]
            self.tabs.setTabText(i, self.lang.get(tab_names[i]))

    def apply_theme(self):
        if self.dark_mode:
            colors = MaterialColor.dark()
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {colors['BACKGROUND']};
                }}
                QWidget {{
                    background-color: {colors['BACKGROUND']};
                    color: {colors['ON_BACKGROUND']};
                }}
                QGroupBox {{
                    color: {colors['ON_SURFACE']};
                    border: 1px solid {colors['OUTLINE']};
                    border-radius: 8px;
                    margin-top: 12px;
                    padding-top: 10px;
                    font-weight: bold;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }}
                QScrollArea {{
                    border: none;
                    background-color: {colors['BACKGROUND']};
                }}
                QTabWidget::pane {{
                    border: none;
                    background-color: {colors['SURFACE']};
                }}
                QTabBar::tab {{
                    background-color: {colors['SURFACE_VARIANT']};
                    color: {colors['ON_SURFACE_VARIANT']};
                    padding: 10px 20px;
                    margin-right: 2px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }}
                QTabBar::tab:selected {{
                    background-color: {colors['PRIMARY_CONTAINER']};
                    color: {colors['ON_PRIMARY_CONTAINER']};
                }}
                QTabBar::tab:hover:!selected {{
                    background-color: {colors['SURFACE_VARIANT']};
                }}
                QFrame#leftPanel {{
                    background-color: {colors['SURFACE']};
                    border-right: 1px solid {colors['OUTLINE']};
                }}
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #FFFBFE;
                }
                QWidget {
                    background-color: #FFFBFE;
                    color: #1C1B1F;
                }
                QGroupBox {
                    color: #1C1B1F;
                    border: 1px solid #E0E0E0;
                    border-radius: 8px;
                    margin-top: 12px;
                    padding-top: 10px;
                    font-weight: bold;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                QScrollArea {
                    border: none;
                    background-color: #FFFBFE;
                }
                QTabWidget::pane {
                    border: none;
                    background-color: #FFFFFF;
                }
                QTabBar::tab {
                    background-color: #E7E0EC;
                    color: #49454F;
                    padding: 10px 20px;
                    margin-right: 2px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QTabBar::tab:selected {
                    background-color: #EADDFF;
                    color: #21005D;
                }
                QTabBar::tab:hover:!selected {
                    background-color: #ECE6F0;
                }
                QFrame#leftPanel {
                    background-color: #FFFFFF;
                    border-right: 1px solid #E0E0E0;
                }
            """)

    def save_config(self):
        config = {
            'language': self.lang_combo.currentData(),
            'theme': self.theme_combo.currentData(),
            'video': {
                'resolution': self.resolution_spin.value(),
                'bitrate': self.bitrate_spin.value(),
                'fps': self.fps_spin.value(),
                'display': self.display_spin.value(),
                'codec': self.codec_combo.currentText(),
                'crop': self.crop_input.text()
            },
            'audio': {
                'enabled': self.audio_check.isChecked(),
                'bitrate': self.audio_bitrate_spin.value(),
                'codec': self.audio_codec_combo.currentText(),
                'source': self.audio_source_combo.currentText()
            },
            'recording': {
                'enabled': self.record_check.isChecked(),
                'format': self.record_format_combo.currentText(),
                'file': self.record_file_input.text(),
                'no_video': self.no_video_playback_check.isChecked(),
                'no_audio': self.no_audio_playback_check.isChecked()
            },
            'control': {
                'prefer_text': self.prefer_text_check.isChecked(),
                'raw_key': self.raw_key_check.isChecked(),
                'gamepad': self.gamepad_check.isChecked(),
                'mouse_bind': self.mouse_bind_combo.currentIndex()
            },
            'window': {
                'title': self.window_title_input.text(),
                'always_on_top': self.always_on_top_check.isChecked(),
                'borderless': self.borderless_check.isChecked(),
                'fullscreen': self.fullscreen_check.isChecked(),
                'x': self.window_x_spin.value(),
                'y': self.window_y_spin.value(),
                'width': self.window_w_spin.value(),
                'height': self.window_h_spin.value(),
                'bg_color': self.bg_color_input.text(),
                'disable_screensaver': self.disable_screensaver_check.isChecked()
            },
            'advanced': {
                'time_limit': self.time_limit_spin.value(),
                'screen_off': self.screen_off_check.isChecked(),
                'power_off': self.power_off_check.isChecked(),
                'no_power_on': self.no_power_on_check.isChecked(),
                'kill_adb': self.kill_adb_check.isChecked(),
                'force_adb': self.force_adb_check.isChecked(),
                'tunnel_host': self.tunnel_host_input.text(),
                'tunnel_port': self.tunnel_port_spin.value()
            }
        }

        config_path = Path.home() / '.scrcpy-gui' / 'config.json'
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        QMessageBox.information(self, self.lang.get('success_title'),
                               "Configuration saved successfully!")

    def load_config_dialog(self):
        config_path = Path.home() / '.scrcpy-gui' / 'config.json'

        if not config_path.exists():
            QMessageBox.warning(self, self.lang.get('warning_title'),
                               "No saved configuration found.")
            return

        self.load_config()
        QMessageBox.information(self, self.lang.get('success_title'),
                               "Configuration loaded successfully!")

    def load_config(self):
        config_path = Path.home() / '.scrcpy-gui' / 'config.json'

        if not config_path.exists():
            return

        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            if 'language' in config:
                idx = self.lang_combo.findData(config['language'])
                if idx >= 0:
                    self.lang_combo.setCurrentIndex(idx)
                    self.lang.set_language(config['language'])

            if 'theme' in config:
                idx = self.theme_combo.findData(config['theme'])
                if idx >= 0:
                    self.theme_combo.setCurrentIndex(idx)
                    self.dark_mode = config['theme'] == 'dark'
                    self.apply_theme()

            if 'video' in config:
                video = config['video']
                self.resolution_spin.setValue(video.get('resolution', 0))
                self.bitrate_spin.setValue(video.get('bitrate', 8))
                self.fps_spin.setValue(video.get('fps', 60))
                self.display_spin.setValue(video.get('display', 0))

                codec_idx = self.codec_combo.findText(video.get('codec', 'h264'))
                if codec_idx >= 0:
                    self.codec_combo.setCurrentIndex(codec_idx)

                self.crop_input.setText(video.get('crop', ''))

            if 'audio' in config:
                audio = config['audio']
                self.audio_check.setChecked(audio.get('enabled', True))
                self.audio_bitrate_spin.setValue(audio.get('bitrate', 128))

                codec_idx = self.audio_codec_combo.findText(audio.get('codec', 'opus'))
                if codec_idx >= 0:
                    self.audio_codec_combo.setCurrentIndex(codec_idx)

                source_idx = self.audio_source_combo.findText(audio.get('source', 'Output'))
                if source_idx >= 0:
                    self.audio_source_combo.setCurrentIndex(source_idx)

            if 'recording' in config:
                recording = config['recording']
                self.record_check.setChecked(recording.get('enabled', False))

                fmt_idx = self.record_format_combo.findText(recording.get('format', 'mp4'))
                if fmt_idx >= 0:
                    self.record_format_combo.setCurrentIndex(fmt_idx)

                self.record_file_input.setText(recording.get('file', ''))
                self.no_video_playback_check.setChecked(recording.get('no_video', False))
                self.no_audio_playback_check.setChecked(recording.get('no_audio', False))

            if 'control' in config:
                control = config['control']
                self.prefer_text_check.setChecked(control.get('prefer_text', False))
                self.raw_key_check.setChecked(control.get('raw_key', False))
                self.gamepad_check.setChecked(control.get('gamepad', False))
                self.mouse_bind_combo.setCurrentIndex(control.get('mouse_bind', 0))

            if 'window' in config:
                window = config['window']
                self.window_title_input.setText(window.get('title', ''))
                self.always_on_top_check.setChecked(window.get('always_on_top', False))
                self.borderless_check.setChecked(window.get('borderless', False))
                self.fullscreen_check.setChecked(window.get('fullscreen', False))
                self.window_x_spin.setValue(window.get('x', -1))
                self.window_y_spin.setValue(window.get('y', -1))
                self.window_w_spin.setValue(window.get('width', -1))
                self.window_h_spin.setValue(window.get('height', -1))
                self.bg_color_input.setText(window.get('bg_color', ''))
                self.disable_screensaver_check.setChecked(window.get('disable_screensaver', False))

            if 'advanced' in config:
                advanced = config['advanced']
                self.time_limit_spin.setValue(advanced.get('time_limit', 0))
                self.screen_off_check.setChecked(advanced.get('screen_off', False))
                self.power_off_check.setChecked(advanced.get('power_off', False))
                self.no_power_on_check.setChecked(advanced.get('no_power_on', False))
                self.kill_adb_check.setChecked(advanced.get('kill_adb', False))
                self.force_adb_check.setChecked(advanced.get('force_adb', False))
                self.tunnel_host_input.setText(advanced.get('tunnel_host', ''))
                self.tunnel_port_spin.setValue(advanced.get('tunnel_port', 22))

            self.update_ui_texts()

        except Exception as e:
            print(f"Error loading config: {e}")

    def reset_settings(self):
        reply = QMessageBox.question(
            self,
            self.lang.get('warning_title'),
            "Reset all settings to defaults?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            config_path = Path.home() / '.scrcpy-gui' / 'config.json'
            if config_path.exists():
                config_path.unlink()

            self.resolution_spin.setValue(0)
            self.bitrate_spin.setValue(8)
            self.fps_spin.setValue(60)
            self.display_spin.setValue(0)
            self.codec_combo.setCurrentIndex(0)
            self.crop_input.clear()

            self.audio_check.setChecked(True)
            self.audio_bitrate_spin.setValue(128)
            self.audio_codec_combo.setCurrentIndex(0)
            self.audio_source_combo.setCurrentIndex(0)

            self.record_check.setChecked(False)
            self.record_format_combo.setCurrentIndex(0)
            self.record_file_input.clear()
            self.no_video_playback_check.setChecked(False)
            self.no_audio_playback_check.setChecked(False)

            self.prefer_text_check.setChecked(False)
            self.raw_key_check.setChecked(False)
            self.gamepad_check.setChecked(False)
            self.mouse_bind_combo.setCurrentIndex(0)

            self.window_title_input.clear()
            self.always_on_top_check.setChecked(False)
            self.borderless_check.setChecked(False)
            self.fullscreen_check.setChecked(False)
            self.window_x_spin.setValue(-1)
            self.window_y_spin.setValue(-1)
            self.window_w_spin.setValue(-1)
            self.window_h_spin.setValue(-1)
            self.bg_color_input.clear()
            self.disable_screensaver_check.setChecked(False)

            self.time_limit_spin.setValue(0)
            self.screen_off_check.setChecked(False)
            self.power_off_check.setChecked(False)
            self.no_power_on_check.setChecked(False)
            self.kill_adb_check.setChecked(False)
            self.force_adb_check.setChecked(False)
            self.tunnel_host_input.clear()
            self.tunnel_port_spin.setValue(22)

    def closeEvent(self, event):
        if self.scrcpy_process and self.scrcpy_process.isRunning():
            reply = QMessageBox.question(
                self,
                self.lang.get('warning_title'),
                "Mirroring is active. Stop and exit?",
                QMessageBox.Yes | QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.scrcpy_process.stop()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = ScrcpyGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
