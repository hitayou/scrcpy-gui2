#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrcpy-gui - Modern GUI for scrcpy with Material Design 3
"""

import sys
import os
import json
import subprocess
import platform
from pathlib import Path

try:
    from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer, QSize, QPropertyAnimation, QEasingCurve, QObject, QEvent
    from PySide6.QtGui import QAction, QFont, QFontDatabase, QColor, QIcon, QPalette, QPainter, QPixmap, QBrush, QPen, QCursor
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
        QPushButton, QLabel, QTabWidget, QFrame, QScrollArea, 
        QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QCheckBox, 
        QGroupBox, QGridLayout, QSplitter, QFileDialog, QMessageBox,
        QDialog, QDialogButtonBox, QTextEdit, QProgressBar, QSlider,
        QRadioButton, QButtonGroup, QSystemTrayIcon, QMenu, QSizePolicy
    )
except ImportError as e:
    print(f"Error importing PySide6: {e}")
    print("Please install PySide6: pip install PySide6")
    sys.exit(1)


class Theme:
    LIGHT = "light"
    DARK = "dark"


class Colors:
    PRIMARY_LIGHT = "#6750A4"
    PRIMARY_DARK = "#D0BCFF"
    BACKGROUND_LIGHT = "#FFFBFE"
    BACKGROUND_DARK = "#141218"
    SURFACE_LIGHT = "#F7F2FA"
    SURFACE_DARK = "#2B2930"
    TEXT_PRIMARY_LIGHT = "#1C1B1F"
    TEXT_PRIMARY_DARK = "#E6E1E5"
    SECONDARY_LIGHT = "#625B71"
    SECONDARY_DARK = "#CCC2DC"
    ERROR_LIGHT = "#B3261E"
    ERROR_DARK = "#F2B8B5"
    SUCCESS_LIGHT = "#006E1C"
    SUCCESS_DARK = "#80D895"
    BORDER_LIGHT = "#E0E0E0"
    BORDER_DARK = "#49454F"


class I18N:
    TRANSLATIONS = {
        'en': {
            'title': 'scrcpy GUI',
            'connect': 'Connect',
            'video': 'Video',
            'audio': 'Audio',
            'recording': 'Recording',
            'control': 'Control',
            'window': 'Window',
            'advanced': 'Advanced',
            'usb_mode': 'USB Mode',
            'wifi_mode': 'WiFi Mode',
            'device': 'Device',
            'refresh': 'Refresh',
            'serial': 'Serial',
            'ip_address': 'IP Address',
            'port': 'Port',
            'connect_btn': 'Connect',
            'disconnect_btn': 'Disconnect',
            'start_mirror': 'Start Mirror',
            'stop_mirror': 'Stop Mirror',
            'resolution': 'Resolution',
            'bit_rate': 'Bit Rate (Mbps)',
            'max_fps': 'Max FPS',
            'display_id': 'Display ID',
            'orientation': 'Orientation',
            'record': 'Record',
            'format': 'Format',
            'save_path': 'Save Path',
            'browse': 'Browse',
            'no_audio': 'No Audio',
            'audio_bit_rate': 'Audio Bit Rate (kbps)',
            'forward_all': 'Forward All Audio',
            'forward_specific': 'Forward Specific Audio',
            'prefer_text': 'Prefer Text Input',
            'gamepad': 'Gamepad',
            'mouse_hover': 'Mouse Hover',
            'fullscreen': 'Fullscreen',
            'always_on_top': 'Always on Top',
            'borderless': 'Borderless',
            'crop': 'Crop',
            'rotation': 'Rotation',
            'stay_awake': 'Stay Awake',
            'turn_screen_off': 'Turn Screen Off',
            'show_touches': 'Show Touches',
            'power_on': 'Power On',
            'unlock': 'Unlock',
            'adb_path': 'ADB Path',
            'scrcpy_path': 'scrcpy Path',
            'log_level': 'Log Level',
            'verbose': 'Verbose',
            'debug': 'Debug',
            'info': 'Info',
            'warn': 'Warn',
            'error': 'Error',
            'none': 'None',
            'tutorial_usb_title': 'USB Connection Tutorial',
            'tutorial_usb_step1': 'Enable USB Debugging on your Android device',
            'tutorial_usb_step2': 'Connect your device via USB cable',
            'tutorial_usb_step3': 'Accept the RSA key dialog on your device',
            'tutorial_usb_step4': 'Click Refresh to see your device',
            'tutorial_wifi_title': 'WiFi Connection Tutorial',
            'tutorial_wifi_step1': 'Connect device via USB first',
            'tutorial_wifi_step2': 'Run: adb tcpip 5555',
            'tutorial_wifi_step3': 'Disconnect USB cable',
            'tutorial_wifi_step4': 'Enter device IP and click Connect',
            'next': 'Next',
            'finish': 'Finish',
            'language': 'Language',
            'theme': 'Theme',
            'light': 'Light',
            'dark': 'Dark',
            'status_connected': 'Connected',
            'status_disconnected': 'Disconnected',
            'status_mirroring': 'Mirroring...',
            'no_device': 'No device found',
            'connecting': 'Connecting...',
            'stopping': 'Stopping...',
            'select_folder': 'Select Folder',
            'scrcpy_not_found': 'scrcpy not found. Please install scrcpy.',
            'adb_not_found': 'ADB not found. Please install ADB.',
            'help': 'Help',
            'about': 'About',
            'minimize_tray': 'Minimize to Tray',
            'quit': 'Quit',
            'shortcuts': 'Shortcuts',
            'shortcut_ctrl_g': 'Ctrl+G: Toggle fullscreen',
            'shortcut_ctrl_h': 'Ctrl+H: Home',
            'shortcut_ctrl_b': 'Ctrl+B: Back',
            'shortcut_ctrl_s': 'Ctrl+S: Screenshot',
            'shortcut_ctrl_o': 'Ctrl+O: Turn screen off',
            'shortcut_ctrl_n': 'Ctrl+N: Expand notification panel',
            'width': 'Width',
            'height': 'Height',
            'lock_ratio': 'Lock Aspect Ratio',
            'buffer_ms': 'Buffer (ms)',
            'tcpip_port': 'TCP/IP Port',
            'auto_start': 'Auto Start',
            'close_on_disconnect': 'Close on Disconnect',
            'clipboard_sync': 'Clipboard Sync',
            'prefer_aph': 'Prefer APH',
            'codec': 'Codec',
            'encoder': 'Encoder',
            'force_adb_forward': 'Force ADB Forward',
            'disable_screensaver': 'Disable Screensaver',
            'key_modifier': 'Key Modifier',
            'left_alt': 'Left Alt',
            'right_alt': 'Right Alt',
            'left_shift': 'Left Shift',
            'right_shift': 'Right Shift',
            'left_ctrl': 'Left Ctrl',
            'right_ctrl': 'Right Ctrl',
            'mouse_bind': 'Mouse Bind',
            'record_format_mp4': 'MP4',
            'record_format_mkv': 'MKV',
            'orientation_0': '0° (Natural)',
            'orientation_90': '90°',
            'orientation_180': '180°',
            'orientation_270': '270°',
            'apply': 'Apply',
            'reset': 'Reset',
            'save_config': 'Save Config',
            'load_config': 'Load Config',
            'config_saved': 'Configuration saved',
            'config_loaded': 'Configuration loaded',
            'device_list': 'Device List',
            'connection_type': 'Connection Type',
            'tutorial': 'Tutorial',
            'settings': 'Settings',
            'output': 'Output',
            'clear_output': 'Clear Output',
            'copy_output': 'Copy Output',
            'version': 'Version',
            'author': 'Author',
            'website': 'Website',
            'license': 'License',
            'description': 'Modern GUI for scrcpy with Material Design 3 support',
        },
        'ru': {
            'title': 'scrcpy GUI',
            'connect': 'Подключение',
            'video': 'Видео',
            'audio': 'Аудио',
            'recording': 'Запись',
            'control': 'Управление',
            'window': 'Окно',
            'advanced': 'Дополнительно',
            'usb_mode': 'Режим USB',
            'wifi_mode': 'Режим WiFi',
            'device': 'Устройство',
            'refresh': 'Обновить',
            'serial': 'Серийный номер',
            'ip_address': 'IP Адрес',
            'port': 'Порт',
            'connect_btn': 'Подключить',
            'disconnect_btn': 'Отключить',
            'start_mirror': 'Запустить',
            'stop_mirror': 'Остановить',
            'resolution': 'Разрешение',
            'bit_rate': 'Битрейт (Мбит/с)',
            'max_fps': 'Макс. FPS',
            'display_id': 'ID Дисплея',
            'orientation': 'Ориентация',
            'record': 'Запись',
            'format': 'Формат',
            'save_path': 'Путь сохранения',
            'browse': 'Обзор',
            'no_audio': 'Без аудио',
            'audio_bit_rate': 'Битрейт аудио (кбит/с)',
            'forward_all': 'Передавать всё аудио',
            'forward_specific': 'Передавать выбранное аудио',
            'prefer_text': 'Предпочитать текстовый ввод',
            'gamepad': 'Геймпад',
            'mouse_hover': 'Наведение мыши',
            'fullscreen': 'Полный экран',
            'always_on_top': 'Всегда сверху',
            'borderless': 'Без рамок',
            'crop': 'Кроп',
            'rotation': 'Поворот',
            'stay_awake': 'Не выключать экран',
            'turn_screen_off': 'Выключить экран',
            'show_touches': 'Показывать касания',
            'power_on': 'Включить питание',
            'unlock': 'Разблокировать',
            'adb_path': 'Путь к ADB',
            'scrcpy_path': 'Путь к scrcpy',
            'log_level': 'Уровень логов',
            'verbose': 'Подробный',
            'debug': 'Отладка',
            'info': 'Инфо',
            'warn': 'Предупреждение',
            'error': 'Ошибка',
            'none': 'Нет',
            'tutorial_usb_title': 'Подключение по USB',
            'tutorial_usb_step1': 'Включите отладку по USB на Android устройстве',
            'tutorial_usb_step2': 'Подключите устройство через USB кабель',
            'tutorial_usb_step3': 'Примите диалог RSA ключа на устройстве',
            'tutorial_usb_step4': 'Нажмите Обновить чтобы увидеть устройство',
            'tutorial_wifi_title': 'Подключение по WiFi',
            'tutorial_wifi_step1': 'Сначала подключите устройство по USB',
            'tutorial_wifi_step2': 'Выполните: adb tcpip 5555',
            'tutorial_wifi_step3': 'Отсоедините USB кабель',
            'tutorial_wifi_step4': 'Введите IP устройства и нажмите Подключить',
            'next': 'Далее',
            'finish': 'Готово',
            'language': 'Язык',
            'theme': 'Тема',
            'light': 'Светлая',
            'dark': 'Тёмная',
            'status_connected': 'Подключено',
            'status_disconnected': 'Отключено',
            'status_mirroring': 'Трансляция...',
            'no_device': 'Устройство не найдено',
            'connecting': 'Подключение...',
            'stopping': 'Остановка...',
            'select_folder': 'Выберите папку',
            'scrcpy_not_found': 'scrcpy не найден. Установите scrcpy.',
            'adb_not_found': 'ADB не найден. Установите ADB.',
            'help': 'Помощь',
            'about': 'О программе',
            'minimize_tray': 'Свернуть в трей',
            'quit': 'Выход',
            'shortcuts': 'Горячие клавиши',
            'shortcut_ctrl_g': 'Ctrl+G: Полный экран',
            'shortcut_ctrl_h': 'Ctrl+H: Домой',
            'shortcut_ctrl_b': 'Ctrl+B: Назад',
            'shortcut_ctrl_s': 'Ctrl+S: Скриншот',
            'shortcut_ctrl_o': 'Ctrl+O: Выключить экран',
            'shortcut_ctrl_n': 'Ctrl+N: Панель уведомлений',
            'width': 'Ширина',
            'height': 'Высота',
            'lock_ratio': 'Сохранять пропорции',
            'buffer_ms': 'Буфер (мс)',
            'tcpip_port': 'TCP/IP Порт',
            'auto_start': 'Автозапуск',
            'close_on_disconnect': 'Закрыть при отключении',
            'clipboard_sync': 'Синхронизация буфера',
            'prefer_aph': 'Предпочитать APH',
            'codec': 'Кодек',
            'encoder': 'Кодировщик',
            'force_adb_forward': 'Принудительная переадресация',
            'disable_screensaver': 'Отключить скринсейвер',
            'key_modifier': 'Модификатор клавиш',
            'left_alt': 'Левый Alt',
            'right_alt': 'Правый Alt',
            'left_shift': 'Левый Shift',
            'right_shift': 'Правый Shift',
            'left_ctrl': 'Левый Ctrl',
            'right_ctrl': 'Правый Ctrl',
            'mouse_bind': 'Привязка мыши',
            'record_format_mp4': 'MP4',
            'record_format_mkv': 'MKV',
            'orientation_0': '0° (Естественная)',
            'orientation_90': '90°',
            'orientation_180': '180°',
            'orientation_270': '270°',
            'apply': 'Применить',
            'reset': 'Сброс',
            'save_config': 'Сохранить конфиг',
            'load_config': 'Загрузить конфиг',
            'config_saved': 'Конфигурация сохранена',
            'config_loaded': 'Конфигурация загружена',
            'device_list': 'Список устройств',
            'connection_type': 'Тип подключения',
            'tutorial': 'Обучение',
            'settings': 'Настройки',
            'output': 'Вывод',
            'clear_output': 'Очистить вывод',
            'copy_output': 'Копировать вывод',
            'version': 'Версия',
            'author': 'Автор',
            'website': 'Сайт',
            'license': 'Лицензия',
            'description': 'Современный GUI для scrcpy с поддержкой Material Design 3',
        }
    }

    def __init__(self, lang='en'):
        self.lang = lang

    def tr(self, key):
        return self.TRANSLATIONS.get(self.lang, {}).get(key, key)


class ScrcpyWorker(QThread):
    output_signal = Signal(str)
    error_signal = Signal(str)
    finished_signal = Signal(int)

    def __init__(self, cmd):
        super().__init__()
        self.cmd = cmd
        self.process = None

    def run(self):
        try:
            self.process = subprocess.Popen(
                self.cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            for line in self.process.stdout:
                self.output_signal.emit(line.strip())
            
            return_code = self.process.wait()
            self.finished_signal.emit(return_code)
        except Exception as e:
            self.error_signal.emit(str(e))
            self.finished_signal.emit(-1)

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()


class AdbWorker(QThread):
    output_signal = Signal(str)
    finished_signal = Signal(list)

    def __init__(self, adb_path='adb'):
        super().__init__()
        self.adb_path = adb_path

    def run(self):
        try:
            result = subprocess.run(
                [self.adb_path, 'devices', '-l'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip() and 'unauthorized' not in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        serial = parts[0]
                        state = parts[1]
                        model = ''
                        for p in parts[2:]:
                            if p.startswith('model:'):
                                model = p.replace('model:', '')
                                break
                        devices.append({
                            'serial': serial,
                            'state': state,
                            'model': model
                        })
            
            self.finished_signal.emit(devices)
        except Exception as e:
            self.finished_signal.emit([])


class TutorialDialog(QDialog):
    def __init__(self, tutorial_type, i18n, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self.tutorial_type = tutorial_type
        self.current_step = 0
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(self.i18n.tr(f'tutorial_{self.tutorial_type}_title'))
        self.setMinimumSize(500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        self.steps_label = QLabel()
        self.steps_label.setWordWrap(True)
        self.steps_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                padding: 20px;
                background-color: #F0F0F0;
                border-radius: 10px;
            }
        """)
        layout.addWidget(self.steps_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.prev_btn = QPushButton(self.i18n.tr('Previous') if hasattr(self.i18n, 'tr') else 'Previous')
        self.prev_btn.clicked.connect(self.prev_step)
        self.prev_btn.setEnabled(False)
        
        self.next_btn = QPushButton(self.i18n.tr('next'))
        self.next_btn.clicked.connect(self.next_step)
        
        btn_layout.addWidget(self.prev_btn)
        btn_layout.addWidget(self.next_btn)
        layout.addLayout(btn_layout)
        
        self.update_step()

    def update_step(self):
        steps_key = f'tutorial_{self.tutorial_type}_step{self.current_step + 1}'
        step_text = self.i18n.tr(steps_key)
        self.steps_label.setText(f"{self.current_step + 1}. {step_text}")
        
        self.prev_btn.setEnabled(self.current_step > 0)
        
        max_steps = 4
        if self.current_step >= max_steps - 1:
            self.next_btn.setText(self.i18n.tr('finish'))
        else:
            self.next_btn.setText(self.i18n.tr('next'))

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step()

    def next_step(self):
        max_steps = 4
        if self.current_step < max_steps - 1:
            self.current_step += 1
            self.update_step()
        else:
            self.accept()


class ModernButton(QPushButton):
    def __init__(self, text, parent=None, primary=False):
        super().__init__(text, parent)
        self.primary = primary
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(48)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.update_style()

    def update_style(self):
        if self.primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #6750A4;
                    color: white;
                    border: none;
                    border-radius: 24px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background-color: #7F67BE;
                }
                QPushButton:pressed {
                    background-color: #4F378B;
                }
                QPushButton:disabled {
                    background-color: #CCCCCC;
                    color: #999999;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #6750A4;
                    border: 2px solid #6750A4;
                    border-radius: 24px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background-color: #F0E6FF;
                }
                QPushButton:pressed {
                    background-color: #E0D0FF;
                }
                QPushButton:disabled {
                    border-color: #CCCCCC;
                    color: #999999;
                }
            """)


class CardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("cardWidget")
        self.setStyleSheet("""
            QFrame#cardWidget {
                background-color: #F7F2FA;
                border-radius: 12px;
                padding: 16px;
            }
        """)


class ScrcpyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.i18n = I18N('en')
        self.theme = Theme.LIGHT
        self.worker = None
        self.is_mirroring = False
        self.adb_path = 'adb'
        self.scrcpy_path = 'scrcpy'
        self.config_path = Path.home() / '.scrcpy-gui' / 'config.json'
        
        self.load_config()
        self.setup_ui()
        self.apply_theme()
        self.refresh_devices()

    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.i18n.lang = config.get('language', 'en')
                    self.theme = config.get('theme', Theme.LIGHT)
                    self.adb_path = config.get('adb_path', 'adb')
                    self.scrcpy_path = config.get('scrcpy_path', 'scrcpy')
            except:
                pass

    def save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        config = {
            'language': self.i18n.lang,
            'theme': self.theme,
            'adb_path': self.adb_path,
            'scrcpy_path': self.scrcpy_path
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    def setup_ui(self):
        self.setWindowTitle(self.i18n.tr('title'))
        self.setMinimumSize(1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()
        
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        self.create_menu_bar()

    def create_left_panel(self):
        panel = QFrame()
        panel.setMinimumWidth(350)
        panel.setMaximumWidth(500)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        title_label = QLabel(self.i18n.tr('title'))
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #6750A4;
                padding: 10px;
            }
        """)
        layout.addWidget(title_label)
        
        connection_card = CardWidget()
        conn_layout = QVBoxLayout(connection_card)
        conn_layout.setSpacing(12)
        
        self.connection_group = QButtonGroup(self)
        usb_radio = QRadioButton(self.i18n.tr('usb_mode'))
        wifi_radio = QRadioButton(self.i18n.tr('wifi_mode'))
        self.connection_group.addButton(usb_radio, 0)
        self.connection_group.addButton(wifi_radio, 1)
        usb_radio.setChecked(True)
        usb_radio.toggled.connect(lambda checked: self.on_connection_type_changed('usb', checked))
        wifi_radio.toggled.connect(lambda checked: self.on_connection_type_changed('wifi', checked))
        
        conn_layout.addWidget(usb_radio)
        conn_layout.addWidget(wifi_radio)
        
        self.device_combo = QComboBox()
        self.device_combo.setMinimumHeight(48)
        self.device_combo.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border-radius: 8px;
                border: 1px solid #E0E0E0;
                background-color: white;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #6750A4;
                margin-right: 10px;
            }
        """)
        conn_layout.addWidget(QLabel(self.i18n.tr('device')))
        conn_layout.addWidget(self.device_combo)
        
        refresh_btn = ModernButton(self.i18n.tr('refresh'), primary=False)
        refresh_btn.clicked.connect(self.refresh_devices)
        conn_layout.addWidget(refresh_btn)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText(self.i18n.tr('ip_address'))
        self.ip_input.setMinimumHeight(48)
        self.ip_input.setVisible(False)
        conn_layout.addWidget(self.ip_input)
        
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(5555)
        self.port_input.setMinimumHeight(48)
        self.port_input.setVisible(False)
        conn_layout.addWidget(QLabel(self.i18n.tr('port')))
        conn_layout.addWidget(self.port_input)
        
        self.connect_btn = ModernButton(self.i18n.tr('connect_btn'), primary=True)
        self.connect_btn.clicked.connect(self.toggle_connection)
        conn_layout.addWidget(self.connect_btn)
        
        layout.addWidget(connection_card)
        
        status_card = CardWidget()
        status_layout = QVBoxLayout(status_card)
        
        self.status_label = QLabel(self.i18n.tr('status_disconnected'))
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #6750A4;
                padding: 10px;
            }
        """)
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_card)
        
        tutorial_btn = ModernButton(self.i18n.tr('tutorial'), primary=False)
        tutorial_btn.clicked.connect(self.show_tutorial_menu)
        layout.addWidget(tutorial_btn)
        
        layout.addStretch()
        
        return panel

    def create_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #F7F2FA;
                border-radius: 12px;
            }
            QTabBar::tab {
                padding: 16px 24px;
                font-size: 14px;
                font-weight: bold;
                color: #6750A4;
                background-color: transparent;
                border: none;
                border-bottom: 3px solid transparent;
            }
            QTabBar::tab:selected {
                border-bottom: 3px solid #6750A4;
            }
            QTabBar::tab:hover:!selected {
                border-bottom: 3px solid #D0BCFF;
            }
        """)
        
        self.tabs.addTab(self.create_video_tab(), self.i18n.tr('video'))
        self.tabs.addTab(self.create_audio_tab(), self.i18n.tr('audio'))
        self.tabs.addTab(self.create_recording_tab(), self.i18n.tr('recording'))
        self.tabs.addTab(self.create_control_tab(), self.i18n.tr('control'))
        self.tabs.addTab(self.create_window_tab(), self.i18n.tr('window'))
        self.tabs.addTab(self.create_advanced_tab(), self.i18n.tr('advanced'))
        
        layout.addWidget(self.tabs)
        
        button_card = CardWidget()
        btn_layout = QVBoxLayout(button_card)
        btn_layout.setSpacing(12)
        
        self.mirror_btn = ModernButton(self.i18n.tr('start_mirror'), primary=True)
        self.mirror_btn.clicked.connect(self.toggle_mirror)
        btn_layout.addWidget(self.mirror_btn)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(150)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 10px;
                font-family: monospace;
                font-size: 12px;
            }
        """)
        btn_layout.addWidget(QLabel(self.i18n.tr('output')))
        btn_layout.addWidget(self.output_text)
        
        clear_btn = ModernButton(self.i18n.tr('clear_output'), primary=False)
        clear_btn.clicked.connect(self.output_text.clear)
        btn_layout.addWidget(clear_btn)
        
        layout.addWidget(button_card)
        
        return panel

    def create_video_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        res_group = QGroupBox(self.i18n.tr('resolution'))
        res_layout = QGridLayout(res_group)
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(0, 7680)
        self.width_spin.setValue(0)
        self.width_spin.setMinimumHeight(40)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(0, 7680)
        self.height_spin.setValue(0)
        self.height_spin.setMinimumHeight(40)
        self.lock_ratio_check = QCheckBox(self.i18n.tr('lock_ratio'))
        
        res_layout.addWidget(QLabel(self.i18n.tr('width')), 0, 0)
        res_layout.addWidget(self.width_spin, 0, 1)
        res_layout.addWidget(QLabel(self.i18n.tr('height')), 1, 0)
        res_layout.addWidget(self.height_spin, 1, 1)
        res_layout.addWidget(self.lock_ratio_check, 2, 0, 1, 2)
        layout.addWidget(res_group)
        
        bit_group = QGroupBox(self.i18n.tr('bit_rate'))
        bit_layout = QVBoxLayout(bit_group)
        self.bitrate_spin = QDoubleSpinBox()
        self.bitrate_spin.setRange(0.1, 100.0)
        self.bitrate_spin.setValue(8.0)
        self.bitrate_spin.setSuffix(' Mbps')
        self.bitrate_spin.setMinimumHeight(40)
        bit_layout.addWidget(self.bitrate_spin)
        layout.addWidget(bit_group)
        
        fps_group = QGroupBox(self.i18n.tr('max_fps'))
        fps_layout = QVBoxLayout(fps_group)
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(0, 120)
        self.fps_spin.setValue(0)
        self.fps_spin.setSpecialValueText(self.i18n.tr('none'))
        self.fps_spin.setMinimumHeight(40)
        fps_layout.addWidget(self.fps_spin)
        layout.addWidget(fps_group)
        
        display_group = QGroupBox(self.i18n.tr('display_id'))
        display_layout = QVBoxLayout(display_group)
        self.display_spin = QSpinBox()
        self.display_spin.setRange(0, 10)
        self.display_spin.setValue(0)
        self.display_spin.setMinimumHeight(40)
        display_layout.addWidget(self.display_spin)
        layout.addWidget(display_group)
        
        orient_group = QGroupBox(self.i18n.tr('orientation'))
        orient_layout = QVBoxLayout(orient_group)
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems([
            self.i18n.tr('orientation_0'),
            self.i18n.tr('orientation_90'),
            self.i18n.tr('orientation_180'),
            self.i18n.tr('orientation_270')
        ])
        self.orientation_combo.setMinimumHeight(40)
        orient_layout.addWidget(self.orientation_combo)
        layout.addWidget(orient_group)
        
        layout.addStretch()
        tab.setWidget(container)
        return tab

    def create_audio_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        self.no_audio_check = QCheckBox(self.i18n.tr('no_audio'))
        layout.addWidget(self.no_audio_check)
        
        audio_bit_group = QGroupBox(self.i18n.tr('audio_bit_rate'))
        audio_bit_layout = QVBoxLayout(audio_bit_group)
        self.audio_bitrate_spin = QSpinBox()
        self.audio_bitrate_spin.setRange(0, 320)
        self.audio_bitrate_spin.setValue(128)
        self.audio_bitrate_spin.setSuffix(' kbps')
        self.audio_bitrate_spin.setMinimumHeight(40)
        audio_bit_layout.addWidget(self.audio_bitrate_spin)
        layout.addWidget(audio_bit_group)
        
        self.forward_all_check = QCheckBox(self.i18n.tr('forward_all'))
        layout.addWidget(self.forward_all_check)
        
        layout.addStretch()
        tab.setWidget(container)
        return tab

    def create_recording_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        self.record_check = QCheckBox(self.i18n.tr('record'))
        layout.addWidget(self.record_check)
        
        format_group = QGroupBox(self.i18n.tr('format'))
        format_layout = QVBoxLayout(format_group)
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            self.i18n.tr('record_format_mp4'),
            self.i18n.tr('record_format_mkv')
        ])
        self.format_combo.setMinimumHeight(40)
        format_layout.addWidget(self.format_combo)
        layout.addWidget(format_group)
        
        path_group = QGroupBox(self.i18n.tr('save_path'))
        path_layout = QHBoxLayout(path_group)
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(os.path.expanduser('~'))
        self.path_input.setMinimumHeight(40)
        browse_btn = ModernButton(self.i18n.tr('browse'), primary=False)
        browse_btn.clicked.connect(self.browse_save_path)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        layout.addWidget(path_group)
        
        layout.addStretch()
        tab.setWidget(container)
        return tab

    def create_control_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        self.prefer_text_check = QCheckBox(self.i18n.tr('prefer_text'))
        layout.addWidget(self.prefer_text_check)
        
        self.gamepad_check = QCheckBox(self.i18n.tr('gamepad'))
        layout.addWidget(self.gamepad_check)
        
        self.mouse_hover_check = QCheckBox(self.i18n.tr('mouse_hover'))
        layout.addWidget(self.mouse_hover_check)
        
        self.stay_awake_check = QCheckBox(self.i18n.tr('stay_awake'))
        layout.addWidget(self.stay_awake_check)
        
        self.turn_off_check = QCheckBox(self.i18n.tr('turn_screen_off'))
        layout.addWidget(self.turn_off_check)
        
        self.show_touches_check = QCheckBox(self.i18n.tr('show_touches'))
        layout.addWidget(self.show_touches_check)
        
        self.power_on_check = QCheckBox(self.i18n.tr('power_on'))
        layout.addWidget(self.power_on_check)
        
        self.unlock_check = QCheckBox(self.i18n.tr('unlock'))
        layout.addWidget(self.unlock_check)
        
        layout.addStretch()
        tab.setWidget(container)
        return tab

    def create_window_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        self.fullscreen_check = QCheckBox(self.i18n.tr('fullscreen'))
        layout.addWidget(self.fullscreen_check)
        
        self.always_on_top_check = QCheckBox(self.i18n.tr('always_on_top'))
        layout.addWidget(self.always_on_top_check)
        
        self.borderless_check = QCheckBox(self.i18n.tr('borderless'))
        layout.addWidget(self.borderless_check)
        
        crop_group = QGroupBox(self.i18n.tr('crop'))
        crop_layout = QGridLayout(crop_group)
        self.crop_width_spin = QSpinBox()
        self.crop_width_spin.setRange(0, 7680)
        self.crop_width_spin.setValue(0)
        self.crop_height_spin = QSpinBox()
        self.crop_height_spin.setRange(0, 7680)
        self.crop_height_spin.setValue(0)
        crop_layout.addWidget(QLabel(self.i18n.tr('width')), 0, 0)
        crop_layout.addWidget(self.crop_width_spin, 0, 1)
        crop_layout.addWidget(QLabel(self.i18n.tr('height')), 1, 0)
        crop_layout.addWidget(self.crop_height_spin, 1, 1)
        layout.addWidget(crop_group)
        
        rotation_group = QGroupBox(self.i18n.tr('rotation'))
        rotation_layout = QVBoxLayout(rotation_group)
        self.rotation_spin = QSpinBox()
        self.rotation_spin.setRange(0, 3)
        self.rotation_spin.setValue(0)
        self.rotation_spin.setMinimumHeight(40)
        rotation_layout.addWidget(self.rotation_spin)
        layout.addWidget(rotation_group)
        
        buffer_group = QGroupBox(self.i18n.tr('buffer_ms'))
        buffer_layout = QVBoxLayout(buffer_group)
        self.buffer_spin = QSpinBox()
        self.buffer_spin.setRange(0, 10000)
        self.buffer_spin.setValue(0)
        self.buffer_spin.setMinimumHeight(40)
        buffer_layout.addWidget(self.buffer_spin)
        layout.addWidget(buffer_group)
        
        layout.addStretch()
        tab.setWidget(container)
        return tab

    def create_advanced_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        adb_group = QGroupBox(self.i18n.tr('adb_path'))
        adb_layout = QHBoxLayout(adb_group)
        self.adb_input = QLineEdit(self.adb_path)
        self.adb_input.setMinimumHeight(40)
        adb_btn = ModernButton(self.i18n.tr('browse'), primary=False)
        adb_btn.clicked.connect(lambda: self.browse_file(self.adb_input))
        adb_layout.addWidget(self.adb_input)
        adb_layout.addWidget(adb_btn)
        layout.addWidget(adb_group)
        
        scrcpy_group = QGroupBox(self.i18n.tr('scrcpy_path'))
        scrcpy_layout = QHBoxLayout(scrcpy_group)
        self.scrcpy_input = QLineEdit(self.scrcpy_path)
        self.scrcpy_input.setMinimumHeight(40)
        scrcpy_btn = ModernButton(self.i18n.tr('browse'), primary=False)
        scrcpy_btn.clicked.connect(lambda: self.browse_file(self.scrcpy_input))
        scrcpy_layout.addWidget(self.scrcpy_input)
        scrcpy_layout.addWidget(scrcpy_btn)
        layout.addWidget(scrcpy_group)
        
        log_group = QGroupBox(self.i18n.tr('log_level'))
        log_layout = QVBoxLayout(log_group)
        self.log_combo = QComboBox()
        self.log_combo.addItems([
            self.i18n.tr('verbose'),
            self.i18n.tr('debug'),
            self.i18n.tr('info'),
            self.i18n.tr('warn'),
            self.i18n.tr('error')
        ])
        self.log_combo.setMinimumHeight(40)
        log_layout.addWidget(self.log_combo)
        layout.addWidget(log_group)
        
        self.clipboard_check = QCheckBox(self.i18n.tr('clipboard_sync'))
        layout.addWidget(self.clipboard_check)
        
        self.screensaver_check = QCheckBox(self.i18n.tr('disable_screensaver'))
        layout.addWidget(self.screensaver_check)
        
        lang_group = QGroupBox(self.i18n.tr('language'))
        lang_layout = QVBoxLayout(lang_group)
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(['English', 'Русский'])
        self.lang_combo.setCurrentIndex(0 if self.i18n.lang == 'en' else 1)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        self.lang_combo.setMinimumHeight(40)
        lang_layout.addWidget(self.lang_combo)
        layout.addWidget(lang_group)
        
        theme_group = QGroupBox(self.i18n.tr('theme'))
        theme_layout = QVBoxLayout(theme_group)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([self.i18n.tr('light'), self.i18n.tr('dark')])
        self.theme_combo.setCurrentIndex(0 if self.theme == Theme.LIGHT else 1)
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.theme_combo.setMinimumHeight(40)
        theme_layout.addWidget(self.theme_combo)
        layout.addWidget(theme_group)
        
        config_layout = QHBoxLayout()
        save_config_btn = ModernButton(self.i18n.tr('save_config'), primary=False)
        save_config_btn.clicked.connect(self.save_config_and_show_message)
        load_config_btn = ModernButton(self.i18n.tr('load_config'), primary=False)
        load_config_btn.clicked.connect(self.load_config_and_show_message)
        config_layout.addWidget(save_config_btn)
        config_layout.addWidget(load_config_btn)
        layout.addLayout(config_layout)
        
        layout.addStretch()
        tab.setWidget(container)
        return tab

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        help_menu = menubar.addMenu(self.i18n.tr('help'))
        
        about_action = QAction(self.i18n.tr('about'), self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction(self.i18n.tr('shortcuts'), self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            line_edit.setText(file_path)

    def browse_save_path(self):
        folder = QFileDialog.getExistingDirectory(self, self.i18n.tr('select_folder'))
        if folder:
            self.path_input.setText(folder)

    def on_connection_type_changed(self, mode, checked):
        if checked:
            if mode == 'usb':
                self.ip_input.setVisible(False)
                self.port_input.setVisible(False)
                self.port_input.label().setVisible(False) if hasattr(self.port_input, 'label') else None
            else:
                self.ip_input.setVisible(True)
                self.port_input.setVisible(True)

    def refresh_devices(self):
        self.device_combo.clear()
        worker = AdbWorker(self.adb_path)
        worker.finished_signal.connect(self.on_devices_refreshed)
        worker.start()

    def on_devices_refreshed(self, devices):
        self.device_combo.clear()
        if devices:
            for dev in devices:
                display = f"{dev['model']} ({dev['serial']})" if dev['model'] else dev['serial']
                self.device_combo.addItem(display, dev['serial'])
        else:
            self.device_combo.addItem(self.i18n.tr('no_device'), '')

    def toggle_connection(self):
        if self.connection_group.checkedId() == 1:
            ip = self.ip_input.text()
            port = self.port_input.value()
            if ip:
                cmd = [self.adb_path, 'connect', f'{ip}:{port}']
                self.run_adb_command(cmd)
        else:
            self.refresh_devices()

    def run_adb_command(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            self.output_text.append(f"> {' '.join(cmd)}\n{result.stdout}{result.stderr}")
        except Exception as e:
            self.output_text.append(f"Error: {e}")

    def toggle_mirror(self):
        if self.is_mirroring:
            self.stop_mirror()
        else:
            self.start_mirror()

    def start_mirror(self):
        serial = self.device_combo.currentData()
        if not serial:
            QMessageBox.warning(self, "Error", self.i18n.tr('no_device'))
            return
        
        cmd = [self.scrcpy_path]
        
        if serial:
            cmd.extend(['-s', serial])
        
        if self.width_spin.value() > 0:
            cmd.extend(['--max-size', str(self.width_spin.value())])
        
        if self.bitrate_spin.value() > 0:
            cmd.extend(['--bit-rate', str(int(self.bitrate_spin.value() * 1000000))])
        
        if self.fps_spin.value() > 0:
            cmd.extend(['--max-fps', str(self.fps_spin.value())])
        
        if self.display_spin.value() > 0:
            cmd.extend(['--display-id', str(self.display_spin.value())])
        
        orientation_map = {0: 0, 1: 90, 2: 180, 3: 270}
        orientation_value = orientation_map.get(self.orientation_combo.currentIndex(), 0)
        if orientation_value != 0:
            cmd.extend(['--rotation', str(orientation_value)])
        
        if self.no_audio_check.isChecked():
            cmd.append('--no-audio')
        else:
            if self.audio_bitrate_spin.value() > 0:
                cmd.extend(['--audio-bit-rate', str(self.audio_bitrate_spin.value() * 1000)])
            if self.forward_all_check.isChecked():
                cmd.append('--audio-buffer=0')
        
        if self.record_check.isChecked():
            fmt = 'mp4' if self.format_combo.currentIndex() == 0 else 'mkv'
            path = self.path_input.text() or os.path.expanduser('~')
            filename = f"recording.{fmt}"
            full_path = os.path.join(path, filename)
            cmd.extend(['--record', full_path, '--record-format', fmt])
        
        if self.prefer_text_check.isChecked():
            cmd.append('--prefer-text')
        
        if self.gamepad_check.isChecked():
            cmd.append('--gamepad=uhid')
        
        if self.mouse_hover_check.isChecked():
            cmd.append('--mouse-hover')
        
        if self.stay_awake_check.isChecked():
            cmd.append('--stay-awake')
        
        if self.turn_off_check.isChecked():
            cmd.append('--turn-screen-off')
        
        if self.show_touches_check.isChecked():
            cmd.append('--show-touches')
        
        if self.power_on_check.isChecked():
            cmd.append('--power-on')
        
        if self.unlock_check.isChecked():
            cmd.append('--unlock')
        
        if self.fullscreen_check.isChecked():
            cmd.append('--fullscreen')
        
        if self.always_on_top_check.isChecked():
            cmd.append('--always-on-top')
        
        if self.borderless_check.isChecked():
            cmd.append('--window-borderless')
        
        if self.crop_width_spin.value() > 0 and self.crop_height_spin.value() > 0:
            cmd.extend(['--crop', f'{self.crop_width_spin.value()}:{self.crop_height_spin.value()}'])
        
        if self.rotation_spin.value() > 0:
            cmd.extend(['--rotate', str(self.rotation_spin.value())])
        
        if self.buffer_spin.value() > 0:
            cmd.extend(['--video-buffer', str(self.buffer_spin.value())])
        
        log_levels = ['verbose', 'debug', 'info', 'warn', 'error']
        selected_log = log_levels[self.log_combo.currentIndex()]
        if selected_log != 'info':
            cmd.extend(['--log-level', selected_log])
        
        if self.clipboard_check.isChecked():
            cmd.append('--clipboard-autosync')
        
        if self.screensaver_check.isChecked():
            cmd.append('--disable-screensaver')
        
        self.output_text.append(f"> {' '.join(cmd)}")
        
        self.worker = ScrcpyWorker(cmd)
        self.worker.output_signal.connect(self.on_worker_output)
        self.worker.error_signal.connect(self.on_worker_error)
        self.worker.finished_signal.connect(self.on_worker_finished)
        self.worker.start()
        
        self.is_mirroring = True
        self.mirror_btn.setText(self.i18n.tr('stop_mirror'))
        self.status_label.setText(self.i18n.tr('status_mirroring'))
        self.status_label.setStyleSheet("QLabel { font-size: 16px; font-weight: bold; color: #006E1C; padding: 10px; }")

    def stop_mirror(self):
        if self.worker:
            self.worker.stop()
            self.worker = None
        
        self.is_mirroring = False
        self.mirror_btn.setText(self.i18n.tr('start_mirror'))
        self.status_label.setText(self.i18n.tr('status_disconnected'))
        self.status_label.setStyleSheet("QLabel { font-size: 16px; font-weight: bold; color: #6750A4; padding: 10px; }")

    def on_worker_output(self, text):
        self.output_text.append(text)

    def on_worker_error(self, text):
        self.output_text.append(f"ERROR: {text}")

    def on_worker_finished(self, code):
        self.stop_mirror()
        if code != 0:
            self.output_text.append(f"Process finished with code: {code}")

    def show_tutorial_menu(self):
        menu = QMenu(self)
        usb_action = menu.addAction(self.i18n.tr('usb_mode'))
        wifi_action = menu.addAction(self.i18n.tr('wifi_mode'))
        
        action = menu.exec_(self.connect_btn.mapToGlobal(self.connect_btn.rect().bottomLeft()))
        
        if action == usb_action:
            dialog = TutorialDialog('usb', self.i18n, self)
            dialog.exec_()
        elif action == wifi_action:
            dialog = TutorialDialog('wifi', self.i18n, self)
            dialog.exec_()

    def change_language(self, index):
        self.i18n.lang = 'en' if index == 0 else 'ru'
        self.save_config()
        QMessageBox.information(self, "Info", "Restart required for language change to take effect.")

    def change_theme(self, index):
        self.theme = Theme.LIGHT if index == 0 else Theme.DARK
        self.apply_theme()
        self.save_config()

    def apply_theme(self):
        if self.theme == Theme.LIGHT:
            bg_color = Colors.BACKGROUND_LIGHT
            surface_color = Colors.SURFACE_LIGHT
            text_color = Colors.TEXT_PRIMARY_LIGHT
            primary_color = Colors.PRIMARY_LIGHT
            border_color = Colors.BORDER_LIGHT
        else:
            bg_color = Colors.BACKGROUND_DARK
            surface_color = Colors.SURFACE_DARK
            text_color = Colors.TEXT_PRIMARY_DARK
            primary_color = Colors.PRIMARY_DARK
            border_color = Colors.BORDER_DARK
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {bg_color};
            }}
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
                font-size: 14px;
            }}
            QTabWidget::pane {{
                background-color: {surface_color};
            }}
            QFrame#cardWidget {{
                background-color: {surface_color};
                border: 1px solid {border_color};
            }}
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 24px;
                padding: 12px 24px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
            QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                padding: 10px;
            }}
            QCheckBox {{
                color: {text_color};
                spacing: 8px;
            }}
            QGroupBox {{
                font-weight: bold;
                color: {primary_color};
                border: 1px solid {border_color};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }}
            QScrollBar:vertical {{
                background-color: {surface_color};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {primary_color};
                border-radius: 6px;
                min-height: 30px;
            }}
            QTextEdit {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
        """)

    def show_about(self):
        QMessageBox.about(
            self,
            self.i18n.tr('about'),
            f"<h2>{self.i18n.tr('title')}</h2>"
            f"<p>{self.i18n.tr('description')}</p>"
            f"<p><b>{self.i18n.tr('version')}:</b> 2.0.0</p>"
            f"<p><b>{self.i18n.tr('license')}:</b> Apache 2.0</p>"
        )

    def show_shortcuts(self):
        shortcuts_text = (
            f"{self.i18n.tr('shortcut_ctrl_g')}\n"
            f"{self.i18n.tr('shortcut_ctrl_h')}\n"
            f"{self.i18n.tr('shortcut_ctrl_b')}\n"
            f"{self.i18n.tr('shortcut_ctrl_s')}\n"
            f"{self.i18n.tr('shortcut_ctrl_o')}\n"
            f"{self.i18n.tr('shortcut_ctrl_n')}"
        )
        QMessageBox.information(self, self.i18n.tr('shortcuts'), shortcuts_text)

    def save_config_and_show_message(self):
        self.adb_path = self.adb_input.text()
        self.scrcpy_path = self.scrcpy_input.text()
        self.save_config()
        QMessageBox.information(self, "Info", self.i18n.tr('config_saved'))

    def load_config_and_show_message(self):
        self.load_config()
        self.adb_input.setText(self.adb_path)
        self.scrcpy_input.setText(self.scrcpy_path)
        self.lang_combo.setCurrentIndex(0 if self.i18n.lang == 'en' else 1)
        self.theme_combo.setCurrentIndex(0 if self.theme == Theme.LIGHT else 1)
        QMessageBox.information(self, "Info", self.i18n.tr('config_loaded'))


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = ScrcpyGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
