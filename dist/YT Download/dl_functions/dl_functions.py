import yt_dlp, os, re, sys, ffmpeg
from collections import OrderedDict
from datetime import datetime
from yt_dlp.postprocessor import FFmpegPostProcessor
FFmpegPostProcessor._ffmpeg_location.set(os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

__all__ = ['check', 'get_res', 'get_bitrate', 'dl_video', 'dl_audio']

# Функция для проверки правильности ссылки
def check(url):
    # Создаем экземпляр класса YoutubeDL
    ydl = yt_dlp.YoutubeDL({'quiet': True})
    # Пытаемся получить информацию из видео. Если получается, значит ссылка правильная - возвращаем True.
    try:
        ydl.extract_info(url, download=False)
        return True
    except:
        return False


def get_res(url, ext):
    # Создаем экземпляр класса YoutubeDL
    ydl = yt_dlp.YoutubeDL({'quiet': True})
    # Создаем список разрешений видео
    res_list = [f.get('resolution') for f in ydl.extract_info(url, download=False).get('formats') if not 'audio only' in f.get('resolution') and f.get('acodec') == 'none' and f.get('vcodec') != 'none' and (f.get('ext') == ext)]
    # Возвращаем отсортированный список
    return list(OrderedDict.fromkeys(res_list))


def get_bitrate(url):
    # Создаем экземпляр класса YoutubeDL
    ydl = yt_dlp.YoutubeDL({'quiet': True})
    # Создаем список частот дискретизации
    bitrate_list = [f.get('asr') for f in ydl.extract_info(url, download=False).get('formats') if f.get('asr') is not None]
    # Возвращаем отсортированный список
    return sorted(set(bitrate_list))
    print(sorted(set(bitrate_list)))


# Функция, которая скачивает видео
def dl_video(url, path, filename, ext, video_format):
    # Создаем экземпляр класса YoutubeDL
    ydl = yt_dlp.YoutubeDL({'quiet': True})
    # Находим format_id нужного формата видео
    for f in ydl.extract_info(url, download=False).get('formats'):
        if f.get('resolution') == video_format and f.get('ext', None) == ext and f.get('acodec') == 'none' and f.get('vcodec') != 'none':
            format_id = f.get('format_id')
    for f in ydl.extract_info(url, download=False).get('formats'):
        if f.get('resolution') == 'audio only' and f.get('asr') == 44100:
            audio_format_id = f.get('format_id')
    # Если имя файла не задано, то берем название видео
    if filename == '':
        video_info = ydl.extract_info(url, download=False)
        filename = video_info.get('title')
    # Удаляем недопустимые символы для названия файла
    filename = re.sub(r'[\'\"|*?<>:\\\n\r\t\v]', '', filename)
    # Создаем полный путь для сохранения видео
    output_path = f'{path}\\{filename}.{ext}'
    # Проверяем существет ли файл с таким названием и если есть дописываем его индекс в скобках
    if os.path.isfile(output_path):
        i = 1
        while True:
            new_filename = f"{path}\\{filename} ({i}).{ext}"
            if not os.path.isfile(f'{output_path} ({i}).{ext}'):
                output_path = new_filename
                break
            i += 1
    # Задаем параметры для загрузки видео
    ydl_opts = {
        'noabortonerror': True,
        'ignoreerrors ': True,
        'format': f'{format_id}+{audio_format_id}',
        'outtmpl': output_path,
        'merge_output_format': ext,
    }
    # Скачиваем видео
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # Ставим дату создания и изменения
    os.utime(output_path, (datetime.now().timestamp(), datetime.now().timestamp()))


# Функция, которая скачивает аудио
def dl_audio(url, path, filename, ext, bitrate):
    bitrate = str(bitrate.split(' ')[0])
    # Создаем экземпляр класса YoutubeDL
    ydl = yt_dlp.YoutubeDL({'quiet': True})
    if filename == '':
        audio_info = ydl.extract_info(url, download=False)
        filename = audio_info.get('title')
    # Удаляем недопустимые символы для названия файла
    filename = re.sub(r'[|*?<>:\\\n\r\t\v]', '', filename)
    # Создаем полный путь для сохранения видео
    output_path = f'{path}\\{filename}'
    # Удаляем файл если он уже существует
    if os.path.isfile(f'{output_path}.{ext}'):
        i = 1
        while True:
            new_filename = f"{output_path} ({i})"
            if not os.path.isfile(f'{output_path} ({i}).{ext}'):
                output_path = new_filename
                break
            i += 1
    if ext == 'wav':
        format_ids = {}
        for f in ydl.extract_info(url, download=False).get('formats'):
            if f.get('asr') == int(bitrate) and f.get('acodec') != 'none':
                format_ids[f.get('format_id')] = f.get('abr')

        ydl_opts = {
            'noabortonerror': True,
            'ignoreerrors ': True,
            'format': max(format_ids, key=format_ids.get),
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ext,
                'preferredquality': bitrate}],
        }
    else:
        ydl_opts = {
            'noabortonerror': True,
            'ignoreerrors ': True,
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': ext,
                'preferredquality': bitrate}],
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    # Ставим дату создания и изменения
    os.utime(f'{output_path}.{ext}', (datetime.now().timestamp(), datetime.now().timestamp()))