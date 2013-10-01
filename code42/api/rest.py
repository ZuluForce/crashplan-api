'''
Created on Sep 28, 2013

@author: planeman
'''


class RESTApi(object):
    pass

class CrashPlanApi(object):
    """
    CrashPlan REST api interface. This provides some convenience over using
    the basic RESTApi such as automatically setting the url encoding scheme.
    """
    def get(self, *args, **kwargs):
        pass
    
    def post(self, *args, **kwargs):
        pass

    def cli(self, command):
        pass
