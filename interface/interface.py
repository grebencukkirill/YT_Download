import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import *

import dl_functions


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def btn_video_clicked(self):
        if self.qle.text() and dl_functions.check(self.qle.text()):
            self.label_video.show()
            self.combo_video_ext.show()
            self.open_button.show()
            self.combo_video_res.show()
            self.qle_name.show()
            self.btn_dl_video.show()

            self.label_audio.hide()
            self.btn_dl_audio.hide()
            self.combo_audio_bitrate.hide()
            self.combo_audio_ext.hide()

            self.combo_video_res.clear()
            res_items = dl_functions.get_res(self.qle.text())
            self.combo_video_res.addItems(res_items)
        else:
            self.show_error_animation()

    def btn_audio_clicked(self):
        if self.qle.text() and dl_functions.check(self.qle.text()):
            self.label_audio.show()
            self.open_button.show()
            self.qle_name.show()
            self.combo_audio_bitrate.show()
            self.combo_audio_ext.show()
            self.btn_dl_audio.show()

            self.label_video.hide()
            self.btn_dl_video.hide()
            self.combo_video_ext.hide()
            self.combo_video_res.hide()
        else:
            self.show_error_animation()

    def open_dialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        folder_path = dialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            self.open_button.setText(folder_path)
            settings = QSettings()
            settings.setValue("folder_path", folder_path)

    def show_error_animation(self):
        opacity_effect = QGraphicsOpacityEffect(self.label_error)
        self.label_error.setGraphicsEffect(opacity_effect)

        self.animation = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

        self.animation_stop = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation_stop.setDuration(2500)
        self.animation_stop.setStartValue(1.0)
        self.animation_stop.setEndValue(1.0)

        self.animation_reverse = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation_reverse.setDuration(300)
        self.animation_reverse.setStartValue(1.0)
        self.animation_reverse.setEndValue(0.0)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.addAnimation(self.animation_stop)
        self.animation_group.addAnimation(self.animation_reverse)
        self.animation_group.start()

    def show_dl_end_animation(self):
        opacity_effect = QGraphicsOpacityEffect(self.label_dl_end)
        self.label_dl_end.setGraphicsEffect(opacity_effect)

        self.animation = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

        self.animation_stop = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation_stop.setDuration(2500)
        self.animation_stop.setStartValue(1.0)
        self.animation_stop.setEndValue(1.0)

        self.animation_reverse = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation_reverse.setDuration(300)
        self.animation_reverse.setStartValue(1.0)
        self.animation_reverse.setEndValue(0.0)

        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.addAnimation(self.animation_stop)
        self.animation_group.addAnimation(self.animation_reverse)
        self.animation_group.start()

    def TextChanged(self):
        self.label_video.hide()
        self.label_audio.hide()
        self.open_button.hide()
        self.qle_name.hide()
        self.combo_video_res.hide()
        self.combo_video_ext.hide()
        self.combo_audio_bitrate.hide()
        self.combo_audio_ext.hide()
        self.btn_dl_video.hide()
        self.btn_dl_audio.hide()


    def btn_download_video(self):
        ext = self.combo_video_ext.currentText()
        res = self.combo_video_res.currentText()
        if self.open_button.text() != 'Папка загрузки':
            dl_functions.dl_video(self.qle.text(),
                                  self.open_button.text(),
                                  self.qle_name.text(),
                                  ext,
                                  res)
            self.show_dl_end_animation()
        else:
            self.show_error_animation()

    def btn_download_audio(self):
        ext = self.combo_audio_ext.currentText()
        br = self.combo_audio_bitrate.currentText()
        if self.open_button.text() != 'Папка загрузки':
            dl_functions.dl_audio(self.qle.text(),
                                  self.open_button.text(),
                                  self.qle_name.text(),
                                  ext,
                                  br)
            self.show_dl_end_animation()
        else:
            self.show_error_animation()

    def initUI(self):
        # Создаем поле ввода
        self.qle = QLineEdit(self)
        self.qle.move(115, 50)
        self.qle.resize(560, 46)
        self.qle.setPlaceholderText('Ссылка на видео')
        self.qle.setStyleSheet('background-color: #D6D6D6; border: none; border-radius: 2px; padding-left: 10px; font-size: 16px')
        self.qle.textChanged.connect(self.TextChanged)

        self.btn_video = QPushButton(QIcon('icons/Video.png'), "", self)
        self.btn_video.move(683, 50)
        self.btn_video.resize(52, 46)
        self.btn_video.setStyleSheet("""
        QPushButton{
            background-color: #EC5555; 
            border: none; 
            border-radius: 2px;
        }
        QPushButton:pressed{
            background-color: #A73C3C;
        }""")
        self.btn_video.clicked.connect(self.btn_video_clicked)

        self.btn_audio = QPushButton(QIcon("icons/Audio.png"), "", self)
        self.btn_audio.move(743, 50)
        self.btn_audio.resize(52, 46)
        self.btn_audio.setStyleSheet("""
        QPushButton{
            background-color: #EC5555; 
            border: none; 
            border-radius: 2px;
        }
        QPushButton:pressed{
            background-color: #A73C3C;
        }""")
        self.btn_audio.clicked.connect(self.btn_audio_clicked)

        self.label_error = QLabel("Произошла ошибка. Проверьте правильность ссылки или повторите попытку позже.", self)
        self.label_error.setStyleSheet("border: none; padding: 16px; font-size: 14px; background: #1B1B1B; box-shadow: 3px 4px 10px rgba(0, 0, 0, 0.25); border-radius: 2px; color: white")
        self.resize(614, 36)
        self.label_error.move(152, 320)
        opacity_effect = QGraphicsOpacityEffect(self.label_error)
        opacity_effect.setOpacity(0)
        self.label_error.setGraphicsEffect(opacity_effect)
        self.label_error.show()

        settings = QSettings()
        saved_folder_path = settings.value("folder_path")
        if saved_folder_path:
            self.open_button.setText(saved_folder_path)

        self.open_button = QPushButton("Папка загрузки", self)
        self.open_button.clicked.connect(self.open_dialog)
        self.open_button.move(145, 160)
        self.open_button.resize(303, 36)
        self.open_button.setStyleSheet("""
        QPushButton{
            background-color: #D6D6D6; 
            border: none; 
            border-radius: 2px;
            text-align: left; 
            padding-left: 10px;
            font-size: 12px;
        }
        QPushButton:pressed{
            background-color: #B7B7B7;
        }""")
        self.open_button.hide()

        self.qle_name = QLineEdit()
        self.qle_name = QLineEdit(self)
        self.qle_name.move(456, 160)
        self.qle_name.resize(303, 36)
        self.qle_name.setPlaceholderText('Название файла (по умолчанию оригинальное)')
        self.qle_name.setStyleSheet('background-color: #D6D6D6; border: none; border-radius: 2px; padding-left: 10px; font-size: 12px')
        self.qle_name.hide()

        self.label_video = QLabel('Параметры загрузки видео', self)
        self.label_video.move(115, 120)
        self.label_video.setStyleSheet('font-size: 16px; color: white; font-weight: light')
        self.label_video.hide()

        self.combo_video_ext = QComboBox(self)
        self.combo_video_ext.move(145, 206)
        self.combo_video_ext.resize(199, 36)
        ext_items = ['mp4', 'webm']
        self.combo_video_ext.addItems(ext_items)
        self.combo_video_ext.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #D6D6D6; 
            border: none; 
            border-radius: 2px; 
            padding-left: 10px; 
            font-size: 12px;
        }
        QComboBox::drop-down {
            width: 0px;
            height: 0px;
            border: 0px;
        }
        QComboBox::down-arrow {
        color: black;
        }
        """)
        self.combo_video_ext.hide()

        self.combo_video_res = QComboBox(self)
        self.combo_video_res.move(353, 206)
        self.combo_video_res.resize(238, 36)
        self.combo_video_res.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #D6D6D6; 
            border: none; 
            border-radius: 2px; 
            padding-left: 10px; 
            font-size: 12px;
        }
        QComboBox::drop-down {
            width: 0px;
            height: 0px;
            border: 0px;
        }
        QComboBox::down-arrow {
        color: black;
        }
        """)
        self.combo_video_res.hide()

        self.btn_dl_video = QPushButton(QIcon("icons/Download.png"), "", self)
        self.btn_dl_video.move(599, 206)
        self.btn_dl_video.resize(160, 36)
        self.btn_dl_video.setStyleSheet("""
        QPushButton{
            background-color: #EC5555; 
            border: none; 
            border-radius: 2px;
        }
        QPushButton:pressed{
            background-color: #A73C3C;
        }""")
        self.btn_dl_video.clicked.connect(self.btn_download_video)
        self.btn_dl_video.hide()

        self.label_audio = QLabel('Параметры загрузки аудио', self)
        self.label_audio.move(115, 120)
        self.label_audio.setStyleSheet('font-size: 16px; color: white; font-weight: light')
        self.label_audio.hide()

        self.combo_audio_ext = QComboBox(self)
        self.combo_audio_ext.move(145, 206)
        self.combo_audio_ext.resize(199, 36)
        ext_items = ['mp3', 'wav']
        self.combo_audio_ext.addItems(ext_items)
        self.combo_audio_ext.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #D6D6D6; 
            border: none; 
            border-radius: 2px; 
            padding-left: 10px; 
            font-size: 12px;
        }
        QComboBox::drop-down {
            width: 0px;
            height: 0px;
            border: 0px;
        }
        QComboBox::down-arrow {
        color: black;
        }
        """)
        self.combo_audio_ext.hide()

        self.combo_audio_bitrate = QComboBox(self)
        self.combo_audio_bitrate.move(353, 206)
        self.combo_audio_bitrate.resize(238, 36)
        bitrate_items = ['128 кбит/с', '192 кбит/с', '256 кбит/с']
        self.combo_audio_bitrate.addItems(bitrate_items)
        self.combo_audio_bitrate.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #D6D6D6; 
            border: none; 
            border-radius: 2px; 
            padding-left: 10px; 
            font-size: 12px;
        }
        QComboBox::drop-down {
            width: 0px;
            height: 0px;
            border: 0px;
        }
        QComboBox::down-arrow {
        color: black;
        }
        """)
        self.combo_audio_bitrate.hide()

        self.btn_dl_audio = QPushButton(QIcon("icons/Download.png"), "", self)
        self.btn_dl_audio.move(599, 206)
        self.btn_dl_audio.resize(160, 36)
        self.btn_dl_audio.setStyleSheet("""
        QPushButton{
            background-color: #EC5555; 
            border: none; 
            border-radius: 2px;
        }
        QPushButton:pressed{
            background-color: #A73C3C;
        }""")
        self.btn_dl_audio.clicked.connect(self.btn_download_audio)
        self.btn_dl_audio.hide()

        self.label_dl_end = QLabel("Загрузка завершена. Если вы повторно скачиваете файл, то он будет перезаписан. ", self)
        self.label_dl_end.setStyleSheet("border: none; padding: 16px; font-size: 14px; background: #1B1B1B; box-shadow: 3px 4px 10px rgba(0, 0, 0, 0.25); border-radius: 2px; color: white")
        self.resize(614, 36)
        self.label_dl_end.move(152, 320)
        opacity_effect = QGraphicsOpacityEffect(self.label_dl_end)
        opacity_effect.setOpacity(0)
        self.label_dl_end.setGraphicsEffect(opacity_effect)
        self.label_dl_end.show()

        self.setFixedSize(860, 420)
        self.move(320, 100)
        self.setWindowTitle('YT Downloader')
        self.setStyleSheet("background-color: #2C2C2C;")
        self.setWindowIcon(QIcon('icons/App_icon.png'))
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())