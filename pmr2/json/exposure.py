import json

import zope.component
import z3c.form.interfaces
from z3c.form import button, field

from Products.CMFCore.utils import getToolByName

from pmr2.z3cform import form

from pmr2.app.exposure.interfaces import IExposureWizard
from pmr2.app.exposure.browser import util

from pmr2.json.mixin import JsonPage, JsonListingBasePage
from pmr2.json.mixin import SimpleJsonFormMixin, SimpleJsonAddFormMixin


class JsonExposureWizardForm(SimpleJsonFormMixin, form.EditForm):

    fields = field.Fields(IExposureWizard)
    buttons = form.EditForm.buttons.copy()
    handlers = form.EditForm.handlers.copy()

    groups = []

    def getContent(self):
        return zope.component.getAdapter(self.context, IExposureWizard)

    # XXX duplicating the real class.

    @button.buttonAndHandler(u'Build', name='build')
    def handleBuild(self, action):
        errors = util.extractError(self)
        if errors:
            self.status = _(u"Unable to build exposure due to input error; "
                "please review the form and make the appropriate changes, "
                "update each subsection using the provided button, and try "
                "again.")
            return

        wh = zope.component.getAdapter(self.context, IExposureWizard)

        try:
            util.moldExposure(self.context, self.request, wh.structure)
        except ProcessingError, e:
            raise z3c.form.interfaces.ActionExecutionError(e)

        self._updated = True
        self._next = ''

    @button.buttonAndHandler(u'Revert', name='revert')
    def handleRevert(self, action):
        porter = ExposurePort(self.context, self.request)
        structure = list(porter.export())
        wh = zope.component.getAdapter(self.context, IExposureWizard)
        wh.structure = structure
        self._updated = True


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
