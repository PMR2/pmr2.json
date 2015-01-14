import json

from zope.interface import implementer
from z3c.form.form import Form
from z3c.form.form import BaseForm

from pmr2.json.mixin import JsonPage
from pmr2.json.interfaces import ISimpleJsonLayer1
from pmr2.json.hal.core import formfields_to_collection_template
from pmr2.json.hal.core import generate_hal
from pmr2.json.hal.core import generate_collection
from pmr2.json.hal.core import update_json_collection_form


@implementer(ISimpleJsonLayer1)
class JsonCollectionFormMixin(Form):
    """
    Mixin for z3c.form type forms that renders JSON+Collection.
    """

    prefix = 'json.'
    json_mimetype = 'application/vnd.physiome.pmr2.json.1'
    indent = False

    # XXX prefix the following with _json?
    _collection = {}
    _collection_error = {}

    def dumps(self, obj):
        return json.dumps(obj, indent=self.indent)

    def update(self):
        """
        Convert JSON input into standard request.
        """

        # XXX at some point we need to consider the security and how
        # this might be vulnerable to XSS (for browsers that do not have
        # origin policy support).
        self.disableAuthenticator = True

        update_json_collection_form(self)

        super(JsonCollectionFormMixin, self).update()
        self._collection = {
            'collection': {
                'version': '1.0',
                'href': None,  # XXX figure how to determine with fallback
                'template': formfields_to_collection_template(self)
            }
        }

        if self._collection_error:
            self._collection['collection']['error'] = self._collection_error
        return None

    def render(self):
        """
        Return JSON representation of form if nothing was submitted.

        If something is, return appropriate error or success message.
        """

        # XXX this is a naive implementation
        # The idea is to capture the widget values and render them.
        self.request.response.setHeader('Content-Type', self.json_mimetype)
        return self.dumps(self._collection)

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
            self._collection_error = {
                'title': 'Error',
                'code': 'error',
                'message': self.formErrorsMessage,
                'errors': errors,
            }
        return result


class JsonHalPage(JsonPage):

    json_mimetype = 'application/vnd.physiome.pmr2.json.1'

    def __init__(self, context, request):
        super(JsonCollectionPage, self).__init__(context, request)
        self.links = []

    def render(self):
        return self.dumps(generate_hal(self.links, data=self.data))


class JsonCollectionPage(JsonPage):

    json_mimetype = 'application/vnd.physiome.pmr2.json.1'

    def __init__(self, context, request):
        super(JsonCollectionPage, self).__init__(context, request)
        self.links = None
        self.items = None
        self.queries = None
        self.template=None
        self.error = None

    def render(self):
        return self.dumps(generate_collection(
            href=self.context.absolute_url() + '/' + self.__name__,
            links=self.links,
            items=self.items,
            queries=self.queries,
            template=self.template,
            error=self.error,
        ))
