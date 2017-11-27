# -*- coding: utf-8 -*-

import unittest

from base_test import BaseTest, USERNAME
from page import PhotosPage, MainPage


class BasePhotoTest(BaseTest):

    def setUp(self):
        super(BasePhotoTest, self).setUp()

        self.added_photos = []

        self.photos_page = PhotosPage(self.driver, USERNAME)
        self.photos_page.open()
        self.photos = self.photos_page.photos()

    def tearDown(self):
        self.photos_page.open()
        for photo in self.added_photos:
            self.delete_photo(photo)
        super(BasePhotoTest, self).tearDown()

    def add_photo(self):
        id = self.photos.upload_photo()
        self.added_photos.append(id)
        self.photos_page.open()
        return id

    def delete_photo(self, id):
        self.photos.open_photo(USERNAME, id)
        self.photos.click_delete()
        self.added_photos.remove(id)


class UploadPhotoTest(BasePhotoTest):
    def test(self):
        self.add_photo()


class OpenPhotoTest(BasePhotoTest):
    def test(self):
        id = self.add_photo()
        self.photos.open_photo(USERNAME, id)


class MakeMainPhotoTest(BasePhotoTest):
    def test(self):
        id = self.add_photo()
        self.photos.open_photo(USERNAME, id)

        self.photos.click_make_main()
        self.photos.check_frame_area()


class SubmitMainPhotoTest(BasePhotoTest):
    def test(self):
        id = self.add_photo()
        self.photos.submit_main(USERNAME, id)

        self.main_page = MainPage(self.driver, USERNAME)
        self.main_page.open()
        self.assertEqual(id, self.main_page.get_photo_id())


class ClosePhotoOverlayTest(BasePhotoTest):
    def test(self):
        id = self.add_photo()
        self.photos.open_photo(USERNAME, id)
        self.photos.click_overlay()
        self.assertTrue(self.photos.check_photo_disappeared())


class ClosePhotoButtonTest(BasePhotoTest):
    def test(self):
        id = self.add_photo()
        self.photos.open_photo(USERNAME, id)
        self.photos.click_close()
        self.assertTrue(self.photos.check_photo_disappeared())


class DeletePhotoTest(BasePhotoTest):
    def test(self):
        id = self.add_photo()
        count = self.photos.get_photos_count()

        self.delete_photo(id)

        self.photos_page.open()
        self.assertEqual(count, self.photos.get_photos_count() + 1)


class RestorePhotoTest(BasePhotoTest):
    def test(self):
        id = self.add_photo()
        self.photos_page.open()
        count = self.photos.get_photos_count()
        self.photos.open_photo(USERNAME, id)
        self.photos.click_delete()

        self.photos.click_restore()
        self.photos.click_close()
        self.photos_page.open()
        self.assertEqual(count, self.photos.get_photos_count())


class AddDescriptionTest(BasePhotoTest):
    def test(self):
        description = "Some description"
        id = self.add_photo()
        self.photos.open_photo(USERNAME, id)
        self.photos.add_description(description)

        self.photos.check_description(description)


class ShowLinkTest(BasePhotoTest):
    def test(self):
        link = "https://ok.ru/{}/pphotos/{}"
        id = self.add_photo()
        self.photos.open_photo(USERNAME, id)
        self.assertEqual(link.format(USERNAME, id), self.photos.get_link())


class AddCommentTest(BasePhotoTest):
    def test(self):
        comment = "Some comment"
        id = self.add_photo()
        self.photos.open_photo(USERNAME, id)
        self.photos.add_comment(comment)

        self.photos.check_comment()


photos_tests = [
    unittest.TestSuite((
        unittest.makeSuite(UploadPhotoTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(OpenPhotoTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(MakeMainPhotoTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(SubmitMainPhotoTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(ClosePhotoOverlayTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(ClosePhotoButtonTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(DeletePhotoTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(RestorePhotoTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(AddDescriptionTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(ShowLinkTest),
    )),
    unittest.TestSuite((
        unittest.makeSuite(AddCommentTest),
    )),
]

