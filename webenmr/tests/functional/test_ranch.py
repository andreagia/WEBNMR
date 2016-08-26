from webenmr.tests import *

class TestRanchController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='ranch', action='index'))
        # Test response...
