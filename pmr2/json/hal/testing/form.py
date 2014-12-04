from z3c.form import button
from z3c.form import field
from z3c.form import form

from .interfaces import IItem


class ItemBaseForm(form.Form):

    fields = field.Fields(IItem)


class ItemForm(ItemBaseForm):

    @button.buttonAndHandler(u'Save', name='save')
    def save(self, action):
        pass

    @button.buttonAndHandler(u'Save and Notify', name='save_notify')
    def save_notify(self, action):
        pass
