from threading import local
from contextlib import contextmanager

import sys
print sys.path
# sys.path = sys.path[2:]

from code42.util import container

class SessionManager(object):
    tlocal = local()

    @staticmethod
    @contextmanager
    def create(*args, **kw):
        tlocal = SessionManager.tlocal

        # Check if a session is already present
        if SessionManager.getSession():
            raise Exception("Session already initiated on this thread")

        tlocal = local()
        tlocal.session = APISession(*args, **kw)
        SessionManager.tlocal = tlocal

        # Hand over control to the user
        try:
            yield tlocal.session
        finally:
            # When we're done destroy the session
            tlocal.session.cleanup()
            SessionManager.tlocal.session = None

    @staticmethod
    def getSession():
        """
        Get the API session currently attached to this thread, if any.
        """
        return getattr(SessionManager.tlocal, 'session', None)

class APISession(object):
    """
    Settings for use by API requests that you want to persist across multiple requests.
    
    Anything can be placed in the APISession but certain arguments have special uses and
    are listed below.
    
    Keyword Arguments:
        auth_provider - An object with a getAuth() method that provides a (username, password) tuple
        
    Examples:
    >>> d = {'auth_provider': container.Bunch(getAuth=lambda x: ('u','p')) }
    >>> s = APISession(*d)
    >>> s.getAuthProvider().getAuth()
    ('u', 'p')
    """
    def __init__(self, *args, **kwargs):
        self.bunch = container.Bunch(**kwargs)

    # === Named Accessors === #

    def getAuthProvider(self):
        print self.bunch
        return self.auth_provider

    def __getattr__(self, name):
        try:
            return self.bunch[name]
        except KeyError as ke:
            raise AttributeError(ke)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
