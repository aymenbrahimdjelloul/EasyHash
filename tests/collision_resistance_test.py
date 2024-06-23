"""
@author : Aymen Brahim Djelloul
date : 11.06.2024


    // This test will check for hashs collisions in the output.

"""

# IMPORTS
import sys
import os
import random
import string
import hashlib


# Initialize the work path
module_path: str = f"/home/{os.getlogin()}/Documents/EasyHash"

if module_path not in sys.path:
    sys.path.append(module_path)


def generate_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def hash_function(data):
    return EasyHash(data.encode()).hexdigest()

def test_collisions(num_tests=1000000):
    hashes = {}
    collisions = []
    
    for _ in range(num_tests):
        data = generate_random_string()
        hash_value = hash_function(data)
        
        if hash_value in hashes:
            collisions.append((hashes[hash_value], data))
        else:
            hashes[hash_value] = data
    
    return collisions

if __name__ == "__main__":

    # Import the EasyHash module
    from easyhash import EasyHash

    # Run the collision test
    collisions_found = test_collisions()

    if collisions_found:
        print(f"Collisions found: {len(collisions_found)}")
        # for collision in collisions_found:
        #     print(f"Collision: {collision[0]} and {collision[1]}")
    else:
        print("No collisions found.")
