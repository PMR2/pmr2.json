Changelog
=========

0.7 - 2017-01-06
----------------

* Server-side injection of CSRF token to authenticate plone.protect; not
  feeding the same token down the webservice forms given that if the
  attacker can make the POST request, they can make the same GET request
  to get those token anyway; this is why CORS was created so browsers
  will block these requests unless permitted by the server.

0.6 - 2016-07-06
----------------

* Have the workspace view return a title field.
* The links provided by exposure files match the ones provided by the
  exposure file views available portlet.

0.5 - 2016-03-08
----------------

* The definition of the .0 and .1 is now defined as encoding format.
* The .1 format is effectively Collection+JSON.
* Version now distinct by version parameter to the mimetype string.
* This also means that the .1 family will not fall back to the .0
  family of the API.
* Various other minor fixes.

0.4 - 2015-03-19
----------------

* Support for Collection+JSON, with accompanied version bump as all
  future services will be based on this.
* Limited support for HAL+JSON as the above was determined to be a
  better fit.
* Migrated most of the existing classes that made use of the initial
  JSON implementation to make use of this, while retaining the existing
  functionality and classes for that in a new submodule called ``v0``.
* Migrated out the support for ``pmr2.ricordo`` and ``pmr2.virtuoso``
  into those respective packages.
* Collection+JSON form views will use the ``form.`` prefix for inline
  validation compatibility reasons as the support for using the mime-
  type ``application/json`` is enabled.

0.3 - 2014-08-14
----------------

* Support for ``pmr2.ricordo`` and ``pmr2.virtuoso``.
* New test harnesses.

0.2 - 2014-04-03
----------------

* Temporary auth support.  Provide a method to generate temporary
  credentials for a user through the webservice calls.
* Provide the workspace format in the result,


0.1 - 2013-07-08
----------------

* Initial release of web services support for PMR.

