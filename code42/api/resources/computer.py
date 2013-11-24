'''
Created on Sep 27, 2013

@author: planeman
'''

from code42.api.resources import MAX_VERSION
from code42.api.versioning import abstract
import code42.util.http as http


class Computer(abstract.ResourceDefinition):
    '''
    The ComputerResource.
    '''
    name = "Computer"

    @classmethod
    def loadAllVersions(cls, registry):
        registry.add_version(cls, ComputerVersion0, ComputerVersion0.versions)
        registry.add_version(cls, ComputerVersion1, ComputerVersion1.versions)


class ComputerVersion0(abstract.VersionedResourceDefinition):
    resource = Computer
    versions = (0, 0)
    methods = (http.verbs.GET, http.verbs.POST)  # @UndefinedVariable


class ComputerVersion1(abstract.VersionedResourceDefinition):
    resource = Computer
    versions = (1, MAX_VERSION)
    methods = (http.verbs.GET)  # @UndefinedVariable
