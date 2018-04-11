from calendar import timegm
from datetime import date

from lxml import etree
from lxml.builder import ElementMaker

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.utils.http import http_date
from django.views.decorators.cache import cache_page


__all__ = ('Sitemap',)


S = ElementMaker(
    namespace='http://www.sitemaps.org/schemas/sitemap/0.9',
    nsmap={
        None: 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'xhtml': 'http://www.w3.org/1999/xhtml',
    },
)
X = ElementMaker(
    namespace='http://www.w3.org/1999/xhtml',
    nsmap={'xhtml': 'http://www.w3.org/1999/xhtml'},
)


class Sitemap(object):
    def __init__(self, *, build_absolute_uri):
        self.urls = []
        self.build_absolute_uri = build_absolute_uri
        self.lastmod = None
        self.all_urls_lastmod = True

    def add(
        self,
        loc,
        *,
        changefreq=None,
        lastmod=None,
        priority=None,
        alternates={}
    ):
        children = [
            S.loc(self.build_absolute_uri(loc)),
        ]
        if changefreq is not None:
            children.append(S.changefreq(changefreq))
        if isinstance(lastmod, date):
            new = timegm(
                lastmod.utctimetuple() if hasattr(lastmod, 'utctimetuple')
                else lastmod.timetuple()
            )
            self.lastmod = max(self.lastmod, new) if self.lastmod else new
            children.append(S.lastmod(lastmod.isoformat()))
        elif lastmod is not None:
            children.append(S.lastmod(lastmod))
        else:
            self.all_urls_lastmod = False
        if priority is not None:
            children.append(S.priority(str(priority)))

        for code, url in alternates.items():
            children.append(X.link({
                'rel': 'alternate',
                'hreflang': code,
                'href': self.build_absolute_uri(url),
            }))

        self.urls.append(S.url(*children))

    def add_django_sitemap(self, sitemap, *, request):
        if callable(sitemap):
            sitemap = sitemap()

        for url in sitemap.get_urls(
                site=get_current_site(request),
                protocol=request.scheme,
        ):
            self.add(
                url['location'],
                changefreq=url.get('changefreq'),
                lastmod=url.get('lastmod'),
                priority=url.get('priority'),
            )

    def serialize(self, *, pretty_print=False):
        return etree.tostring(
            S.urlset(*self.urls),
            encoding='UTF-8',
            pretty_print=pretty_print,
            xml_declaration=True,
        )

    def response(self, *, pretty_print=False):
        response = HttpResponse(
            self.serialize(pretty_print=pretty_print),
            content_type='application/xml',
        )
        response['X-Robot-Tag'] = 'noindex, noodp, noarchive'
        if self.all_urls_lastmod and self.lastmod is not None:
            response['Last-Modified'] = http_date(self.lastmod)
        return response


def robots_txt(*, timeout=0, sitemaps=['/sitemap.xml']):
    @cache_page(timeout)
    def view(request):
        lines = ['User-agent: *\n']
        lines.extend(
            'Sitemap: %s\n' % request.build_absolute_uri(str(sitemap))
            for sitemap in sitemaps
        )
        return HttpResponse(''.join(lines), content_type='text/plain')
    return view
