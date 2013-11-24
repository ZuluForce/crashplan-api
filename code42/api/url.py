'''
Created on Nov 23, 2013

@author: planeman
'''


def code42UrlBuilder(target, vresource, session):
    """
    Arguments:
        target - (string) The host that the url should target
        req_info - (APISession) Request information

    Examples:
    >>> from code42.api.auth import APISession
    >>> from code42.api.resources import computer
    >>> sess = APISession()
    >>> sess.setResourceVersion(computer.ComputerVersion0).setSsl(True) # doctest: +ELLIPSIS
    <...
    >>> sess.setUrlId(10) # doctest:+ELLIPSIS
    <...
    >>> code42UrlBuilder('myhost.com', sess)
    'https://myhost.com/api/v0/Computer/10'
    >>> sess.setUrlId(None) # doctest:+ELLIPSIS
    <...
    >>> code42UrlBuilder('myhost.com', sess)
    'https://myhost.com/api/v0/Computer'
    """

    base_pattern = "{}/api/v{}/{}{}"
    ssl = session.getSsl()

    full_pattern = "http{}://{}".format('s' if ssl else '', base_pattern)

    url_id = session.getUrlId()

    resource = vresource.resource
    version = vresource.getMaxVersion()  # Use the highest api version

    # Build the url
    return full_pattern.format(target, version, resource.getName(), '/'+str(url_id) if url_id else '')