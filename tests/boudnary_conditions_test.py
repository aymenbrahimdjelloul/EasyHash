""" 
@author : Aymen Brahim DJelloul
date : 11.06.2024


    // This test will check the behaviors of the EasyHash algorithm when it be used in boundary
    conditions like Non-ASCI characters or empty input etc.

"""

# IMPORT
import sys
import os

# Initialize the work path
module_path: str = f"/home/{os.getlogin()}/Documents/EasyHash"

if module_path not in sys.path:
    sys.path.append(module_path)

# Import the EasyHash module
from easyhash import EasyHash

# Test empty input hash
empty_hash: int = EasyHash(b"").digest()
print(empty_hash)