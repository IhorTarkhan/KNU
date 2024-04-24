import threading
import time

_time_delay = 0.5

common = [0]  # to pass as a reference

tickets = {
    1: {'price': 28, 'name': 'Kyiv'},
    2: {'price': 37, 'name': 'Istanbul'},
    3: {'price': 50, 'name': 'London'},
    4: {'price': 77, 'name': 'Berlin'},
    5: {'price': 91, 'name': 'Paris'}
}

money = {
    1: 50,
    2: 25,
    5: 20,
    10: 15,
    25: 10,
    50: 5
}


def ts(_local, _common):
    if _common[0] == 0:
        _common[0] = 1
        _local[0] = 0
    else:
        time.sleep(_time_delay)


class ProcesB(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, target=self._target)
        self._stop_event = threading.Event()
        self._param = None
        self._local = [0]  # to pass as a reference

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
        self._local[0] = 1
        while self._local[0] == 1:
            ts(self._local, common)

        temp_money = money.copy()
        amount = self._param

        for par in sorted(temp_money.keys(), reverse=True):
            while amount >= par and temp_money[par] > 0:
                amount -= par
                temp_money[par] -= 1

        if amount == 0:
            money.update(temp_money)
            print("Proces B: success to give the rest, money:", money)
        else:
            print("Proces B: impossible to give the rest money:", money)

        common[0] = 0


class ProcesA(threading.Thread):
    def __init__(self):
        super().__init__(target=self._target)
        self._stop_event = threading.Event()
        self.proces_b = ProcesB()
        self._local = [0]  # to pass as a reference

    def _target(self):
        while not self._stop_event.is_set():
            command = input('Proces A: command ')

            if not command.isnumeric():
                self._stop_event.set()
                continue

            self.execute(int(command))

        self.proces_b.stop()

    def execute(self, command):
        self._local[0] = 1
        while self._local[0] == 1:
            ts(self._local, common)

        if command == 0:
            print('Proces A: Turning on Proces B')
            self.proces_b.start()
            common[0] = 0
            print()
            return

        ticket = tickets[command]
        rest = 100 - ticket['price']
        print('Proces A: Ticket to', ticket['name'], 'for', ticket['price'], 'копійок, Rest:', rest, 'копійок')

        common[0] = 0
        self.proces_b.trigger(rest)
        print()


def main():
    ProcesA().start()


if __name__ == '__main__':
    main()
