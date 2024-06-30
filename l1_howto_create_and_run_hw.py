# Модуль №10. Мультипоточность. Домашнее задание по теме "Создание потоков".

from time import sleep
from threading import Thread

def print_char():
    string_1 = 'abcdefghij'
    for i in string_1:
        print(i)
        sleep(1)

def print_num():
    for i in range(1, 11):
        print(i)
        sleep(1)

thread_1 = Thread(target=print_char)
thread_2 = Thread(target=print_num)

thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()
