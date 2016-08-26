from webenmr.tests import *

class TestFilesystemController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='filesystem', action='index'))
        # Test response...
