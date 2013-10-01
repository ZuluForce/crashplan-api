'''
Created on Sep 27, 2013

@author: planeman

Exceptions pertaining to the usage of any general object.
'''

class UnassignableException(Exception):
    """
    An assignment was attempted on something that doesn't support it.
    """
    pass

class NonInstantiableException(Exception):
    """
    A given object cannot/should not be instantiated.
    """
    pass


class MissingRequiredProperty(Exception):
    """
    A property that must exist is missing.
    """
    pass
