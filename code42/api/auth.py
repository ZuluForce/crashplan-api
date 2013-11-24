import requests

from threading import local
from contextlib import contextmanager

import code42.api.url as url
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
    >>> d = {'auth_provider': container.Bunch(getAuth=lambda: ('u','p')) }
    >>> s = APISession(*d)
    >>> s.getAuthProvider().getAuth()
    ('u', 'p')
    """
    def __init__(self, *args, **kwargs):
        self.bunch = container.Bunch(**kwargs)

        self.headers = {}
        self.dynamic_header = None

        # Default to Code42 url builder
        self.setUrlBuilder(url.code42UrlBuilder)

    # =-=-= Named Setters =-=-= #
    def setSsl(self, useSsl):
        self.ssl = useSsl
        return self

    def setUrlId(self, url_id):
        """
        Url id is a convention you can use when querying a rest resource.
        For example, if I wanted to query a user resource I could do it 2 ways:
        1. www.crashplan.com/api/user?user_id=1234
        2. www.crashplan.com/api/user/1234

        The second of these is using a url mapping id.
        """
        self.url_id = url_id
        return self

    def setUrlBuilder(self, builder):
        self.url_builder = builder

    def setResourceVersion(self, resource):
        """
        Set a version of a resource to be used for this request.
        """
        self.vresource = resource
        return self

    def addHeader(self, key, value):
        self.headers[key] = value

    def addHeaders(self, headerMap):
        self.headers.update(headerMap)

    def addHeaderProvider(self, providerFn):
        self.dynamic_header = providerFn

    # =-=-= Named Accessors =-=-= #

    def getAuthProvider(self):
        provider = self.getWithDefault('auth_provider', None)

        if provider is None:
            return lambda: None

        return self.auth_provider

    def getUrlBuilder(self):
        return self.url_builder

    def getSsl(self):
        return self.getWithDefault('ssl', False)

    def getUrlId(self):
        return self.getWithDefault('url_id', None)

    def getResourceVersion(self):
        return self.vresource

    # =-=-= Internal Accessors =-=-= #
    def getWithDefault(self, name, default):
        try:
            return getattr(self, name)
        except AttributeError:
            return default

    def __getattr__(self, name):
        """
        Fallback. If a property access cannot be found on the session object
        it will be looked up in the "bunch" which is user provided.
        """
        try:
            return self.bunch[name]
        except KeyError as ke:
            raise AttributeError(ke)

    # =-=-= Request Builders =-=-= #
    def build_session(self, base=None):
        """
        Apply any request modifications that go on the Session. Requests uses the
        session as a persistent container for request settings.
        """
        session = base if base else requests.Session()
        self._apply_session_setting(session, 'verify')
        self._apply_session_setting(session, 'timeout')
        self._apply_session_setting(session, 'cert')
        self._apply_session_setting(session, 'proxies')

        return session


    def _apply_session_setting(self, session, setting, unset_val=None):
        """
        Apply this session setting, if we have a value for it, to the given
        request session.
        """
        setting_value = self.getWithDefault(setting, unset_val)
        if setting_value != unset_val:
            setattr(session, setting, setting_value)

    def build(self, raw_request):
        """
        Build and return a prepared request.

        Arguments:
        raw_request - A requests library unprepared Request object
        """

        # -- Authentication --
        creds_provider = self.getAuthProvider()
        creds = creds_provider.getAuth() if creds_provider else None

        if creds is not None:
            raw_request.auth = creds

        # Build all headers
        headers = dict(self.headers)
        if self.dynamic_header is not None:
            headers.update(self.dynamic_header(request))

        return raw_request.prepare()

    def send(self, request, session=None):
        """
        Send the given request and return a response.

        Arguments:
            request - The request that is prepped to send

        Keywords:
            session - If a session is provided it will be used and added
                        onto with any defined session settings. If no session
                        is provided, a default one is created and settings
                        applied to it.
        """
        session = self.build_session(session)

        return session.send(request)

    def build_and_send(self, raw_request, session=None):
        """
        Wrapper method to handle prepping the request (build method) and
        sending it which also involves setting up the request session.
        """
        prepped = self.build(raw_request)
        return self.send(prepped, session=session)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
