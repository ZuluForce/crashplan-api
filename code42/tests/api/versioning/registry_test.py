'''
Created on Sep 28, 2013

@author: planeman
'''
import unittest

from code42.api.versioning import registry

class ResourceRegistryTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ResourceRegistryTest, self).__init__(*args, **kwargs)
        self.registry = registry.get_registry()

    def testAddVersion(self):
        o = object()
        o2 = object()
        self.registry.add_version(o, o2, (0, 1))

        version = self.registry.get_version(o, 0)
        self.assertEqual(o2, version, "Unable to grab version 0 back from registry")

        version = self.registry.get_version(o, 1)
        self.assertEqual(o2, version, "Unable to grab version 0 back from registry")

    def testMultiVersion(self):
        resource = object()
        versionA = object()
        versionB = object()

        self.registry.add_version(resource, versionA, (0, 10))
        self.registry.add_version(resource, versionB, (11, 11))

        self.assertEqual(versionA, self.registry.get_version(resource, 0), "Failed to get resource by version")
        self.assertEqual(versionA, self.registry.get_version(resource, 5), "Failed to get resource by version")
        self.assertEqual(versionA, self.registry.get_version(resource, 10), "Failed to get resource by version")

        self.assertEqual(versionB, self.registry.get_version(resource, 11), "Failed to get resource by version")
        
        all_versions = self.registry.get_all_versions(resource)
        all_versions = zip(*all_versions)[-1]
        self.assertEqual(2, len(all_versions), "Incorrect total number of versions")
        self.assertTrue(versionA in all_versions, "VersionA not included in all_versions")
        self.assertTrue(versionB in all_versions, "VersionB not included in all_versions")

        all_versions = self.registry.get_verison_by_range(resource, (0, 12))
        self.assertEqual(2, len(all_versions), "Incorrect total number of versions")
        self.assertTrue(versionA in all_versions, "VersionA not included in all_versions")
        self.assertTrue(versionB in all_versions, "VersionB not included in all_versions")

    def testNoOverlappingVersions(self):
        with self.assertRaises(registry.OverlappingResourceVersionException):
            resource = object()
            v1 = object()
            v2 = object()
            self.registry.add_version(resource, v1, (0, 3))
            self.registry.add_version(resource, v2, (3, 5))

    def testIntersectionEqual(self):
        self.assertTrue(self.registry._check_intersection((0, 2), (0, 2)))

    def testIntersectionOffset(self):
        self.assertTrue(self.registry._check_intersection((0, 4), (2, 6)))

    def testIntersectionNested(self):
        self.assertTrue(self.registry._check_intersection((0, 4), (2, 2)))

    def testIntersectionSameEndpoint(self):
        self.assertTrue(self.registry._check_intersection((0, 4), (4, 6)))

    def testNoIntersection(self):
        self.assertFalse(self.registry._check_intersection((0, 4), (5, 10)))

    def testNoIntersectionReversed(self):
        self.assertFalse(self.registry._check_intersection((5, 10), (0, 4)))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
