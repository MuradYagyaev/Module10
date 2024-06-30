# Модуль №10. Мультипоточность. Домашнее задание по теме "Блокировки потоков для доступа к общим данным"

from threading import Thread, Lock

class BankAccount:

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        lock_1.acquire()
        self.balance += amount
        print(f'Deposited {amount}, new balance is {self.balance}')
        lock_1.release()

    def withdraw(self, amount):
        lock_1.acquire()
        self.balance -= amount
        print(f'Withdraw {amount}, new balance is {self.balance}')
        lock_1.release()


def deposit_task(account, amount):
    for _ in range(10):
        account.deposit(amount)

def withdraw_task(account, amount):
    for _ in range(10):
        account.withdraw(amount)

account_1 = BankAccount(1000)

lock_1 = Lock()

deposit_thread = Thread(target=deposit_task, args=(account_1, 100))
withdraw_thread = Thread(target=withdraw_task, args=(account_1, 150))

deposit_thread.start()
withdraw_thread.start()

deposit_thread.join()
withdraw_thread.join()
