'''
Created on Nov 23, 2013

@author: planeman
'''
import unittest

import requests

import code42.api.rest as rest
import code42.api.resources.computer as computer

from code42.api.auth import APISession
from code42.util.container import Bunch

class APISessionTest(unittest.TestCase):
    mock_auth = { 'auth_provider' : Bunch(getAuth=lambda: ('x','y')) }

    def testAPISessionPrepRequest(self):
        """
        Test the prepping of a request using the APISession
        """
        s = APISession(**APISessionTest.mock_auth)
        raw_get = requests.Request('GET')
        raw_post = requests.Request('POST')
        raw_put = requests.Request('PUT')
        raw_delete = requests.Request('DELETE')

        url = s.getUrlBuilder()("www.blah.com", computer.ComputerVersion0, s)
        print url

        raw_get.url = url
        raw_post.url = url
        raw_put.url = url
        raw_delete.url = url

        prep_get = s.build(raw_get)
        prep_post = s.build(raw_post)
        prep_put = s.build(raw_put)
        prep_delete = s.build(raw_delete)

        self.assertIsNotNone(prep_get)
        self.assertIsNotNone(prep_post)
        self.assertIsNotNone(prep_put)
        self.assertIsNotNone(prep_delete)

        self.assertEquals(type(prep_get), requests.PreparedRequest)
        self.assertEquals(type(prep_post), requests.PreparedRequest)
        self.assertEquals(type(prep_put), requests.PreparedRequest)
        self.assertEquals(type(prep_delete), requests.PreparedRequest)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()