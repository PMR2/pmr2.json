import unittest
import json

from z3c.form.testing import TestRequest
from z3c.form.testing import setUp
from z3c.form.testing import setupFormDefaults
from z3c.form.testing import tearDown

from pmr2.json.hal import core

from pmr2.json.hal.testing import model
from pmr2.json.hal.testing import form
from pmr2.json.hal.testing import interfaces


class CollectionsTestCase(unittest.TestCase):
    """
    Collections+JSON test case.
    """

    def setUp(self):
        setUp(self)
        setupFormDefaults()
        self.item = model.Item()
        self.request = TestRequest()

    def tearDown(self):
        tearDown(self)

    def test_base_render(self):
        f = form.ItemForm(self.item, self.request)
        f.update()

        result = core.formfields_to_collection_template(f)

        answer = json.loads("""
        {
            "data": [
                {
                    "name": "item_id", "value": null, "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "description": "The unique identifier for this item."
                },
                {
                    "name": "name", "value": null, "prompt": "Name",
                    "type": "TextLine", "required": true,
                    "description": "Name of this item."
                },
                {
                    "name": "description", "value": null,
                    "type": "TextLine", "required": false,
                    "prompt": "Description",
                    "description": "The description of this item."
                }
            ]
        }
        """)

        self.assertEqual(result, answer)


        # for when we do options:
        # {name: "gender", value: "male", prompt: "Gender", options: [
        #     {value: "male", text: "Male"}, 
        #     {value: "female", text: "Female"}
        # ]}


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CollectionsTestCase))
    return suite
