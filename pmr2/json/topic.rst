Topic webservice view
=====================

First add some news items and publish them::

    >>> self.setRoles(['Manager'])
    >>> o = self.portal.news.invokeFactory('News Item', id='test')
    >>> self.portal.news.test.edit(text='Please ignore.', title='Test News')
    >>> o = self.portal.news.invokeFactory('News Item', id='reset')
    >>> self.portal.news.reset.edit(text='All the things.', title='Reset')
    >>> self.portal.portal_workflow.doActionFor(
    ...     self.portal.news.test, 'publish')
    >>> self.portal.portal_workflow.doActionFor(
    ...     self.portal.news.reset, 'publish')

Try accessing the news aggregator's summary view normally::

    >>> from Testing.testbrowser import Browser
    >>> tb = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> tb.open(portal_url + '/news/aggregator/summary_view')
    >>> print tb.contents
    <BLANKLINE>
    ...
    <li class="navTreeItem visualNoMarker section-reset">
      <a href="http://nohost/plone/news/reset" ...>
        <span>Reset</span>
      </a>
    </li>
    <li class="navTreeItem visualNoMarker section-test">
      <a href="http://nohost/plone/news/test" ...>
        <span>Test News</span>
      </a>
    </li>
    ...

Now try again after application of the header::

    >>> tb = Browser()
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.0')
    >>> tb.open(portal_url + '/news/aggregator/summary_view')
    >>> print tb.contents
    [{"target": "http://nohost/plone/news/reset", "title": "Reset"},
     {"target": "http://nohost/plone/news/test", "title": "Test News"}]

Thew view should apply normally at the top level news object as the
aggregator is the default item, with the ``folder_summary_view`` being
the default view also registered to provide this same view::

    >>> tb = Browser()
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.0')
    >>> tb.open(portal_url + '/news')
    >>> print tb.contents
    [{"target": "http://nohost/plone/news/reset", "title": "Reset"},
     {"target": "http://nohost/plone/news/test", "title": "Test News"}]
