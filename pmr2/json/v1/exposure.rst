Exposure with JSON
==================

Handling Exposures with JSON is similar to workspace.  To demonstrate
this, start by importing some related modules::

    >>> from cStringIO import StringIO
    >>> import json
    >>> import zope.component
    >>> from pmr2.app.exposure.interfaces import IExposureWizard
    >>> from pmr2.json.v1.exposure import JsonExposureWizardForm
    >>> from pmr2.json.tests.base import TestRequest

Instead of dealing with each wizard elements individually, the entire
JSON representation of the exposure can be replaced in one go::

    >>> self._mkexposure(u'/plone/workspace/test', u'3', '3')
    >>> context = self.portal.exposure['3']
    >>> request = TestRequest()
    >>> form = JsonExposureWizardForm(context, request)
    >>> form.update()
    >>> results = json.loads(form.render())
    >>> results['collection']['version'] == '1.0'
    True
    >>> len(results['collection']['template']['data']) == 4
    True

Now post a structure::

    >>> raw_structure = [
    ...     ['dir1/nested/file', {
    ...         'file_type': '/plone/docgen_type',
    ...         'hidden_views': [],
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
    ...         'hidden_views': [],
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
    >>> payload = {
    ...     'template': {
    ...         'data': [
    ...             {
    ...                 'name': 'form.widgets.structure',
    ...                 'value': raw_structure,
    ...             },
    ...             {
    ...                 'name': 'form.buttons.apply',
    ...                 'value': True,
    ...             }
    ...         ],
    ...     }
    ... }
    >>> stdin = StringIO()
    >>> json.dump(payload, stdin)
    >>> request = TestRequest(method='POST', stdin=stdin)
    >>> form = JsonExposureWizardForm(context, request)
    >>> form.update()
    >>> result = json.loads(form.render())
    >>> result['collection']['template']['data'][0]['value'] == raw_structure
    True

Ensure that the values have been correctly applied::

    >>> ewiz1 = zope.component.getAdapter(context, IExposureWizard)
    >>> ewiz1.structure == raw_structure
    True

Now generate the exposure::

    >>> payload['template']['data'][1]['name'] = 'form.buttons.build'
    >>> stdin = StringIO()
    >>> json.dump(payload, stdin)
    >>> request = TestRequest(method='POST', stdin=stdin)
    >>> form = JsonExposureWizardForm(context, request)
    >>> form.update()
    >>> result = json.loads(form.render())
    >>> result['collection']['template']['data'][0]['value'] == raw_structure
    True

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

Now use the testbrowser class to attempt to view this::

    >>> tb = self.testbrowser
    >>> tb.addHeader('Accept', 'application/vnd.physiome.pmr2.json.1')
    >>> portal_url = context.absolute_url()
    >>> tb.open(portal_url + '/wizard')
    >>> result = json.loads(tb.contents)
    >>> result['collection']['template']['data'][0]['value'] == raw_structure
    True

Then manipulate.  Note that error checking is still NOT implemented::

    >>> payload['template']['data'][0]['value'] = ['faildata']
    >>> payload['template']['data'][1]['name'] = 'form.buttons.apply'
    >>> data = json.dumps(payload)
    >>> tb.open(portal_url + '/wizard', data=data)
    >>> print tb.url
    http://nohost/plone/exposure/3/wizard
    >>> ewiz1.structure
    [u'faildata']

Unfortunately at this point in time there is no strict schema involved.
If we were to attempt to build this an error will be generated::

    >>> data = json.dumps({'template': {'data': [{
    ...     'name': 'form.buttons.build', 'value': True}]}})
    >>> tb.open(portal_url + '/wizard', data=data)
    >>> print tb.url
    http://nohost/plone/exposure/3/wizard
    >>> result = json.loads(tb.contents)
    >>> result['collection']['error']
    {u'message': u'There were errors generating the exposure',
     u'code': u'error', u'errors': [], u'title': u'Error'}

Select revert to regenerate the wizard using the structure that was
committed earlier::

    >>> data = json.dumps({'template': {'data': [{
    ...     'name': 'form.buttons.revert', 'value': True}]}})
    >>> tb.open(portal_url + '/wizard', data=data)
    >>> print tb.url
    http://nohost/plone/exposure/3/wizard
    >>> raw_structure[-2][1]['views'][1][1]['text'] = u'file'
    >>> raw_structure[-1][1]['commit_id'] = u'3'
    >>> json.loads(json.dumps(ewiz1.structure)) == raw_structure
    True

Now render the default page of the created exposure.  Currently a search
for all exposure files is done, with the search done recursively and
results returned in a flat list::

    >>> target = context.absolute_url()
    >>> tb.open(target)
    >>> result = json.loads(tb.contents)
    >>> result['collection']['links'] == [
    ... {u'href': u'http://nohost/plone/exposure/3/dir1/nested/file/view',
    ...  u'prompt': u'file', u'rel': u'bookmark'},
    ... {u'href': u'http://nohost/plone/exposure/3/file1/view',
    ...  u'prompt': u'file1', u'rel': u'bookmark'},
    ... {u'href': u'http://nohost/plone/workspace/test',
    ...  u'prompt': u'Workspace URL', u'rel': u'via'}]
    True
    >>> result['collection']['items'] == [{
    ...     u'href': 'http://nohost/plone/exposure/3/exposure_info',
    ...     u'data': [{
    ...         u'prompt': u'Title', u'name': u'title',
    ...         u'value': u'',
    ...     }]
    ... }]
    True

The exposure files can be accessed like so::

    >>> tb.open(result['collection']['links'][0]['href'])
    >>> result = json.loads(tb.contents)
    >>> result['collection']['links'] == [
    ... {
    ...     "href": "http://nohost/plone/exposure/3/dir1/nested/file/docgen",
    ...     "prompt": "Documentation",
    ...     "rel": "section"
    ... },
    ... {
    ...     "href": "dir1/nested/file",
    ...     "prompt": None,
    ...     "rel": "section"
    ... }]
    True

Data section should look like so, with the value to the file_type be a
valid URL to the type::

    >>> result['collection']['items'][0]['data'] == [{
    ...     u'prompt': u'File type for this exposure',
    ...     u'name': u'file_type',
    ...     u'value': u'http://nohost/plone/docgen_type'
    ... }, {
    ...     u'prompt': u'Title', u'name': u'title', u'value': u'file',
    ... }]
    True

Navigating at that URL should return a proper representation::

    >>> tb.open(result['collection']['items'][0]['data'][0]['value'])
    >>> filetype = json.loads(tb.contents)
    >>> filetype['collection'] == {
    ...     u'items': [{
    ...         u'data': [{
    ...             u'prompt': u'Title', u'name': u'title',
    ...             u'value': u'Docgen Type', u'description': u''
    ...         }, {
    ...             u'prompt': u'Views', u'name': u'views',
    ...             u'value': [u'docgen', u'filename_note'],
    ...             u'description': u'The list of views to be created.'
    ...         }, {
    ...             u'prompt': u'Select View', u'name': u'select_view',
    ...             u'value': None,
    ...             u'description': u'If defined, select this view if the '
    ...                 'generation is successful.'
    ...         }, {
    ...             u'prompt': u'Tags', u'name': u'tags', u'value': [],
    ...             u'description':
    ...                 u'List of tags to be assigned to this file.'
    ...         }]
    ...     }],
    ...     u'href': u'http://nohost/plone/docgen_type/eftype_view',
    ...     u'version': u'1.0'
    ... }
    True

As for what those notes will return, this depend on the implementation
of the annotation views.  Not all will have the appropriate web service
views implemented.

First view is the docgen.  Generally this is dedicated for html clients,
thus there will be no JSON view for them::

    >>> tb.open(result['collection']['links'][0]['href'])
    >>> json.loads(tb.contents)
    Traceback (most recent call last):
    ...
    ValueError: No JSON object could be decoded

Whereas views that have json views defined for them will behave as
expected, though we have to manually resolve the one for the one for
the ``filename_note`` as it was overridden to be relative for another
demonstration elsewhere::

    >>> href = "http://nohost/plone/exposure/3/dir1/nested/file/filename_note"
    >>> tb.open(href)
    >>> json.loads(tb.contents)
    {u'collection': {u'items':
    [{u'name': u'filename', u'value': u'dir1/nested/file'}],
    u'href': u'http://nohost/plone/exposure/3/dir1/nested/file/filename_note',
    u'version': u'1.0'}}
