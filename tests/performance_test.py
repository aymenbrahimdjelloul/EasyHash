"""
@author : Aymen Brahim Djelloul
date : 11.06.2024


    // The peformance test will test the speed and performance of EasyHash.

"""

# IMPORTS
import sys
import os
import time

# Initializa the work path
module_path: str = f"/home/{os.getlogin()}/Documents/EasyHash"

if module_path not in sys.path:
    sys.path.append(module_path)


if __name__ == "__main__":

    #   // THIS TEST MIGHT TAKE A FEW SECONDS
        # Import EasyHash module
    from easyhash import EasyHash

    # Generate 1 KB data
    data1: bytes = os.urandom(1024) # 1024 bytes = 1 KB

    # Get the start test time
    s_time: float = time.time()

    # Create a hash object
    hash1 = EasyHash(data1).digest()

    # Print the time to hash a 1kb of data
    print(f"Done 1KB in : {time.time() - s_time:.4f} seconds")

    # Generate 1 MB data
    data2: bytes = os.urandom(1024*1024) # 1024 * 1024 = 1 MB

    # Get the start test time
    s_time: float = time.time()

    # hash 1 MB data
    hash2 = EasyHash(data2).digest()

    # Print the time to hash a 1MB of data
    print(f"Done 1MB in : {time.time() - s_time:.4f} seconds")

    # Calculate how long it take to hash a 1Gb data
    print(f"Done 1Gb in : {(time.time() - s_time) * 1000:.4f} seconds")
