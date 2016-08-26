from webenmr.tests import *

class TestCalculationsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='calculations', action='index'))
        # Test response...
