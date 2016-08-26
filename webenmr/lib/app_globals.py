"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))
        #self.grid_req = """( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-long" );"""
        
        self.grid_req = """( other.GlueCEUniqueID == "ce01.dur.scotgrid.ac.uk:2119/jobmanager-lcgpbs-q6h" || other.GlueCEUniqueID == "deimos.htc.biggrid.nl:2119/jobmanager-pbs-medium" || other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-verylong");"""
        #se funziona il top bdii
        #delf.grid_req = """ other.GlueCEPolicyMaxCPUTime > 1439 && (other.GlueCEInfoHostName == "deimos.htc.biggrid.nl" || other.GlueCEInfoHostName == "pbs-enmr.cerm.unifi.it" ||other.GlueCEInfoHostName == "ce01.dur.scotgrid.ac.uk") """
        
        #self.grid_req = """( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-verylong" );"""
        #self.grid_req = """( other.GlueCEUniqueID == "pbs-enmr.cerm.unifi.it:8443/cream-pbs-long" || other.GlueCEUniqueID == "ce01.dur.scotgrid.ac.uk:2119/jobmanager-lcgpbs-q6h" );"""
        #self.grid_req = """( other.GlueCEUniqueID == "deimos.htc.biggrid.nl:2119/jobmanager-pbs-medium" );"""