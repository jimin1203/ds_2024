from circularLinkedList import CircularLinkedList  

class LRUCacheSimulator:
    def __init__(self, cache_slots):
        self.cache_size = cache_slots
        self.cache_slots = CircularLinkedList()
        self.cache_hit = 0
        self.tot_cnt = 1

    def do_sim(self, page):
        if page in self.cache_slots: # 캐시 슬롯에 페이지가 있는 경우
            self.cache_slots.remove(page) # 해당 페이지를 리스트에서 제거
            self.cache_slots.append(page) # 가장 최근에 사용된 페이지로 추가
            self.cache_hit += 1  # 캐시 히트 횟수 증가
        else: # 캐시 슬롯에 페이지가 없는 경우
            if self.cache_slots.size() >= self.cache_size:
                self.cache_slots.pop(0)
            self.cache_slots.append(page)
        self.tot_cnt += 1

    def print_stats(self):
        print("cache_slot =", self.cache_size, "cache_hit =", self.cache_hit, "hit ratio =", self.cache_hit / self.tot_cnt)


if __name__ == "__main__":
    data_file = open("lru_sim/linkbench.trc")
    lines = data_file.readlines()

    for cache_slots in range(100, 1001, 100):
        cache_sim = LRUCacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)

        cache_sim.print_stats()
