from webenmr.tests import *

class TestStatisticsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='statistics', action='index'))
        # Test response...
