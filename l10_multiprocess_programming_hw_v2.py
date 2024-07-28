# Модуль №10. Мультипоточность. Часть 2. Домашнее задание по теме "Многопроцессное программирование".
import multiprocessing as mp
from time import sleep


class WarehouseManager:     # Вариант 2
    def __init__(self):
        self.data = {}

    def process_request(self, request, dict0):
        if request[1] == 'receipt':
            if request[0] in dict0:
                dict0[request[0]] += request[2]
            else:
                dict0.update({request[0]: request[2]})
        elif request[1] == 'shipment':
            if request[0] in dict0:
                if dict0[request[0]] > request[2]:
                    dict0[request[0]] -= request[2]
                elif dict0[request[0]] > 0 and dict0[request[0]] < request[2]:
                    dict0[request[0]] -= dict0[request[0]]
            else:
                print('Нет такого товара на складе')

    def run(self, requests):
        mgr = mp.Manager()
        dict1 = mgr.dict()
        for request in requests:
            request_process = mp.Process(target=self.process_request, args=(request, dict1))
            request_process.start()
            request_process.join()
            sleep(1)
        self.data = dict1


if __name__ == '__main__':
    manager = WarehouseManager()
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]
    manager.run(requests)
    print(manager.data)

    # Вывод на консоль
    # {"product1": 70, "product2": 100, "product3": 200}