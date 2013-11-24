'''
Created on Sep 27, 2013

@author: planeman

This module contains abstract base classes for defining resources and their
versions.
'''
import logging

from code42.util.exceptions import operations as obj_exceptions
from code42.api.versioning import registry

log = logging.getLogger(__name__)

class ResourceExcpetion(Exception):
    """
    Base exception for api resources.
    """
    pass

class ResourceVersionException(Exception):
    """
    An exception pertaining to a resource version object or its use.
    """
    pass

class MalformedVersionRangeException(ResourceVersionException):
    """
    The resource version range is not valid
    """
    pass

class InvalidReferenceResourceException(ResourceVersionException):
    """
    The resourced referenced by the version is invalid
    """
    pass

class ImmutableClassMeta(type):
    """
    A class providing weak immutablity and uninstantiability for
    classes. There is no attempt to prevent all mutability, just
    the obvious accidental ones.
    """

    def __new__(cls, name, bases, dct):

        def block_init(self):
            raise obj_exceptions.NonInstantiableException("Cannot instantiate resource: " + name)

        dct['__init__'] = block_init
        inst = super(ImmutableClassMeta, cls).__new__(cls, name, bases, dct)

        return inst

    @classmethod
    def __setattr__(cls, *args):
        raise obj_exceptions.UnassignableException("Resource definitions are immutable: " + str(cls))


class ResourceDefinition(object):
    '''
    Abstract base class that other resource definitions should
    extend from.
    '''
    __metaclass__ = ImmutableClassMeta

    @classmethod
    def getName(cls):
        return cls.name

    @classmethod
    def loadAllVersions(cls, registr):
        """
        Load all versions of this resource into the given registry.
        """
        raise Exception("loadAllVersions not implemented for {}".format(cls))

class VersionMetaWrapper(ImmutableClassMeta):
    def __new__(cls, name, bases, dct):
        new_cls = super(VersionMetaWrapper, cls).__new__(cls, name, bases, dct)

        if dct.get('__abstract__', False):
            return new_cls

        # Validate the new resource version
        versions = cls._assert_and_get_versions(new_cls)
        resource = cls._assert_and_get_resource(new_cls)

        registry.get_registry().add_version(resource, new_cls, versions)

        return new_cls

    @classmethod
    def _assert_and_get_versions(cls, new_cls):
        if 'versions' not in dir(new_cls):
            raise obj_exceptions.MissingRequiredProperty(
                                "Missing 'versions' property on resource version {}".format(new_cls))

        versions = new_cls.versions
        try:
            iter(versions)
            assert len(versions) == 2
        except TypeError:
            raise MalformedVersionRangeException("'versions' property is not an iterable")
        except AssertionError:
            raise MalformedVersionRangeException("'versions' must be a 2 element tuple")

        return versions

    @classmethod
    def _assert_and_get_resource(cls, new_cls):
        if 'resource' not in dir(new_cls):
            raise obj_exceptions.MissingRequiredProperty(
                                "Missing 'resource' property on resource version {}".format(new_cls))

        resource = new_cls.resource
        if not issubclass(resource, ResourceDefinition):
            raise InvalidReferenceResourceException("Resource {} is invalid reference for version {}".format(resource, new_cls))

        return resource

class VersionedResourceDefinition(object):
    '''
    Abstract base class for resource version definitions to
    extend from.
    '''
    __metaclass__ = VersionMetaWrapper

    __abstract__ = True

    @classmethod
    def getResource(cls):
        """
        Get the resource this version definition corresponds to.
        """
        return cls.resource

    @classmethod
    def getMaxVersion(cls):
        """
        Get the max api version supported by this definition. The version
        range will be defined in the implementing class.
        """
        return cls.versions[1]
