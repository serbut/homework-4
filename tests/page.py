# -*- coding: utf-8 -*-

import urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class Page(object):
    BASE_URL = 'https://ok.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        # self.driver.maximize_window()
        self.driver.get(url)


class AuthPage(Page):
    PATH = ''

    @property
    def form(self):
        return AuthForm(self.driver)


class PhotosPage(Page):
    PATH = ''

    def __init__(self, driver, user):
        super(PhotosPage, self).__init__(driver)
        self.PATH = user + '/photos'

    def photos(self):
        return Photos(self.driver)


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class Photos(Component):
    PHOTO = '//a[@class="photo-card_cnt"][@href!="/technopark55/pphotos/859093386145"]'
    RESULT = '//div[@data-l="t,image"]'
    FULLSCREEN = '//i[@class="tico_img ic ic_full-scr"]'
    MAKEMAIN = '//i[@class="tico_img ic ic_i_mainPhoto"]'
    FRAME_AREA = '//div[@class="jcrop-tracker"]'
    SUBMITMAIN = '//button[@class="js-doCrop button-pro"]'

    def open_photo(self):
        self.driver.find_element_by_xpath(self.PHOTO).click()

    def check_photo_opened(self):
        expected_conditions.invisibility_of_element_located((By.XPATH, self.RESULT))
        self.driver.find_element_by_xpath(self.RESULT)

    def open_fullscreen(self):
        self.driver.find_element_by_xpath(self.FULLSCREEN).click()

    def make_main(self):
        self.driver.find_element_by_xpath(self.MAKEMAIN).click()

    def check_frame_area(self):
        self.driver.find_element_by_xpath(self.FRAME_AREA)


class AuthForm(Component):
    LOGIN = '//input[@name="st.email"]'
    PASSWORD = '//input[@name="st.password"]'
    SUBMIT = '//input[@data-l="t,loginButton"]'

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, pwd):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()
