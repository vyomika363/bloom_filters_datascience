import random
import string
from standard_bf import BloomFilter

def random_key(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def test_zero_false_negatives():
    print("Testing: zero false negatives...")
    bf = BloomFilter(n=10000, fpr=0.01)
    keys = [random_key() for _ in range(10000)]
    for k in keys:
        bf.insert(k)
    for k in keys:
        assert bf.query(k), f"False negative found on key: {k}"
    print("PASS: all 10,000 inserted keys found correctly\n")

def test_fpr():
    print("Testing: false positive rate...")
    target_fpr = 0.01
    bf = BloomFilter(n=10000, fpr=target_fpr)

    positives = [random_key() for _ in range(10000)]
    for k in positives:
        bf.insert(k)

    positive_set = set(positives)
    false_positives = 0
    trials = 100000

    for _ in range(trials):
        key = random_key(length=15)  # longer keys = almost certainly not inserted
        if key not in positive_set and bf.query(key):
            false_positives += 1

    actual_fpr = false_positives / trials
    print(f"Target FPR : {target_fpr:.3f}")
    print(f"Actual FPR : {actual_fpr:.4f}")
    assert actual_fpr < target_fpr * 2, "FPR is way off — check your formulas"
    print("PASS: FPR within acceptable range\n")

def test_memory():
    print("Testing: memory_bits()...")
    bf = BloomFilter(n=10000, fpr=0.01)
    bits = bf.memory_bits()
    assert bits > 0
    print(f"PASS: memory_bits() = {bits} bits ({bits // 8} bytes)\n")

test_zero_false_negatives()
test_fpr()
test_memory()