# -*- coding: utf-8 -*-


import random
import threading


class ATM:
    def __init__(self, start_cash, client_first_balance):
        self.account_balance = random.randint(1000, 10000)  # Баланс рахунку
        self.bills = start_cash  # Доступні купюри
        self.client_initial_balance = client_first_balance  # Баланс першого клієнта
        self.flag = [False, False]  # Прапорці для алгоритму Деккера
        self.turn = 0  # Черга для алгоритму Деккера

    def check_sufficient_funds(self, amount):
        total_cash = sum(bill * quantity for bill, quantity in self.bills.items())
        # print(f"Перевірка: {amount} <= {total_cash}")
        return amount <= total_cash

    def check_client_funds(self, amount):
        return amount <= self.client_initial_balance

    def new_check_client_funds(self):
        self.client_initial_balance = random.randint(200, 1000)
        print(f"Рахунок нового клієнта {self.client_initial_balance} грн.")

    def client_funds(self):
        print(f"Рахунок клієнта після зняття коштів: {self.client_initial_balance} грн.")

    def withdraw(self, amount):
        if not self.check_sufficient_funds(amount):
            print("Недостатньо коштів для видачі.")
            return False
        if not self.check_client_funds(amount):
            print("Недостатньо коштів у клієнта.")
            return False
        self.client_initial_balance -= amount
        denominations = [100, 50, 20, 10, 5, 2, 1]
        to_dispense = {}
        for bill in denominations:
            if amount >= bill:
                count = min(self.bills[bill], amount // bill)
                amount -= count * bill
                to_dispense[bill] = count
                self.bills[bill] -= count
            if amount == 0:
                break

        if amount == 0:
            print(f"Готується до видачі: {to_dispense}")
            return True
        else:
            print("Неможливо видати точну запитану суму.")
            return False

    def total_cash_available(self):
        total_cash = sum(bill * quantity for bill, quantity in self.bills.items())
        print(f"Загальна сума готівки в банкоматі: {total_cash} грн.")
        self.account_balance = total_cash
        return total_cash


def process_A(atm, request_amount):
    atm.flag[0] = True
    atm.turn = 1
    while atm.flag[1] and atm.turn == 1:
        pass

    if atm.check_sufficient_funds(request_amount) and atm.check_client_funds(request_amount):
        print(f"Процес А: Запит на видачу {request_amount} грн успішний.")
        success = True
    else:
        print(f"Процес А: Неможливо видати {request_amount} грн.")
        success = False

    atm.flag[0] = False
    return success


def process_B(atm, request_amount):
    atm.flag[1] = True
    atm.turn = 0
    while atm.flag[0] and atm.turn == 0:
        pass

    if atm.check_sufficient_funds(request_amount):
        success = atm.withdraw(request_amount)
        print(f"Процес B: Видача успішна {request_amount} грн.")
    else:
        print(f"Процес B: Недостатньо коштів для видачі {request_amount} грн.")
        success = False

    atm.flag[1] = False
    return success


def main():
    start_cash = {
        1: 20,
        2: 20,
        5: 15,
        10: 15,
        20: 15,
        50: 10,
        100: 10
    }
    print(f"Початковий кеш: {start_cash}")
    client_first_balance = random.randint(200, 1000)
    atm = ATM(start_cash, client_first_balance)

    while atm.total_cash_available() > 0:
        request_amount = random.randint(100, 900)
        print(f"Запит на суму: {request_amount} грн.")
        atm.new_check_client_funds()

        t1 = threading.Thread(target=process_A, args=(atm, request_amount))
        t2 = threading.Thread(target=process_B, args=(atm, request_amount))

        t1.start()

        if not atm.check_sufficient_funds(request_amount) or not atm.check_client_funds(request_amount):
            print("\nБанкомат не може продовжувати виплати.")
            break

        t2.start()

        t1.join()
        t2.join()

        atm.client_funds()


if __name__ == "__main__":
    main()
