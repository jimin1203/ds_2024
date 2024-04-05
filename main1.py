from listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, items, customer_list):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.customer_list = customer_list
        self.worker = threading.Thread(target=self.run)
        
    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item
        else:
            return None

    def run(self):  
        while True:
            time.sleep(0.2)
            if self.__alive:
                item = self.get_item()
                if item != None :
                    self.customer_list.enqueue(item)
                    print("Arrived:", item)
                else:
                    break   
            else:
                break
        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()
    
    
class Consumer: # 멀티스레딩 환경에서 독립적임.
    def __init__(self,customer_list):
        self.__alive = True # 스레드가 작동 중임
        self.customer_list = customer_list
        self.worker = threading.Thread(target=self.run)  # 스레드가 실행할 함수:self.run 

    def run(self): # 스레드에 의해 별도의 실행 흐름에서 호출
        while True:
            time.sleep(1)
            if not self.customer_list.isEmpty():
                result = customer_list.dequeue()
                print("Boarding:", result)
            else:
                if not self.__alive:
                    break
        print("Consumer is dying...")

    def start(self):
        self.worker.start() # 스레드 실행

    def finish(self):
        self.__alive = False # run의 무한루프 종료시킴
        self.worker.join()

if __name__ == "__main__":
    
    customers = []
    with open("producer_consumer/customer.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            customer = line.split() # customer[0]:등급 customer[1]:이름
            customers.append(customer)

    # FIFO
    names = []
    customer_list=ListQueue()
    for c in customers:
        names.append(c[1])
    
    producer = Producer(names,customer_list)

    # Priority 
    consumer = Consumer(customer_list)    
    producer.start()
    consumer.start()
    time.sleep(16)
    producer.finish()
    consumer.finish()


    