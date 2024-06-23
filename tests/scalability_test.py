"""
@author : Aymen Brahim Djelloul
date : 11.06.2024


    // This test check if the EasyHash algorithm gets the same output size with diffrent
    input sizes.

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

    #   // THIS TEST MIGT TAKE A FEW SECONDS !

    # Get the start time 
    s_time: float = time.time()
    # Import EasyHash module
    from easyhash import EasyHash

    # Generate 1 KB data
    data1: bytes = os.urandom(1024) # 1024 bytes = 1 KB

    # Create a hash object
    hash1 = EasyHash(data1).digest()

    # Generate 1 MB data
    data2: bytes = os.urandom(1024*1024) # 1024 * 1024 = 1 MB
    # hash 1 MB data
    hash2 = EasyHash(data2).digest()

    # Generate 100 MB data
    data3: bytes = os.urandom(1024*1024*100) # 1024 * 1024 * 100 = 100 MB

    # hash the 100 MB data
    hash3 = EasyHash(data3).digest()

    # Get the test result
    if len(str(hash1)) and len(str(hash2)) and len(str(hash3)) == 16:
        print("Test pass successfuly !")
        print(f"Test ended in : {time.time() - s_time}")

    else:
        print("Test Failed !")


