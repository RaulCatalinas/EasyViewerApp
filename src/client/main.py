"""Start the app"""

from threading import Thread

import flet as ft

from app_logic.confirm_close import ConfirmClose
from app_logic.select_directory import SelectDirectory
from app_logic.validations import Validations
from app_settings import AppSettings
from create_buttons import CreateIconButton
from create_inputs import CreateInputs
from progressbar import CreateProgressBar
from taskbar import TaskBar

validations = Validations()


class Main(AppSettings):
    def __init__(self, page: ft.Page):
        super().__init__()

        # Set the window title and resize it
        page.title = self.get_config_json("WINDOW", "TITLE")
        page.window_width = self.get_config_json("WINDOW", "WIDTH")
        page.window_height = self.get_config_json("WINDOW", "HIGH")

        # Center window
        page.window_center()

        # Center elements
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.CrossAxisAlignment.CENTER

        # Set window size
        page.window_resizable = False
        page.window_maximizable = False

        # Set user selected color theme
        page.theme_mode = page.client_storage.get("theme")

        # Window close confirmation
        page.window_prevent_close = True

        self.confirm_dialog = ConfirmClose(page)

        def __event_close_window(event):
            if event.data == "close":
                page.dialog = self.confirm_dialog
                self.confirm_dialog.open = True
                page.update()

        page.on_window_event = __event_close_window

        self.input_url = CreateInputs(
            placeholder_input=self.get_config_excel(14),
            text_size_input=20,
            keyboard_type_input=ft.KeyboardType.URL,
            text_align_input=ft.TextAlign.CENTER,
            autofocus_input=True,
        )

        self.input_directory = CreateInputs(
            placeholder_input=self.get_config_excel(15),
            text_size_input=20,
            text_align_input=ft.TextAlign.CENTER,
            read_only_input=True,
            offset_input=ft.Offset(0, 0.5),
        )

        self.button_directory = CreateIconButton(
            icon_button=ft.icons.FOLDER,
            function=lambda e: SelectDirectory(
                page=page,
                confirm_dialog=self.confirm_dialog,
                input_directory=self.input_directory,
            ),
            offset_button=ft.Offset(0, 1.5),
            scale_button=2.5,
        )

        self.button_download_video = CreateIconButton(
            icon_button=ft.icons.VIDEO_FILE,
            function=lambda e: [
                Thread(target=self.download_video, daemon=True).start()
            ],
            offset_button=ft.Offset(-0.9, 2.5),
            scale_button=2.5,
        )

        self.button_download_audio = CreateIconButton(
            icon_button=ft.icons.AUDIO_FILE,
            function=lambda e: [
                Thread(target=self.download_audio, daemon=True).start()
            ],
            offset_button=ft.Offset(1, 1.3),
            scale_button=2.5,
        )

        self.progress_bar = CreateProgressBar(
            color_progressbar=self.get_config_json("COLORS", "GREEN"),
            value_progressbar=0,
            offset_progressbar=ft.Offset(0, 23),
        )

        self.taskbar = TaskBar(
            page=page,
            input_url=self.input_url,
            input_directory=self.input_directory,
            update_dialog=self.confirm_dialog.update_dialog,
            title_dialog=self.confirm_dialog.title_dialog,
            content_dialog=self.confirm_dialog.content_dialog,
            button_exit_the_app=self.confirm_dialog.button_exit_the_app,
        )

        page.add(
            self.input_url,
            self.input_directory,
            self.button_directory,
            self.button_download_video,
            self.button_download_audio,
            self.progress_bar,
            self.taskbar,
        )

    def download_video(self):
        print("Download video")

    def download_audio(self):
        print("Download audio")


ft.app(target=Main)
