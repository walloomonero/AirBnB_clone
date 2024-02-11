#!/usr/bin/python3
"""The script defines unittests for models/amenity.py.

Unittest classes:
    TestAmenity_save
    TestAmenity_instantiation
    TestAmenity_to_dict
"""
import os
import unittest
import models
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests to test instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        my_amenity = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", my_amenity.__dict__)

    def test_two_amenities_unique_ids(self):
        my_amenity1 = Amenity()
        my_amenity2 = Amenity()
        self.assertNotEqual(my_amenity1.id, my_amenity2.id)

    def test_two_amenities_different_created_at(self):
        my_amenity1 = Amenity()
        sleep(0.05)
        my_amenity2 = Amenity()
        self.assertLess(my_amenity1.created_at, my_amenity2.created_at)

    def test_two_amenities_different_updated_at(self):
        my_amenity1 = Amenity()
        sleep(0.05)
        my_amenity2 = Amenity()
        self.assertLess(my_amenity1.updated_at, my_amenity2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_amenity = Amenity()
        my_amenity.id = "123456"
        my_amenity.created_at = my_amenity.updated_at = dt
        my_amenity_str = my_amenity.__str__()
        self.assertIn("[Amenity] (123456)", my_amenity_str)
        self.assertIn("'id': '123456'", my_amenity_str)
        self.assertIn("'created_at': " + dt_repr, my_amenity_str)
        self.assertIn("'updated_at': " + dt_repr, my_amenity_str)

    def test_args_unused(self):
        my_amenity = Amenity(None)
        self.assertNotIn(None, my_amenity.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_amenity = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_amenity.id, "345")
        self.assertEqual(my_amenity.created_at, dt)
        self.assertEqual(my_amenity.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests to test the save method of an Amenity class."""

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
        my_amenity = Amenity()
        sleep(0.05)
        first_updated_at = my_amenity.updated_at
        my_amenity.save()
        self.assertLess(first_updated_at, my_amenity.updated_at)

    def test_two_saves(self):
        my_amenity = Amenity()
        sleep(0.05)
        first_updated_at = my_amenity.updated_at
        my_amenity.save()
        second_updated_at = my_amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_amenity.save()
        self.assertLess(second_updated_at, my_amenity.updated_at)

    def test_save_with_arg(self):
        my_amenity = Amenity()
        with self.assertRaises(TypeError):
            my_amenity.save(None)

    def test_save_updates_file(self):
        my_amenity = Amenity()
        my_amenity.save()
        my_amenity_id = "Amenity." + my_amenity.id
        with open("file.json", "r") as f:
            self.assertIn(my_amenity_id, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests to test the to_dict method of an Amenity class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_amenity = Amenity()
        self.assertIn("id", my_amenity.to_dict())
        self.assertIn("created_at", my_amenity.to_dict())
        self.assertIn("updated_at", my_amenity.to_dict())
        self.assertIn("__class__", my_amenity.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_amenity = Amenity()
        my_amenity.middle_name = "Holberton"
        my_amenity.my_number = 98
        self.assertEqual("Holberton", my_amenity.middle_name)
        self.assertIn("my_number", my_amenity.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_amenity = Amenity()
        my_amenity_dict = my_amenity.to_dict()
        self.assertEqual(str, type(my_amenity_dict["id"]))
        self.assertEqual(str, type(my_amenity_dict["created_at"]))
        self.assertEqual(str, type(my_amenity_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_amenity = Amenity()
        my_amenity.id = "123456"
        my_amenity.created_at = my_amenity.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_amenity.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_amenity = Amenity()
        self.assertNotEqual(my_amenity.to_dict(), my_amenity.__dict__)

    def test_to_dict_with_arg(self):
        my_amenity = Amenity()
        with self.assertRaises(TypeError):
            my_amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()
