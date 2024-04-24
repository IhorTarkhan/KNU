import threading
import time

_time_delay = 0.2


class ProcesB(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, target=self._target)
        self._stop_event = threading.Event()
        self._param = None
        self.local = [0]

    def _target(self):
        while not self._stop_event.is_set():
            if self._param is not None:
                self.execute()
                self._param = None
            time.sleep(_time_delay)

    def trigger(self, value):
        self._param = value
        time.sleep(_time_delay)

    def stop(self):
        self._stop_event.set()

    def execute(self):
        print("Proces B: command", self._param)


class ProcesA(threading.Thread):
    def __init__(self):
        super().__init__(target=self._target)
        self._stop_event = threading.Event()
        self.proces_b = ProcesB()

    def _target(self):
        self.proces_b.start()
        while not self._stop_event.is_set():
            command = input("Proces A: command ")

            if not command.isnumeric():
                self._stop_event.set()
                continue

            self.execute(int(command))

        self.proces_b.stop()

    def execute(self, command):
        self.proces_b.trigger(command)


def main():
    ProcesA().start()


if __name__ == "__main__":
    main()
