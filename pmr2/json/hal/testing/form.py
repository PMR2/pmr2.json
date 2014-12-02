from z3c.form import form
from z3c.form import field

from .interfaces import IItem


class ItemForm(form.Form):

    fields = field.Fields(IItem)
