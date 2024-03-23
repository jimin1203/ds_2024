class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_size = cache_slots  
        self.cache_slots = []  
        self.cache_hit = 0
        self.tot_cnt = 1

    def do_sim(self, page):
        if page in self.cache_slots: # 기존 리스트에 page가 있다면
            self.cache_slots.remove(page) # 리스트에 있던 page 삭제
            self.cache_slots.append(page) # 리스트 맨 뒤에 page 추가
            self.cache_hit+=1 # 캐시 히트 횟수 추가
        else: # 기존 리스트에 page가 없다면
            if len(self.cache_slots) >= self.cache_size: # 캐시가 꽉 찼을 경우
                self.cache_slots.pop(0) # 가장 오래된 page 제거
            self.cache_slots.append(page) # 리스트 맨 뒤에 page 추가
        self.tot_cnt+=1 # 엑세스 횟수 추가

    def print_stats(self):
        print("cache_slot = ", self.cache_size, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)


if __name__ == "__main__":

    data_file = open("lru_sim/linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)
        
        cache_sim.print_stats()
