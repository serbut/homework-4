import unittest

from base_test import BaseTest, USERNAME
from page import PhotosPage


class BasePhotoTest(BaseTest):
    def setUp(self):
        super(BasePhotoTest, self).setUp()

        self.photos_page = PhotosPage(self.driver, USERNAME)
        self.photos_page.open()
        self.photos = self.photos_page.photos()


class OpenPhotoTest(BasePhotoTest):
    def test(self):
        self.photos.open_photo()
        self.photos.check_photo_opened()


class OpenFullScreenTest(BasePhotoTest):
    def test(self):
        self.photos.open_photo()
        self.photos.check_photo_opened()

        self.photos.open_fullscreen()
        # TODO test


class MakeMainPhotoTest(BasePhotoTest):
    def test(self):
        self.photos.open_photo()
        self.photos.check_photo_opened()

        self.photos.make_main()
        self.photos.check_frame_area()


photos_tests = [
    unittest.TestSuite((
        unittest.makeSuite(OpenPhotoTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(OpenFullScreenTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(MakeMainPhotoTest),
    )),

]

