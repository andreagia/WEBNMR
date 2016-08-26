from webenmr.tests import *

class TestXplorController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='xplor', action='index'))
        # Test response...
