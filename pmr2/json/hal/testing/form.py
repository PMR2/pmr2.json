from z3c.form import button
from z3c.form import field
from z3c.form import form

from .interfaces import IItem
from .interfaces import IOption

from pmr2.json.hal.mixin import JsonCollectionFormMixin


class ItemBaseForm(JsonCollectionFormMixin, form.Form):

    fields = field.Fields(IItem)


class ItemForm(ItemBaseForm):

    @button.buttonAndHandler(u'Save', name='save')
    def save(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        content = self.getContent()
        form.applyChanges(self, content, data)

    @button.buttonAndHandler(u'Save and Notify', name='save_notify')
    def save_notify(self, action):
        pass


class OptionBaseForm(JsonCollectionFormMixin, form.Form):

    fields = field.Fields(IOption)


class OptionForm(OptionBaseForm):

    @button.buttonAndHandler(u'Submit', name='submit')
    def submit(self, action):
        pass
