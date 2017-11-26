# -*- coding: utf-8 -*-

import unittest

from base_test import BaseTest, USERNAME
from page import PhotosPage, MainPage


class BasePhotoTest(BaseTest):
    def setUp(self):
        super(BasePhotoTest, self).setUp()

        self.photos_page = PhotosPage(self.driver, USERNAME)
        self.photos_page.open()
        self.photos = self.photos_page.photos()


class UploadPhotoTest(BasePhotoTest):
    def test(self):
        self.photos.upload_photo()


class OpenPhotoTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos.open_photo(USERNAME, id)


class OpenFullScreenTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos.open_photo(USERNAME, id)

        self.photos.open_fullscreen()
        self.photos.check_fullscreen_opened()


class MakeMainPhotoTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos.open_photo(USERNAME, id)

        self.photos.click_make_main()
        self.photos.check_frame_area()


class SubmitMainPhotoTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos.submit_main(USERNAME, id)

        self.main_page = MainPage(self.driver, USERNAME)
        self.main_page.open()
        # TODO: Check new photo appeared


class ClosePhotoOverlayTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos.open_photo(USERNAME, id)
        self.photos.click_overlay()
        self.assertTrue(self.photos.check_photo_dissapeared())


class ClosePhotoButtonTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos.open_photo(USERNAME, id)
        self.photos.click_close()
        self.assertTrue(self.photos.check_photo_dissapeared())


class DeletePhotoTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos_page.open()
        count = self.photos.get_photos_count()

        self.photos.open_photo(USERNAME, id)

        self.photos.click_delete()
        self.photos_page.open()
        self.assertEqual(count, self.photos.get_photos_count() + 1)


class RestorePhotoTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos_page.open()
        count = self.photos.get_photos_count()
        self.photos.open_photo(USERNAME, id)
        self.photos.click_delete()

        self.photos.click_restore()
        self.photos_page.open()
        self.assertEqual(count, self.photos.get_photos_count())


class AddDescriptionTest(BasePhotoTest):
    def test(self):
        description = "Some text"
        id = self.photos.upload_photo()
        self.photos.open_photo(USERNAME, id)
        self.photos.add_description(description)

        self.photos.check_description(description)


class ShowLinkTest(BasePhotoTest):
    def test(self):
        id = self.photos.upload_photo()
        self.photos.open_photo(USERNAME, id)
        self.assertEqual(self.driver.current_url, self.photos.get_link())


photos_tests = [
    # unittest.TestSuite((
    #     unittest.makeSuite(UploadPhotoTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(OpenPhotoTest),
    # )),
    unittest.TestSuite((
        unittest.makeSuite(OpenFullScreenTest),
    )),
    # unittest.TestSuite((
    #     unittest.makeSuite(MakeMainPhotoTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(SubmitMainPhotoTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(ClosePhotoOverlayTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(ClosePhotoButtonTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(DeletePhotoTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(RestorePhotoTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(AddDescriptionTest),
    # )),
    # unittest.TestSuite((
    #     unittest.makeSuite(ShowLinkTest),
    # )),
]

