#!/usr/bin/python3
"""The script defines unittests for models/state.py.

Unittest classes:
    TestState_instantiation
    TestState_to_dict
    TestState_save
"""
import os
import models
import unittest
from datetime import datetime
from models.state import State
from time import sleep


class TestState_instantiation(unittest.TestCase):
    """Unittests to test the instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        my_state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(my_state))
        self.assertNotIn("name", my_state.__dict__)

    def test_two_states_unique_ids(self):
        my_state1 = State()
        my_state2 = State()
        self.assertNotEqual(my_state1.id, my_state2.id)

    def test_two_states_different_created_at(self):
        my_state1 = State()
        sleep(0.05)
        my_state2 = State()
        self.assertLess(my_state1.created_at, my_state2.created_at)

    def test_two_states_different_updated_at(self):
        my_state1 = State()
        sleep(0.05)
        my_state2 = State()
        self.assertLess(my_state1.updated_at, my_state2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_state = State()
        my_state.id = "123456"
        my_state.created_at = my_state.updated_at = dt
        my_state_str = my_state.__str__()
        self.assertIn("[State] (123456)", my_state_str)
        self.assertIn("'id': '123456'", my_state_str)
        self.assertIn("'created_at': " + dt_repr, my_state_str)
        self.assertIn("'updated_at': " + dt_repr, my_state_str)

    def test_args_unused(self):
        my_state = State(None)
        self.assertNotIn(None, my_state.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_state = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_state.id, "345")
        self.assertEqual(my_state.created_at, dt)
        self.assertEqual(my_state.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests to test the save method of the State class."""

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
        my_state = State()
        sleep(0.05)
        first_updated_at = my_state.updated_at
        my_state.save()
        self.assertLess(first_updated_at, my_state.updated_at)

    def test_two_saves(self):
        my_state = State()
        sleep(0.05)
        first_updated_at = my_state.updated_at
        my_state.save()
        second_updated_at = my_state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_state.save()
        self.assertLess(second_updated_at, my_state.updated_at)

    def test_save_with_arg(self):
        my_state = State()
        with self.assertRaises(TypeError):
            my_state.save(None)

    def test_save_updates_file(self):
        my_state = State()
        my_state.save()
        my_state_id = "State." + my_state.id
        with open("file.json", "r") as f:
            self.assertIn(my_state_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests to test the to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_state = State()
        self.assertIn("id", my_state.to_dict())
        self.assertIn("created_at", my_state.to_dict())
        self.assertIn("updated_at", my_state.to_dict())
        self.assertIn("__class__", my_state.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_state = State()
        my_state.middle_name = "Holberton"
        my_state.my_number = 98
        self.assertEqual("Holberton", my_state.middle_name)
        self.assertIn("my_number", my_state.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_state = State()
        my_state_dict = my_state.to_dict()
        self.assertEqual(str, type(my_state_dict["id"]))
        self.assertEqual(str, type(my_state_dict["created_at"]))
        self.assertEqual(str, type(my_state_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_state = State()
        my_state.id = "123456"
        my_state.created_at = my_state.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_state.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_state = State()
        self.assertNotEqual(my_state.to_dict(), my_state.__dict__)

    def test_to_dict_with_arg(self):
        my_state = State()
        with self.assertRaises(TypeError):
            my_state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
