"""Start the app"""

from threading import Thread

from flet import (
    Page,
    icons,
    CrossAxisAlignment,
    KeyboardType,
    TextAlign,
    Offset,
    app,
    MainAxisAlignment,
)

from app_logic.confirm_close import ConfirmClose
from app_logic.control_variables import ControlVariables
from app_logic.download import Download
from app_logic.select_directory import SelectDirectory
from app_logic.validations import Validations
from app_settings import AppSettings
from create_buttons import CreateIconButton, CreateElevatedButton
from create_dialog import CreateDialog
from create_inputs import CreateInputs
from progressbar import CreateProgressBar
from taskbar import TaskBar


class Main(AppSettings, Validations, ControlVariables):
    def __init__(self, page: Page):
        AppSettings.__init__(self)
        Validations.__init__(self)
        ControlVariables.__init__(self)

        self.set_environment_variable(page)

        self.confirm_dialog = ConfirmClose(page)

        VIDEO_LOCATION = self.get_control_variables("VIDEO_LOCATION")

        # Set the window title and resize it
        page.title = self.get_config_json("WINDOW", "TITLE")
        page.window_width = self.get_config_json("WINDOW", "WIDTH")
        page.window_height = self.get_config_json("WINDOW", "HIGH")

        # Center window
        page.window_center()

        # Center elements
        page.horizontal_alignment = CrossAxisAlignment.CENTER
        page.vertical_alignment = CrossAxisAlignment.CENTER

        # Set window size
        page.window_resizable = False
        page.window_maximizable = False

        # Set user selected color theme
        page.theme_mode = page.client_storage.get("theme")

        # Window close confirmation
        page.window_prevent_close = True

        def __event_close_window(event):
            if event.data == "close":
                self.__overlay(page)
                page.dialog = self.confirm_dialog

                if self.error_dialog.open:
                    self.error_dialog.change_state(page)

                self.confirm_dialog.change_state_close_dialog(page)

        page.on_window_event = __event_close_window

        # Error dialog
        self.button_close_dialog = CreateElevatedButton(
            text_button="Ok", function=lambda e: None
        )

        self.error_dialog = CreateDialog(
            icon=True,
            title_dialog=icons.ERROR,
            title_size=1.3,
            content_dialog="",
            content_size=23,
            actions_dialog=[self.button_close_dialog],
            actions_alignment_dialog=MainAxisAlignment.END,
        )

        self.input_url = CreateInputs(
            placeholder_input=self.get_config_excel(14),
            text_size_input=20,
            keyboard_type_input=KeyboardType.URL,
            text_align_input=TextAlign.CENTER,
            autofocus_input=True,
        )

        self.input_directory = CreateInputs(
            placeholder_input=self.get_config_excel(15),
            text_size_input=20,
            text_align_input=TextAlign.CENTER,
            read_only_input=True,
            offset_input=Offset(0, 0.5),
            value_input=VIDEO_LOCATION or None,
        )

        self.select_directory = SelectDirectory(
            page=page,
            input_directory=self.input_directory,
            set_control_variable_in_ini=self.set_control_variable_in_ini,
        )

        self.button_directory = CreateIconButton(
            icon_button=icons.FOLDER,
            function=lambda e: self.select_directory.select_directory(),
            offset_button=Offset(0, 1.5),
            scale_button=2.5,
        )

        self.button_download_video = CreateIconButton(
            icon_button=icons.VIDEO_FILE,
            function=lambda e: [
                Thread(target=self.__download, args=[page, True], daemon=True).start()
            ],
            offset_button=Offset(-0.9, 2.5),
            scale_button=2.5,
        )

        self.button_download_audio = CreateIconButton(
            icon_button=icons.AUDIO_FILE,
            function=lambda e: [
                Thread(target=self.__download, args=[page, False], daemon=True).start()
            ],
            offset_button=Offset(1, 1.3),
            scale_button=2.5,
        )

        self.progress_bar = CreateProgressBar(
            color_progressbar=self.get_config_json("COLORS", "GREEN"),
            value_progressbar=0,
            offset_progressbar=Offset(0, 23),
        )

        self.taskbar = TaskBar(
            page=page,
            input_url=self.input_url,
            input_directory=self.input_directory,
            close_dialog=self.confirm_dialog,
            button_exit_the_app=self.confirm_dialog.button_exit_the_app,
        )

        Thread(target=self.__add, args=[page], daemon=False).start()
        Thread(target=self.__overlay, args=[page], daemon=False).start()

    def __download(self, page, download_video):
        """
        Download the video if the parameter "download video" is true, otherwise it'll download the audio of the video
        """

        self.set_control_variable_in_ini("URL_VIDEO", self.input_url.value)

        URL = self.get_control_variables("URL_VIDEO")
        VIDEO_LOCATION = self.get_control_variables("VIDEO_LOCATION")

        try:
            if (
                self.check_if_a_url_has_been_entered(URL)
                and self.check_if_is_url_youtube(URL)
                and self.check_if_directory_is_selected(
                    input_directory=self.input_directory,
                    page=page,
                    video_location=VIDEO_LOCATION,
                    set_control_variable_in_ini=self.set_control_variable_in_ini,
                )
                and self.check_internet_connection()
                and self.check_if_the_video_is_available(URL)
            ):
                Download(
                    button_select_location=self.button_directory,
                    button_download_video=self.button_download_video,
                    button_download_audio=self.button_download_audio,
                    input_url=self.input_url,
                    download_video=download_video,
                    page=page,
                )

        except Exception as exception:
            self.__show_dialog_error(error=exception, page=page)

    def __show_dialog_error(self, error, page):
        """Displays a dialog with the error occurred"""

        self.button_close_dialog.on_click = lambda e: self.error_dialog.change_state(
            page
        )
        self.error_dialog.content_text.change_text(error)

        self.__overlay(page)
        page.dialog = self.error_dialog

        self.error_dialog.change_state(page)

    def __add(self, page):
        ITEMS_TO_ADD_TO_THE_PAGE = [
            self.input_url,
            self.input_directory,
            self.button_directory,
            self.button_download_video,
            self.button_download_audio,
            self.progress_bar,
            self.taskbar,
            self.select_directory,
        ]

        for item in ITEMS_TO_ADD_TO_THE_PAGE:
            page.add(item)

    def __overlay(self, page):
        TO_ADD_TO_THE_OVERLAY_OF_THE_PAGE = [
            self.confirm_dialog,
            self.error_dialog,
        ]

        for i in TO_ADD_TO_THE_OVERLAY_OF_THE_PAGE:
            page.overlay.append(i)


if __name__ == "__main__":
    app(target=Main)
