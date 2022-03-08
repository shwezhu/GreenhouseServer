# Syntax in python

## 1. None
---
Python uses the keyword None to define null objects and variables.

None is not 0. 

If the function doesn't return anything that means its None in Python.

## 2. Method
---
A `staticmethod` is a method that knows nothing about the class or instance it was called on. 

A `classmethod`, on the other hand, is a method that gets passed the class it was called on, or the class of the instance it was called on, as first argument.
[Find more](https://stackoverflow.com/questions/136097/difference-between-staticmethod-and-classmethod)

## 3. Context Manager
---
When creating context managers using classes, user need to ensure that the class has the methods: `__enter__()` and `__exit__()`. The `__enter__()` returns the resource that needs to be managed and the `__exit__()` does not return anything but performs the cleanup operations.

`__enter__` should return an object that is assigned to the variable after as.
[Context Manager Python](https://www.geeksforgeeks.org/context-manager-in-python/)

