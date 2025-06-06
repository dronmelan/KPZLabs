from typing import List, Optional

from task5.document import TextDocument, DocumentMemento


class TextEditor:

    def __init__(self):
        self._document = TextDocument()
        self._history: List[DocumentMemento] = []
        self._current_position = -1
        self._max_history_size = 50

    def get_content(self) -> str:
        return self._document.get_content()

    def write_text(self, text: str) -> None:
        self._save_current_state()
        self._document.set_content(text)

    def append_text(self, text: str) -> None:
        self._save_current_state()
        self._document.append_text(text)

    def _save_current_state(self) -> None:
        if self._current_position < len(self._history) - 1:
            self._history = self._history[:self._current_position + 1]

        memento = self._document.create_memento()
        self._history.append(memento)
        self._current_position += 1

        if len(self._history) > self._max_history_size:
            self._history.pop(0)
            self._current_position -= 1

    def undo(self) -> bool:
        if self._current_position > 0:
            self._current_position -= 1
            memento = self._history[self._current_position]
            self._document.restore_from_memento(memento)
            return True
        return False

    def redo(self) -> bool:
        if self._current_position < len(self._history) - 1:
            self._current_position += 1
            memento = self._history[self._current_position]
            self._document.restore_from_memento(memento)
            return True
        return False

    def can_undo(self) -> bool:
        return self._current_position > 0

    def can_redo(self) -> bool:
        return self._current_position < len(self._history) - 1

    def get_history_info(self) -> List[dict]:
        return [memento.get_info() for memento in self._history]

    def get_document_info(self) -> dict:
        return self._document.get_info()