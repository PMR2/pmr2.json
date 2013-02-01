Exposure with JSON
==================

Handling Exposures with JSON is similar to workspace.  To demonstrate
this, start by importing some related modules::

    >>> from cStringIO import StringIO
    >>> import json
    >>> import zope.component
    >>> from pmr2.app.exposure.interfaces import IExposureWizard
    >>> from pmr2.json.exposure import JsonExposureWizardForm
    >>> from pmr2.json.tests.base import TestRequest

Instead of dealing with each wizard elements individually, the entire
JSON representation of the exposure can be replaced in one go::

    >>> context = self.portal.exposure['1']
    >>> request = TestRequest()
    >>> form = JsonExposureWizardForm(context, request)
    >>> form.update()
    >>> results = json.loads(form.render())
    >>> sorted(results['actions'].keys())
    [u'apply', u'build', u'revert']

Now post a structure::

    >>> fields = {'structure': [
    ...     ['dir1/nested/file', {
    ...         'file_type': '/plone/docgen_type',
    ...         'views': [[u'docgen', None], [u'filename_note', None]],
    ...         'selected_view': None, 'Subject': []
    ...     }],
    ...     ['dir1/nested', {
    ...         'docview_gensource': None,
    ...         'docview_generator': None,
    ...         'Subject': [],
    ...     }],
    ...     ['dir1', {
    ...         'docview_gensource': None,
    ...         'docview_generator': None,
    ...         'Subject': [],
    ...     }],
    ...     ['', {
    ...         'commit_id': u'3',
    ...         'title': u'',
    ...         'curation': {},
    ...         'workspace': u'/plone/workspace/test',
    ...         'docview_gensource': None,
    ...         'docview_generator': None,
    ...         'Subject': [],
    ...     }],
    ... ]}
    >>> actions = {"apply": 1}
    >>> stdin = StringIO()
    >>> json.dump({'fields': fields, 'actions': actions}, stdin)
    >>> request = TestRequest(method='POST', stdin=stdin)
    >>> form = JsonExposureWizardForm(context, request)
    >>> form.update()
    >>> form.render()
    '{...}'

Ensure that the values have been correctly applied::

    >>> ewiz1 = zope.component.getAdapter(context, IExposureWizard)
    >>> ewiz1.structure == fields['structure']
    True

Now generate the exposure::

    >>> actions = {"build": 1}
    >>> stdin = StringIO()
    >>> json.dump({'actions': actions}, stdin)
    >>> request = TestRequest(method='POST', stdin=stdin)
    >>> form = JsonExposureWizardForm(context, request)
    >>> form.update()
    >>> form.render()
    '{...}'
    >>> context['dir1'].keys()
    ['nested']
