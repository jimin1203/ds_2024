from listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, customers):
        self.__alive = True
        self.customers = customers
        self.ranks = {"1" : ListQueue(), "2":ListQueue(), "3":ListQueue()}
        self.worker = threading.Thread(target=self.run)

    def run(self): 
        for customer in self.customers:
            time.sleep(0.2) 
            level, name = customer
            self.ranks[level].enqueue(name)
            print(f"Arrived: {name} (Level: {level})")
        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()
    
    
class Consumer: # 멀티스레딩 환경에서 독립적임.
    def __init__(self,ranks):
        self.__alive = True # 스레드가 작동 중임
        self.ranks = ranks
        self.worker = threading.Thread(target=self.run)  # 스레드가 실행할 함수:self.run 

    def run(self): # 스레드에 의해 별도의 실행 흐름에서 호출
        while self.__alive:
            for level in ["3", "2", "1"]:
                if not self.ranks[level].isEmpty():
                    time.sleep(1)
                    customer = self.ranks[level].dequeue()
                    print(f"Boarding: {customer} (Level: {level})")
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
            level, name = line.strip().split() # customer[0]:등급 customer[1]:이름
            customers.append((level, name))
        
    producer = Producer(customers)

    # Priority 
    consumer = Consumer(producer.ranks)    
    producer.start()
    consumer.start()
    time.sleep(16)
    producer.finish()
    consumer.finish()


    