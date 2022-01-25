==========
Change log
==========

`Next version`_
~~~~~~~~~~~~~~~


`2.0.1`_ (2022-01-25)
~~~~~~~~~~~~~~~~~~~~~

- Fixed cases where empty priority tags were added if priority was an
  empty string (which is always the default case with Django sitemaps).
- Added pre-commit, switched to a declarative setup, etc.
- Made ``add_django_sitemap`` always build URLs using ``build_absolute_uri``
  too to avoid problems when using ``django.contrib.sites``.


`1.1`_ (2018-04-11)
~~~~~~~~~~~~~~~~~~~

- Added the ``lxml`` dependency to ``install_requires``.
- Added documentation.
- Added the ``robots_txt`` view for easily adding a ``/robots.txt``
  view returning sitemap URLs.


`1.0`_ (2017-03-29)
~~~~~~~~~~~~~~~~~~~

- Initial release!

.. _1.0: https://github.com/matthiask/django-sitemaps/commit/df0841349
.. _1.1: https://github.com/matthiask/django-sitemaps/compare/1.0...1.1
.. _2.0.1: https://github.com/matthiask/django-sitemaps/compare/1.1...2.0.1
.. _Next version: https://github.com/matthiask/django-sitemaps/compare/2.0.1...main
