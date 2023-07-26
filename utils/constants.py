"""
Constants needed for the application
"""

from platform import system

from osutils import GetPaths

ROOT_PATH = GetPaths.get_project_root_path()

USER_HOME = GetPaths.get_user_home_path()

DESKTOP_PATH = USER_HOME.joinpath("Desktop")

CONFIG_FILES = {
    "INI": ROOT_PATH.joinpath("settings/control_variables.ini"),
    "JSON": ROOT_PATH.joinpath("settings/settings.json"),
    "EXCEL": ROOT_PATH.joinpath("settings/languages.xlsx"),
    "ENV": ROOT_PATH.joinpath("settings/.env"),
}

ICONS = {
    "Windows": ROOT_PATH.joinpath("icon/icon-Windows.ico"),
    "Darwin": ROOT_PATH.joinpath("icon/icon-macOS.icns"),
    "Linux": ROOT_PATH.joinpath("icon/icon-Linux.png"),
}

INVALID_CHARS = {"Windows": r'[<>:/\\"|?*]', "Darwin": r"[:/]", "Linux": r"[/]"}

SYSTEM_NAME = system()

ENABLED_TYPE_CHECKING = True

CACHE_FILE = "./src/backend/cache/github_cache.json"
