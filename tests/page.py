# -*- coding: utf-8 -*-

import urlparse

import os
from selenium.common.exceptions import NoSuchElementException
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


class MainPage(Page):
    def __init__(self, driver, user):
        super(MainPage, self).__init__(driver)
        self.PATH = user

    # def get


class PhotosPage(Page):
    def __init__(self, driver, user):
        super(PhotosPage, self).__init__(driver)
        self.PATH = user + '/photos'

    def photos(self):
        return Photos(self.driver)


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class Photos(Component):
    UPLOAD = '//span[@class="html5-link_w js-fileapi-wrapper photo_upload_btn"]'
    # UPLOAD
    PHOTO = '//a[@class="photo-card_cnt"]'
    RESULT = '//div[@data-l="t,image"]'
    FULLSCREEN = '//i[@class="tico_img ic ic_full-scr"]'

    MAKEMAIN = '//i[@class="tico_img ic ic_i_mainPhoto"]'
    FRAME_AREA = '//div[@class="jcrop-tracker"]'
    SUBMITMAIN = '//button[@class="js-doCrop button-pro"]'

    CLOSE_OVERLAY = '//div[@data-l="t,closeOverlay"]'
    CLOSE_BUTTON = '//div[@data-l="t,close"]'

    MINIMIZE_BUTTON = '//div[@class="ic photo-layer_fullscreen_btn __enabled"]'

    DELETE = '//i[@class="tico_img ic ic_delete"]'
    RESTORE = '//a[contains(text(), "Восстановить")]'

    DESCRIPTION_BUTTON = '//span[@class="tico_txt"]'
    DESCRIPTION_FIELD = '//textarea[@class="js-textarea itx photo-layer_descr_ceditable"]'
    DESCRIPTION_SAVE = '//input[@class="button-pro __small form-actions_yes"]'
    DESCRIPTION = '//span[contains(text(), "{}")]'

    SHOW_LINK = '//span[contains(text(), "Получить ссылку")]'
    LINK = '//input[@class="photo-layer_get-link_ac"]'

    BACK = '//span[@class="tico tico__12"][contains(text(), "Вернуться")]'
    SUCCESS = '//div[@class="js-show-controls"]'
    ALBUM = '//span[@class="portlet_h_name_t"]/a[@class="o"]'


    def upload_photo(self):
        self.driver.find_element_by_xpath(self.UPLOAD).click()
        self.driver.find_element_by_xpath(
            '//input[@type="file"][@name="photo"][not(@value)]').send_keys(os.path.join(os.getcwd(), 'tests/photos/img.jpg'))
        try:
            expected_conditions.visibility_of_element_located((By.XPATH, self.SUCCESS))
            self.driver.find_element_by_xpath(self.BACK).click()
        except NoSuchElementException:
            self.driver.find_element_by_xpath(self.ALBUM).click()

        href = self.driver.find_element_by_xpath(self.PHOTO).get_attribute('href').split('/')
        return href[len(href) - 1]

    def get_photos_count(self):
        return len(self.driver.find_elements_by_xpath(self.PHOTO))

    def click_on_photo(self, user, id):
        self.driver.find_element_by_xpath('//a[@class="photo-card_cnt"][@href!="/{}/pphotos/{}"]'.format(user, id)).click()

    def check_photo_opened(self):
        expected_conditions.visibility_of_element_located((By.XPATH, self.RESULT))
        self.driver.find_element_by_xpath(self.RESULT)

    def open_photo(self, user, id):
        self.click_on_photo(user, id)
        self.check_photo_opened()

    def open_fullscreen(self):
        self.driver.find_element_by_xpath(self.FULLSCREEN).click()

    def check_fullscreen_opened(self):
        # TODO
        return True

    def click_make_main(self):
        self.driver.find_element_by_xpath(self.MAKEMAIN).click()

    def check_frame_area(self):
        self.driver.find_element_by_xpath(self.FRAME_AREA)

    def submit_main(self, user, id):
        self.open_photo(user, id)
        self.click_make_main()
        self.check_frame_area()
        self.driver.find_element_by_xpath(self.SUBMITMAIN).click()

    def click_overlay(self):
        element = self.driver.find_element_by_xpath(self.CLOSE_OVERLAY)
        self.driver.execute_script("arguments[0].click();", element)

    def click_close(self):
        self.driver.find_element_by_xpath(self.CLOSE_BUTTON).click()

    def check_photo_dissapeared(self):
        return len(self.driver.find_elements_by_xpath(self.RESULT)) == 0

    def click_delete(self):
        self.driver.find_element_by_xpath(self.DELETE).click()

    def click_restore(self):
        self.driver.find_element_by_xpath(self.RESTORE).click()

    def add_description(self, text):
        self.driver.find_element_by_xpath(self.DESCRIPTION_BUTTON).click()
        expected_conditions.visibility_of_element_located((By.XPATH, self.DESCRIPTION_FIELD))
        self.driver.find_element_by_xpath(self.DESCRIPTION_FIELD).send_keys(text)
        self.driver.find_element_by_xpath(self.DESCRIPTION_SAVE).click()

    def check_description(self, text):
        expected_conditions.visibility_of_element_located((By.XPATH, self.DESCRIPTION.format(text)))

    def get_link(self):
        self.driver.find_element_by_xpath(self.SHOW_LINK).click()
        expected_conditions.visibility_of_element_located((By.XPATH, self.LINK))
        return self.driver.find_element_by_xpath(self.LINK).get_attribute('value')


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
