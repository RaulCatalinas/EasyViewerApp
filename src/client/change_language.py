"""Control the logic to be able to change the language of the app"""

from flet import Dropdown, dropdown, alignment, Offset

from app_settings import AppSettings


class ChangeLanguage(Dropdown, AppSettings):
    """Allows the user to change the language of the app"""

    def __init__(
        self,
        appbar,
        page,
        input_url,
        input_directory,
        close_dialog,
        dropdown_contact,
        spanish_flag,
        english_flag,
        icon_language,
        icon_theme,
    ):
        self.appbar = appbar
        self.page = page
        self.input_url = input_url
        self.input_directory = input_directory
        self.close_dialog = close_dialog
        self.dropdown_contact = dropdown_contact
        self.spanish_flag = spanish_flag
        self.english_flag = english_flag
        self.icon_language = icon_language
        self.icon_theme = icon_theme

        AppSettings.__init__(self)

    def _build(self):
        return Dropdown.__init__(
            self,
            options=[
                dropdown.Option(self.get_config_excel(7)),
                dropdown.Option(self.get_config_excel(8)),
            ],
            value=self.get_language(),
            visible=False,
            alignment=alignment.center,
            on_change=lambda e: self.__change_language(),
        )

    def change_visibility_dropdown_language(self):
        """Show or hide the dropdown if it is hidden or not respectively"""

        if not self.visible:
            self.visible = True
            self.appbar.toolbar_height = 114
            self.spanish_flag.offset = Offset(0, -0.85)
            self.english_flag.offset = Offset(0, -0.85)
            self.icon_language.offset = Offset(6.50, 0.3)
            self.icon_theme.offset = Offset(0, -0.65)

            return self.page.update(self, self.appbar)

        self.visible = False
        self.icon_language.offset = Offset(0, 0.3)

        if not self.dropdown_contact.visible:
            self.appbar.toolbar_height = 63
            self.icon_theme.offset = Offset(0, 0)
            self.spanish_flag.offset = Offset(0, 0)
            self.english_flag.offset = Offset(0, 0)

        return self.page.update(self, self.appbar)

    def __change_language(self):
        """Change the language of the app, update the texts of the app and update the environment variable to the chosen language"""

        if self.value in ["Spanish", "Español"]:
            self.set_language("Español")
            self.appbar.title = self.spanish_flag

        else:
            self.set_language("English")
            self.appbar.title = self.english_flag

        self.visible = False

        self.options = [
            dropdown.Option(self.get_config_excel(7)),
            dropdown.Option(self.get_config_excel(8)),
        ]
        self.value = self.get_language()

        self.input_url.change_placeholder(self.get_config_excel(14))
        self.input_directory.change_placeholder(self.get_config_excel(15))
        self.close_dialog.update_text(
            text_title=self.get_config_excel(12), text_content=self.get_config_excel(3)
        )
        self.dropdown_contact.hint_text = self.get_config_excel(16)

        self.icon_language.offset = Offset(0, 0.3)

        if not self.dropdown_contact.visible:
            self.appbar.toolbar_height = 63
            self.icon_theme.offset = Offset(0, 0)
            self.spanish_flag.offset = Offset(0, 0)
            self.english_flag.offset = Offset(0, 0)

        return self.page.update(
            self.appbar,
            self.input_url,
            self.input_directory,
            self,
            self.dropdown_contact,
        )
