import json

from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
from z3c.form.form import Form
from z3c.form.form import BaseForm

from pmr2.json.mixin import _disable_csrf_for_webservices
from pmr2.json.mixin import JsonPage
from pmr2.json.interfaces import ISimpleJsonLayer1
from pmr2.json.collection.core import formfields_to_collection_template
from pmr2.json.collection.core import generate_hal
from pmr2.json.collection.core import generate_collection
from pmr2.json.collection.core import update_json_collection_form
from pmr2.json.collection.core import view_url

from pmr2.json.collection.core import json_collection_view_init
from pmr2.json.collection.core import json_collection_view_render
from pmr2.json.layer import set_content_type


@implementer(ISimpleJsonLayer1)
class JsonCollectionFormMixin(Form):
    """
    Mixin for z3c.form type forms that renders JSON+Collection.
    """

    # prefix = 'json.'
    json_mimetype = 'application/vnd.physiome.pmr2.json.1'
    indent = False

    def __init__(self, context, request):
        json_collection_view_init(self)
        super(JsonCollectionFormMixin, self).__init__(context, request)

    def dumps(self, obj):
        return json.dumps(obj, indent=self.indent)

    def update(self):
        """
        Convert JSON input into standard request.
        """

        _disable_csrf_for_webservices(self)
        update_json_collection_form(self)
        super(JsonCollectionFormMixin, self).update()
        self._jc_template = formfields_to_collection_template(self)

        return None

    def render(self):
        """
        Return JSON representation of form if nothing was submitted.

        If something is, return appropriate error or success message.
        """

        return json_collection_view_render(self)

    def extractData(self, *a, **kw):
        result = super(JsonCollectionFormMixin, self).extractData(*a, **kw)
        if result[1]:  # error
            errors = [
                {
                    'name': e.form.prefix + e.form.widgets.prefix +
                            e.field.__name__,
                    'message': e.message,
                } for e in result[1]
            ]
            self._jc_error = {
                'title': 'Error',
                'code': 'error',
                'message': self.formErrorsMessage,
                'errors': errors,
            }
        return result

    def __call__(self):
        if set_content_type(self.request, self.json_mimetype):
            return super(JsonCollectionFormMixin, self).__call__()


class JsonCollectionViewFormMixin(JsonCollectionFormMixin):
    """
    Mixin for z3c.form ViewForms that renders JSON+Collection.
    """

    def update(self):
        # one level above as we don't need the template
        super(JsonCollectionFormMixin, self).update()
        if self.ignoreContext:
            # Can't extract any meaningful thing so we quit.
            # XXX error message?
            return

        self._jc_items = [{
            'data': [{
                'name': key,
                'prompt': self.fields[key].field.title,
                'description': self.fields[key].field.description,
                'value': self.fields[key].field.get(self.context),
            } for key in self.fields.keys()]
        }]


class JsonCollectionAddFormMixin(JsonCollectionFormMixin):

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ""
        return super(JsonCollectionAddFormMixin, self).render()


class JsonCollectionPage(JsonPage):

    json_mimetype = 'application/vnd.physiome.pmr2.json.1'

    def __init__(self, context, request):
        json_collection_view_init(self)
        super(JsonCollectionPage, self).__init__(context, request)

    def render(self):
        return json_collection_view_render(self)


class JsonCollectionCatalogBase(JsonCollectionPage):
    """
    Provide a reusable base class for handling the catalog.
    """

    def make_query(self):
        raise NotImplementedError

    def catalog(self, query):
        return self._catalog(**query)

    def update_jc(self, results):
        """
        Takes a catalog result to populate the self._jc_ attributes.
        """

        self._jc_links = [
            {
                'rel': 'bookmark',
                'href': view_url(self.context, i),
                'prompt': i.Title,
            } for i in results
        ]

        self._jc_items = [{
            'href': '%s/%s' % (self.context.absolute_url(), self.__name__),
            'data': [{
                'name': 'title',
                'value': self.context.title,
                'prompt': 'Title',
            }],
        }]


    def update(self):
        self._catalog = getToolByName(self.context, 'portal_catalog')
        query = self.make_query()
        if query:
            try:
                results = self.catalog(query)
            except:
                self._jc_error = 'input error'
            else:
                self.update_jc(results)


class JsonCollectionCatalogPage(JsonCollectionCatalogBase):
    """
    Basic presentation of a catalog listing as links with the bookmark
    relationship.  This is the most basic and generic form, it makes no
    guarantees as to the linked data will be in the same Collection+JSON
    format.
    """

    portal_type = None

    def make_query(self):
        return {
            'portal_type': self.portal_type,
            'path': [
                u'/'.join(self.context.getPhysicalPath()),
            ],
            'sort_on': 'sortable_title',
        }


class JsonCollectionItemCatalogPage(JsonCollectionCatalogPage):
    """
    This presents the items returned as a list of items, which may be
    used to retrieve a Collection+JSON document, which implies the
    targeted link MUST have a Collection+JSON view.
    """

    def update_jc(self, results):
        """
        Instead of doing them as links these are items.  The linked
        items MUST be able to provided a Collection+JSON view.
        """

        self._jc_items = [{
            'href': view_url(self.context, i),
            'data': [{
                'name': 'title',
                'value': self.context.title,
                'prompt': 'Title',
            }],
        } for i in results]

