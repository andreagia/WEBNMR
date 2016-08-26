from webenmr.tests import *

class TestRestartController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='restart', action='index'))
        # Test response...
