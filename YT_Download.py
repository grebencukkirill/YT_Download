import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
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
            res_items = dl_functions.get_res(self.qle.text(), self.combo_video_ext.currentText())
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

    # Функция выбора папки
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
            settings = QSettings()
            settings.setValue('folder_path', folder_path)
            settings.sync()

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
    def text_changed(self):
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
        #  Запускаем функцию из файла dl_functions.py
        dl_functions.dl_video(self.qle.text(),
                              self.open_button.text(),
                              self.qle_name.text(),
                              ext,
                              res)
        # Запускаем анимацию текста окончания загрузки
        self.show_dl_end_animation()

    # Функция загрузки аудио
    def btn_download_audio(self):
        ext = self.combo_audio_ext.currentText()
        bitrate = self.combo_audio_bitrate.currentText()
        # Запускаем функцию из файла dl_functions.py
        dl_functions.dl_audio(self.qle.text(),
                              self.open_button.text(),
                              self.qle_name.text(),
                              ext,
                              bitrate)
        # Запускаем анимацию текста окончания загрузки
        self.show_dl_end_animation()

    # Функция, которая запускается при выборе другого расширения видеофайла
    def video_ext_changed(self):
        self.combo_video_res.clear()
        res_items = dl_functions.get_res(self.qle.text(), self.combo_video_ext.currentText())
        self.combo_video_res.addItems(res_items)

    # Функция, которая запускается при выборе другого расширения видеофайла
    def audio_ext_changed(self):
        ext = self.combo_audio_ext.currentText()
        if ext == 'wav':
            bitrate_items = dl_functions.get_bitrate(self.qle.text())
            for i in range(len(bitrate_items)):
                bitrate_items[i] = str(bitrate_items[i]) + ' Гц'
        else:
            bitrate_items = ['128 кбит/с', '192 кбит/с', '256 кбит/с']
        self.combo_audio_bitrate.clear()
        self.combo_audio_bitrate.addItems(bitrate_items)

    # Функция со всеми элементами интерфейса
    def initUI(self):

        # Создаем поле ввода для ссылки
        self.qle = QLineEdit(self)
        self.qle.move(160, 65)  # Указываем положение
        self.qle.resize(630, 55)    # Указываем размер
        self.qle.setPlaceholderText('Ссылка на видео')  # Добавляем плейсхолдер
        # Задаем стиль, аналогично стилям CSS
        self.qle.setStyleSheet("""
        QLineEdit{
           background-color: #131313; 
           border: 1px solid #333333; 
           border-radius: 27px; 
           padding-left: 20px; 
           font-size: 18px; 
           color: #E5E1E5
        }""")
        self.qle.textChanged.connect(self.text_changed)  # Считываем изменение текста и запускаем функцию, скрывает все настройки загрузки
        self.qle.show() # Выводим на экран

        # Создаем кнопку с инкокой Video.png и без текста
        self.btn_video = QPushButton(QIcon('icons/Video.ico'), "", self)
        self.btn_video.setIconSize(QSize(24, 24))
        self.btn_video.move(800, 65)
        self.btn_video.resize(55, 55)
        self.btn_video.setStyleSheet("""
        QPushButton{
            background-color: #222222; 
            border: 1px solid #333333; 
            border-radius: 27px;
        }
        QPushButton:pressed{
            background-color: #0E0E0E;
        }""")
        self.btn_video.clicked.connect(self.btn_video_clicked)  # Запускаем функцию при нажатии на кнопку
        self.btn_video.show()

        # Создаем кнопку с инкокой Audio.png и без текста
        self.btn_audio = QPushButton(QIcon("icons/Audio.ico"), "", self)
        self.btn_audio.setIconSize(QSize(24, 24))
        self.btn_audio.move(865, 65)
        self.btn_audio.resize(55, 55)
        self.btn_audio.setStyleSheet("""
        QPushButton{
            background-color: #222222; 
            border: 1px solid #333333; 
            border-radius: 27px;
        }
        QPushButton:pressed{
            background-color: #0E0E0E;
        }""")
        self.btn_audio.clicked.connect(self.btn_audio_clicked)  # Запускаем функцию при нажатии на кнопку
        self.btn_audio.show()

        # Создаем текст, оповещающий об ошибке
        self.label_error = QLabel("Произошла ошибка. Проверьте правильность ссылки или повторите попытку позже.", self)
        self.label_error.setStyleSheet("""
        QLabel{
           border: none; 
           padding: 16px; 
           font-size: 16px; 
           background: rgba(0, 0, 0, 0.2); 
           border-radius: 15px; 
           color: white; 
           padding-left: 30px
        }""")
        self.label_error.resize(700, 50)
        self.label_error.move(190, 450)
        opacity_effect = QGraphicsOpacityEffect(self.label_error)   # Создаем объект эффекта прозражности
        opacity_effect.setOpacity(0)    # Задаем ему нулевое значение
        self.label_error.setGraphicsEffect(opacity_effect)  # Применяем его на текст
        self.label_error.show()

        # Создаем кнопку для выбора папки
        self.open_button = QPushButton(os.path.join(os.environ['USERPROFILE'], 'Downloads'), self)
        self.open_button.clicked.connect(self.open_dialog)
        self.open_button.move(210, 190)
        self.open_button.resize(322, 45)
        self.open_button.setStyleSheet("""
        QPushButton{
            background-color: #272727; 
            border: none; 
            border-radius: 10px;
            text-align: left; 
            padding-left: 10px;
            font-size: 14px;
            color: #FFFFFF;
        }
        QPushButton:pressed{
            background-color: #131313;
        }""")
        self.open_button.hide()

        # Создаем объект QSettings
        settings = QSettings()
        if not settings.isWritable():
            pass
            # print('Нет прав на запись в файл настроек')
        # Считываем в нем параметр folder_path
        folder_path = settings.value('folder_path', defaultValue='')
        # Если он есть, то применяем его кнопке для выбора папки
        if folder_path:
            self.open_button.setText(folder_path)

        # Создаем поле ввода для названия файла
        self.qle_name = QLineEdit(self)
        self.qle_name.move(548, 190)
        self.qle_name.resize(323, 45)
        self.qle_name.setPlaceholderText('Название (по умолчанию оригинальное)')
        self.qle_name.setStyleSheet("""
        QLineEdit{
            background-color: #272727; 
            border: none; 
            border-radius: 10px; 
            padding-left: 10px; 
            font-size: 14px; 
            color: #FFFFFF
        }""")
        self.qle_name.hide()

        # Создаем заголовок для настроек видео
        self.label_video = QLabel('Параметры загрузки видео', self)
        self.label_video.move(210, 150)
        self.label_video.setStyleSheet("""
        QLabel{
            font-size: 18px; 
            color: white; 
            font-weight: light
        }""")
        self.label_video.hide()

        # Создаем выпадающий список для расширений видеофайла
        self.combo_video_ext = QComboBox(self)
        self.combo_video_ext.move(210, 255)
        self.combo_video_ext.resize(270, 45)
        ext_items = ['mp4', 'webm'] # Создаем список с расширениями
        self.combo_video_ext.addItems(ext_items)    # Добавляем его в выпадающий список
        self.combo_video_ext.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #272727; 
            border: none; 
            border-radius: 10px; 
            padding-left: 10px; 
            font-size: 14px;
            color: #FFFFFF;
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
        self.combo_video_ext.currentIndexChanged.connect(self.video_ext_changed)
        self.combo_video_ext.hide()

        # Создаем выпадающий список для разрешений видео
        self.combo_video_res = QComboBox(self)
        self.combo_video_res.move(495, 255)
        self.combo_video_res.resize(270, 45)
        self.combo_video_res.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #272727; 
            border: none; 
            border-radius: 10px; 
            padding-left: 10px; 
            font-size: 14px;
            color: #FFFFFF;
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
        self.btn_dl_video = QPushButton(QIcon("icons/Download.ico"), "", self)
        self.btn_dl_video.setIconSize(QSize(24, 24))
        self.btn_dl_video.move(780, 255)
        self.btn_dl_video.resize(90, 45)
        self.btn_dl_video.setStyleSheet("""
        QPushButton{
            background-color: #B62828; 
            border: none; 
            border-radius: 10px;
        }
        QPushButton:pressed{
            background-color: #5F1010;
        }""")
        self.btn_dl_video.clicked.connect(self.btn_download_video)  # Запускаем функцию загрузки видео при нажатии
        self.btn_dl_video.hide()

        # Создаем заголовок для настроек аудио
        self.label_audio = QLabel('Параметры загрузки аудио', self)
        self.label_audio.move(210, 150)
        self.label_audio.setStyleSheet("""
        QLabel{    
            font-size: 18px; 
            color: white; 
            font-weight: light
        }""")
        self.label_audio.hide()

        # Создаем выпадающий список с расширениями аудиофайлов
        self.combo_audio_ext = QComboBox(self)
        self.combo_audio_ext.move(210, 255)
        self.combo_audio_ext.resize(270, 45)
        ext_items = ['mp3', 'wav']
        self.combo_audio_ext.addItems(ext_items)
        self.combo_audio_ext.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #272727; 
            border: none; 
            border-radius: 10px; 
            padding-left: 10px; 
            font-size: 14px;
            color: #FFFFFF;
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
        self.combo_audio_ext.currentIndexChanged.connect(self.audio_ext_changed)
        self.combo_audio_ext.hide()

        # Создаем выпадающий список со значениями битрейта
        self.combo_audio_bitrate = QComboBox(self)
        self.combo_audio_bitrate.move(495, 255)
        self.combo_audio_bitrate.resize(270, 45)
        bitrate_items = ['128 кбит/с', '192 кбит/с', '256 кбит/с']
        self.combo_audio_bitrate.addItems(bitrate_items)
        self.combo_audio_bitrate.setStyleSheet("""
        QComboBox, QComboBox QAbstractItemView{
            background-color: #272727; 
            border: none; 
            border-radius: 10px; 
            padding-left: 10px; 
            font-size: 14px;
            color: #FFFFFF;
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
        self.btn_dl_audio = QPushButton(QIcon("icons/Download.ico"), "", self)
        self.btn_dl_audio.setIconSize(QSize(24, 24))
        self.btn_dl_audio.move(780, 255)
        self.btn_dl_audio.resize(90, 45)
        self.btn_dl_audio.setStyleSheet("""
        QPushButton{
            background-color: #B62828; 
            border: none; 
            border-radius: 10px;
        }
        QPushButton:pressed{
            background-color: #5F1010;
        }""")
        self.btn_dl_audio.clicked.connect(self.btn_download_audio)  # Запускаем функцию загрузки аудио при нажатии
        self.btn_dl_audio.hide()

        # Создаем текст, оповещающий об окончании загрузки
        self.label_dl_end = QLabel("Загрузка завершена.", self)
        self.label_dl_end.setStyleSheet("""
        QLabel{
            border: none; 
            padding: 16px; 
            font-size: 16px; 
            background: rgba(0, 0, 0, 0.2); 
            border-radius: 15px; 
            color: white; 
            padding-left: 30px
        }""")
        self.label_dl_end.resize(215, 50)
        self.label_dl_end.move(432, 450)
        opacity_effect = QGraphicsOpacityEffect(self.label_dl_end)
        opacity_effect.setOpacity(0)
        self.label_dl_end.setGraphicsEffect(opacity_effect)
        self.label_dl_end.show()

        # Задаем параметры окна
        self.setFixedSize(1080, 560) # Задаем фиксированный размер
        self.move(120, 10) # Задаем расположение на экране
        self.setWindowTitle('YT Downloader') # Задаем название
        self.setStyleSheet("background-color: #0F0F0F;") # Задаем цвет фона
        self.setWindowIcon(QIcon('icons/App_icon.png')) # Задаем иконку приложения
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)    # Создаем объект класса QApplication
    ex = App()  # Создаем объект класса App
    sys.exit(app.exec_()) # Запускаем цикл событий приложения и ожидаем ввода от пользователя. Когда пользователь закрывает окно, цикл завершается и программа закрывается.