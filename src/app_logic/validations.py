"""
Validating various aspects of a YouTube video download request
"""

from os import environ
from os.path import join

from pytube import YouTube
from requests import get, ConnectionError, Timeout

from client.app_settings import AppSettings
from client.logging_management import LoggingManagement


class Validations(LoggingManagement, AppSettings):
    """
    Validating various aspects of a YouTube video download request
    """

    def __init__(self):
        LoggingManagement.__init__(self)
        AppSettings.__init__(self)

    def check_if_a_url_has_been_entered(self, url: str) -> bool:
        """
        Checks if a URL has been entered.

        :param url: a string representing a URL that needs to be checked if it has been entered or not

        :type url: str

        :return: A boolean value indicating whether a URL has been entered or not.
        """

        if not url:
            self.write_error("No URL entered")
            raise ValueError(self.get_config_excel(9))

        self.write_log("A URL has been entered")
        return True

    def check_if_is_url_youtube(self, url: str) -> bool:
        """
        This function checks if a given URL is from YouTube.

        :param url: A string representing a URL that needs to be checked if it is from YouTube or not

        :type url: str

        :return: If the URL is from YouTube, the function returns True. If the URL is not from YouTube, the function raises a ValueError.
        """

        if "https://www.youtube.com" in url or "https://youtu.be/" in url:
            self.write_log("The URL is from YouTube")
            return True

        self.write_error("The URL is not from YouTube")
        raise ValueError(self.get_config_excel(11))

    def check_if_directory_is_selected(
        self,
        input_directory: str,
        page: object,
        video_location: str,
        set_control_variable_in_ini,
    ) -> bool:
        """
        Checks if a directory is selected

        :param input_directory: a string representing the path of the selected directory

        :param page: Is a reference to the app window

        :param set_control_variable_in_ini: A function that sets a value for a specific key in an INI configuration file

        :param video_location: A string representing the directory where the video will be saved. If no directory has been selected, it will be set to "None"

        :type input_directory: str

        :type page: object

        :type video_location: str

        :return: A boolean value.
        """

        if not video_location or video_location == "None":
            DEFAULT_DIRECTORY = join(join(environ["USERPROFILE"]), "Desktop")
            input_directory.set_value(DEFAULT_DIRECTORY)
            set_control_variable_in_ini("VIDEO_LOCATION", DEFAULT_DIRECTORY)

            self.write_log("Default directory set")
            page.update(input_directory)

        else:
            self.write_log("A directory has been selected to save the video")

        return True

    def check_internet_connection(self) -> bool:
        """
        Checks if there is an internet connection by attempting to connect to Google.

        :return: A boolean value indicating whether an internet connection is available or not.
        """

        try:
            get("https://www.google.com", timeout=5)
        except (ConnectionError, Timeout) as exc:
            self.write_error("No internet connection")
            raise ConnectionError(self.get_config_excel(10)) from exc

        self.write_log("Internet connection is available")
        return True

    def check_if_the_video_is_available(self, url: str) -> bool:
        """
        This function checks if a YouTube video is available by attempting to access its URL.

        :param url: A string representing the URL of a YouTube video

        :type url: str

        :return: A boolean value indicating whether the video is available or not.
        """

        try:
            YouTube(url).check_availability()
            self.write_log("The video is available")
            return True

        except Exception as exception:
            self.write_error(exception)
            raise ValueError(exception) from exception
