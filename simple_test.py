# IMPORTS
from easyhash import easyhash_hex, easyhash
import time

# Store simple data as hello world text
data = b"hello world!"

# Measure the start time
s_time = time.perf_counter()

# Get the hexdigest hash
hash_ = easyhash_hex(data)

# Print results
print(f"executed in : {time.perf_counter() - s_time:.4f}")
print(f"hash : {hash_}")
