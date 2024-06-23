from easyhash import EasyHash
 
# data = open("/home/aymen/Documents/EasyHash/picture.jpg", "rb").read()
# r = EasyHash(data).digest()

# print(len(str(r)))
# print(r)

# import os
# # import hashlib
# import time
# from easyhash import EasyHash
# # # Define the size in bytes (1 MB = 1024 * 1024 bytes)
# size_in_bytes = 1024 * 100
# # # Generate random data
# # data = os.urandom(size_in_bytes)
# data = b"Hello world!"

# s_time = time.time()
# print("start hashing ..")
# # r = hashlib.sha1(data).digest()

# r = EasyHash(data).digest()
# print(len(hex(r)))
# # Check the length of generated data (should be size_in_bytes)
# # print(len(random_data))  # Output: 1048576
# print(f"{time.time() - s_time}")



r = EasyHash(b"r")

print(r.digest())

r.update(b"hello world !")

print(r.digest())

