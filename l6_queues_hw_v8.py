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
        self.customer_threads = {}

    # def table_search(self):
    #     is_table = False
    #     current_table = None
    #     for table in self.tables:
    #         if not table.is_busy:
    #             is_table = True
    #             current_table = table
    #             break
    #     return is_table, current_table

    def table_search(self):
        for table in self.tables:
            if not table.is_busy:
                return True, table
        return False, None

    def customer_arrival(self):     # приход посетителя каждую секунду
        for customer in range(1, 21):
            customer = f'Посетитель номер {customer}'
            print(f'{customer} прибыл', flush=True)
            self.serve_customer(customer)
            sleep(1)

    def serve_customer(self, customer):
        is_table, current_table = self.table_search()
        if  is_table and self.queue_of_customers.qsize() == 0:
            customer_thread = Customer(customer, current_table)
            customer_thread.start()
            self.customer_threads.update({current_table.number: customer_thread})
        else:
            print(f'{customer} ожидает свободный стол. (помещение в очередь)', flush=True)
            self.queue_of_customers.put(customer)

    def table_service(self, table1):
        while True:
            sleep(1)
            start = False
            if table1.number in self.customer_threads:
                self.customer_threads[table1.number].join()
                # self.customer_threads.__delitem__(table1.number)
                start = True
            if start:
                try:
                    customer = self.queue_of_customers.get(timeout=10)
                    customer_thread = Customer(customer, table1)
                    customer_thread.start()
                    self.customer_threads.update({table1.number: customer_thread})
                    # customer_thread.join()
                except queue.Empty:
                    break
class Customer(Thread):
    def __init__(self, customer, table):
        super().__init__()
        self.customer = customer
        self.table = table

    def run(self):
        print(f'{self.customer} сел за стол {self.table.number}. (начало обслуживания)', flush=True)
        self.table.set_status(True)
        sleep(5)
        print(f'{self.customer} покушал и ушел. (конец обслуживания)', flush=True)
        self.table.set_status(False)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]
table_service_threads = []

cafe = Cafe(tables)

customer_arrival_thread = Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

for table in tables:
    table_service_thread = Thread(target=cafe.table_service, args=(table, ))
    table_service_thread.start()
    table_service_threads.append(table_service_thread)

customer_arrival_thread.join()
for table_service_thread in table_service_threads:
    table_service_thread.join()


