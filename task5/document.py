from datetime import datetime


class TextDocument:

    def __init__(self, content: str = ""):
        self._content = content
        self._created_at = datetime.now()
        self._modified_at = datetime.now()

    def get_content(self) -> str:
        return self._content

    def set_content(self, content: str) -> None:
        self._content = content
        self._modified_at = datetime.now()

    def append_text(self, text: str) -> None:
        self._content += text
        self._modified_at = datetime.now()

    def get_info(self) -> dict:
        return {
            "length": len(self._content),
            "created_at": self._created_at,
            "modified_at": self._modified_at
        }

    def create_memento(self) -> 'DocumentMemento':
        return DocumentMemento(self._content, self._modified_at)

    def restore_from_memento(self, memento: 'DocumentMemento') -> None:
        self._content = memento._get_content()
        self._modified_at = memento._get_timestamp()


class DocumentMemento:

    def __init__(self, content: str, timestamp: datetime):
        self.__content = content  # Приватні атрибути для захисту стану
        self.__timestamp = timestamp

    def _get_content(self) -> str:
        return self.__content

    def _get_timestamp(self) -> datetime:
        return self.__timestamp

    def get_preview(self) -> str:
        preview = self.__content[:50]
        if len(self.__content) > 50:
            preview += "..."
        return preview

    def get_info(self) -> dict:
        return {
            "timestamp": self.__timestamp,
            "content_length": len(self.__content),
            "preview": self.get_preview()
        }