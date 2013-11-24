'''
Created on Sep 28, 2013

@author: planeman
'''
import requests

from functools import wraps


def ApiMethod(method):
    """
    A function decorator which takes in an HTTP verb to facilitate building requests.

    Order of operations:
    * A requests object is built using the method provided to the decorator
    * The wrapped function is called with the raw request and the request builder. The return
        value of the wrapped function is not used.
    * The prepped request is created by passing the Request object to the RequestBuilder's build
        method and saving the return value.
    * The request is sent using a requests Session. If a session was provided to the API method as
        the rsession keyword then it's used, otherwise a fresh Session object is created and used.
    * The return value of Session.send, a requests Response object, is returned.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, target, vresource, apiSession):
            req = requests.Request(method=method)
            func(self, req, apiSession, vresource, target)

            req.url = apiSession.getUrlBuilder()(target, vresource, apiSession)

            return apiSession.build_and_send(req)

        return wrapper

    return decorator

class RESTApi(object):
    """
    A RESTApi instance exposes the http verbs for accessing
    a resource.
    """
    pass

class CrashPlanApi(RESTApi):
    """
    CrashPlan REST api interface. This provides some convenience over using
    the basic RESTApi such as automatically setting the url encoding scheme.
    """

    @ApiMethod('GET')
    def get(self, raw, apiSession, vresource, target):
        """
        Build and send a GET request.
        """
        apiSession.setUrlBuilder(url.code42UrlBuilder)


    @ApiMethod('POST')
    def post(self, builder, apiSession, vresource, target):
        """
        Build and send a POST request.
        """
        apiSession.setUrlBuilder(url.code42UrlBuilder)


    @ApiMethod('PUT')
    def put(self, raw, apiSession, vresource, target):
        """
        Build and send a PUT request.
        """
        apiSession.setUrlBuilder(url.code42UrlBuilder)


    @ApiMethod('DELETE')
    def delete(self, builder, apiSession, vresource, target):
        """
        Build and send a DELETE request.
        """
        apiSession.setUrlBuilder(url.code42UrlBuilder)



if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)