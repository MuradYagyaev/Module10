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

    def __init__(self, tables):
        self.queue_of_customers = queue.Queue()
        self.tables = tables
        self.serve_customer_threads = []
        self.customer_threads = []

    def is_table(self):
        for table in self.tables:
            if not table.is_busy:
                return table

    def customer_arrival(self):     # приход посетителя каждую секунду
        for customer in range(1, 21):
            customer = f'Посетитель номер {customer}'
            print(f'{customer} прибыл')
            # self.serve_customer(customer)
            serve_customer_thread = Thread(target=self.serve_customer, args=(customer, ))
            serve_customer_thread.start()
            self.serve_customer_threads.append(serve_customer_thread)
            # serve_customer_thread.join()
            sleep(1)
        for thread in self.serve_customer_threads:
            thread.join()

    def serve_customer(self, customer):
        # is_table = False
        # for table in self.tables:
        #     if not table.is_busy:
        #         is_table = True
        #         current_table = table
        #         break
        current_table = self.is_table()
        if current_table and self.queue_of_customers.qsize() == 0:
            customer_thread = Customer(customer, current_table)
            customer_thread.start()
            customer_thread.join()
            return
        else:
            print(f'{customer} ожидает свободный стол. (помещение в очередь)')
            self.queue_of_customers.put(customer)
        while True:
            current_table = self.is_table()
            if current_table:
                # customer2 = self.queue_of_customers.get()
                customer_thread = Customer(customer, current_table)
                customer_thread.start()
                break



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

customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()
customer_arrival_thread.join()
