# -*- coding: utf-8 -*-

from sqlalchemy.orm import object_session

"""
This module contains the classes for the models.
"""

class BaseModel(object):
    """
    BaseModel provides a base object with a set of generic functions
    """
    @classmethod
    def populate(cls, **kwargs):
        """
        Creates an instance of a class and populates it, returning the instance
        """
        me = cls()
        keys = kwargs.keys()
        for key in keys:
            me.__setattr__(key, kwargs[key])
        return me


class Users(BaseModel):

    def __str__(self):
        return self.email
    
    def has_access(self, permission):

        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission:
                    return True
        return False
    
 
class MyProxy(BaseModel):

    def __str__(self):
        return self.myproxy
    
    
class Projects(BaseModel):

    def __str__(self):
        return self.name

    
class CalculationTipology(BaseModel):

    def __str__(self):
        return self.name


class Calculations(BaseModel):
    
    def __str__(self):
        return self.name


class Jobs(BaseModel):
    
    def __str__(self):
        return self.guid
    
    
class Role(BaseModel):

    def __str__(self):
        return self.name

    
class Permissions(BaseModel):
    
    def __str__(self):
        return self.name
    
    
class Menu(BaseModel):
    
    def __str__(self):
        return self.name

    def can_show(self, member):
        if member is None:
            return False
        if len(self.permissions) == 0:
            return True;
        for permission in self.permissions:
            if member.has_access(permission.name):
                return True
        return False
