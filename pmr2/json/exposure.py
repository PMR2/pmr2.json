import json

import zope.component
import z3c.form.interfaces
from z3c.form import button, field

from Products.CMFCore.utils import getToolByName

from pmr2.z3cform import form

from pmr2.app.exposure.interfaces import IExposureWizard
from pmr2.app.exposure.browser import util
from pmr2.app.exposure.browser import wizard

from pmr2.json.mixin import JsonPage, JsonListingBasePage
from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin


class JsonExposureWizardForm(SimpleJsonFormMixin, form.EditForm):

    fields = field.Fields(IExposureWizard)

    # Stealing buttons and handlers from edit form and the real wizard
    # form and merge them together.  Omit the add file function as it is
    # meaningless in this context.
    buttons = wizard.ExposureWizardForm.buttons.omit('add_file')
    handlers = form.EditForm.handlers.copy()
    for k in buttons.keys():
        b = buttons[k]
        handlers.addHandler(
            b, wizard.ExposureWizardForm.handlers.getHandler(b))
    buttons += form.EditForm.buttons
    # Groups are not provided or handled here, but some wizard form
    # hanlding methods attempts to process this.
    groups = []

    def getContent(self):
        return zope.component.getAdapter(self.context, IExposureWizard)


class JsonExposureContainerList(JsonListingBasePage):
    portal_type = 'Exposure'


#class JsonExposurePage(JsonPage, ExposurePage):
#
#    def render(self):
#        obj = {
#            'id': self.context.id,
#            'url': self.context.absolute_url(),
#            'description': self.context.description,
#        }
#
#        return json.dumps(obj)
