from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Any
from enum import Enum


class EventType(Enum):
    CLICK = "click"
    MOUSEOVER = "mouseover"
    MOUSEOUT = "mouseout"
    FOCUS = "focus"
    BLUR = "blur"
    KEYDOWN = "keydown"
    KEYUP = "keyup"
    CHANGE = "change"
    SUBMIT = "submit"
    LOAD = "load"


class Event:

    def __init__(self, event_type: EventType, target: 'EventTarget', data: Dict[str, Any] = None):
        self.type = event_type
        self.target = target
        self.data = data or {}
        self.timestamp = self._get_current_timestamp()
        self.propagation_stopped = False

    def _get_current_timestamp(self) -> int:
        import time
        return int(time.time() * 1000)

    def stop_propagation(self):
        self.propagation_stopped = True

    def __str__(self):
        return f"Event({self.type.value}, target={self.target.__class__.__name__})"


class EventListener(ABC):

    @abstractmethod
    def handle_event(self, event: Event) -> None:
        pass


class FunctionEventListener(EventListener):

    def __init__(self, callback: Callable[[Event], None]):
        self.callback = callback

    def handle_event(self, event: Event) -> None:
        self.callback(event)


class EventTarget:

    def __init__(self):
        self._event_listeners: Dict[EventType, List[EventListener]] = {}
        self._parent_target: 'EventTarget' = None

    def add_event_listener(self, event_type: EventType, listener: EventListener) -> None:
        if event_type not in self._event_listeners:
            self._event_listeners[event_type] = []
        self._event_listeners[event_type].append(listener)

    def add_event_listener_function(self, event_type: EventType, callback: Callable[[Event], None]) -> None:
        listener = FunctionEventListener(callback)
        self.add_event_listener(event_type, listener)

    def remove_event_listener(self, event_type: EventType, listener: EventListener) -> bool:
        if event_type in self._event_listeners:
            try:
                self._event_listeners[event_type].remove(listener)
                return True
            except ValueError:
                pass
        return False

    def dispatch_event(self, event: Event) -> None:
        if event.type in self._event_listeners:
            for listener in self._event_listeners[event.type]:
                try:
                    listener.handle_event(event)
                except Exception as e:
                    print(f"Error in event listener: {e}")

                if event.propagation_stopped:
                    break

        if not event.propagation_stopped and self._parent_target:
            self._parent_target.dispatch_event(event)

    def trigger_event(self, event_type: EventType, data: Dict[str, Any] = None) -> None:
        event = Event(event_type, self, data)
        self.dispatch_event(event)

    def set_parent_target(self, parent: 'EventTarget') -> None:
        self._parent_target = parent

    def get_listeners_count(self, event_type: EventType) -> int:
        return len(self._event_listeners.get(event_type, []))

    def get_all_listeners_count(self) -> int:
        return sum(len(listeners) for listeners in self._event_listeners.values())


class EventManager:

    def __init__(self):
        self._global_listeners: Dict[EventType, List[EventListener]] = {}
        self._event_log: List[Event] = []
        self._logging_enabled = False

    def add_global_listener(self, event_type: EventType, listener: EventListener) -> None:
        if event_type not in self._global_listeners:
            self._global_listeners[event_type] = []
        self._global_listeners[event_type].append(listener)

    def remove_global_listener(self, event_type: EventType, listener: EventListener) -> bool:
        if event_type in self._global_listeners:
            try:
                self._global_listeners[event_type].remove(listener)
                return True
            except ValueError:
                pass
        return False

    def process_global_event(self, event: Event) -> None:
        if self._logging_enabled:
            self._event_log.append(event)

        if event.type in self._global_listeners:
            for listener in self._global_listeners[event.type]:
                try:
                    listener.handle_event(event)
                except Exception as e:
                    print(f"Error in global event listener: {e}")

    def enable_logging(self, enabled: bool = True) -> None:
        self._logging_enabled = enabled

    def get_event_log(self) -> List[Event]:
        return self._event_log.copy()

    def clear_event_log(self) -> None:
        self._event_log.clear()


event_manager = EventManager()


class LoggingEventListener(EventListener):

    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def handle_event(self, event: Event) -> None:
        message = f"{self.prefix}[EVENT] {event.type.value} on {event.target.__class__.__name__}"
        if event.data:
            message += f" with data: {event.data}"
        print(message)


class CountingEventListener(EventListener):

    def __init__(self, name: str = "Counter"):
        self.name = name
        self.count = 0

    def handle_event(self, event: Event) -> None:
        self.count += 1
        print(f"{self.name}: Handled {event.type.value} event #{self.count}")

    def get_count(self) -> int:
        return self.count

    def reset_count(self) -> None:
        self.count = 0


class ConditionalEventListener(EventListener):

    def __init__(self, condition: Callable[[Event], bool], action: Callable[[Event], None]):
        self.condition = condition
        self.action = action

    def handle_event(self, event: Event) -> None:
        if self.condition(event):
            self.action(event)