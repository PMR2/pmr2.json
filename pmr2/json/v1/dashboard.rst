JSON Dashboard
==============

The dashboard lists available options/functions exposed to end-users of
the webservice API

Version 1 complies with Collection+JSON::

    >>> import json
    >>> tb = self.testbrowser
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.1')
    >>> portal_url = self.portal.absolute_url()
    >>> tb.open(portal_url + '/pmr2-dashboard')
    >>> result = json.loads(tb.contents)
    >>> result.keys()
    [u'collection']
    >>> links = result['collection']['links']
    >>> print sorted(item['name'] for item in links)
    [u'workspace-add', u'workspace-home']
