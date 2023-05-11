import yt_dlp, os, re
from collections import OrderedDict
from datetime import datetime
from yt_dlp.postprocessor import FFmpegPostProcessor
FFmpegPostProcessor._ffmpeg_location.set(os.path.join(os.path.dirname(os.path.abspath(__file__))))
import interface


__all__ = ['check', 'get_res', 'dl_video', 'dl_audio']

# Функция для проверки правильности ссылки
def check(url):
    # Создаем экземпляр класса YoutubeDL
    ydl = yt_dlp.YoutubeDL({})
    # Пытаемся получить информацию из видео. Если получается, значит ссылка правильная - возвращаем True.
    try:
        ydl.extract_info(url, download=False)
        return True
    except:
        return False

def get_res(url):
    try:
        # Создаем экземпляр класса YoutubeDL
        ydl = yt_dlp.YoutubeDL({})
        # Создаем список разрешений видео
        res_list = [f.get('resolution') for f in ydl.extract_info(url, download=False).get('formats') if not 'audio only' in f.get('resolution') and f.get('acodec') == 'none' and f.get('vcodec') != 'none' and (f.get('ext') == 'mp4' or f.get('ext') == 'webm')]
        # Возвращаем отсортированный список
        return list(OrderedDict.fromkeys(res_list))
    except:
        interface.App.show_error_animation()

# Функция, которая скачивает видео
def dl_video(url, path, filename, ext, video_format):
    try:
        # Создаем экземпляр класса YoutubeDL
        ydl = yt_dlp.YoutubeDL({})
        # Находим format_id нужного формата видео
        for f in ydl.extract_info(url, download=False).get('formats'):
            if f.get('resolution') == video_format and f.get('ext', None) == ext and f.get('acodec') == 'none' and f.get('vcodec') != 'none':
                format_id = f.get('format_id')
        # Если имя файла не задано, то берем название видео
        if filename == '':
            video_info = ydl.extract_info(url, download=False)
            filename = video_info.get('title')
        # Удаляем недопустимые символы для названия файла
        filename = re.sub(r'[|*?<>:\\\n\r\t\v]', '', filename)
        # Создаем полный путь для сохранения видео
        output_path = f'{path}\\{filename}.{ext}'
        # Удаляем файл если он уже существует
        if os.path.isfile(output_path):
            os.remove(output_path)
        # Задаем параметры для загрузки видео
        ydl_opts = {
            'noabortonerror': True,
            'ignoreerrors ': True,
            'format': f'{format_id}+bestaudio',
            'outtmpl': output_path,
            'merge_output_format': ext,
        }
        # Скачиваем видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Ставим дату создания и изменения
        os.utime(output_path, (datetime.now().timestamp(), datetime.now().timestamp()))
    except:
        interface.App.show_error_animation()



def dl_audio(url, path, filename, ext, br):
    try:
        br = str(br.split(' ')[0])
        # Создаем экземпляр класса YoutubeDL
        ydl = yt_dlp.YoutubeDL({})
        if filename == '':
            audio_info = ydl.extract_info(url, download=False)
            filename = audio_info.get('title')
        # Удаляем недопустимые символы для названия файла
        filename = re.sub(r'[|*?<>:\\\n\r\t\v]', '', filename)
        # Создаем полный путь для сохранения видео
        output_path = f'{path}\\{filename}'
        # Удаляем файл если он уже существует
        if os.path.isfile(f'{output_path}.{ext}'):
            os.remove(f'{output_path}.{ext}')
        ydl_opts = {
            'noabortonerror': True,
            'ignoreerrors ': True,
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ext,
                'preferredquality': br}]
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # Ставим дату создания и изменения
        os.utime(f'{output_path}.{ext}', (datetime.now().timestamp(), datetime.now().timestamp()))
    except:
        interface.App.show_error_animation()
