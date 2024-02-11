#!/usr/bin/python3
"""The script defines unittests for models/user.py.

Unittest classes:
    TestUser_instantiation
    TestUser_save
    TestUser_to_dict
"""
import os
import models
import unittest
from models.user import User
from datetime import datetime
from time import sleep


class TestUser_instantiation(unittest.TestCase):
    """Unittests to test the instantiation of the User class."""

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_is_public_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_is_public_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_is_public_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_is_public_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_unique_ids(self):
        my_user1 = User()
        my_user2 = User()
        self.assertNotEqual(my_user1.id, my_user2.id)

    def test_two_users_different_created_at(self):
        my_user1 = User()
        sleep(0.05)
        my_user2 = User()
        self.assertLess(my_user1.created_at, my_user2.created_at)

    def test_two_users_different_updated_at(self):
        my_user1 = User()
        sleep(0.05)
        my_user2 = User()
        self.assertLess(my_user1.updated_at, my_user2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_user = User()
        my_user.id = "123456"
        my_user.created_at = my_user.updated_at = dt
        my_user_str = my_user.__str__()
        self.assertIn("[User] (123456)", my_user_str)
        self.assertIn("'id': '123456'", my_user_str)
        self.assertIn("'created_at': " + dt_repr, my_user_str)
        self.assertIn("'updated_at': " + dt_repr, my_user_str)

    def test_args_unused(self):
        my_user = User(None)
        self.assertNotIn(None, my_user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_user.id, "345")
        self.assertEqual(my_user.created_at, dt)
        self.assertEqual(my_user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests to test the save method of the  class."""

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
        my_user = User()
        sleep(0.05)
        first_updated_at = my_user.updated_at
        my_user.save()
        self.assertLess(first_updated_at, my_user.updated_at)

    def test_two_saves(self):
        my_user = User()
        sleep(0.05)
        first_updated_at = my_user.updated_at
        my_user.save()
        second_updated_at = my_user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_user.save()
        self.assertLess(second_updated_at, my_user.updated_at)

    def test_save_with_arg(self):
        my_user = User()
        with self.assertRaises(TypeError):
            my_user.save(None)

    def test_save_updates_file(self):
        my_user = User()
        my_user.save()
        my_user_id = "User." + my_user.id
        with open("file.json", "r") as f:
            self.assertIn(my_user_id, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the User class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_user = User()
        self.assertIn("id", my_user.to_dict())
        self.assertIn("created_at", my_user.to_dict())
        self.assertIn("updated_at", my_user.to_dict())
        self.assertIn("__class__", my_user.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_user = User()
        my_user.middle_name = "Holberton"
        my_user.my_number = 98
        self.assertEqual("Holberton", my_user.middle_name)
        self.assertIn("my_number", my_user.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_user = User()
        my_user_dict = my_user.to_dict()
        self.assertEqual(str, type(my_user_dict["id"]))
        self.assertEqual(str, type(my_user_dict["created_at"]))
        self.assertEqual(str, type(my_user_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_user = User()
        my_user.id = "123456"
        my_user.created_at = my_user.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_user.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_user = User()
        self.assertNotEqual(my_user.to_dict(), my_user.__dict__)

    def test_to_dict_with_arg(self):
        my_user = User()
        with self.assertRaises(TypeError):
            my_user.to_dict(None)


if __name__ == "__main__":
    unittest.main()
