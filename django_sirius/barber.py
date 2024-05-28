from multiprocessing import Process, Queue, Event, synchronize
import time
import random

def sleep_random_interval(interval: tuple[int|float]) -> None:
    time.sleep(random.randint(*interval))

class Client:
    def __init__(self, name: str) -> None:
        self.name = name
    
class Barber(Process):
    
    def __init__(self, queue, awake_barber: synchronize.Event) -> None:
        super().__init__()
        self.queue = queue
        self.awake = awake_barber

    def _sleep(self) -> None:
        self.awake.clear()
        print('Barber is sleeping')
        self.awake.wait()
        print('Barber woke up')

    def _cutting(self, client: Client) -> None:
        print(f'Barber is cutting {client.name}')
        sleep_random_interval((1, 3))
        print(f'Barber finished cutting {client.name}')
        sleep_random_interval((1, 3))
        print(f'Barber is done with {client.name}')


    def run(self) -> None:
        while True:
            self._sleep()
            client = self.queue.get()
            self._cutting(client)

        

class BarberShop:
    _CLIENT_INTERVAL = 1, 3
    def __init__(self, clients: list[Client], queue_size: int = 3) -> None:
        self.queue = Queue(queue_size)
        self.clients = clients
        self._awake_barber = Event()
        self.barber = Barber(self.queue, self._awake_barber)
    
    def run(self) -> None:
        for client in self.clients:
            if self.queue.full():
                print(f'{client.name} left the shop')
                continue
            if self.queue.empty() and not self._awake_barber.is_set():
                print(f'{client.name} woke up the barber')
                self._awake_barber.set()
            print(f'{client.name} is waiting')
            self.queue.put(client)

            sleep_random_interval(self._CLIENT_INTERVAL)
                

if __name__ == '__main__':
    clients = [Client(name) for name in ['Alice', 'Bob', 'Charlie', 'David', 'Eve']]
    shop = BarberShop(clients)
    shop.barber.start()
    shop.run()