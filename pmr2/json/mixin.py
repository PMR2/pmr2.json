import json

import zope.interface
from z3c.form.form import BaseForm

from Products.CMFCore.utils import getToolByName

from pmr2.z3cform.page import SimplePage
from pmr2.json.interfaces import ISimpleJsonLayer
from pmr2.json.utils import extractRequestObj
from pmr2.json.utils import objToRequest
from pmr2.json.layer import set_content_type


class JsonPage(SimplePage):
    """
    Ensure that the custom mimetype is sent.
    """

    indent = None
    # we could derive the mimetype header to send back to client but
    # this needs to wait until complete handling of accept header is
    # done.
    json_mimetype = 'application/vnd.physiome.pmr2.json.0'

    def dumps(self, obj):
        return json.dumps(obj, indent=self.indent)

    def __call__(self):
        set_content_type(self.request, self.json_mimetype)
        return super(JsonPage, self).__call__()


class JsonListingBasePage(JsonPage):

    portal_type = None

    def render(self):
        catalog = getToolByName(self.context, 'portal_catalog')

        query = {
            'portal_type': self.portal_type,
            'path': [
                u'/'.join(self.context.getPhysicalPath()),
            ],
            'sort_on': 'sortable_title',
        }
        results = catalog(**query)

        keys = ['title', 'target']
        values = [dict(zip(keys, (i.Title, i.getURL(),))) for i in results]
        return json.dumps(values)


class SimpleJsonFormMixin(BaseForm):
    """
    Generic mixin for z3c.form type objects.

    This is the simple version.
    """

    zope.interface.implements(ISimpleJsonLayer)

    prefix = 'json.'
    json_mimetype = 'application/vnd.physiome.pmr2.json.0'

    def update(self):
        """
        Convert JSON input into standard request.
        """

        # XXX at some point we need to consider the security and how
        # this might be vulnerable to XSS (for browsers that do not have
        # origin policy support).
        self.disableAuthenticator = True

        updateJsonForm(self)
        super(SimpleJsonFormMixin, self).update()
        self.json_faa = extractFieldsAndActions(self)
        return None

    def render(self):
        """
        Return JSON representation of form if nothing was submitted.

        If something is, return appropriate error or success message.
        """

        set_content_type(self.request, self.json_mimetype)
        return json.dumps(self.json_faa)


class SimpleJsonAddFormMixin(SimpleJsonFormMixin):
    """
    Generic mixin for all AddForms.

    Only the render method needs to be overridden.
    """

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ""
        return super(SimpleJsonAddFormMixin, self).render()


# Helper functions.

def updateJsonForm(form):
    # As a JSON request is a JSON, read from stdin of request.
    request = form.request
    obj = extractRequestObj(request)

    if not isinstance(obj, dict):
        # Not a JSON object type (hashtable/dict)
        return

    # XXX the second part of the prefixes are assumptions.
    prefix = '%s%s' % (form.prefix, 'widgets.')
    a_prefix = '%s%s' % (form.prefix, 'buttons.')
    keys = form.fields.keys()

    fields = obj.get('fields', {})
    action = obj.get('actions', {})

    # XXX might be a good idea to report errors to client if malformed
    # value types are received.
    objToRequest(fields, form.fields.keys(), prefix, request)
    objToRequest(action, form.buttons.keys(), a_prefix, request)

def extractFieldsAndActions(form):
    fields_keys = ['description',]
    widget_keys = ['error', 'items', 'klass', 'value',]
    action_keys = ['title',]
    fields = {}
    widgets = {}
    actions = {}

    def to_dict(keys, value):
        result = []
        for k in keys:
            v = getattr(value, k, None)
            # error is a view, get the raw message instead.
            if hasattr(v, 'message'):
                result.append((k, v.message))
                continue
            elif callable(v):
                result.append((k, v()))
            else:
                result.append((k, v))
        return dict(result)

    for id_, v in form.fields.items():
        fields[id_] = to_dict(fields_keys, v.field)

    for id_, v in form.widgets.items():
        widgets[id_] = to_dict(widget_keys, v)
        # we only care about fields that have a widget.
        widgets[id_].update(fields.get(id_, {}))

    for id_, v in form.actions.items():
        actions[id_] = to_dict(action_keys, v)

    results = {
        'fields': widgets,  # This contains the fields, see above.
        'actions': actions,
    }
    return results
