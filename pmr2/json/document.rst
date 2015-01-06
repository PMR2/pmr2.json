Document webservice view
========================

Try accessing the news aggregator's summary view normally::

    >>> from Testing.testbrowser import Browser
    >>> tb = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> tb.open(portal_url + '/front-page')
    >>> '<a href="http://nohost/plone/plone_control_panel">Site Setup</a>' in \
    ...     tb.contents
    True

Now try again after application of the header::

    >>> tb = Browser()
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.1')
    >>> tb.open(portal_url + '/front-page')
    >>> '{"href": "http://nohost/plone/plone_control_panel", ' \
    ... '"label": "Site Setup"}' in tb.contents
    True
