from email_extractor import scrape_email
from django.test import TestCase
from nose.plugins.skip import SkipTest
from os.path import split, join


FIXTURE_PATH = join(split(__file__)[0], 'fixtures')


class TestEmails(TestCase):
    def get_url(self, filename):
        return "file://" + join(FIXTURE_PATH, filename)

    def test_nature(self):
        emails = scrape_email(self.get_url('nature.html'), domain='nature.com')
        if set([]) == emails:
            raise SkipTest("Emails aren't available on nature.com")
        raise AssertionError("Expected no emails")

    def test_sciencemag_org(self):
        emails = scrape_email(self.get_url('sciencemag.html'), "stke.sciencemag.org")
        assert set(['gelvin@purdue.edu']) == emails

    def test_plos(self):
        emails = scrape_email(self.get_url('plos.html'), "www.plosone.org")
        assert set(['chenfh@wfu.edu']) == emails

    def test_thirdbit(self):
        emails = scrape_email(self.get_url('third-bit.html'), 'www.third-bit.com')
        assert set(['gvwilson@third-bit.com']) == emails

    def test_plus_addresses(self):
        emails = scrape_email(self.get_url('plus.html'), 'www.third-bit.com')
        assert set(['gvwilson+oabutton@third-bit.com']) == emails

    def test_springerlink(self):
        emails = scrape_email(self.get_url('springerlink.html'))
        self.assertEquals(set(['kamkin.a@g23.relcom', 'imaik-ort@umin.ac']), emails)
