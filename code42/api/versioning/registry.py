'''
Created on Sep 27, 2013

@author: planeman

The versioning registry tracks known versions of API resources
and makes these easily accessible to the end-user.
'''

from collections import defaultdict

from code42.util.patterns import singleton

class OverlappingResourceVersionException(Exception):
    """
    A resource version cannot be added due to conflicting version
    ranges.
    """
    def __init__(self, resource, conflicts, vrange):
        Exception.__init__(self)

        self.resource = resource
        self.vrange = vrange
        self.conflicts = conflicts

    def __str__(self):
        return "Resource {} has conflicts for range {}: {}".format(self.resource, self.vrange, self.conflicts)


class ResourceRegistry(object):
    __metaclass__ = singleton.Singleton
    def __init__(self):
        self.resource_versions = defaultdict(dict)


    # TODO: Remove requirement for versions parameter. You should be able to get
    # it off the versioncls
    def add_version(self, resource, versionCls, versions):
        """
        Add a resource version satisfying the given version range.

        Raises:
            OverlappingResourceVersionException - When the given version range conflicts with
                an already registered one.
        """
        version_map = self.resource_versions[resource]

        conflicts = self.get_verison_by_range(resource, versions)
        if conflicts is not None and len(conflicts) > 0:
            raise OverlappingResourceVersionException(resource, conflicts, versions)

        version_map[versions] = versionCls


    def get_version(self, resource, version, autoLoad=True):
        """
        Get a resource version by providing a single target version.
        """
        version_map = self.resource_versions.get(resource, None)

        if version_map is None:
            if autoLoad:
                resource.loadAllVersions(self)
                return self.get_version(resource, version, autoLoad=False)

            return None

        for vrange, versionCls in version_map.items():
            low = vrange[0]
            high = vrange[1]
            if version >= low and version <= high:
                return versionCls


    def get_verison_by_range(self, resource, versions):
        """
        Get one or more resource versions falling into the given range.
        """
        version_map = self.resource_versions.get(resource, None)
        if version_map is None:
            return None

        version_set = set()
        for vrange, versionCls in version_map.items():
            if self._check_intersection(vrange, versions):
                version_set.add(versionCls)

        return version_set

    def get_all_versions(self, resource, exclude_ranges=False):
        """
        Get all versions for this resource as a list.

        Examples:
        >>> r = ResourceRegistry()
        >>> r.get_all_versions(object())
        []
        >>> mock_resource = object()
        >>> mock_v1 = object()
        >>> mock_v2 = object()
        >>> r.add_version(mock_resource, mock_v1, (0,1))
        >>> r.get_all_versions(mock_resource)             # doctest: +ELLIPSIS
        [((0, 1), <object...>)]
        >>> r.add_version(mock_resource, mock_v2, (2,4))
        >>> r.get_all_versions(mock_resource)                # doctest: +ELLIPSIS
        [((0, 1), <object...>), ((2, 4), <object...>)]
        >>> len(r.get_all_versions(mock_resource, exclude_ranges=True))
        2
        """
        version_map = self.resource_versions.get(resource, {})

        if exclude_ranges:
            return zip(*version_map.items())[-1]

        return version_map.items()

    def _check_intersection(self, r1, r2):
        """
        Check if the given ranges intersect.

        Examples:
        >>> r = ResourceRegistry()
        >>> r._check_intersection((0,2), (0,2))
        True
        >>> r._check_intersection((0,4), (2,6))
        True
        >>> r._check_intersection((0,4), (4,10))
        True
        >>> r._check_intersection((0,4), (5,10))
        False
        >>> r._check_intersection((6,10), (0,2))
        False
        >>> r._check_intersection((0,10), (4,5))
        True
        """

        intersect_range = range(max(r1[0], r2[0]), min(r1[1], r2[1]) + 1)
        return len(intersect_range) > 0


def get_registry():
    return ResourceRegistry()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
