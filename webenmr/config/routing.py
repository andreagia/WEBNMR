"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.connect('cerm', 'http://www.cerm.unifi.it', _static=True)
    map.connect('google', 'http://www.google.it', _static=True)
    #map.connect('SSO_resp_1', 'http://nbk36.cerm.unifi.it/1.html', _static=True)
    #map.connect('SSO_resp_2', 'http://nbk36.cerm.unifi.it/2.html', _static=True)
    #map.connect('SSO_resp_3', 'http://nbk36.cerm.unifi.it/3.html', _static=True)
    #map.connect('SSO_resp_4', 'http://nbk36.cerm.unifi.it/4.html', _static=True)
    #map.connect('SSO_resp_5', 'http://nbk36.cerm.unifi.it/5.html', _static=True)
    #map.connect('SSO_resp_6', 'http://nbk36.cerm.unifi.it/6.html', _static=True)
    map.connect('/', controller='users', action='index', id=None)
    map.connect('/{controller}/', action='index', id=None)
    map.connect(None, '/{controller}/{action}')
    map.connect(None, '/{controller}/{action}/{id}')
    return map
