import threading
import logging
import random
import time


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )
M=50
N=50
def withdraw(fromAcc,fromAcc2):
    take = 0
    for i in range(M):
         r = random.random()
         fromAcc.withdraw(r)
         fromAcc2.withdraw(r)
         take -= r
    print("You withdraw %d",take)
def deposit(toAcc,toAcc2):
    get = 0
    for i in range(N):
         r = random.random()
         toAcc.deposit(r)
         toAcc2.deposit(r)
         get += r
    print("You deposit %d",get)

class bankAcc(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start  # initial account value

    def withdraw(self,value):
        self.lock.acquire()
        try:
            self.value-=value
        finally:
            self.lock.release()

    def deposit(self,value):
        self.lock.acquire();
        try:
            self.value+=value
        finally:
            self.lock.release()


if __name__ == '__main__':
    A = bankAcc(10)
    B = bankAcc(3)

    for i in range(3):
        t = threading.Thread(target=deposit, args=(A,B))
        t.start()
    for i in range(3):
        t = threading.Thread(target=withdraw, args=(A,B))
        t.start()

    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    print('A: %d B %d', A.value,B.value)
