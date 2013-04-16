"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client # use the client to mimic a web browser for view tests.


class ChannelModelTests(TestCase):
    def setUpClass(self):
        
        
    def ChannelTest(self):
        
        
    def LinkTest(self):
        
        
    def FeedItemTest(self):
        
        
    def FeedTrackerTest(self):
        
        
class ChannelViewTests(TestCase):
    def setUpClass(self):
        

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
