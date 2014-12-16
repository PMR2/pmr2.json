import unittest
import json
from cStringIO import StringIO

from z3c.form.testing import setUp
from z3c.form.testing import setupFormDefaults
from z3c.form.testing import tearDown

from pmr2.json.hal import core

from pmr2.json.hal.testing import TestRequest
from pmr2.json.hal.testing import model
from pmr2.json.hal.testing import form
from pmr2.json.hal.testing import interfaces


"""
# XXX issues
- Options are applied not consistently? figure out how to make it be
  part of an object or not?
- Namespace for the types?  How pedantic do we want to map everything
  between z3c forms and this.
- Why are standards so hard.
"""


class CollectionsTestCase(unittest.TestCase):
    """
    Collections+JSON test case.
    """

    def setUp(self):
        setUp(self)
        setupFormDefaults()
        self.item = model.Item()
        self.option = model.Option()
        self.request = TestRequest()

    def tearDown(self):
        tearDown(self)

    def test_base_render(self):
        f = form.ItemBaseForm(self.item, self.request)
        f.update()

        result = core.formfields_to_collection_template(f)

        answer = json.loads("""
        {
            "data": [
                {
                    "name": "item_id", "value": "", "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "The unique identifier for this item."
                },
                {
                    "name": "name", "value": "", "prompt": "Name",
                    "type": "TextLine", "required": true,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "Name of this item."
                },
                {
                    "name": "description", "value": "",
                    "prompt": "Description",
                    "type": "TextLine", "required": false,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "The description of this item."
                }
            ]
        }
        """)

        self.assertEqual(result, answer)
        self.assertEqual(result, f._collection['collection']['template'])

    def test_handler_render(self):
        """
        Show that the handlers are also added into the data field, as
        the Collection+JSON has this undefined, and that at the protocol
        level (for both ``application/x-www-form-urlencoded`` and
        ``multipart/form-data`` encode "buttons" like any other field
        anyway.  We will have type to distinguish between the standard
        inputs and those that have attached handlers.
        """

        f = form.ItemForm(self.item, self.request)
        f.update()

        result = core.formfields_to_collection_template(f)

        answer = json.loads("""
        {
            "data": [
                {
                    "name": "item_id", "value": "", "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "The unique identifier for this item."
                },
                {
                    "name": "name", "value": "", "prompt": "Name",
                    "type": "TextLine", "required": true,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "Name of this item."
                },
                {
                    "name": "description", "value": "",
                    "prompt": "Description",
                    "type": "TextLine", "required": false,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "The description of this item."
                },
                {
                    "name": "save", "value": null,
                    "type": "Button", "required": false,
                    "prompt": "Save",
                    "prefix": "json.buttons.",
                    "description": null
                },
                {
                    "name": "save_notify", "value": null,
                    "type": "Button", "required": false,
                    "prompt": "Save and Notify",
                    "prefix": "json.buttons.",
                    "description": null
                }
            ]
        }
        """)

        self.assertEqual(result, answer)
        self.assertEqual(result, f._collection['collection']['template'])

    def test_choice_render(self):
        """
        Choice rendering
        """

        f = form.OptionForm(self.option, self.request)
        f.update()

        result = core.formfields_to_collection_template(f)

        # XXX the --NOVALUE-- token really needs rethinking.  Plone
        # does not seem to let mapping of these things to be done nicely
        answer = json.loads("""
        {
            "data": [
                {
                    "name": "item_id", "value": "", "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "prefix": "json.widgets.",
                    "description":
                        "The item id that this option is attached to."
                },
                {
                    "name": "option", "value": [], "prompt": "Option",
                    "type": "Choice", "required": false,
                    "prefix": "json.widgets.",
                    "options": [
                        {"value": "--NOVALUE--", "text": "No value"},
                        {"value": "small", "text": "small"},
                        {"value": "medium", "text": "medium"},
                        {"value": "large",  "text": "large"}
                    ],
                    "description": "The desired option."
                },
                {
                    "name": "submit", "value": null,
                    "type": "Button", "required": false,
                    "prefix": "json.buttons.",
                    "prompt": "Submit",
                    "description": null
                }
            ]
        }
        """)

        self.assertEqual(result, answer)
        self.assertEqual(result, f._collection['collection']['template'])

    def test_update_json_collection_form(self):
        request = TestRequest(stdin=StringIO('''{ "template": {
            "data": [
                {
                    "name": "item_id", "value": 2,
                    "prefix": "json.widgets."
                },
                {
                    "name": "name", "value": "The Name",
                    "prefix": "form.widgets."
                }
            ]
        }}'''))

        f = form.ItemForm(self.item, request)
        core.update_json_collection_form(f)
        self.assertEqual(request.form['json.widgets.item_id'], 2)
        self.assertEqual(request.form['form.widgets.name'], 'The Name')

    def test_submit_error(self):
        request = TestRequest(stdin=StringIO('''{ "template": {
            "data": [
                {
                    "name": "item_id", "value": "TestItem\\nID",
                    "prefix": "json.widgets."
                },
                {
                    "name": "name", "value": "A Test Item Name",
                    "prefix": "json.widgets."
                },
                {
                    "name": "description", "value": "This describes the item.",
                    "prefix": "json.widgets."
                },
                {
                    "name": "save", "value": 1,
                    "prefix": "json.buttons."
                }
            ]
        }}'''))

        f = form.ItemForm(self.item, request)
        f.update()
        result = core.formfields_to_collection_template(f)

        answer = json.loads("""
        {
            "data": [
                {
                    "name": "item_id", "value": "TestItem\\nID",
                    "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "The unique identifier for this item."
                },
                {
                    "name": "name", "value": "A Test Item Name",
                    "prompt": "Name",
                    "type": "TextLine", "required": true,
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "Name of this item."
                },
                {
                    "name": "description", "value": "This describes the item.",
                    "type": "TextLine", "required": false,
                    "prompt": "Description",
                    "prefix": "json.widgets.",
                    "options": null,
                    "description": "The description of this item."
                },
                {
                    "name": "save", "value": null,
                    "type": "Button", "required": false,
                    "prefix": "json.buttons.",
                    "prompt": "Save",
                    "description": null
                },
                {
                    "name": "save_notify", "value": null,
                    "type": "Button", "required": false,
                    "prefix": "json.buttons.",
                    "prompt": "Save and Notify",
                    "description": null
                }
            ]
        }
        """)

        # XXX value for the save MUST be indicated somehow...

        self.assertEqual(result, answer)
        self.assertEqual(result, f._collection['collection']['template'])

        # XXX also need to deal with error, should test the functions
        # that f.update() called individually


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CollectionsTestCase))
    return suite
