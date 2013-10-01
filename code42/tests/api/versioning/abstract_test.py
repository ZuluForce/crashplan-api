'''
Created on Sep 27, 2013

@author: planeman
'''
import unittest

from code42.api.versioning import abstract
from code42.util.exceptions import operations

class ValidTestResource(abstract.ResourceDefinition):
    name = "AbstractTestResource"

class AbstractVersioningTest(unittest.TestCase):
    def testBaslineWorks(self):
        """
        The baseline minimum for a resource version is accepted.
        """
        class ValidResourceVersion(abstract.VersionedResourceDefinition):
            resource = ValidTestResource
            versions = (0, 1)
            
        print ValidResourceVersion.resource.name


    def testVersionRequiresRange(self):
        """
        Test that a resource version cannot be declared without defining a
        supported version range.
        """
        with self.assertRaises(operations.MissingRequiredProperty):
            class test_version(abstract.VersionedResourceDefinition):
                resource = ValidTestResource


    def testVersioningRequriresIterableRange(self):
        """
        A resource should only accept a version range that is iterable, ie tuple, list,...
        """
        with self.assertRaises(abstract.MalformedVersionRangeException):
            class test_version(abstract.VersionedResourceDefinition):
                resource = ValidTestResource
                versions = 1

    def testVersioningRequriresTwoPartRange(self):
        """
        A resource should only accept a version range that is iterable, ie tuple, list,...
        """
        with self.assertRaises(abstract.MalformedVersionRangeException):
            class test_version(abstract.VersionedResourceDefinition):
                resource = ValidTestResource
                versions = (0,)

    def testVersioningRequriresResource(self):
        """
        A resource should only accept a version range that is iterable, ie tuple, list,...
        """
        with self.assertRaises(operations.MissingRequiredProperty):
            class test_version(abstract.VersionedResourceDefinition):
                versions = (0, 1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
