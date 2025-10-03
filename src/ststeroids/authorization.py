import os
from typing import Callable, Union, Iterable, Optional
import requests


class Authorization:
    def __init__(self, feature_provider: Optional[Callable[[str], bool]] = None, user_provider: Optional[Callable[[], str]] = None):
        """
        feature_provider: A callable that takes a feature name and returns True/False
        user_profider: A callable that returns the currently active user identifier, this can be a username, email enz. Optionaly combined with a list of groups they belong to
        """
        self.feature_provider = feature_provider
        # Default: local provider
        if feature_provider is None:
            if user_provider is None:
                raise ValueError("You must provide either a feature_provider or a user_provider")
            feature_provider = LocalFeatureProvider(user_provider)
        self.feature_provider = feature_provider

    def allow_deny(self, feature: str) -> bool:
        return self.feature_provider(feature)

class LocalFeatureProvider:
    def __init__(self, user_provider: Callable[[], Union[str, Iterable[str]]]):
        """
        Initialize the Authorization instance.

        :param user_provider: Function returning current user as string or list of feature names
        """
        if not callable(user_provider):
            raise ValueError("user_provider must be callable")
        self._get_current_user = user_provider

    def __call__(self, feature_name: str) -> bool:
        """
        Check if the current user or any of their groups have persmission for the given feature.
        Environment variables can contain usernames or other group names.
        """
        current_users = self._get_current_user()
        if isinstance(current_users, str):
            current_users = [current_users]
        current_users = [u.lower() for u in current_users]

        feature_upper = feature_name.upper()
        allow_env = os.getenv(f"{feature_upper}_ALLOW", "")
        deny_env = os.getenv(f"{feature_upper}_DENY", "")
        flex_auth = os.getenv("STS_FLEX_AUTH", "").strip().lower() in ("1", "true", "yes")


        if not allow_env.strip() and not deny_env.strip() and flex_auth:
            return True

        allow_items = [u.strip().lower() for u in allow_env.split(",") if u.strip()]
        deny_items = [u.strip().lower() for u in deny_env.split(",") if u.strip()]

        # First check deny: if any current_user is in deny_items → deny
        if any(user in deny_items for user in current_users):
            return False

        # Check allow: if any current_user is in allow_items → allow
        if any(user in allow_items for user in current_users):
            return True

        # Default deny if nothing matches
        return False