import requests

def link_validation(id):
    checker_url = ['https://www.youtube.com/playlist?list=', 'https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=', 'https://www.youtube.com/shorts/']

    codes = []

    for i in checker_url:
        request = requests.get(i + id)
        codes.append(request.status_code)

    return 200 in codes


class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# ℹ️ See "progress_hooks" in help(yt_dlp.YoutubeDL)
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')


def download_options (formato, tipo, caminho):
    options = {
        'logger': MyLogger(),
        'progress_hooks': [my_hook]
    }
    
    ### configurando o formato
    if formato == 'Vídeo':
        options.update(list(options.items()) + list({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'}.items()))
    elif formato == 'Audio':
        options.update(list(options.items()) + list({'final_ext': 'mp3', 'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'nopostoverwrites': False, 'preferredcodec': 'mp3', 'preferredquality': '5'}]}.items()))

    ### configurando a saída
    if tipo == 'Arquivo':
        options.update(list(options.items()) + list({'outtmpl': {'default': '{}/%(title)s.%(ext)s'.format(caminho)}}.items()))
    elif tipo == 'Playlist':
        options.update(list(options.items()) + list({'outtmpl': {'default': '{}/%(playlist_title)s/%(title)s.%(ext)s'.format(caminho)}}.items()))
    elif tipo == 'Capítulos':
            options.update(list(options.items()) + list({'outtmpl': {'chapter': '{}/%(title)s/%(section_number)s - '
                    '%(section_title)s.%(ext)s'.format(caminho)},
'postprocessors': [{'force_keyframes': False, 'key': 'FFmpegSplitChapters'}]}.items()))
    
    return options

format = ['Vídeo', 'Audio']
type = ['Arquivo', 'Playlist', 'Capítulos']