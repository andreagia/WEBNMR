from webenmr.tests import *

class TestSednmrController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='sedNMR', action='index'))
        # Test response...
