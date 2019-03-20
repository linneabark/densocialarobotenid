import time
from selenium import webdriver
from selenium.webdriver.support.select import Select


class WebManager():


    def __init__(self):
        self.driver = webdriver.Safari()

    def findSchema(self):
        self.driver.get('https://cloud.timeedit.net/chalmers/web/public/ri1Q7.html')

        # Select type of search object
        type = self.driver.find_element_by_id('fancytypeselector')
        select = Select(type)
        select.select_by_visible_text('Klass')

        # Search for the class
        search = self.driver.find_element_by_id('ffsearchname')
        search.send_keys('Tkite')
        searchbutton = self.driver.find_element_by_class_name('ffsearchbutton')
        searchbutton.click()

        self.driver.implicitly_wait(10)

        # Choose schema
        klass = self.driver.find_element_by_id('objectbasketitemX1')
        klass.click()

        self.driver.implicitly_wait(10)
        # Open schema
        knapp = self.driver.find_element_by_id('objectbasketgo')
        knapp.click()

        self.driver.implicitly_wait(10)
        time.sleep(1)
        url = self.driver.current_url
        self.driver.get(url)
        self.driver.save_screenshot("test.png")
        self.driver.close()
