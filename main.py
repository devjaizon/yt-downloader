from yt_dlp import YoutubeDL
import flet as ft
import func


class ID_Section(ft.Column):
    def __init__(self):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.valid_id = False

        self.txt_video_id = ft.TextField(
            label='Cole o ID do vídeo/short/playlist aqui...', on_change=self.make_invalid,
            autofocus=True
        )
        self.bt_validate_id = ft.ElevatedButton(text="Validar", on_click=self.validate)
        self.txt_id_status = ft.Text('Insira uma ID para começar!', size=14, color='yellow')

        self.controls = [
            ft.Row([
                self.txt_video_id,
                self.bt_validate_id,
            ],
            ft.MainAxisAlignment.CENTER
            ),
            self.txt_id_status,
        ]

    def check_id(self, e):
        if self.valid_id:
             self.txt_id_status.value='ID válida!'
             self.txt_id_status.color='green'
        elif self.txt_video_id.value== '':
             self.txt_id_status.value='Insira uma ID para começar!'
             self.txt_id_status.color='yellow'
        else:
             self.txt_id_status.value='Insira uma ID válida!'
             self.txt_id_status.color='red'


    def make_invalid(self, e):
        self.valid_id = False
        self.check_id(e)
        self.update()

    def validate(self, e):
        if self.txt_video_id.value != '':
            self.valid_id = func.link_validation(self.txt_video_id.value)
            self.check_id(e)
            self.update()

    def return_data (self):
        return  self.valid_id, self.txt_video_id.value


class Path_Button(ft.ElevatedButton):
    def __init__(self):
        super().__init__()

        self.file_picker = ft.FilePicker(on_result=self.get_path)

        self.text = 'Escolha um diretório'
        self.on_click = lambda _: self.file_picker.get_directory_path()
        

    def get_path(self, e: ft.FilePickerResultEvent):
        self.path = e.path
    

class Options_Section(ft.Row):
    def __init__(self, file_picker):
        super().__init__()
        self.alignment = ft.MainAxisAlignment.CENTER

        self.opt_format = ft.Dropdown(
            label="Formato:",
            width=120
        )

        self.opt_type = ft.Dropdown(
            label="Tipo:",
            width=120
        )

        self.file_picker = file_picker

        self.dir_path = ft.ElevatedButton("Escolha um diretório...", on_click=lambda _: self.file_picker.get_directory_path())

        for format in func.format:
            self.opt_format.options.append(ft.dropdown.Option(format))

        for type in func.type:
            self.opt_type.options.append(ft.dropdown.Option(type))

        self.controls = [
            self.opt_format,
            self.opt_type,
            file_picker
        ]

    def get_path (e: ft.FilePickerResultEvent):
        print(e.path)


class Downlaod_Button(ft.CupertinoFilledButton):
    def __init__(self, id_data, opt_data, upd):
        super().__init__()

        self.upd = upd

        self.id_data = id_data
        self.opt_data = opt_data

        self.content = ft.Text("Baixar")
        self.on_click = self.download_vid

    def download_vid(self, e):
        if self.id_data.valid_id and self.id_data.txt_video_id.value and self.opt_data.opt_format.value and self.opt_data.opt_type.value and self.opt_data.file_picker.path:
            download_options = func.download_options(self.opt_data.opt_format.value, self.opt_data.opt_type.value, self.opt_data.file_picker.path)

            e.control.disabled=True
            e.control.content = ft.Text("Baixando...", color='white')
            self.upd()

            while True:
                ydl = YoutubeDL(download_options)
                ydl.download(self.id_data.txt_video_id.value)
                break

            e.control.disabled=False
            e.control.content = ft.Text("Baixar")
            self.upd()
                

class Download_Section(ft.Column):
    def __init__(self, id_section, opt_section, upd):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.id_data = id_section
        self.opt_data = opt_section

        self.download_bt = Downlaod_Button(self.id_data, self.opt_data, upd)

        self.controls = [
            ft.Row(height=20),
            self.download_bt
        ]


def main(page: ft.Page):
    page.title = 'YouTube Downloader'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.min_width = 700        
    page.window.max_width = 725        
    page.window.min_height = 500       
    page.window.max_height = 525       
    # page.window.resizable = False

    def upd():
        page.update()

    file_picker = Path_Button()
    page.overlay.append(file_picker.file_picker)
    id_section = ID_Section()
    opt_section = Options_Section(file_picker)
    download_section = Download_Section(id_section, opt_section, upd)

    page.add(
        ft.Text('YouTube Downloader', size=28),
        ft.Row(height=20),
        id_section,
        ft.Row(height=20),
        opt_section,
        download_section
    )

ft.app(main)