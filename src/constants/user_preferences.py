# Standard library
from typing import Any

# App enums
from app_enums import UserPreferencesKeys

USER_PREFERENCES_FILE = "user_preferences"

DEFAULT_USER_PREFERENCES: dict[UserPreferencesKeys, Any] = {
    UserPreferencesKeys.THEME: "light",
    UserPreferencesKeys.AUTOMATIC_NOTIFICATIONS: True,
    UserPreferencesKeys.LANGUAGE: "en",
    UserPreferencesKeys.LATEST_GITHUB_VERSION: "0.0.0",
    UserPreferencesKeys.DISCLAIMER_SHOWN: False,
    UserPreferencesKeys.LAST_UPDATE_CHECK: "1970-01-01",
}
