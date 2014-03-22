from email_extractor import scrape_email
from django.test import TestCase
from nose.plugins.skip import SkipTest


class TestEmails(TestCase):
    def test_sciencemag_org(self):
        url = "http://stke.sciencemag.org/cgi/content/abstract/sigtrans;6/302/ra100?view=abstract"
        emails = scrape_email(url)
        assert set(['gelvin@purdue.edu']) == emails

    def test_plos(self):
        url = "http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0052814"
        emails = scrape_email(url)
        assert set(['chenfh@wfu.edu']) == emails

    def test_nature(self):
        url = "http://www.nature.com/nature/journal/v483/n7391/full/483531a.html"
        try:
            emails = scrape_email(url)
        except RuntimeError, re:
            raise SkipTest("Nature.com is behaving badly")

        if set([]) == emails:
            raise SkipTest("Emails aren't available on nature.com")
        raise AssertionError("Expected no emails")

    def test_thirdbit(self):
        url = "http://third-bit.com/oab/"
        emails = scrape_email(url)
        assert set(['gvwilson@third-bit.com']) == emails
