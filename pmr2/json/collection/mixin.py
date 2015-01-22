import json

from zope.interface import implementer
from z3c.form.form import Form
from z3c.form.form import BaseForm

from pmr2.json.mixin import JsonPage
from pmr2.json.interfaces import ISimpleJsonLayer1
from pmr2.json.collection.core import formfields_to_collection_template
from pmr2.json.collection.core import generate_hal
from pmr2.json.collection.core import generate_collection
from pmr2.json.collection.core import update_json_collection_form

from pmr2.json.collection.core import json_collection_view_init
from pmr2.json.collection.core import json_collection_view_render


@implementer(ISimpleJsonLayer1)
class JsonCollectionFormMixin(Form):
    """
    Mixin for z3c.form type forms that renders JSON+Collection.
    """

    prefix = 'json.'
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

        # XXX at some point we need to consider the security and how
        # this might be vulnerable to XSS (for browsers that do not have
        # origin policy support).
        self.disableAuthenticator = True

        update_json_collection_form(self)

        super(JsonCollectionFormMixin, self).update()

        self._jc_template = formfields_to_collection_template(self)

        return None

    def render(self):
        """
        Return JSON representation of form if nothing was submitted.

        If something is, return appropriate error or success message.
        """

        # XXX this is a naive implementation
        # The idea is to capture the widget values and render them.
        self.request.response.setHeader('Content-Type', self.json_mimetype)
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


class JsonCollectionAddFormMixin(JsonCollectionFormMixin):

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ""
        return super(JsonCollectionAddFormMixin, self).render()


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
        json_collection_view_init(self)
        super(JsonCollectionPage, self).__init__(context, request)

    def render(self):
        return json_collection_view_render(self)
