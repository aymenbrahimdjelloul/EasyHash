"""
@author : Aymen Brahim Djelloul
date : 11.06.2024


    // The consistency test across session will rerun the same hashing function
    with the same input for multiple times (for example 10,000 time) to ensure thats
    the EasyHash algorithm generate the same output each time .

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

    # Define a data
    data: bytes = b"hello world, hello world, hello world !"

    # Create EasyHash object
    hash_obj = EasyHash(data)

    # Get the hash result
    hash1 = hash_obj.digest()

    # Iterate through multiple hashing sessions and test hashing consistency
    for i in range(10000):

        # Get a new hash result
        hash2 = hash_obj.digest()
        # Check if the two hashes are match
        if hash1 != hash2:
            print(f"CONSISTENCY TEST ACROSS SESSIONS FAILED !\n"
                  "FAILED IN SESSION NUMBER {i}")

            break

    # Print message when test succed
    if i == 9999:
        print("Test passed successfully!")