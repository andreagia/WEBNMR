# -*- coding: utf-8 -*-

"""Setup the WebENMR application"""
import logging
import hashlib

from webenmr.config.environment import load_environment
from webenmr.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup wwmr2010 here"""
    load_environment(conf.global_conf, conf.local_conf)

    from webenmr.model.meta import Session, metadata
    from webenmr.model import Users, Role, Permissions, Menu, Projects, CalculationTipology
    
    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine, checkfirst=True)

    log.info(u'Creating basic roles...')
    role_admin = Role.populate(name=u'Administrator', description=u'The administrator of the system.')
    role_member = Role.populate(name=u'Member', description=u'A member account')
    role_guest = Role.populate(name=u'Guest', description=u'A guest account')

    log.info(u'Creating permissions...')
    manage_members = Permissions.populate(name=u'Manage Members', description=u'You can modify/remove member')
    create_projects = Permissions.populate(name=u'Create Projects', description=u'You can create Projects')
    manage_account = Permissions.populate(name=u'Manage Account', description=u'You can manage your account')
    run_jobs = Permissions.populate(name=u'Run Jobs', description=u'You can run Jobs')
    fill_amber = Permissions.populate(name=u'Fill Amber', description=u'You can fill Amber form')
    fill_xplor = Permissions.populate(name=u'Fill Xplor', description=u'You can fill Xplor form')
    role_admin.permissions.extend([manage_members, create_projects, run_jobs, fill_amber, fill_xplor])
    role_member.permissions.extend([manage_account, create_projects, run_jobs, fill_amber, fill_xplor])
    role_guest.permissions.extend([fill_amber, fill_xplor])
    
    log.info(u'Creating menus...')
    # Access Menu
    menu_access = Menu.populate(name=u'My Account', weight=1,
        title=u'My Account', url=u'/access')
    menu_access.permissions.append(manage_account)
    #menu_access_proxy = Menu.populate(name=u'Create/Manage your Proxy', weight=1,
    #    title=u'Create and Manage your Proxy', url=u'/access/proxy')
    menu_access_login = Menu.populate(name=u'Accounting', weight=2,
        title=u'Manage Login and Password', url=u'/access')
    menu_access_create = Menu.populate(name=u'Create an account', weight=1,
        title=u'Create an Account', url=u'/access/account_create')
    menu_access_edit = Menu.populate(name=u'Edit your account', weight=2,
        title=u'Edit your Account', url=u'/access/account_edit')
    menu_access.children.extend([menu_access_login])
    menu_access_login.sibling.extend([menu_access_create, menu_access_edit])
    
    # Admin Menu
    menu_admin = Menu.populate(name=u'Admin', weight=1,
        title=u'Administration Menu', url=u'/admin')
    menu_admin.permissions.append(manage_members)
    menu_admin_users = Menu.populate(name=u'Users', weight=1,
        title=u'Users Management', url=u'/admin/users')
    menu_admin_users_create = Menu.populate(name=u'Create', weight=1,
        title=u'Create a new user', url=u'/admin/create_user')
    menu_admin_users_list = Menu.populate(name=u'List', weight=2,
        title=u'Users list', url=u'/admin/users_list')
    menu_admin.children.extend([menu_admin_users])
    menu_admin_users.sibling.extend([menu_admin_users_create, menu_admin_users_list])
    
    # Calculations Menu
    menu_calculations_amber = Menu.populate(name=u'Amber', weight=2,
        title=u'Amber Calculations', url=u'/calculations/amber')
    menu_calculations_amber.permissions.append(fill_amber)
    menu_calculations_amber_start = Menu.populate(name=u'New calculation', weight=1,
        title = u'Start new Amber calculation', url=u'/calculations/amber')
    menu_calculations_amber.children.extend([menu_calculations_amber_start])
    
    
    #menu_calculations_amber = Menu.populate(name=u'Amber', weight=1,
    #    title=u'Amber structure calculations', url=u'/calculations/amber')
    #menu_calculations.children.extend([menu_calculations_amber])
    #menu_calculations_xplor = Menu.populate(name=u'Xplor', weight=1,
    #    title=u'Xplor structure calculation', url=u'/calculations/xplor')
    #menu_calculations_xplor_struct = Menu.populate(name=u'Structure calculation', weight=1,
    #    title=u'Xplor structure calculation', url=u'/calculations/xplor')
    #menu_calculations_xplor_tensor = Menu.populate(name=u'Tensor Convergence', weight=2,
    #    title=u'Xplor structure calculation', url=u'/calculations/xplor_tensor')
    #menu_calculations.children.extend([menu_calculations_xplor])
    #menu_calculations_xplor.sibling.extend([menu_calculations_xplor_struct, menu_calculations_xplor_tensor])
    
    # Projects Menu
    menu_projects = Menu.populate(name=u'Projects', weight=3,
        title=u'Projects management', url=u'/projects')
    menu_projects.permissions.append(create_projects)
    menu_new_project = Menu.populate(name=u'Create', weight=1,
        title=u'Create new project', url=u'/projects/project_create')
    menu_projects_list = Menu.populate(name=u'Manage', weight=2,
        title=u'Projects management', url=u'/projects/list')
    
    menu_projects.children.extend([menu_projects_list, menu_new_project])
    
    # Jobs Menu
    menu_jobs = Menu.populate(name=u'Jobs', weight=3,
        title=u'Jobs Management', url=u'/jobs')
    menu_jobs.permissions.append(run_jobs)
    menu_jobs_show_all = Menu.populate(name=u'Show All', weight=1,
        title=u'Show all jobs', url=u'/jobs/show/all')
    menu_jobs_finished = Menu.populate(name=u'Terminated', weight=2,
        title=u'Show terminated jobs', url=u'/jobs/show/term')
    menu_jobs_running = Menu.populate(name=u'Running', weight=3,
        title=u'Show running jobs', url=u'/jobs/show/run')
    menu_jobs_shceduled = Menu.populate(name=u'Schedules', weight=4,
        title=u'Show schedules jobs', url=u'/jobs/show/sched')
    menu_jobs_cancelled = Menu.populate(name=u'Cancelled', weight=5,
        title=u'Show cancelled jobs', url=u'/jobs/show/canc')
    menu_jobs.children.extend([menu_jobs_show_all, menu_jobs_finished,
                               menu_jobs_running, menu_jobs_shceduled,
                               menu_jobs_cancelled])
    # Converter data
    #menu_converter = Menu.populate(name=u'Converter', weight=4,
    #    title=u'Convert Data', url=u'/converter')
    #menu_upl2tbl = Menu.populate(name=u'Upl to Tbl', weight=1,
    #    title=u'Convert Upl file in Tbl format', url=u'/converter/upl2tbl')
    #menu_converter.children.extend([menu_upl2tbl])
    #
    # Utilities menu
    #menu_utilities = Menu.populate(name=u'Utilities', weight=5,
    #    title=u'Utilities', url=u'/utilities')
    #menu_rsgfs = Menu.populate(name=u'Antechamber topology', weight=1,
    #    title=u'Antechamber topology', url=u'/utilities/antechamber')
    #menu_downt= Menu.populate(name=u'Metal Top&Par creation', weight=2,
    #    title=u'Metal Top&Par creation', url=u'/utilities/metal')
    #menu_utilities.children.extend([menu_rsgfs, menu_downt])
       
    menu_logout = Menu.populate(name=u'Logout', weight=6,
        title=u'Logout', url=u'/users/logout')
    
    menus = [menu_admin, menu_admin_users_list, menu_admin_users_create,
             menu_access, menu_access_login, menu_access_create,
             menu_access_edit,  menu_calculations_amber, 
             menu_projects, menu_projects_list,
             menu_jobs, menu_jobs_show_all, menu_jobs_finished,
             menu_jobs_running, menu_jobs_cancelled,
             menu_logout]

    log.info(u'Creating users...')
    user1 = Users.populate(title=u'Mr', firstname=u'Admin', lastname=u'Admin',
                          email=u'admin@cerm.unifi.it', logname=u'admin',
                          password=unicode(hashlib.sha1('pippo').hexdigest()))
    user1.roles.append(role_admin)
    
    user2 = Users.populate(title=u'Mr', firstname=u'Guest', lastname=u'guest',
                          email=u'guest@cerm.unifi.it', logname=u'guest',
                          password=unicode(hashlib.sha1('guest').hexdigest()))
    user2.roles.append(role_guest)
    
    user3 = Users.populate(title=u'Mr', firstname=u'Andrea', lastname=u'Giachetti',
                          email=u'giachetti@cerm.unifi.it', logname=u'andreagia',
                          password=unicode(hashlib.sha1('pippo').hexdigest()))
    user3.roles.append(role_member)

    user4 = Users.populate(title=u'Mr', firstname=u'Lucio', lastname=u'Ferella',
                          email=u'ferella@cerm.unifi.it', logname=u'ferella',
                          password=unicode(hashlib.sha1('pippo').hexdigest()))
    user4.roles.append(role_member)
    
    #user5 = User.populate(title=u'Mr', firstname=u'David', lastname=u'Case',
    #                      email=u'case@biomaps.rutgers.edu', logname=u'case',
    #                      password=unicode(hashlib.sha1('dav1dcas3').hexdigest()))
    #user5.roles.append(role_member)
    
    #users = [user1, user2, user3, user4, user5]
    users = [user1, user2, user3, user4]
    
    log.info(u'Calculations tiplogy creation...')
    ct1 = CalculationTipology.populate(tipology='xplor')
    ct2 = CalculationTipology.populate(tipology='amber')
    cat = [ct1, ct2]
    
    log.info(u'Committing data to database...')
    Session.add_all(menus)
    Session.add_all(users)
    Session.add_all(cat)
 
    
    
    Session.commit()
    log.info(u'Successfully committed data.')
    
