import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import *

import dl_functions

# Определяем класс App, который наследуется от класса QWidget
class App(QWidget):
    def __init__(self):
        super().__init__()  # Вызываем конструктор класса QWidget
        self.initUI()

    # Функция нажатия на кнопку
    def btn_video_clicked(self):
        # Проверяем введено ли что-нибудь и является ли это рабочей ссылкой
        if self.qle.text() and dl_functions.check(self.qle.text()):
            # Выводим на экран настройки загрузки видео
            self.label_video.show()
            self.combo_video_ext.show()
            self.open_button.show()
            self.combo_video_res.show()
            self.qle_name.show()
            self.btn_dl_video.show()

            # Скрываем настройки загрузки аудио
            self.label_audio.hide()
            self.btn_dl_audio.hide()
            self.combo_audio_bitrate.hide()
            self.combo_audio_ext.hide()

            # Сначала отчищаем выпадающий список, потом вписываем в него разрешения видео
            self.combo_video_res.clear()
            res_items = dl_functions.get_res(self.qle.text())
            self.combo_video_res.addItems(res_items)
        else:
            # В противном случае запускаем анимацию текста ошибки
            self.show_error_animation()

    # Функция нажатия на кнопку
    def btn_audio_clicked(self):
        # Проверяем введено ли что-нибудь и является ли это рабочей ссылкой
        if self.qle.text() and dl_functions.check(self.qle.text()):
            # Выводим на экран настройки загрузки аудио
            self.label_audio.show()
            self.open_button.show()
            self.qle_name.show()
            self.combo_audio_bitrate.show()
            self.combo_audio_ext.show()
            self.btn_dl_audio.show()

            # Скрываем настройки загрузки видео
            self.label_video.hide()
            self.btn_dl_video.hide()
            self.combo_video_ext.hide()
            self.combo_video_res.hide()
        else:
            # В противном случае запускаем анимацию текста ошибки
            self.show_error_animation()

    # Функция для выбора папки
    def open_dialog(self):
        # Создаем диологовое окно
        dialog = QFileDialog()
        # Устанавливаем режим, чтобы принимать только пути к каталогам.
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        # Открываем диалоговое окно
        folder_path = dialog.getExistingDirectory(self, "Выберите папку")
        # Если пользователь выбрал путь к каталогу, обновляем текст кнопки с путем и записываем путь в настройки
        if folder_path:
            self.open_button.setText(folder_path)
            self.settings.setValue("folder_path", folder_path)

    # Функция анимации текста ошибки
    def show_error_animation(self):
        opacity_effect = QGraphicsOpacityEffect(self.label_error)
        self.label_error.setGraphicsEffect(opacity_effect)

        # Создаем анимацию появления
        self.animation = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)

        self.animation_stop = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation_stop.setDuration(2500)
        self.animation_stop.setStartValue(1.0)
        self.animation_stop.setEndValue(1.0)

        # Создаем анимацию изчезновения
        self.animation_reverse = QPropertyAnimation(opacity_effect, b"opacity", self)
        self.animation_reverse.setDuration(300)
        self.animation_reverse.setStartValue(1.0)
        self.animation_reverse.setEndValue(0.0)

        # Объединяем анимации и воспроизводим
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.animation)
        self.animation_group.addAnimation(self.animation_stop)
        self.animation_group.addAnimation(self.animation_reverse)
        self.animation_group.start()

    # Функция анимации текста окончания загрузки
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

    # Функция, которая запускается при изменении текста в поле ввода и скрывает все настройки загрузки
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

    # Функция загрузки видео
    def btn_download_video(self):
        ext = self.combo_video_ext.currentText()
        res = self.combo_video_res.currentText()
        #  Если выбрана папка загрузки запускаем функцию из файла dl_functions.py
        if self.open_button.text() != 'Папка загрузки':
            dl_functions.dl_video(self.qle.text(),
                                  self.open_button.text(),
                                  self.qle_name.text(),
                                  ext,
                                  res)
            # Запускаем анимацию текста окончания загрузки
            self.show_dl_end_animation()
        else:
            # В противном случае запускаем анимацию текста ошибки
            self.show_error_animation()

    # Функция загрузки аудио
    def btn_download_audio(self):
        ext = self.combo_audio_ext.currentText()
        br = self.combo_audio_bitrate.currentText()
        #  Если выбрана папка загрузки запускаем функцию из файла dl_functions.py
        if self.open_button.text() != 'Папка загрузки':
            dl_functions.dl_audio(self.qle.text(),
                                  self.open_button.text(),
                                  self.qle_name.text(),
                                  ext,
                                  br)
            # Запускаем анимацию текста окончания загрузки
            self.show_dl_end_animation()
        else:
            # В противном случае запускаем анимацию текста ошибки
            self.show_error_animation()

    # Функция со всеми элементами интерфейса
    def initUI(self):

        # Создаем поле ввода для ссылки
        self.qle = QLineEdit(self)
        self.qle.move(115, 50)  # Указываем положение
        self.qle.resize(560, 46)    # Указываем размер
        self.qle.setPlaceholderText('Ссылка на видео')  # Добавляем плейсхолдер
        # Задаем стиль, аналогично стилям CSS
        self.qle.setStyleSheet('background-color: #D6D6D6; border: none; border-radius: 2px; padding-left: 10px; font-size: 16px')
        self.qle.textChanged.connect(self.TextChanged)  # Считываем изменение текста и запускаем функцию, скрывает все настройки загрузки
        self.qle.show() # Выводим на экран

        # Создаем кнопку с инкокой Video.png и без текста
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
        self.btn_video.clicked.connect(self.btn_video_clicked)  # Запускаем функцию при нажатии на кнопку
        self.btn_video.show()

        # Создаем кнопку с инкокой Audio.png и без текста
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
        self.btn_audio.clicked.connect(self.btn_audio_clicked)  # Запускаем функцию при нажатии на кнопку
        self.btn_audio.show()

        # Создаем текст, оповещающий об ошибке
        self.label_error = QLabel("Произошла ошибка. Проверьте правильность ссылки или повторите попытку позже.", self)
        self.label_error.setStyleSheet("border: none; padding: 16px; font-size: 14px; background: #1B1B1B; box-shadow: 3px 4px 10px rgba(0, 0, 0, 0.25); border-radius: 2px; color: white")
        self.resize(614, 36)
        self.label_error.move(152, 320)
        opacity_effect = QGraphicsOpacityEffect(self.label_error)   # Создаем объект эффекта прозражности
        opacity_effect.setOpacity(0)    # Задаем ему нулевое значение
        self.label_error.setGraphicsEffect(opacity_effect)  # Применяем его на текст
        self.label_error.show()

        # Создаем кнопку для выбора папки
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

        # Создаем объект QSettings
        self.settings = QSettings(self)
        # Считываем в нем параметр folder_path
        saved_folder_path = self.settings.value("folder_path")
        # Если он есть, то применяем его кнопке для выбора папки
        if saved_folder_path:
            self.open_button.setText(saved_folder_path)

        # Создаем поле ввода для названия файла
        self.qle_name = QLineEdit()
        self.qle_name = QLineEdit(self)
        self.qle_name.move(456, 160)
        self.qle_name.resize(303, 36)
        self.qle_name.setPlaceholderText('Название файла (по умолчанию оригинальное)')
        self.qle_name.setStyleSheet('background-color: #D6D6D6; border: none; border-radius: 2px; padding-left: 10px; font-size: 12px')
        self.qle_name.hide()

        # Создаем заголовок для настроек видео
        self.label_video = QLabel('Параметры загрузки видео', self)
        self.label_video.move(115, 120)
        self.label_video.setStyleSheet('font-size: 16px; color: white; font-weight: light')
        self.label_video.hide()

        # Создаем выпадающий список для расширений видеофайла
        self.combo_video_ext = QComboBox(self)
        self.combo_video_ext.move(145, 206)
        self.combo_video_ext.resize(199, 36)
        ext_items = ['mp4', 'webm'] # Создаем список с расширениями
        self.combo_video_ext.addItems(ext_items)    # Добавляем его в выпадающий список
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

        # Создаем выпадающий список для разрешений видео
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

        # Создаем кнопку загрузки видео
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
        self.btn_dl_video.clicked.connect(self.btn_download_video)  # Запускаем функцию загрузки видео при нажатии
        self.btn_dl_video.hide()

        # Создаем заголовок для настроек аудио
        self.label_audio = QLabel('Параметры загрузки аудио', self)
        self.label_audio.move(115, 120)
        self.label_audio.setStyleSheet('font-size: 16px; color: white; font-weight: light')
        self.label_audio.hide()

        # Создаем выпадающий список с расширениями аудиофайлов
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

        # Создаем выпадающий список со значениями битрейта
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

        # Создаем кнопку загрузки аудио
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
        self.btn_dl_audio.clicked.connect(self.btn_download_audio)  # Запускаем функцию загрузки аудио при нажатии
        self.btn_dl_audio.hide()

        # Создаем текст, оповещающий об окончании загрузки
        self.label_dl_end = QLabel("Загрузка завершена. Если вы повторно скачиваете файл, то он будет перезаписан. ", self)
        self.label_dl_end.setStyleSheet("border: none; padding: 16px; font-size: 14px; background: #1B1B1B; box-shadow: 3px 4px 10px rgba(0, 0, 0, 0.25); border-radius: 2px; color: white")
        self.resize(614, 36)
        self.label_dl_end.move(152, 320)
        opacity_effect = QGraphicsOpacityEffect(self.label_dl_end)
        opacity_effect.setOpacity(0)
        self.label_dl_end.setGraphicsEffect(opacity_effect)
        self.label_dl_end.show()

        # Задаем параметры окна
        self.setFixedSize(860, 420) # Задаем фиксированный размер
        self.move(320, 100) # Задаем расположение на экране
        self.setWindowTitle('YT Downloader') # Задаем название
        self.setStyleSheet("background-color: #2C2C2C;") # Задаем цвет фона
        self.setWindowIcon(QIcon('icons/App_icon.png')) # Задаем иконку приложения
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)    # Создаем объект класса QApplication
    ex = App()  # Создаем объект класса App
    sys.exit(app.exec_()) # Запускаем цикл событий приложения и ожидаем ввода от пользователя. Когда пользователь закрывает окно, цикл завершается и программа закрывается.