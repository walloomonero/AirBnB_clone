#!/usr/bin/python3
"""The script defines unittests for models/base_model.py.

Unittest classes:
    TestBaseModel_save
    TestBaseModel_to_dict
    TestBaseModel_instantiation
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests to test instantiation of the BaseModel class."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        my_base_model1 = BaseModel()
        my_base_model2 = BaseModel()
        self.assertNotEqual(my_base_model1.id, my_base_model2.id)

    def test_two_models_different_created_at(self):
        my_base_model1 = BaseModel()
        sleep(0.05)
        my_base_model2 = BaseModel()
        self.assertLess(my_base_model1.created_at, my_base_model2.created_at)

    def test_two_models_different_updated_at(self):
        my_base_model1 = BaseModel()
        sleep(0.05)
        my_base_model2 = BaseModel()
        self.assertLess(my_base_model1.updated_at, my_base_model2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_base_model = BaseModel()
        my_base_model.id = "123456"
        my_base_model.created_at = my_base_model.updated_at = dt
        my_base_model_str = my_base_model.__str__()
        self.assertIn("[BaseModel] (123456)", my_base_model_str)
        self.assertIn("'id': '123456'", my_base_model_str)
        self.assertIn("'created_at': " + dt_repr, my_base_model_str)
        self.assertIn("'updated_at': " + dt_repr, my_base_model_str)

    def test_args_unused(self):
        my_base_model = BaseModel(None)
        self.assertNotIn(None, my_base_model.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_base_model = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_base_model.id, "345")
        self.assertEqual(my_base_model.created_at, dt)
        self.assertEqual(my_base_model.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_base_model = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_base_model.id, "345")
        self.assertEqual(my_base_model.created_at, dt)
        self.assertEqual(my_base_model.updated_at, dt)


class TestBaseModel_save(unittest.TestCase):
    """Unittests to test the save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp.json")
        except IOError:
            pass

    @classmethod
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
        my_base_model = BaseModel()
        sleep(0.05)
        first_updated_at = my_base_model.updated_at
        my_base_model.save()
        self.assertLess(first_updated_at, my_base_model.updated_at)

    def test_two_saves(self):
        my_base_model = BaseModel()
        sleep(0.05)
        first_updated_at = my_base_model.updated_at
        my_base_model.save()
        second_updated_at = my_base_model.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_base_model.save()
        self.assertLess(second_updated_at, my_base_model.updated_at)

    def test_save_with_arg(self):
        my_base_model  = BaseModel()
        with self.assertRaises(TypeError):
            my_base_model.save(None)

    def test_save_updates_file(self):
        my_base_model = BaseModel()
        my_base_model.save()
        my_base_model_id = "BaseModel." + my_base_model.id
        with open("file.json", "r") as f:
            self.assertIn(my_base_model_id, f.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests to test the to_dict method of the BaseModel class."""

    def test_to_dict_type(self):
        my_base_model = BaseModel()
        self.assertTrue(dict, type(my_base_model.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_base_model = BaseModel()
        self.assertIn("id", my_base_model.to_dict())
        self.assertIn("created_at", my_base_model.to_dict())
        self.assertIn("updated_at", my_base_model.to_dict())
        self.assertIn("__class__", my_base_model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_base_model = BaseModel()
        my_base_model.name = "Holberton"
        my_base_model.my_number = 98
        self.assertIn("name", my_base_model.to_dict())
        self.assertIn("my_number", my_base_model.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_base_model = BaseModel()
        my_base_model_dict = my_base_model.to_dict()
        self.assertEqual(str, type(my_base_model_dict["created_at"]))
        self.assertEqual(str, type(my_base_model_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_base_model = BaseModel()
        my_base_model.id = "123456"
        my_base_model.created_at = my_base_model.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(my_base_model.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_base_model = BaseModel()
        self.assertNotEqual(my_base_model.to_dict(), my_base_model.__dict__)

    def test_to_dict_with_arg(self):
        my_base_model = BaseModel()
        with self.assertRaises(TypeError):
            my_base_model.to_dict(None)


if __name__ == "__main__":
    unittest.main()
