from multiprocessing import Process, RLock, synchronize, BoundedSemaphore
import time
import random


class Philosopher(Process):
    _DINING_TIME = 1, 3
    _THINKING_TIME = 2, 4
    def __init__(
            self, name: str,
            left_stick: synchronize.RLock,
            right_stick: synchronize.RLock,
            semaphore: synchronize.BoundedSemaphore
    ) -> None:
        super().__init__()
        self.name = name
        self.waiter = semaphore
        self._right_stick = right_stick
        self._left_stick = left_stick
 
    
    def print(self, message: str) -> None:
        print(f'{self.name}: {message}')

    
    def _dine(self) -> None:
        self.print('is dining')
        time.sleep(random.randint(*self._DINING_TIME))
    
    def _think(self) -> None:
        self.print('is thinking')
        time.sleep(random.randint(*self._THINKING_TIME))
        
    def run(self) -> None:
        while True:
            self.print('waiting for the WAITER')
            with self.waiter:
          
    

names = ['Kant', 'Hume', 'Descartes', 'Locke', 'Leibniz']
sticks = [RLock() for _ in range(len(names))]
philosophers = []
semaphore = BoundedSemaphore(len(names) - 1)
for i, name in enumerate(names):
    philosopher = Philosopher(name,semaphore, sticks[i-1], sticks[i])
    philosophers.append(philosopher)
    philosopher.start()