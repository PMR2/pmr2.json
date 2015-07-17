import zope.interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.form.interfaces import IWidget

from pmr2.app.interfaces import IPMR2AppLayer


class IBaseJsonLayer(IPMR2AppLayer, IDefaultBrowserLayer):
    """
    The base JSON layer.
    """


class IJsonWidget(IWidget):
    """
    Generic JSON widget.
    """
