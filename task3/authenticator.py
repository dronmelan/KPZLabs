from typing import Optional
from task3.singleton_meta import SingletonMeta


class Authenticator(metaclass=SingletonMeta):


    def __init__(self):
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self._authenticated_users = set()
        self._session_tokens = {}
        print(f"Authenticator instance created with ID: {id(self)}")

    def authenticate(self, username: str, password: str) -> bool:
        if username and password and len(password) >= 6:
            self._authenticated_users.add(username)
            token = f"token_{username}_{len(self._session_tokens)}"
            self._session_tokens[username] = token
            print(f"User {username} authenticated successfully")
            return True
        print(f"Authentication failed for user {username}")
        return False

    def is_authenticated(self, username: str) -> bool:
        return username in self._authenticated_users

    def get_session_token(self, username: str) -> Optional[str]:
        return self._session_tokens.get(username)

    def logout(self, username: str) -> bool:
        if username in self._authenticated_users:
            self._authenticated_users.remove(username)
            self._session_tokens.pop(username, None)
            print(f"User {username} logged out")
            return True
        return False

    def get_instance_info(self) -> str:
        return f"Authenticator instance ID: {id(self)}, Users: {len(self._authenticated_users)}"