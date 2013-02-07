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

    >>> self._mkexposure(u'/plone/workspace/test', u'3', '3')
    >>> context = self.portal.exposure['3']
    >>> request = TestRequest()
    >>> form = JsonExposureWizardForm(context, request)
    >>> form.update()
    >>> results = json.loads(form.render())
    >>> sorted(results['actions'].keys())
    [u'apply', u'build', u'revert']

Now post a structure::

    >>> original_structure = [
    ...     ['dir1/nested/file', {
    ...         'file_type': '/plone/docgen_type',
    ...         'views': [
    ...             [u'docgen', {'source': 'dir1/nested/file',
    ...                                    'generator': u'safe_html'}],
    ...             [u'filename_note', {'filename': 'dir1/nested/file'}]
    ...         ],
    ...         'selected_view': None, 'Subject': [],
    ...         'docview_gensource': None,
    ...         'docview_generator': None,
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
    ...     ['file1', {
    ...         'views': [
    ...             [u'edited_note', {'note': u'Testing'}],
    ...             [u'post_edited_note', {'chars': 4}],
    ...             [u'rot13', None],
    ...         ],
    ...         'file_type': '/plone/test_type',
    ...         'selected_view': None,
    ...         'docview_gensource': None,
    ...         'docview_generator': None,
    ...         'Subject': ['please_ignore',]
    ...     }],
    ...     ['', {
    ...         'commit_id': u'2',
    ...         'title': u'',
    ...         'curation': {},
    ...         'workspace': u'/plone/workspace/test',
    ...         'docview_gensource': None,
    ...         'docview_generator': None,
    ...         'Subject': [],
    ...     }],
    ... ]
    >>> fields = {'structure': original_structure}
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

Verify that the objects are created as expected.  Note that the value
for the commit_id remains unaffected::

    >>> context.commit_id == u'3'
    True
    >>> sorted(context.keys())
    ['dir1', 'file1']
    >>> context['dir1'].keys()
    ['nested']
    >>> file = context['dir1']['nested']['file']
    >>> file.views
    [u'docgen', u'filename_note']
    >>> file1 = context['file1']
    >>> note1 = zope.component.getAdapter(file1, name='edited_note')
    >>> note1.note == u'Testing'
    True
    >>> note2 = zope.component.getAdapter(file1, name='post_edited_note')
    >>> note2.chars == 4
    True
    >>> note2.text == u'file'
    True

Now use the testbrowser class to attempt to manipulate this::

    >>> tb = self.testbrowser
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.0')
    >>> portal_url = context.absolute_url()
    >>> tb.open(portal_url + '/wizard')
    >>> result = json.loads(tb.contents)
    >>> result['fields'].keys()
    [u'structure']
    >>> fields = {'structure': ['faildata']}
    >>> actions = {"apply": 1}
    >>> data = json.dumps({'fields': fields, 'actions': actions})
    >>> tb.open(portal_url + '/wizard', data=data)
    >>> print tb.url
    http://nohost/plone/exposure/3/wizard
    >>> ewiz1.structure
    [u'faildata']

Unfortunately at this point in time there is no strict schema involved.
If we were to attempt to build this an error will be generated::

    >>> actions = {"build": 1}
    >>> data = json.dumps({'actions': actions})
    >>> tb.open(portal_url + '/wizard', data=data)
    >>> print tb.url
    http://nohost/plone/exposure/3/wizard
    >>> result = json.loads(tb.contents)

Select revert to regenerate the wizard using the structure that was
committed earlier::

    >>> actions = {"revert": 1}
    >>> data = json.dumps({'actions': actions})
    >>> tb.open(portal_url + '/wizard', data=data)
    >>> print tb.url
    http://nohost/plone/exposure/3/wizard
    >>> original_structure[-2][1]['views'][1][1]['text'] = u'file'
    >>> original_structure[-1][1]['commit_id'] = u'3'
    >>> json.loads(json.dumps(ewiz1.structure)) == original_structure
    True

Now render the default page of the created exposure.  Currently a search
for all exposure files is done, with the search done recursively and
results returned in a flat list::

    >>> portal_url = context.absolute_url()
    >>> tb.open(portal_url)
    >>> result = json.loads(tb.contents)
    >>> print result
    [{u'URI': u'.../3/dir1/nested/file/view', u'Title': u'file'},
    {u'URI': u'.../3/file1/view', u'Title': u'file1'}]

The exposure files can be accessed like so::

    >>> tb.open(result[0]['URI'])
    >>> result = json.loads(tb.contents)
    >>> result
    {u'file_type': u'/plone/docgen_type',
    u'source_uri':
    u'http://nohost/plone/workspace/test/rawfile/3/dir1/nested/file',
    u'views': {u'docgen':
    u'http://nohost/plone/exposure/3/dir1/nested/file/docgen',
    u'filename_note':
    u'http://nohost/plone/exposure/3/dir1/nested/file/filename_note'}}
