# Модуль №10. Мультипоточность. Домашнее задание по теме "Потоки на классах".

from threading import Thread

class Knight(Thread):

    def __init__(self, name, skill):
        super().__init__()
        self.name = name
        self.skill = skill
        self.enemies = 100

    def run(self):
        day = 0
        print(f'{self.name}, на нас напали!')
        while self.enemies > 0:
            day += 1
            if self.enemies >= self.skill:
                self.enemies -= self.skill
            elif self.enemies < self.skill:
                self.enemies -= self.enemies
            print(f'{self.name}, сражается {day} день(дня), осталось {self.enemies} воинов.')
        print(f'{self.name} одержал победу спустя {day} дней!')


knight1 = Knight('Sir Lancelot', 10)
knight2 = Knight('Sir Galahad', 20)

knight1.start()
knight2.start()
knight1.join()
knight2.join()
print(f'Все битвы закончились!')
