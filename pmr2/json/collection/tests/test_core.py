import unittest
import json
from cStringIO import StringIO

from z3c.form.testing import setUp
from z3c.form.testing import setupFormDefaults
from z3c.form.testing import tearDown

from pmr2.json.collection import core

from pmr2.json.collection.testing import TestRequest
from pmr2.json.collection.testing import model
from pmr2.json.collection.testing import form
from pmr2.json.collection.testing import interfaces


"""
# XXX issues
- Options are applied not consistently? figure out how to make it be
  part of an object or not?
- Namespace for the types?  How pedantic do we want to map everything
  between z3c forms and this.
- Why are standards so hard.
"""


class CollectionsFormConversionTestCase(unittest.TestCase):
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
                    "name": "form.widgets.item_id",
                    "value": "", "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "description": "The unique identifier for this item."
                },
                {
                    "name": "form.widgets.name", "value": "", "prompt": "Name",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "description": "Name of this item."
                },
                {
                    "name": "form.widgets.description", "value": "",
                    "prompt": "Description",
                    "type": "TextLine", "required": false,
                    "options": null,
                    "description": "The description of this item."
                }
            ]
        }
        """)

        self.assertEqual(result, answer)
        self.assertEqual(result, f._jc_template)

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
                    "name": "form.widgets.item_id",
                    "value": "", "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "description": "The unique identifier for this item."
                },
                {
                    "name": "form.widgets.name",
                    "value": "", "prompt": "Name",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "description": "Name of this item."
                },
                {
                    "name": "form.widgets.description",
                    "value": "",
                    "prompt": "Description",
                    "type": "TextLine", "required": false,
                    "options": null,
                    "description": "The description of this item."
                },
                {
                    "name": "form.buttons.save",
                    "value": null,
                    "type": "Button", "required": false,
                    "prompt": "Save",
                    "description": null
                },
                {
                    "name": "form.buttons.save_notify",
                    "value": null,
                    "type": "Button", "required": false,
                    "prompt": "Save and Notify",
                    "description": null
                }
            ]
        }
        """)

        self.assertEqual(result, answer)
        self.assertEqual(result, f._jc_template)

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
                    "name": "form.widgets.item_id",
                    "value": "", "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "description":
                        "The item id that this option is attached to."
                },
                {
                    "name": "form.widgets.option",
                    "value": [], "prompt": "Option",
                    "type": "Choice", "required": false,
                    "options": [
                        {"value": "--NOVALUE--", "text": "No value"},
                        {"value": "small", "text": "small"},
                        {"value": "medium", "text": "medium"},
                        {"value": "large",  "text": "large"}
                    ],
                    "description": "The desired option."
                },
                {
                    "name": "form.buttons.submit",
                    "value": null,
                    "type": "Button", "required": false,
                    "prompt": "Submit",
                    "description": null
                }
            ]
        }
        """)

        self.assertEqual(result, answer)
        self.assertEqual(result, f._jc_template)

    def test_update_json_collection_form(self):
        request = TestRequest(stdin=StringIO('''{ "template": {
            "data": [
                {
                    "name": "form.widgets.item_id",
                    "value": 2
                },
                {
                    "name": "form.widgets.name",
                    "value": "The Name"
                }
            ]
        }}'''))

        f = form.ItemForm(self.item, request)
        core.update_json_collection_form(f)
        self.assertEqual(request.form['form.widgets.item_id'], 2)
        self.assertEqual(request.form['form.widgets.name'], 'The Name')

    def test_update_json_collection_form_not_fail(self):
        request = TestRequest(stdin=StringIO('{}'))
        f = form.ItemForm(self.item, request)
        core.update_json_collection_form(f)
        # should not fail.

        request = TestRequest(stdin=StringIO(''))
        f = form.ItemForm(self.item, request)
        core.update_json_collection_form(f)

    def test_submit_error(self):
        request = TestRequest(stdin=StringIO('''{ "template": {
            "data": [
                {
                    "name": "form.widgets.item_id",
                    "value": "TestItem\\nID"
                },
                {
                    "name": "form.widgets.name",
                    "value": "A Test Item Name"
                },
                {
                    "name": "form.widgets.description",
                    "value": "This describes the item."
                },
                {
                    "name": "form.buttons.save",
                    "value": 1
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
                    "name": "form.widgets.item_id",
                    "value": "TestItem\\nID",
                    "prompt": "Item ID",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "description": "The unique identifier for this item."
                },
                {
                    "name": "form.widgets.name",
                    "value": "A Test Item Name",
                    "prompt": "Name",
                    "type": "TextLine", "required": true,
                    "options": null,
                    "description": "Name of this item."
                },
                {
                    "name": "form.widgets.description",
                    "value": "This describes the item.",
                    "type": "TextLine", "required": false,
                    "prompt": "Description",
                    "options": null,
                    "description": "The description of this item."
                },
                {
                    "name": "form.buttons.save",
                    "value": null,
                    "type": "Button", "required": false,
                    "prompt": "Save",
                    "description": null
                },
                {
                    "name": "form.buttons.save_notify",
                    "value": null,
                    "type": "Button", "required": false,
                    "prompt": "Save and Notify",
                    "description": null
                }
            ]
        }
        """)

        self.assertEqual(result, answer)
        self.assertEqual(result, f._jc_template)

        error_answer = json.loads("""
        {
            "title": "Error",
            "code": "error",
            "message": "There were some errors.",
            "errors": [
                {
                    "message": "Constraint not satisfied",
                    "name": "form.widgets.item_id"
                }
            ]
        }
        """)

        self.assertEqual(error_answer, f._jc_error)

        # that item is still unchanged.
        self.assertIsNone(self.item.description)

    def test_submit_applied(self):
        """
        Applies the changes using the standard pattern.
        """

        self.assertIsNone(self.item.item_id)

        request = TestRequest(stdin=StringIO('''{ "template": {
            "data": [
                {
                    "name": "form.widgets.item_id", "value": "TestItem"
                },
                {
                    "name": "form.widgets.name", "value": "A Test Item Name"
                },
                {
                    "name": "form.widgets.description",
                    "value": "This describes the item."
                },
                {
                    "name": "form.buttons.save", "value": 1
                }
            ]
        }}'''))

        f = form.ItemForm(self.item, request)
        f.update()

        self.assertEqual(self.item.item_id, 'TestItem')
        self.assertEqual(self.item.name, 'A Test Item Name')
        self.assertEqual(self.item.description, 'This describes the item.')


class CollectionsUtilsTestCase(unittest.TestCase):

    def test_core_generate_collection_base(self):
        result = core.generate_collection(href='http://www.example.com/')
        self.assertEqual(result, {'collection': {
            'version': '1.0',
            'href': 'http://www.example.com/',
        }})

    def test_core_generate_collection_omitted(self):
        self.assertRaises(TypeError, core.generate_collection,
            href='http://www.example.com/', wrongarg='foo')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(CollectionsFormConversionTestCase))
    suite.addTest(makeSuite(CollectionsUtilsTestCase))
    return suite
