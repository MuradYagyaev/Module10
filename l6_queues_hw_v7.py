# Модуль №10. Мультипоточность. Часть 2. Домашнее задание по теме "Очереди для обмена данными между потоками."

from threading import Thread, Lock
import queue
from time import sleep


class Table:
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.is_busy = False
        # self.lock = Lock()

    def set_status(self, status):
        self.is_busy = status


class Cafe:

    def __init__(self, tables):
        self.queue_of_customers = queue.Queue()
        self.tables = tables
        self.serve_customer_threads = []

    def customer_arrival(self):     # приход посетителя каждую секунду
        for customer in range(1, 21):
            customer = f'Посетитель номер {customer}'
            print(f'{customer} прибыл')
            self.serve_customer(customer)
            sleep(1)

    def serve_customer(self, customer):
        is_table = False
        current_table = None
        for table in self.tables:
            if not table.is_busy:
                is_table = True
                current_table = table
                break
        if is_table and self.queue_of_customers.qsize() == 0:
            customer_thread = Customer(customer, current_table)
            customer_thread.start()
            # customer_thread.join()
            return
        else:
            print(f'{customer} ожидает свободный стол. (помещение в очередь)')
            self.queue_of_customers.put(customer)
        while True:
            is_table = False
            for table in self.tables:
                if not table.is_busy:
                    is_table = True
                    current_table = table
                    break
            if is_table:
                customer2 = self.queue_of_customers.get()
                customer_thread = Customer(customer2, current_table)
                customer_thread.start()
                break
            sleep(1)


class Customer(Thread):
    def __init__(self, customer, table):
        super().__init__()
        self.customer = customer
        self.table = table

    def run(self):
        print(f'{self.customer} сел за стол {self.table.number}. (начало обслуживания)')
        self.table.set_status(True)
        sleep(5)
        print(f'{self.customer} покушал и ушел. (конец обслуживания)')
        self.table.set_status(False)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Cafe(tables)
# lock_1 = Lock()

customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()
customer_arrival_thread.join()
