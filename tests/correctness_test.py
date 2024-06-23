"""
@author : Aymen Brahim Djelloul
date : 11.02.2024

    // Correctness test will make sure that EasyHash perform correctly without bugs
    in normal and usual use cases.

"""

# IMPORTS
import sys
import os

# Initializa the work path
module_path: str = f"/home/{os.getlogin()}/Documents/EasyHash"

if module_path not in sys.path:
    sys.path.append(module_path)

if __name__ == "__main__":
    # Import the EasyHash module
    from easyhash import EasyHash
    # Define the data will hashed
    data: bytes = b"hello world hello world hello world !"
    # Create EasyHash object
    hash_obj = EasyHash(data)

    # TEST 1 : digest hash
    print(f"This the hash : {hash_obj.digest()}")

    # TEST 2 : hexadecimal hash
    print(f"This is the hexadecimal hash : {hash_obj.hexdigest()}")

    # TEST 3 : update the data
    new_data = b"THIS IS JUST A TEST !"
    hash_obj.update(new_data)
    print(f"Hash a new data : {hash_obj.digest()}")

    print("Test passed successfully!")
