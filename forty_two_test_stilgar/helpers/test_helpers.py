"""Helpers for tests using tddspry."""
import re
from tddspry.django import HttpTestCase
from twill.errors import TwillAssertionError
from BeautifulSoup import BeautifulSoup
from django.utils.html import escape as real_escape


# pylint: disable=R0904
class HttpParsingTestCase(HttpTestCase):
    """Subclass of HttpTestCase with support for search on page, parsed as
    HTML."""
    def find(self, what, flags='', flat=False, count=None, escape=False,
            plain_text=False, collapse_whitespace=True):
        """
        Twill used regexp for searching content on web-page. Use ``flat=True``
        to search content on web-page by standart Python ``what in html``
        expression.

        If this expression was not True (was not found on page) it's raises
        ``TwillAssertionError`` as in ``twill.commands.find`` method.

        Specify ``count`` to test that ``what`` occurs ``count`` times in the
        content of the web-page.

        You could escape ``what`` text by standart ``django.utils.html.escape``
        function if call method with ``escape=True``, like::

            self.find('Text with "quotes"', escape=True)

        Set ``plain_text`` to True to search in text of page disregarding html
        tags (i. e. parsed by html parser).

        """
        if not isinstance(what, basestring):
            what = unicode(what)

        what = re.sub('\r\n|\r', '\n', what)
        if collapse_whitespace:
            what = re.sub('(\r\n|\r|\n)+', '\n', what)
            what = re.sub(' +', ' ', what)

        if escape:
            what = real_escape(what)

        if isinstance(what, str):
            what = what.decode('UTF-8')

        html = self.get_browser().get_html().decode('UTF-8')
        html = re.sub('(\r\n|\r|\n)+', '\n', html)
        if plain_text:
            soup = BeautifulSoup(html,
                                 convertEntities=BeautifulSoup.XHTML_ENTITIES)
            if not flat and not count:
                return soup.find(text=what)
            page_content = []
            for element in soup.body.recursiveChildGenerator():
                if isinstance(element, unicode):
                    page_content.append(element)
                elif str(element) == '<br />':
                    page_content.append('\n')
            page_content = ''.join(page_content)
            if flat:
                real_count = page_content.count(what)
            else:
                real_count = len(re.findall(what, page_content))
        else:
            if not flat and not count:
                return self._find(what.encode('UTF-8'), flags)
            real_count = html.count(what)

        if count is not None and count != real_count:
            raise TwillAssertionError('Matched to %s %d times, not %d ' \
                                      'times.' % (what, real_count, count))
        elif real_count == 0:
            raise TwillAssertionError('No match to %s' % what)

        return True
