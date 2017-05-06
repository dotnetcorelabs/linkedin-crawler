from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time

class DataOut(object):
    href = ''
    name = ''
    job = ''

class Spyder(object):
    """spyder class."""
    name = 'LinkedSpider'
    """name of spyder"""
    login_page = 'https://www.linkedin.com/uas/login'
    """the login page"""
    start_urls = [
        'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22br%3A6399%22%5D&keywords=gerente%20de%20marketing&origin=GLOBAL_SEARCH_HEADER',
        'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22br%3A6399%22%5D&keywords=Diretor%20de%20marketing&origin=GLOBAL_SEARCH_HEADER'
    ]
    """urls to scrapy"""
    user_login = '{USERNAME-HERE}'
    """user login"""
    user_password = '{PASSWORD-HERE}'
    """user password"""
    items_out = []
    """items to write to file"""
    file_name = "dat_"
    """name of file"""
    max_page = 10

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
        page_index = 1
        next_page = True
        while next_page:
            self.go_to_bottom()
            result_coll = self.driver.find_elements_by_xpath(
                "//div[starts-with(@class, 'search-results__primary-cluster')]/div/ul/li")
            item_index = 1
            for result in result_coll:
                self.go_to_localization(result.location['y'])
                self.parse_item(result, item_index)
                item_index = item_index + 1
            next_page = self.go_to_next_page()
            page_index = page_index + 1
            if next_page:
                next_page = page_index < self.max_page

    def go_to_bottom(self):
        """go to bottom of page"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3 * 2);")
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    def go_to_localization(self, height):
        """go to localization"""
        self.driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        #time.sleep(3)

    def go_to_next_page(self):
        """find the next button and click"""
        try:
            button_next = self.driver.find_element_by_css_selector('button.next')
            button_next.click()
            return True
        except Exception:
            return False

    def parse_item(self, result, index):
        """parse item element of page"""
        item = self.driver.find_element_by_xpath(
            "(//div[starts-with(@class, 'search-results__primary-cluster')]/div/ul/li)[" + str(index) + "]")
        soup = BeautifulSoup(item.get_attribute('innerHTML'))
        a_elem_coll = soup.find_all('a', {"class": "search-result__result-link ember-view"})
        span_elem_name = soup.find_all('span', {"class": "name actor-name"})
        span_elem_job = soup.find_all('p', {'class': 'subline-level-1 Sans-15px-black-85% search-result__truncate'})

        elem_out = DataOut()
        if a_elem_coll:
            elem_out.href = a_elem_coll[0].get('href')

        if span_elem_name:
            elem_out.name = span_elem_name[0].get_text()

        if span_elem_job:
            elem_out.job = span_elem_job[0].get_text()

        self.items_out.append(elem_out)

    def find_by_name(self, name):
        """find element by name"""
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_name(name))
        return element

    def find_by_id(self, data):
        """find element by id"""
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_id(data))
        return element

    def find_elements_by_class_name(self, data):
        """find elements by class name"""
        element = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_elements_by_class_name(data))
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
        indice = 1
        for site in self.start_urls:
            self.scrapy_page(site)
            self.make_csv(self.items_out, indice)
            self.items_out = []
            indice = indice + 1

    def scrapy_page(self, url):
        """scrapy the current page"""
        self.driver.get(url)
        self.find_elements_by_class_name('search-results__cluster-content')
        self.go_to_bottom()
        self.parse_items()


    def make_csv(self, items, index):
        """write data to csv file"""
        with open(self.file_name + str(index) + '.csv', 'wb') as csv_file:
            wr = csv.writer(csv_file, delimiter=',')
            for item in items:
                wr.writerow([item.name.encode('utf-8'), item.href.encode('utf-8'), item.job.encode('utf-8')])

spyder = Spyder()
spyder.login()
spyder.navigate()