# EasyHash 🔐⚡
EasyHash is a custom-designed 128-bit cryptographic hashing algorithm developed for educational purposes. This project aims to demonstrate the fundamental principles of hash functions, including data integrity verification, deterministic output generation, and resistance to basic collision attacks. While not intended for production-level security, EasyHash serves as a learning tool for understanding hash mechanics, bitwise operations, and cryptographic concepts. 


## Use Cases (Educational Only):

Demonstrating how hash functions process variable-length input into fixed-length output.

Comparing performance and properties against established algorithms.

Experimenting with custom modifications (e.g., adjusting rounds, mixing operations).

Disclaimer:
EasyHash is not suitable for real-world cryptographic applications due to its simplified design and lack of rigorous security analysis. For secure hashing, use industry-standard algorithms like SHA-256 or SHA-3.


## 🔧 Usage
~~~
from easyhash import easyhash_hex, easyhash

# Store simple data as hello world text
data = b"hello world!"

# Get the hexdigest hash
hash_ = easyhash_hex(data)

print(f"hash : {hash_}")
~~~

## ⚠️ Disclaimer
This is not a cryptographically secure hashing function. It’s built for speed and uniqueness, not encryption or authentication.

## 📄 License
MIT License
Here’s a polished and engaging version of your README.md with improved formatting, clarity, and a touch of visual appeal:

EasyHash 🔐⚡
A custom 128-bit hashing algorithm designed for education and experimentation

EasyHash is a lightweight, 128-bit cryptographic hashing algorithm created to help developers and students understand the core principles of hash functions. It demonstrates key concepts like deterministic output, fixed-length hashing, and basic collision resistance—all while prioritizing simplicity and transparency.

⚠️ Note: EasyHash is not secure for real-world cryptography. Use it for learning, testing, or prototyping—not for sensitive data!

🔍 Features
✔ 128-bit output → Fixed 32-character hexadecimal hash.
✔ Deterministic → Same input = same output, every time.
✔ Educational → Clean, readable code for studying hash mechanics.
✔ Customizable → Easy to modify (rounds, bit ops, mixing functions).

🚀 Use Cases (Educational Only!)
Learn how hashing works – See step-by-step how input becomes a hash.

Compare with SHA/MD5 – Benchmark speed vs. industry standards.

Experiment freely – Tweak the algorithm and observe changes.

~~~
from easyhash import easyhash_hex, easyhash

data = b"hello world!"  
hash_hex = easyhash_hex(data)  # Returns 128-bit hex string
hash_bytes = easyhash(data)    # Returns raw bytes

print(f"Hash (hex): {hash_hex}")  
print(f"Hash (bytes): {hash_bytes}")  
~~~

## 📜 Algorithm Overview
(Briefly summarize how it works, e.g.:)

Padding → Input is padded to a multiple of 512 bits.

Mixing Rounds → Bit shifts, XOR, and modular arithmetic scramble the state.

Finalization → Output is condensed into 16 bytes (128 bits).

(Add a diagram or pseudocode if desired!)

## ⚠️ Critical Disclaimer
DO NOT USE FOR SECURITY! EasyHash lacks:
❌ Cryptographic analysis → No resistance to advanced attacks.
❌ Collision guarantees → Unsuitable for checksums or authentication.

For real projects, use SHA-256, SHA-3, or BLAKE3.

## 📄 License

MIT License © [Aymen Brahim Djelloul] – Free for learning and tinkering!
