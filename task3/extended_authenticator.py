from task3.authenticator import Authenticator
import time

class ExtendedAuthenticator(Authenticator):

    def __init__(self):
        super().__init__()
        print(f"ExtendedAuthenticator instance created with ID: {id(self)}")

    def extended_method(self):
        return "This is extended functionality"


def test_singleton_in_thread(thread_id: int, results: list):
    print(f"Thread {thread_id} starting...")

    time.sleep(0.1)

    auth = Authenticator()
    results.append((thread_id, id(auth)))

    auth.authenticate(f"user_{thread_id}", "password123")

    print(f"Thread {thread_id} finished with instance ID: {id(auth)}")