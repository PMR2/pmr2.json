from zope.interface import implementer
from z3c.form.form import Form
from z3c.form.form import BaseForm

from pmr2.json.interfaces import ISimpleJsonLayer1
from pmr2.json.hal.core import formfields_to_collection_template
from pmr2.json.hal.core import update_json_collection_form


@implementer(ISimpleJsonLayer1)
class JsonCollectionFormMixin(Form):
    """
    Mixin for z3c.form type forms that renders JSON+Collection.
    """

    prefix = 'json.'
    json_mimetype = 'application/vnd.physiome.pmr2.json.1'

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
        return None

    def render(self):
        """
        Return JSON representation of form if nothing was submitted.

        If something is, return appropriate error or success message.
        """

        # XXX this is a naive implementation
        # The idea is to capture the widget values and render them.
        self.request.response.setHeader('Content-Type', self.json_mimetype)
        return json.dumps(self._collection)
