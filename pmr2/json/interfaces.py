import zope.interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form.interfaces import IWidget

from pmr2.app.interfaces import IPMR2AppLayer


class ISimpleJsonLayer(IPMR2AppLayer, IDefaultBrowserLayer):
    """
    The base simple json layer.
    """


class ISimpleJsonLayer1(ISimpleJsonLayer):
    """
    Version 1.
    """


class IJsonWidget(IWidget):
    """
    Generic JSON widget.
    """
