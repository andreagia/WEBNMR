# -*- coding: utf-8 -*-

"""The application's model objects"""

from sqlalchemy.orm import scoped_session, sessionmaker, mapper, relation, backref

from webenmr.model import meta
from webenmr.model.tables import *
from webenmr.model.classes import *


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    sm = sessionmaker(autoflush=True, autocommit=False, bind=engine)
    meta.engine = engine
    meta.Session = scoped_session(sm)


mapper(Users, users_table,
       properties={
           'roles': relation(Role, backref='users',
            secondary=users_roles_table),
           'projects': relation(Projects, backref='users',
                secondary=users_projects_table)
       })

mapper(MyProxy, myproxy_table,
       properties={
           'users': relation(Users, backref='myproxy')
        })

mapper(Projects, projects_table,
       properties={
           'owner': relation(Users, backref='users')
        })

mapper(CalculationTipology, calculation_tipology)

mapper(Calculations, calculations_table,
       properties={
           'project': relation(Projects, backref='calculation'),
           'calc_type': relation(CalculationTipology)
        })

mapper(Jobs, jobs_table,
       properties={
           'calculation': relation(Calculations, backref='job')
        })

mapper(Role, roles_table)

mapper(Permissions, permissions_table,
       properties={
           'roles': relation(Role, backref='permissions',
               secondary=permissions_roles_table)
       })

mapper(Menu, menus_table,
       properties={
           'children': relation(Menu, order_by='weight',
                primaryjoin=menus_table.c.id==menus_table.c.parent_id),
           'sibling': relation(Menu, order_by='weight',
                primaryjoin=menus_table.c.id==menus_table.c.sibling_id),
           'permissions': relation(Permissions, backref='menus',
               secondary=menus_permissions_table),
          
       })
