"""
@author : Aymen Brahim Djelloul
version : 1.0
date : 08.06.2024
license : MIT


    // EasyHash is a simple and basic method for hashing a string. 
    The EasyHash algorithm employs a hash length of 128 bits, ensuring a 
    balance between security and efficiency. By utilizing a 128-bit hash length,
    EasyHash provides a reasonable level of collision resistance and preimage
    resistance, making it suitable for a wide range of applications.

    // With its simplicity and effectiveness, EasyHash serves as a 
    reliable solution for hashing strings in various scenarios, 
    ranging from data verification to password storage and authentication.

    // ATTENTION : This hashing algorithm is intended solely for educational purposes;
      it should not be employed for security-sensitive applications. Nevertheless, it can be effectively
        utilized for tasks such as data verification.

    
    // STEPS :



        
    // sources :

        1. https://www.geeksforgeeks.org/introduction-to-hashing-data-structure-and-algorithm-tutorials/


"""

# IMPORTS
import sys
from exceptions import *

__author__ = "Aymen Brahim Djelloul"
__version__ = "1.0"


class EasyHash:

    # Declare global variables
    name: str = "EasyHash"
    digest_size: int = 20

    # Declare hashing function variables
    __HASH_TABLE: dict = {}
    __block_size: int = 4

    def __init__(self, string: bytes) -> None:
        self.string = string
        # Initialize the block size
        self.__initialize_block_size()

    def digest(self) -> bytes:
        """ This method will return the digested string in bytes"""

        # STEP 1: Convert the string into blocks and store in a list
        blocks = [self.string[i:i + self.__block_size] for i in range(0, len(self.string), self.__block_size)]

        # STEP 2: Padd the last block to ensure that it has length of used block size
        if blocks[-1] != self.__block_size:
            # Get the number for char needed
            num_char = self.__block_size - len(blocks[-1])
            # print(num_char)
            for i in range(num_char):
                blocks[-1] = blocks[-1] + b"X"

        # STEP 3: calucalting blocks value
        block_count: int = 0
        for block in blocks:

            # Declare block value variable as zero
            block_value: int = 0
            for byte in block:
                block_value = block_value + byte

            # Replace the block with its value modded to the length of blocks set
            # to put it in a hash table
            blocks[block_count] = block_value
            block_count += 1

        # STEP 4 : Create a hashmap thats fit the blocks size in prime number
        # First it will get the primne number to use it as hash table size which
        # it will the closes prime numnber to the number of blocks
        self.__create_hashtable(self.__closest_prime_number(len(blocks)), blocks)

        # Calculate the final digest
        # Convert the hash table into immutable structure
        immutable_hashtable = frozenset(self.__HASH_TABLE.items())

        # Generate the hash by using hash method in python
        final_hash: str = str(abs(hash(immutable_hashtable)))[0:16]

        return int(final_hash)
    
    def hexdigest(self) -> str:
        """ This method will return the digested string in hash format"""
        return hex(self.digest())

    def update(self, string: bytes) -> None:
        """ This method will update a new string"""
        self.string = string
        # Re initialize the block size
        self.__initialize_block_size()

    def __create_hashtable(self, blocks_size: int, blocks: list) -> None:
        """ This method will create the hash table according to the given size"""
        self.__HASH_TABLE = {i: blocks[i] for i in range(len(blocks))}

    def __closest_prime_number(self, n: int) -> int:
        """ This method will get the closest possible prime number to a given input"""

        if n <= 2:
            return 2  # The closest prime to any number <= 2 is 2

        while True:
            
            n += 1
            if self.__is_prime(n):
                return n

    @staticmethod
    def __is_prime(n: int) -> bool:
        """ This method will check if the given input is a prime number or not"""

        if n <= 1:
            # Clear memory from n variable
            del n

            return False

        if n <= 3:
            # Clear memory from n variable
            del n

            return True

        if n % 2 == 0 or n % 3 == 0:
            # Clear memory from n variable
            del n

            return False
        
        i = 5

        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                # Clear memory  from 'i, n'
                del i, n

                return False
            i += 6

        # Clear memory from 'i. n'
        del i, n
        return True

    def __initialize_block_size(self):

        # initialize the block size according to the data size
        data_size = sys.getsizeof(self.string)
        if data_size >= 102400:         # Check if the data is up to 1kb
            self.__block_size = 16

        elif data_size >= 512000:       # Check if the data is up to 500kb
            self.__block_size = 32

        elif data_size >= 1048576:      # Check if the data is up to 1Mb
            self.__block_size = 64


if __name__ == "__main__":
    sys.exit()
