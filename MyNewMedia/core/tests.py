"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class SeleniumTests(LiveServerTestCase):
    fixtures = ['user-data.json']
    
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()
        
    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
        
    def test_search(self):
        
        
    def test_user_home(self):
        
    
    def test_subscriptions(self):
        
        
    def test_channel_manager(self):
        
        
    def test_channel_home(self):    
    
    
    def test_feed_pull(self):
    
    
    def test_logout(self):
        
        
    def test_splash(self):
        
        
        
class PackageTests(TestCase):
    def setUpClass(self):
        
    def test_messages(self):
        
    def test_tags(self):
        
    def test_counter(self):
        
    def test_registration(self):
        
    def test_feed(self):


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
