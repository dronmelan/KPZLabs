import threading


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # Перша перевірка без блокування для оптимізації
        if cls not in cls._instances:
            with cls._lock:
                # Друга перевірка з блокуванням
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]