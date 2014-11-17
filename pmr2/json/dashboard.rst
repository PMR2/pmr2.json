JSON Dashboard
==============

The dashboard lists available options/functions exposed to end-users of
the webservice API::

    >>> import json
    >>> tb = self.testbrowser
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.0')
    >>> portal_url = self.portal.absolute_url()
    >>> tb.open(portal_url + '/pmr2-dashboard')
    >>> result = json.loads(tb.contents)
    >>> keys = result.keys()
    >>> print sorted(keys)
    [u'workspace-add', u'workspace-home']

The fallback should work from 1 to 0::

    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.1')
    >>> portal_url = self.portal.absolute_url()
    >>> tb.open(portal_url + '/pmr2-dashboard')
    >>> result = json.loads(tb.contents)
    >>> keys = result.keys()
    >>> print sorted(keys)
    [u'workspace-add', u'workspace-home']

