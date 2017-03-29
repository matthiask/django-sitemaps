===============
django-sitemaps
===============

``sitemap.xml`` generation using lxml with support for alternates.

Usage
=====

::

    from app.pages.sitemaps import PagesSitemap

    def sitemap(request):
        sitemap = Sitemap(build_absolute_uri=request.build_absolute_uri)
        sitemap.add_django_sitemap(request, PagesSitemap)

        for p in Page.objects.active():
            url = p.get_absolute_url()
            sitemap.add(
                url,
                changefreq='weekly',
                priority=0.5,
                lastmod=p.modification_date,
                alternates={
                    code: urljoin(domain, url)
                    for code, domain in PAGE_DOMAINS[p.language].items()
                },
            )

        return sitemap.response(pretty_print=settings.DEBUG)
