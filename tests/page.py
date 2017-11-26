# -*- coding: utf-8 -*-

import urlparse

import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


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
    @property
    def form(self):
        return AuthForm(self.driver)


class MainPage(Page):
    PHOTO = '//a[@class="card_wrp"]'

    def __init__(self, driver, user):
        super(MainPage, self).__init__(driver)
        self.PATH = user

    def get_photo_id(self):
        href = self.driver.find_element_by_xpath(self.PHOTO).get_attribute('href').split('/')
        return href[len(href) - 1]


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
    TOP = '//div[@class="mainTopContentRow"]'

    UPLOAD = '//input[@title="Добавить фото"]'
    DESC = '//div[@class="photo-crop"]'
    UPLOADED = '//div[@class="h-mod __uploaded"]'

    PREVIEW = '//a[@class="photo-card_cnt"]'
    PHOTO = '//a[@class="photo-card_cnt"][@href="/{}/pphotos/{}"]'
    COUNT = '//div[@id="hook_Block_UserStreamPhotosV2Block"]//span[@class="portlet_h_name_aux lstp-t"]'
    RESULT = '//div[@data-l="t,image"]'

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

    COMMENT_ADD = '//div[@class="itx js-comments_add js-ok-e comments_add-ceditable "]'
    COMMENT_SAVE = '//button[@class="button-pro form-actions_yes"]'
    COMMENT = '//div[@class="comments_text textWrap"]'

    BACK = '//span[@class="tico tico__12"][contains(text(), "Вернуться назад")]'
    ALBUM = '//span[@class="portlet_h_name_t"]/a[@class="o"]'

    def upload_photo(self):
        expected_conditions.visibility_of_element_located((By.XPATH, self.TOP))
        self.driver.find_element_by_xpath(self.UPLOAD).send_keys(os.path.join(os.getcwd(), 'tests/photos/img.jpg'))
        expected_conditions.visibility_of_element_located((By.XPATH, self.UPLOADED))
        self.driver.implicitly_wait(1)

        if len(self.driver.find_elements_by_xpath(self.BACK)) != 0:
            self.driver.find_element_by_xpath(self.BACK).click()
        else:
            self.driver.find_element_by_xpath(self.ALBUM).click()

        self.driver.implicitly_wait(5)
        href = self.driver.find_element_by_xpath(self.PREVIEW).get_attribute('href').split('/')
        return href[len(href) - 1]

    def get_photos_count(self):
        return int(self.driver.find_element_by_xpath(self.COUNT).text)

    def click_on_photo(self, user, id):
        expected_conditions.visibility_of_element_located((By.XPATH, self.PHOTO.format(user, id)))
        self.driver.find_element_by_xpath(self.PHOTO.format(user, id)).click()

    def check_photo_opened(self):
        expected_conditions.visibility_of_element_located((By.XPATH, self.RESULT))
        self.driver.find_element_by_xpath(self.RESULT)

    def open_photo(self, user, id):
        self.click_on_photo(user, id)
        self.check_photo_opened()

    def click_make_main(self):
        overlay = self.driver.find_element_by_xpath(self.MAKEMAIN)
        self.driver.execute_script("arguments[0].click();", overlay)

    def check_frame_area(self):
        expected_conditions.visibility_of_element_located((By.XPATH, self.FRAME_AREA))
        self.driver.find_element_by_xpath(self.FRAME_AREA)

    def submit_main(self, user, id):
        self.open_photo(user, id)
        self.click_make_main()
        self.check_frame_area()
        self.driver.find_element_by_xpath(self.SUBMITMAIN).click()

    def click_overlay(self):
        overlay = self.driver.find_element_by_xpath(self.CLOSE_OVERLAY)
        self.driver.execute_script("arguments[0].click();", overlay)

    def click_close(self):
        button = self.driver.find_element_by_xpath(self.CLOSE_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)

    def check_photo_dissapeared(self):
        self.driver.implicitly_wait(1)
        is_dissapeared = len(self.driver.find_elements_by_xpath(self.RESULT)) == 0
        self.driver.implicitly_wait(5)
        return is_dissapeared

    def click_delete(self):
        button = self.driver.find_element_by_xpath(self.DELETE)
        self.driver.execute_script("arguments[0].click();", button)

    def click_restore(self):
        button = self.driver.find_element_by_xpath(self.RESTORE)
        self.driver.execute_script("arguments[0].click();", button)

    def add_description(self, text):
        button_save = self.driver.find_element_by_xpath(self.DESCRIPTION_BUTTON)
        self.driver.execute_script("arguments[0].click();", button_save)

        expected_conditions.visibility_of_element_located((By.XPATH, self.DESCRIPTION_FIELD))
        self.driver.find_element_by_xpath(self.DESCRIPTION_FIELD).send_keys(text)

        button_save = self.driver.find_element_by_xpath(self.DESCRIPTION_SAVE)
        self.driver.execute_script("arguments[0].click();", button_save)

    def check_description(self, text):
        expected_conditions.visibility_of_element_located((By.XPATH, self.DESCRIPTION.format(text)))

    def get_link(self):
        self.driver.find_element_by_xpath(self.SHOW_LINK).click()
        expected_conditions.visibility_of_element_located((By.XPATH, self.LINK))
        return self.driver.find_element_by_xpath(self.LINK).get_attribute('value')

    def add_comment(self, text):
        self.driver.find_element_by_xpath(self.COMMENT_ADD).send_keys(text)
        self.driver.find_element_by_xpath(self.COMMENT_SAVE).click()

    def check_comment(self):
        expected_conditions.visibility_of_element_located((By.XPATH, self.COMMENT))


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
