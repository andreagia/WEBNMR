# -*- coding: utf-8 -*-

"""
This module contains the table definitions.
"""

from datetime import datetime
from sqlalchemy import Column, Table, MetaData, ForeignKey, types
from webenmr.model.meta import metadata

"""
Entity tables
"""
# Definition of the "member" table
users_table = Table('users', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('firstname', types.Unicode(30)),
    Column('lastname', types.Unicode(30)),
    Column('logname', types.Unicode(20)),
    Column('email', types.Unicode(50)),
    Column('password', types.Unicode(40)),
    Column('quota', types.Unicode(100)),
    Column('home', types.Unicode(100)),
    Column('cert_present', types.Boolean, default=False),
    Column('dn', types.Unicode(254)),
    Column('hash', types.Unicode(40)),
    Column('removed', types.Boolean, default=False),
    Column('ssoxs_uid', types.Integer),
    Column('access_token', types.Unicode(2048)),
    Column('refresh_token', types.Unicode(2048)),
    Column('iam_subject' , types.Unicode(50)),
    Column('access_tok_creation', types.DateTime),
    Column('refresh_tok_creation', types.DateTime),
    )

myproxy_table = Table('myproxy', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('myproxy', types.Unicode(200)),
    Column('voms_attr', types.Unicode(120)),
    Column('termination_time', types.DateTime),
    Column('user_id', types.Integer, ForeignKey('users.id')),
    Column('user', types.Unicode(30)),
    Column('password', types.Unicode(30)),
    )

projects_table = Table('projects', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('name', types.Unicode(50),nullable=False),
    Column('owner_id', types.Integer, ForeignKey('users.id')),
    Column('creation_date', types.DateTime),
    Column('removed', types.Boolean, default=False),
    )

calculation_tipology = Table('calc_type', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('tipology', types.Unicode(50)),
    )

calculations_table = Table('calculations', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('project_id', types.Integer, ForeignKey('projects.id')),
    Column('calc_type_id', types.Integer, ForeignKey('calc_type.id')),
    Column('name', types.Unicode(100)),
    Column('jobs_to_submit', types.Integer, default=-1),
    Column('creation_date', types.DateTime),
    Column('removed', types.Boolean, default=False),
    )

jobs_table = Table('jobs', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('calculation_id', types.Integer, ForeignKey('calculations.id')),
    Column('guid', types.Unicode(100)),
    Column('status', types.Unicode(20)),
    Column('start_date', types.DateTime),
    Column('log', types.Unicode(254)),
    Column('dir_name', types.Text),
    Column('removed', types.Boolean, default=False),
    Column('submitted_date', types.DateTime),
    Column('waiting_date', types.DateTime),
    Column('ready_date', types.DateTime),
    Column('scheduled_date', types.DateTime),
    Column('running_date', types.DateTime),
    Column('done_date', types.DateTime),
    Column('aborted_date', types.DateTime),
    Column('cancelled_date', types.DateTime),
    Column('unknown_date', types.DateTime),
    Column('cfp2000', types.Float),
    Column('cint2000', types.Float),
    Column('ce', types.Text),
    )

# Definition of the "roles" table
roles_table = Table('roles', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('name', types.Unicode(80), nullable=False, index=True),
    Column('description', types.UnicodeText)
)

# Definition of the "permissions" table
permissions_table = Table('permissions', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('name', types.Unicode(80), nullable=False, index=True),
    Column('description', types.UnicodeText)
)

# Definition of the "menus" table
menus_table = Table('menus', metadata,
    Column('id', types.Integer, primary_key=True),
    Column('parent_id', types.Integer, ForeignKey('menus.id')),
    Column('sibling_id', types.Integer, ForeignKey('menus.id')),
    Column('calctype_id', types.Integer, ForeignKey('calc_type.id')),
    Column('name', types.Unicode(80), nullable=False),
    Column('title', types.Unicode(80)),
    Column('url', types.Unicode(80)),
    Column('weight', types.Integer, index=True)
)


# Definition of the "members_roles" bridging table
users_roles_table = Table('users_roles', metadata,
    Column('user_id', types.Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', types.Integer, ForeignKey('roles.id'), primary_key=True)
)

# Definition of the "permissions_roles" bridging table
permissions_roles_table = Table('permissions_roles', metadata,
    Column('permission_id', types.Integer, ForeignKey('permissions.id'), primary_key=True),
    Column('role_id', types.Integer, ForeignKey('roles.id'), primary_key=True)
)

# Definition of the "menus_permissions" bridging table
menus_permissions_table = Table('menus_permissions', metadata,
    Column('menu_id', types.Integer, ForeignKey('menus.id'), primary_key=True),
    Column('permission_id', types.Integer, ForeignKey('permissions.id'), primary_key=True)
)

users_projects_table = Table('users_projects', metadata,
    Column('user_id', types.Integer, ForeignKey('users.id'), primary_key=True),
    Column('project_id', types.Integer, ForeignKey('projects.id'), primary_key=True)
    )
