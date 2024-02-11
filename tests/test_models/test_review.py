#!/usr/bin/python3
"""The script defines unittests for models/review.py.

Unittest classes:
    TestReview_save
    TestReview_to_dict
    TestReview_instantiation
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Unittests to test the instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        my_review = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(my_review))
        self.assertNotIn("place_id", my_review.__dict__)

    def test_user_id_is_public_class_attribute(self):
        my_review = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(my_review))
        self.assertNotIn("user_id", my_review.__dict__)

    def test_text_is_public_class_attribute(self):
        my_review = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(my_review))
        self.assertNotIn("text", my_review.__dict__)

    def test_two_reviews_unique_ids(self):
        my_review1 = Review()
        my_review2 = Review()
        self.assertNotEqual(my_review1.id, my_review2.id)

    def test_two_reviews_different_created_at(self):
        my_review1 = Review()
        sleep(0.05)
        my_review2 = Review()
        self.assertLess(my_review1.created_at, my_review2.created_at)

    def test_two_reviews_different_updated_at(self):
        my_review1 = Review()
        sleep(0.05)
        my_review2 = Review()
        self.assertLess(my_review1.updated_at, my_review2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_review = Review()
        my_review.id = "123456"
        my_review.created_at = my_review.updated_at = dt
        my_review_str = my_review.__str__()
        self.assertIn("[Review] (123456)", my_review_str)
        self.assertIn("'id': '123456'", my_review_str)
        self.assertIn("'created_at': " + dt_repr, my_review_str)
        self.assertIn("'updated_at': " + dt_repr, my_review_str)

    def test_args_unused(self):
        my_review = Review(None)
        self.assertNotIn(None, my_review.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_review = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_review.id, "345")
        self.assertEqual(my_review.created_at, dt)
        self.assertEqual(my_review.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests to test the save method of the Review class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp.json")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp.json", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        my_review = Review()
        sleep(0.05)
        first_updated_at = my_review.updated_at
        my_review.save()
        self.assertLess(first_updated_at, my_review.updated_at)

    def test_two_saves(self):
        my_review = Review()
        sleep(0.05)
        first_updated_at = my_review.updated_at
        my_review.save()
        second_updated_at = my_review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_review.save()
        self.assertLess(second_updated_at, my_review.updated_at)

    def test_save_with_arg(self):
        my_review = Review()
        with self.assertRaises(TypeError):
            my_review.save(None)

    def test_save_updates_file(self):
        my_review = Review()
        my_review.save()
        my_review_id = "Review." + my_review.id
        with open("file.json", "r") as f:
            self.assertIn(my_review_id, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests to test the to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_review = Review()
        self.assertIn("id", my_review.to_dict())
        self.assertIn("created_at", my_review.to_dict())
        self.assertIn("updated_at", my_review.to_dict())
        self.assertIn("__class__", my_review.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_review = Review()
        my_review.middle_name = "Holberton"
        my_review.my_number = 98
        self.assertEqual("Holberton", my_review.middle_name)
        self.assertIn("my_number", my_review.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_review = Review()
        my_review_dict = my_review.to_dict()
        self.assertEqual(str, type(my_review_dict["id"]))
        self.assertEqual(str, type(my_review_dict["created_at"]))
        self.assertEqual(str, type(my_review_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_review = Review()
        my_review.id = "123456"
        my_review.created_at = my_review.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_review.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_review = Review()
        self.assertNotEqual(my_review.to_dict(), my_review.__dict__)

    def test_to_dict_with_arg(self):
        my_review = Review()
        with self.assertRaises(TypeError):
            my_review.to_dict(None)


if __name__ == "__main__":
    unittest.main()
