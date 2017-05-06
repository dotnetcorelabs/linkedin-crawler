from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import getpass

class Spyder(object):
    name = 'LinkedSpider'    
    download_delay = 3
    allowed_domains = ['linkedin.com']
    login_page = 'https://www.linkedin.com/uas/login'
    start_urls = [
    'https://www.linkedin.com/search/results/index/?keywords=Gerente%20de%20marketing&origin=GLOBAL_SEARCH_HEADER',
    'https://www.linkedin.com/search/results/index/?keywords=Diretor%20de%20marketing&origin=GLOBAL_SEARCH_HEADER'
    ]
    user_login = ''
    user_password = ''
    
    def __init__(self):
        print 'Starting spyder ' + self.name
        self.driver = webdriver.Firefox()
        
    def init(self, username, password):
        user_login = user
        user_password = password
    
    def find_by_xpath(locator):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator)))
        return element
    
    def parse_items(self):
        for item in self.driver.find_elements_by_class_name('search-results__primary-cluster search-results__container'):
          print('item ' + item)
        
    def find_by_name(self, name):
        element = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_name(name))
        return element

    def find_by_id(self, id):
        element = WebDriverWait(self.driver, 10).until(lambda driver: self.driver.find_element_by_id(id))
        return element
        
    def wait_for_title(self, title):
        print('old ' + self.driver.title)
        wait = WebDriverWait(self.driver,10)
        wait.until(lambda driver: self.driver.title.lower().startswith(title))
        print('title ' + self.driver.title)
        
    def wait_for_different_title(self, title):
        print('old ' + self.driver.title)
        wait = WebDriverWait(self.driver,10)
        wait.until(lambda driver: self.driver.title != title)
        print('title ' + self.driver.title)
        
    def get_last_title(self):
        return self.driver.title
                
    def login(self):
        self.driver.get(self.login_page)
        self.find_by_name('session_key').send_keys(self.user_login)
        self.find_by_name('session_password').send_keys(self.user_password)
        self.find_by_name('session_password').send_keys(Keys.ENTER)
        #wait for home page
        #self.find_by_id('feed-tab-icon')
        self.wait_for_title('linkedin')
        
    def navigate(self):
        for site in self.start_urls:
            self.scrapy_page(site)
    
    def scrapy_page(self, url):
        last_page_title = self.get_last_title()
        self.driver.get(url)
        #crawl
        self.parse_items()
        self.wait_for_different_title(last_page_title)
        
    
spyder = Spyder()

username = getpass.getpass(prompt='Username: ')
password = getpass.getpass(prompt='Password: ')

spyder.init(username=username, password=password)
spyder.login()
spyder.navigate()