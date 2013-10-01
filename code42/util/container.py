class Bunch(dict):
    """
    A class to hold a "bunch" of items. This has the advantage of a regular dictionary
    of providing dot access to elements.
    
    Example:
    >>> b = Bunch(GET='GET', POST='POST')
    >>> b.GET
    'GET'
    >>> b['GET']
    'GET'
    >>> b = Bunch(**{'a' : 1, 'b' : 2})
    >>> b.a
    1
    >>> b.b
    2
    """
    def __init__(self, **kwargs):
        dict.__init__(self, kwargs)
        self.__dict__ = self

    def findByValue(self, sval):
        """
        Find all keys with the given value.
        
        Examples:
        >>> b = Bunch(a=2, b=2, c=1)
        >>> b.findByValue(2)
        ['a', 'b']
        >>> b.findByValue(1)
        ['c']
        """
        keys = []
        for key, val in self.__dict__.items():
            if sval == val:
                keys.append(key)

        return keys
                
    def findFirstByValue(self, sval):
        """
        Find the first key with the given value. Since key:value pairs are stored
        in a dictionary there is no guarantee on ordering.
        
        Examples:
        >>> b = Bunch(a=2, b=3, c=4, d=5)
        >>> b.findFirstByValue(2)
        'a'
        >>> b.findFirstByValue(10)
        >>>
        """
        for key, val in self.__dict__.items():
            if sval == val:
                return key

if __name__ == '__main__':
    import doctest
    doctest.testmod()
