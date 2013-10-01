'''
Created on Sep 27, 2013

@author: planeman
'''
import unittest

from code42.api.resources import computer
from code42.api.versioning import registry

from code42.util.exceptions import operations as op_exceptions


class ComputerResourceTest(unittest.TestCase):

    def testNotAssignable(self):
        with self.assertRaises(op_exceptions.UnassignableException):
            c = computer.Computer
            c.name = "SomeBadValue"

            print c.name

    def testNotInstantiable(self):
        with self.assertRaises(op_exceptions.NonInstantiableException):
            computer.Computer()
            
    def testVersionsInRegistry(self):
        """
        Al versions should be in the registry. When new versions are added update this test.
        """
        versions = registry.get_registry().get_all_versions(computer.Computer, exclude_ranges=True)
        self.assertIn(computer.ComputerVersion0, versions, "Version0 not registered")
        self.assertIn(computer.ComputerVersion1, versions, "Version1 not registered")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
