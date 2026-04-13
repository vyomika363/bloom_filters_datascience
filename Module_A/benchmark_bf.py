import random
import string
from standard_bf import BloomFilter

def random_key(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

n = 10000
print(f"n = {n} elements\n")
print(f"{'Target FPR':>12} {'Bits (m)':>10} {'Bytes':>8} {'k (hashes)':>12} {'Actual FPR':>12}")
print("-" * 58)

for fpr in [0.001, 0.01, 0.05, 0.1]:
    bf = BloomFilter(n=n, fpr=fpr)

    keys = [random_key() for _ in range(n)]
    for k in keys:
        bf.insert(k)

    positive_set = set(keys)
    fp = sum(
        1 for _ in range(50000)
        if (k := random_key(length=15)) not in positive_set and bf.query(k)
    )
    actual = fp / 50000

    print(f"{fpr:>12.3f} {bf.memory_bits():>10} {bf.memory_bits()//8:>8} {bf.k:>12} {actual:>12.4f}")