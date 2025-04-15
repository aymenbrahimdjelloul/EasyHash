"""
@author : Aymen Brahim Djelloul
Date : 15.04.2025
License : MIT
"""

# IMPORTS
import os
import sys
import struct
import multiprocessing
from typing import List, Union, Optional, Tuple
from concurrent.futures import ProcessPoolExecutor
import array


class EasyHash:

    # Class constants
    digest_size: int = 16  # True 128-bit/16-byte output
    block_size: int = 64   # Standard block size for processing

    # Default parallel processing settings - optimized values
    __DEFAULT_CHUNK_SIZE = 8 * 1024 * 1024  # 8MB chunks - larger for better efficiency
    __DEFAULT_MIN_SIZE_FOR_MP = 16 * 1024 * 1024  # 16MB minimum - avoid MP overhead for smaller data
    __DEFAULT_MAX_WORKERS = max(1, min(os.cpu_count() or 4, 8))  # Limit max workers to reduce context switching

    # Prime numbers for mixing operations
    __PRIME1: int = 0x9E3779B1  # 2654435761
    __PRIME2: int = 0x85EBCA77  # 2246822519
    __PRIME3: int = 0xC2B2AE3D  # 3266489917
    __PRIME4: int = 0x27D4EB2F  # 668265263

    # Initialization vector (4 32-bit values = 128 bits total)
    __IV: List[int] = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A]

    def __init__(self, data: Union[bytes, str, None] = None,
                parallel: bool = True,
                chunk_size: int = None,
                min_size_for_mp: int = None,
                max_workers: int = None) -> None:
        """
        Initialize the hash object, optionally with input data

        Args:
            data: Initial data to hash
            parallel: Enable multiprocessing for large inputs
            chunk_size: Size of chunks for parallel processing (bytes)
            min_size_for_mp: Minimum input size to use multiprocessing
            max_workers: Maximum number of worker processes
        """
        # Internal state (128 bits divided into 4 32-bit values)
        self.__state = array.array('I', self.__IV)  # Use array for better performance
        self.__length = 0

        # Multiprocessing settings
        self.__parallel = parallel
        self.__chunk_size = chunk_size or self.__DEFAULT_CHUNK_SIZE
        self.__min_size_for_mp = min_size_for_mp or self.__DEFAULT_MIN_SIZE_FOR_MP
        self.__max_workers = max_workers or self.__DEFAULT_MAX_WORKERS

        # Prepare worker pool if we're using parallelism
        self.__pool = None
        if parallel:
            # Create process pool on demand to avoid initialization overhead
            pass

        # Buffer for incomplete blocks
        self.__buffer = bytearray()

        # If data is provided, update the hash
        if data is not None:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.update(data)

    def update(self, data: bytes) -> None:
        """Update the hash object with new data"""
        if not isinstance(data, bytes):
            raise TypeError(f"Expected bytes, got {type(data).__name__}")

        self.__length += len(data)

        # Add to buffer first
        self.__buffer.extend(data)

        # If we have enough data for parallel processing and it's enabled
        if self.__parallel and len(self.__buffer) >= self.__min_size_for_mp:
            self.__process_parallel()
        else:
            # Process complete blocks
            self.__process_sequential()

    def __process_sequential(self) -> None:
        """Process data sequentially in blocks"""
        # Process complete blocks
        offset = 0
        buffer_len = len(self.__buffer)

        # Fast path for processing full blocks
        while offset + self.block_size <= buffer_len:
            self.__process_block(self.__buffer[offset:offset + self.block_size])
            offset += self.block_size

        # Keep remaining bytes in buffer
        if offset > 0:
            self.__buffer = self.__buffer[offset:]

    def __process_parallel(self) -> None:
        """Process data in parallel using multiprocessing"""
        # Calculate how many complete blocks we have
        complete_blocks_size = (len(self.__buffer) // self.block_size) * self.block_size

        # Reserve incomplete final block if needed
        if complete_blocks_size < len(self.__buffer):
            remainder = self.__buffer[complete_blocks_size:]
            data_to_process = self.__buffer[:complete_blocks_size]
        else:
            remainder = bytearray()
            data_to_process = self.__buffer

        # Only parallelize if we have enough data
        if len(data_to_process) >= self.__min_size_for_mp:
            # Determine chunks - make them significantly larger to reduce overhead
            chunk_count = min(self.__max_workers, max(1, len(data_to_process) // self.__chunk_size))

            if chunk_count > 1:
                # Initialize the process pool if needed
                if not self.__pool:
                    ctx = multiprocessing.get_context('spawn')  # More stable than fork
                    self.__pool = ProcessPoolExecutor(max_workers=self.__max_workers, mp_context=ctx)

                # Calculate chunk size (ensure it's a multiple of block_size)
                base_chunk_size = len(data_to_process) // chunk_count
                chunk_size = (base_chunk_size // self.block_size) * self.block_size

                # Process the chunks in parallel
                futures = []
                chunk_states = []

                # Submit chunks for processing
                for i in range(0, len(data_to_process), chunk_size):
                    end = min(i + chunk_size, len(data_to_process))
                    chunk = bytes(data_to_process[i:end])  # Convert to bytes for immutability in MP
                    if len(chunk) % self.block_size == 0:
                        futures.append(self.__pool.submit(self.__process_chunk_static, chunk))
                    else:
                        # Process incomplete chunk directly
                        for j in range(0, len(chunk) - self.block_size + 1, self.block_size):
                            self.__process_block(chunk[j:j+self.block_size])

                # Collect results and merge states
                for future in futures:
                    state = future.result()
                    chunk_states.append(state)

                # Merge all states at once
                if chunk_states:
                    self.__merge_states(chunk_states)
            else:
                # Process sequentially if only one chunk
                self.__process_data_blocks(data_to_process)
        else:
            # Process sequentially if not enough data
            self.__process_data_blocks(data_to_process)

        # Update buffer with remainder
        self.__buffer = remainder

    def __process_data_blocks(self, data: bytes) -> None:
        """Process data in block-sized chunks sequentially"""
        for i in range(0, len(data), self.block_size):
            self.__process_block(data[i:i+self.block_size])

    @staticmethod
    def __process_chunk_static(chunk: bytes) -> Tuple[int, int, int, int]:
        """Static method to process a chunk in a separate process"""
        # Create initial state
        state = array.array('I', EasyHash.__IV)

        # Process all complete blocks in this chunk
        for i in range(0, len(chunk), EasyHash.block_size):
            block = chunk[i:i+EasyHash.block_size]

            # Extract words using struct (more efficient)
            words = array.array('I')
            for j in range(0, EasyHash.block_size, 4):
                if j + 4 <= len(block):
                    word = struct.unpack("<I", block[j:j+4])[0]
                    words.append(word)
                else:
                    break

            # Mix the words into the state
            a, b, c, d = state

            # Unroll the loop for better performance
            for i, word in enumerate(words):
                # Apply different mixing based on position
                if i & 3 == 0:  # i % 4 == 0, but faster
                    a = (a + word) & 0xFFFFFFFF
                    a = (a * EasyHash.__PRIME1) & 0xFFFFFFFF
                    a = ((a << 7) | (a >> 25)) & 0xFFFFFFFF  # rotate_left(a, 7)
                    a = (a * EasyHash.__PRIME2) & 0xFFFFFFFF
                elif i & 3 == 1:
                    b = (b + word) & 0xFFFFFFFF
                    b = (b * EasyHash.__PRIME2) & 0xFFFFFFFF
                    b = ((b << 11) | (b >> 21)) & 0xFFFFFFFF  # rotate_left(b, 11)
                    b = (b * EasyHash.__PRIME3) & 0xFFFFFFFF
                elif i & 3 == 2:
                    c = (c + word) & 0xFFFFFFFF
                    c = (c * EasyHash.__PRIME3) & 0xFFFFFFFF
                    c = ((c << 13) | (c >> 19)) & 0xFFFFFFFF  # rotate_left(c, 13)
                    c = (c * EasyHash.__PRIME4) & 0xFFFFFFFF
                else:  # i & 3 == 3
                    d = (d + word) & 0xFFFFFFFF
                    d = (d * EasyHash.__PRIME4) & 0xFFFFFFFF
                    d = ((d << 17) | (d >> 15)) & 0xFFFFFFFF  # rotate_left(d, 17)
                    d = (d * EasyHash.__PRIME1) & 0xFFFFFFFF

            # Cross-mixing step for avalanche
            a = (a ^ d) & 0xFFFFFFFF
            b = (b ^ a) & 0xFFFFFFFF
            c = (c ^ b) & 0xFFFFFFFF
            d = (d ^ c) & 0xFFFFFFFF

            state[0], state[1], state[2], state[3] = a, b, c, d

        # Return as tuple for efficient transport across processes
        return (state[0], state[1], state[2], state[3])

    def __merge_states(self, states: List[Tuple[int, int, int, int]]) -> None:
        """Efficiently merge multiple states"""
        a, b, c, d = self.__state

        # Mix in each state
        for state in states:
            s0, s1, s2, s3 = state

            # XOR the states
            a ^= s0
            b ^= s1
            c ^= s2
            d ^= s3

            # Mix for better avalanche
            a = ((a << 9) | (a >> 23)) & 0xFFFFFFFF
            b = ((b << 13) | (b >> 19)) & 0xFFFFFFFF
            c = ((c << 17) | (c >> 15)) & 0xFFFFFFFF
            d = ((d << 21) | (d >> 11)) & 0xFFFFFFFF

            # Additional mixing with primes
            a = (a * self.__PRIME1) & 0xFFFFFFFF
            b = (b * self.__PRIME2) & 0xFFFFFFFF
            c = (c * self.__PRIME3) & 0xFFFFFFFF
            d = (d * self.__PRIME4) & 0xFFFFFFFF

        # Final mixing step
        a = (a ^ d) & 0xFFFFFFFF
        b = (b ^ a) & 0xFFFFFFFF
        c = (c ^ b) & 0xFFFFFFFF
        d = (d ^ c) & 0xFFFFFFFF

        self.__state[0], self.__state[1], self.__state[2], self.__state[3] = a, b, c, d

    def __process_block(self, block: bytes) -> None:
        """Process a single block of data - optimized with direct array access"""
        # Quick word extraction using struct
        words = array.array('I')
        for i in range(0, min(len(block), self.block_size), 4):
            if i + 4 <= len(block):
                word = struct.unpack_from("<I", block, i)[0]  # unpack_from is faster
                words.append(word)
            else:
                padded = block[i:] + b'\x00' * (4 - (len(block) - i))
                word = struct.unpack("<I", padded)[0]
                words.append(word)

        # Mix the words into the state
        a, b, c, d = self.__state

        # Unroll the loop for better performance
        for i, word in enumerate(words):
            # Apply different mixing based on position
            if i & 3 == 0:  # i % 4 == 0, but faster
                a = (a + word) & 0xFFFFFFFF
                a = (a * self.__PRIME1) & 0xFFFFFFFF
                a = self.__rotate_left(a, 7)
                a = (a * self.__PRIME2) & 0xFFFFFFFF
            elif i & 3 == 1:
                b = (b + word) & 0xFFFFFFFF
                b = (b * self.__PRIME2) & 0xFFFFFFFF
                b = self.__rotate_left(b, 11)
                b = (b * self.__PRIME3) & 0xFFFFFFFF
            elif i & 3 == 2:
                c = (c + word) & 0xFFFFFFFF
                c = (c * self.__PRIME3) & 0xFFFFFFFF
                c = self.__rotate_left(c, 13)
                c = (c * self.__PRIME4) & 0xFFFFFFFF
            else:  # i & 3 == 3
                d = (d + word) & 0xFFFFFFFF
                d = (d * self.__PRIME4) & 0xFFFFFFFF
                d = self.__rotate_left(d, 17)
                d = (d * self.__PRIME1) & 0xFFFFFFFF

        # Cross-mixing step for avalanche
        a = (a ^ d) & 0xFFFFFFFF
        b = (b ^ a) & 0xFFFFFFFF
        c = (c ^ b) & 0xFFFFFFFF
        d = (d ^ c) & 0xFFFFFFFF

        self.__state[0], self.__state[1], self.__state[2], self.__state[3] = a, b, c, d

    @staticmethod
    def __rotate_left(value: int, bits: int) -> int:
        """Rotate the bits of a 32-bit integer to the left - optimized version"""
        return ((value << bits) | (value >> (32 - bits))) & 0xFFFFFFFF

    def digest(self) -> bytes:
        """Return the digest of the data"""
        # Process any remaining data
        temp_instance = self.copy()

        # Process remaining buffer
        if temp_instance.__buffer:
            # Pad the final incomplete block
            remaining = bytes(temp_instance.__buffer)
            pad_len = temp_instance.block_size - len(remaining) % temp_instance.block_size
            if pad_len == temp_instance.block_size:
                pad_len = 0
            padding = bytes([pad_len] * pad_len)

            # Process blocks sequentially (no need for parallelism here)
            padded = remaining + padding
            for i in range(0, len(padded), temp_instance.block_size):
                temp_instance.__process_block(padded[i:i+temp_instance.block_size])

            temp_instance.__buffer = bytearray()

        # Mix in the total length for better uniqueness
        final_state = array.array('I', temp_instance.__state)
        length_word = (temp_instance.__length & 0xFFFFFFFF)
        final_state[0] ^= length_word
        final_state[1] ^= (temp_instance.__length >> 32) & 0xFFFFFFFF

        # Finalize each word
        for i in range(4):
            final_state[i] = temp_instance.__finalize(final_state[i])

        # Combine the four 32-bit values into a 16-byte output
        digest_bytes = struct.pack("<IIII", *final_state)  # Pack all at once is faster
        return digest_bytes

    def __finalize(self, value: int) -> int:
        """Finalization function with good avalanche effect"""
        value ^= value >> 15
        value = (value * self.__PRIME2) & 0xFFFFFFFF
        value ^= value >> 13
        value = (value * self.__PRIME3) & 0xFFFFFFFF
        value ^= value >> 16
        return value

    def hexdigest(self) -> str:
        """Return the digest as a hexadecimal string"""
        return self.digest().hex()

    def copy(self):
        """Create a copy of the hash object"""
        new_copy = EasyHash(parallel=self.__parallel,
                          chunk_size=self.__chunk_size,
                          min_size_for_mp=self.__min_size_for_mp,
                          max_workers=self.__max_workers)
        new_copy.__state = array.array('I', self.__state)
        new_copy.__buffer = bytearray(self.__buffer)
        new_copy.__length = self.__length
        new_copy.__pool = self.__pool  # Share the pool for efficiency
        return new_copy

    def __del__(self):
        """Clean up the process pool when the object is destroyed"""
        if hasattr(self, '__pool') and self.__pool:
            self.__pool.shutdown(wait=False)

    @classmethod
    def new(cls, data: Optional[bytes] = None, parallel: bool = True,
           chunk_size: int = None, min_size_for_mp: int = None,
           max_workers: int = None):
        """Create a new hash object with optional configuration"""
        return cls(data, parallel, chunk_size, min_size_for_mp, max_workers)


def easyhash(data: Union[bytes, str], parallel: bool = True) -> bytes:
    """Convenience function to get digest directly"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return EasyHash(data, parallel=parallel).digest()


def easyhash_hex(data: Union[bytes, str], parallel: bool = True) -> str:
    """Convenience function to get hexdigest directly"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return EasyHash(data, parallel=parallel).hexdigest()


if __name__ == "__main__":
    sys.exit()
