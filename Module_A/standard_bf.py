import mmh3
from bitarray import bitarray
import math
class BloomFilter:
    def __init__(self, n: int, fpr: float):
        #n is the expected number of elements
        #fpr is the desired false positive rate (like 0.01 for 1%)
        self.n = n
        self.fpr = fpr
        self.m = self._optimal_m(n, fpr)   #number of bits
        self.k = self._optimal_k(self.m, n) #number of hash functions
        self.bit_array = bitarray(self.m)
        self.bit_array.setall(0)

    def _optimal_m(self, n, fpr):
        return int(-n * math.log(fpr) / (math.log(2) ** 2))

    def _optimal_k(self, m, n):
        return max(1, int((m / n) * math.log(2)))

    def _hashes(self, key: str):
        #this will generate k different hash indices using mmh3 with different seeds
        return [mmh3.hash(key, seed=i, signed=False) % self.m for i in range(self.k)]

    def insert(self, key: str) -> None:
        for idx in self._hashes(key):
            self.bit_array[idx] = 1

    def query(self, key: str) -> bool:
        return all(self.bit_array[idx] for idx in self._hashes(key))

    def memory_bits(self) -> int:
        return self.m
