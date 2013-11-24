'''
Created on Oct 6, 2013

@author: planeman
'''
from code42.api.versioning.abstract import ResourceDefinition,\
    VersionedResourceDefinition
from code42.api.resources import MAX_VERSION

class ServerEnvResource(ResourceDefinition):
    name = "ServerEnv"

class ServerEnvVersionAll(VersionedResourceDefinition):
    resource = ServerEnvResource
    version = (0,MAX_VERSION)