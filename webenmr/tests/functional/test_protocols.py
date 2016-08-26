from webenmr.tests import *

class TestProtocolsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='protocols', action='index'))
        # Test response...
