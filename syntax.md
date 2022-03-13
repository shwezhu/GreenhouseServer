# Syntax in python

## 1. None
Python uses the keyword None to define null objects and variables.

None is not 0. 

If the function doesn't return anything that means its None in Python.

## 2. Method
A `staticmethod` is a method that knows nothing about the class or instance it was called on. 

A `classmethod`, on the other hand, is a method that gets passed the class it was called on, or the class of the instance it was called on, as first argument.
[Find more](https://stackoverflow.com/questions/136097/difference-between-staticmethod-and-classmethod)

## 3. Context Manager
---
When creating context managers using classes, user need to ensure that the class has the methods: `__enter__()` and `__exit__()`. The `__enter__()` returns the resource that needs to be managed and the `__exit__()` does not return anything but performs the cleanup operations.

`__enter__` should return an object that is assigned to the variable after as.
[Context Manager Python](https://www.geeksforgeeks.org/context-manager-in-python/)

## 4. Reference Counting
Reference counting works by counting the number of times an object is referenced by other objects in the system. When references to an object are removed, the reference count for an object is decremented. When the reference count becomes zero, the object is deallocated.
[Garbage Collection](https://www.geeksforgeeks.org/memory-management-in-python/)

## 5. Local Variables
In Python or any other programming languages, the definition of local variables remains the same, which is “A variable declared inside the function is called local function”. We can access a local variable inside but not outside the function.

## 6. Socket Programming in Python
Socket programming is a way of connecting two nodes on a network to communicate with each other. 
One socket(node) listens on a particular port at an IP, while the other socket reaches out to the other to form a connection. 
They are the real backbones behind web browsing.

```python
# create a socket
import socket
try:
    # AF_INET refers to the address-family ipv4.
    # The SOCK_STREAM means connection-oriented TCP protocol.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" % err)
...
# 5 here means that 5 connections are kept waiting if the server is busy
# and if a 6th socket tries to connect then the connection is refused.
s.listen(5)
```

## 7. Byte String 
To store anything in a computer, you must first encode it, i.e. convert it to bytes.

MP3, WAV, PNG, JPEG, ASCII and UTF-8 are examples of encodings. An encoding is a format to represent audio, images, text, etc in bytes.

There are multiple encodings through which a character string can be converted into a byte string, such as ASCII and UTF-8.

```python
'I am a string'.encode('ASCII')
```
[Difference between a string and a byte string](https://stackoverflow.com/questions/6224052/what-is-the-difference-between-a-string-and-a-byte-string)

## 8. 


