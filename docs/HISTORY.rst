Changelog
=========

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

