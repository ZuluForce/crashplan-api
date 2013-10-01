'''
Created on Sep 27, 2013

@author: planeman
'''

import code42.util.http as http

from code42.api.versioning import abstract

class Computer(abstract.ResourceDefinition):
    '''
    The ComputerResource.
    '''
    name = "Computer"


class ComputerVersion0(abstract.VersionedResourceDefinition):
    resource = Computer
    versions = (0, 10)
    methods = (http.verbs.GET, http.verbs.POST)  # @UndefinedVariable


class ComputerVersion1(abstract.VersionedResourceDefinition):
    resource = Computer
    versions = (11, 12)
    methods = (http.verbs.GET)  # @UndefinedVariable
