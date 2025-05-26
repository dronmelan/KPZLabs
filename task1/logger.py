class Logger:

    GREEN = '\033[92m'
    RED = '\033[91m'
    ORANGE = '\033[93m'
    RESET = '\033[0m'

    def Log(self, message):
        print(f"{self.GREEN}[LOG] {message}{self.RESET}")

    def Error(self, message):
        print(f"{self.RED}[ERROR] {message}{self.RESET}")

    def Warn(self, message):
        print(f"{self.ORANGE}[WARN] {message}{self.RESET}")