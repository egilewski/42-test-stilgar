# -*- coding: utf-8 -*-

from tddspry.django import DatabaseTestCase
from tddspry.django import HttpTestCase
from twill.errors import TwillAssertionError
# FIXME: delete prefix, fix django-nose to work without it.
from forty_two_test_stilgar.apps.frontpage_profile.models import Profile
from django.utils.formats import date_format
from django.utils.html import escape as real_escape
import datetime
import re
from BeautifulSoup import BeautifulSoup


class TestFrontPageProfileDB(DatabaseTestCase):
    def test_front_page(self):
        self.assert_count(Profile, 1)


class TestFrontPageProfileHTTP(HttpTestCase):
    xhtml = True

    def test_front_page(self):
        profile_data = Profile.objects.all()[0]
        self.go200('/')
        # Check all fields. If some field will be added and shouldn't be
        # outputed to the front page, it's OK for test to fail so it will be
        # obviuos that it needs to be changed.
        for field in profile_data._meta.fields:
            if field.column == 'id':
                continue
            value = getattr(profile_data, field.column)
            if isinstance(value, datetime.date):
                value = date_format(value)
            value = re.sub('\n+', '\n', value)
            value = re.sub(' +', ' ', value)
            self.find(value, flat=True, plain_text=True)

    def find(self, what, flags='', flat=False, count=None, escape=False,
            plain_text=False):
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
        if escape:
            what = real_escape(what)

        if isinstance(what, str):
            what = what.decode('UTF-8')

        html = self.get_browser().get_html().decode('UTF-8')
        if plain_text:
            soup = BeautifulSoup(html)
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
