# EasyHash 🔐⚡
A fast and simple 128-bit hashing algorithm written in pure Python, designed for high performance and easy integration. Supports parallel processing for large input datasets.

## 🚀 Features
- ⚡ **Fast 128-bit hashing** algorithm
- 🧵 **Multiprocessing** support for large-scale input
- 📦 Easy to use, extend, and integrate
- 🧪 Deterministic and consistent output
- 🧠 Custom-designed for performance-critical applications

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

