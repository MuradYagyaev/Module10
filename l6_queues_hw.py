# Модуль №10. Мультипоточность. Часть 2. Домашнее задание по теме "Очереди для обмена данными между потоками."

from threading import Thread
import queue
from time import sleep


class Table:
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.is_busy = False

    def set_status(self, status):
        self.is_busy = status


class Cafe:
    num_of_customer = 0

    def __init__(self, tables):
        self.queue1 = queue.Queue()
        self.tables = tables
        self.is_table = False

    def customer_arrival(self):     # приход посетителя каждую секунду
        while True:
            Cafe.num_of_customer += 1
            print(f'Посетитель номер {Cafe.num_of_customer} прибыл')
            self.serve_customer(Cafe.num_of_customer)
            sleep(1)

    def serve_customer(self, customer):
        self.is_table = False
        for table in self.tables:
            if not table.is_busy:
                self.is_table = True
                self.current_table = table
                break
        if self.is_table:
            if self.queue1.qsize() == 0:
                customer_thread = Customer(customer, self.current_table)
                customer_thread.start()
            else:
                print(f'Посетитель номер {customer} ожидает свободный стол. (помещение в очередь)')
                self.queue1.put(customer)
                num_of_customer = self.queue1.get()
                customer_thread = Customer(num_of_customer, self.current_table)
                customer_thread.start()
        else:
            print(f'Посетитель номер {customer} ожидает свободный стол. (помещение в очередь)')
            self.queue1.put(customer)


class Customer(Thread):
    def __init__(self, number, table):
        super().__init__()
        self.number = number
        self.table = table

    def run(self):
        print(f'Посетитель номер {self.number} сел за стол {self.table.number}. (начало обслуживания)')
        self.table.set_status(True)
        sleep(5)
        print(f'Посетитель номер {self.number} покушал и ушел. (конец обслуживания)')
        self.table.set_status(False)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Cafe(tables)

customer_arrival_thread = Thread(target=cafe.customer_arrival)

customer_arrival_thread.start()

customer_arrival_thread.join()
