from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import getpass


class Spyder(object):
    """spyder class."""
    name = 'LinkedSpider'
    """name of spyder"""
    login_page = 'https://www.linkedin.com/uas/login'
    """the login page"""
    start_urls = [
        'https://www.linkedin.com/search/results/index/?keywords=Gerente%20de%20marketing&origin=GLOBAL_SEARCH_HEADER',
        'https://www.linkedin.com/search/results/index/?keywords=Diretor%20de%20marketing&origin=GLOBAL_SEARCH_HEADER'
    ]
    """urls to scrapy"""
    user_login = ''
    """user login"""
    user_password = ''
    """user password"""

    def __init__(self):
        print 'Starting spyder ' + self.name
        self.driver = webdriver.Firefox()

    def set_params(self, username, password):
        """set parameters before begin spyder."""
        self.user_login = username
        self.user_password = password

    def find_by_xpath(self, xpath):
        """find element using xpath"""
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
        return element

    def parse_items(self):
        """parse items of the current page"""
        for item in self.driver.find_elements_by_class_name(
            'search-results__primary-cluster search-results__container'):
            print 'item ' + item

    def find_by_name(self, name):
        """find element by name"""
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_name(name))
        return element

    def find_by_id(self, id):
        """find element by id"""
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_id(id))
        return element

    def wait_for_title(self, title):
        """wait for the page to change title"""
        print 'old title -->' + self.driver.title
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.title.lower().startswith(title))
        print 'new title -->' + self.driver.title

    def wait_for_different_title(self, title):
        """wait for the page to change to a differente of the current"""
        print 'old title -->' + self.driver.title
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: self.driver.title != title)
        print 'new title -->' + self.driver.title

    def get_last_title(self):
        """get the current title of the page"""
        return self.driver.title

    def login(self):
        """make login at the page"""
        self.driver.get(self.login_page)
        self.find_by_name('session_key').send_keys(self.user_login)
        self.find_by_name('session_password').send_keys(self.user_password)
        self.find_by_name('session_password').send_keys(Keys.ENTER)
        self.wait_for_title('linkedin')

    def navigate(self):
        """navigate at pages to scrapy"""
        for site in self.start_urls:
            self.scrapy_page(site)

    def scrapy_page(self, url):
        """scrapy the current page"""
        last_page_title = self.get_last_title()
        self.driver.get(url)
        #crawl
        self.parse_items()
        self.wait_for_different_title(last_page_title)


spyder = Spyder()

username_param = getpass.getpass(prompt='Username: ')
password_param = getpass.getpass(prompt='Password: ')

spyder.set_params(username=username_param, password=password_param)
spyder.login()
spyder.navigate()