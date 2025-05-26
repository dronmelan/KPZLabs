from datetime import datetime


class FileLoggerAdapter:

    def __init__(self, file_writer):
        self.file_writer = file_writer

    def _get_timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def Log(self, message):
        timestamp = self._get_timestamp()
        self.file_writer.WriteLine(f"[{timestamp}] [LOG] {message}")

    def Error(self, message):
        timestamp = self._get_timestamp()
        self.file_writer.WriteLine(f"[{timestamp}] [ERROR] {message}")

    def Warn(self, message):
        timestamp = self._get_timestamp()
        self.file_writer.WriteLine(f"[{timestamp}] [WARN] {message}")