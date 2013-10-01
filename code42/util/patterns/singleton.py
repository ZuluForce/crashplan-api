'''
Created on Sep 27, 2013

@author: planeman

Utilities for implementing the singleton pattern.
'''

class Singleton(type):
    """
    A metaclass implementation of the singleton pattern. Simple add this
    class as the __metaclass__ for your class.
    
    If you want singleton objects (instances) then add this as a base class.
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):  # @NoSelf
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
