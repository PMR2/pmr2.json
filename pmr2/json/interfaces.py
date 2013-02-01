import zope.interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form.interfaces import IWidget

from pmr2.app.interfaces import IPMR2AppLayer


class ISimpleJsonLayer(IPMR2AppLayer, IDefaultBrowserLayer):
    """
    The simple json layer.
    """


class IJsonWidget(IWidget):
    """
    Generic JSON widget.
    """
