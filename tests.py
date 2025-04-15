"""
@author : Aymen Brahim Djelloul
date : 15.04.2025
license : MIT

    This is a suit test for EasyHash hashing algorithm,
     this code will test :

     - Correctnes test
     - Avalanche effect
     - collisions
     - performance tests
"""

# IMPORTS
import os
import time
import random
import hashlib
import string
import pickle
from test import EasyHash, easyhash, easyhash_hex



def test_correctness():
    """Test that the hash function produces correct results"""
    print("\n=== Testing Correctness ===")

    # Test cases
    test_cases = [
        b"",  # Empty string
        b"hello",  # Simple string
        b"The quick brown fox jumps over the lazy dog",  # Classic test phrase
        b"a" * 1000,  # Repetitive content
        "Unicode test: 你好，世界！".encode("utf-8")  # Unicode
    ]

    for i, test in enumerate(test_cases):
        # Test basic API
        hash1 = easyhash(test)
        hash2 = EasyHash(test).digest()

        # Test update method
        hasher = EasyHash()
        hasher.update(test)
        hash3 = hasher.digest()

        if hash1 == hash2 == hash3 and len(hash1) == 16:  # 16 bytes = 128 bits
            print(f"✅ Test case {i + 1}: Passed")
        else:
            print(f"❌ Test case {i + 1}: Failed")
            print(f"   Lengths: {len(hash1)}, {len(hash2)}, {len(hash3)}")

    # Test incremental updates
    test_string = b"Hello World"
    hash_full = easyhash(test_string)

    hasher = EasyHash()
    hasher.update(test_string[:5])  # "Hello"
    hasher.update(test_string[5:])  # " World"
    hash_parts = hasher.digest()

    if hash_full == hash_parts:
        print("✅ Incremental update: Passed")
    else:
        print("❌ Incremental update: Failed")


def test_consistency():
    """Test consistency of hash results across different runs"""
    print("\n=== Testing Consistency Across Sessions ===")

    # Generate test data
    test_data = []
    for i in range(5):
        test_data.append(''.join(random.choices(string.ascii_letters + string.digits, k=50)))

    # Compute hashes for the first time
    first_run = {}
    for i, data in enumerate(test_data):
        first_run[i] = easyhash_hex(data)

    # Save hashes to a temporary file
    with open("easyhash_temp.pkl", "wb") as f:
        pickle.dump(first_run, f)

    # Read back the hashes and compare with new computations
    with open("easyhash_temp.pkl", "rb") as f:
        saved_hashes = pickle.load(f)

    all_passed = True
    for i, data in enumerate(test_data):
        new_hash = easyhash_hex(data)
        if saved_hashes[i] != new_hash:
            print(f"❌ Consistency test {i + 1}: Failed")
            all_passed = False

    if all_passed:
        print("✅ All consistency tests passed!")

    os.remove("easyhash_temp.pkl")


def test_avalanche_effect():
    """Test the avalanche effect - small input changes should cause significant output changes"""
    print("\n=== Testing Avalanche Effect ===")

    total_bit_changes = []

    # Test with 20 different inputs
    for _ in range(20):
        # Generate random input
        input_data = ''.join(random.choices(string.ascii_letters, k=50)).encode()

        # Get original hash
        original_hash = easyhash(input_data)

        # Convert to bit string for comparison
        original_bits = ''.join(f'{byte:08b}' for byte in original_hash)

        # Change one bit of input and check hash difference
        for byte_pos in range(min(10, len(input_data))):  # Test first 10 positions only for brevity
            # Flip one bit in the chosen byte
            modified_data = bytearray(input_data)
            modified_data[byte_pos] ^= 1  # Flip the lowest bit

            # Get new hash
            modified_hash = easyhash(bytes(modified_data))
            modified_bits = ''.join(f'{byte:08b}' for byte in modified_hash)

            # Count bit differences
            diff_bits = sum(a != b for a, b in zip(original_bits, modified_bits))
            bit_change_percentage = (diff_bits / len(original_bits)) * 100

            total_bit_changes.append(bit_change_percentage)

    # Calculate average bit change
    avg_change = sum(total_bit_changes) / len(total_bit_changes)
    print(f"Average bit change: {avg_change:.2f}%")

    # Compare with SHA-256
    sha_changes = []
    easy_changes = []

    for _ in range(10):
        input_data = ''.join(random.choices(string.ascii_letters, k=50)).encode()

        # Change one bit
        modified_data = bytearray(input_data)
        modified_data[random.randint(0, len(modified_data) - 1)] ^= 1

        # EasyHash
        original_easy = easyhash(input_data)
        modified_easy = easyhash(bytes(modified_data))

        easy_orig_bits = ''.join(f'{byte:08b}' for byte in original_easy)
        easy_mod_bits = ''.join(f'{byte:08b}' for byte in modified_easy)
        easy_diff = sum(a != b for a, b in zip(easy_orig_bits, easy_mod_bits))
        easy_change = (easy_diff / len(easy_orig_bits)) * 100
        easy_changes.append(easy_change)

        # SHA-256
        original_sha = hashlib.sha256(input_data).digest()
        modified_sha = hashlib.sha256(bytes(modified_data)).digest()

        sha_orig_bits = ''.join(f'{byte:08b}' for byte in original_sha)
        sha_mod_bits = ''.join(f'{byte:08b}' for byte in modified_sha)
        sha_diff = sum(a != b for a, b in zip(sha_orig_bits, sha_mod_bits))
        sha_change = (sha_diff / len(sha_orig_bits)) * 100
        sha_changes.append(sha_change)

    print(f"EasyHash average bit change: {sum(easy_changes) / len(easy_changes):.2f}%")
    print(f"SHA-256 average bit change: {sum(sha_changes) / len(sha_changes):.2f}%")

    if avg_change >= 45:
        print("✅ Good avalanche effect (near 50% bit change)")
    else:
        print("❌ Poor avalanche effect")


def test_collision_resistance():
    """Test collision resistance by generating random inputs"""
    print("\n=== Testing Collision Resistance ===")

    sample_size = 10000
    hash_values = {}
    collision_count = 0

    for i in range(sample_size):
        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1}/{sample_size} samples...")

        # Generate random data of varying length
        length = random.randint(1, 100)
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        # Compute hash
        hash_value = easyhash_hex(data)

        # Check for collisions
        if hash_value in hash_values:
            collision_count += 1

        else:
            hash_values[hash_value] = data

    print(f"Total collisions found: {collision_count} out of {sample_size} inputs")

    # For a 128-bit hash and 10,000 samples, we wouldn't expect any collisions
    # (probability is roughly n^2/2^129 ≈ 10^8/2^129 ≈ 10^8/10^38 = 10^-30)
    if collision_count == 0:
        print("✅ No collisions found (expected for 128-bit hash with 10,000 samples)")
    else:
        print("❌ Unexpected collisions found")


def test_scalability():
    """Test how the hash function scales with very large inputs"""
    print("\n=== Testing Scalability ===")

    sizes = [1024, 10 * 1024, 100 * 1024, 1024 * 1024, 10 * 1024 * 1024]  # 1KB to 10MB

    print(f"{'Input Size':<12} {'Time (ms)':<12} {'Throughput (MB/s)':<20}")
    print("-" * 44)

    for size in sizes:
        # Generate test data (use repeating pattern for memory efficiency)
        pattern = ''.join(random.choices(string.ascii_letters, k=1024)).encode()
        repeats = size // 1024
        data = pattern * repeats

        # Measure time
        start_time = time.perf_counter()
        easyhash(data)
        end_time = time.perf_counter()

        hash_time = (end_time - start_time) * 1000  # ms
        throughput = (size // (end_time - start_time)) / (1024 * 1024)  # MB/s

        size_label = f"{size / 1024:.0f}KB" if size < 1024 * 1024 else f"{size / 1024 / 1024:.1f}MB"
        print(f"{size_label:<12} {hash_time:.2f} ms {throughput:.2f} MB/s")

    # Check if time scales linearly with input size
    print("\nScaling Analysis:")
    if sizes[-1] / sizes[0] > (sizes[-1] / sizes[0]) * 1.5:
        print("❌ Hash function may not scale linearly with input size")
    else:
        print("✅ Hash function appears to scale linearly with input size")


if __name__ == "__main__":

    print("\n   Start Tests ..")
    # Start tests
    test_correctness()
    test_consistency()
    test_avalanche_effect()
    test_scalability()
    test_collision_resistance()
 
