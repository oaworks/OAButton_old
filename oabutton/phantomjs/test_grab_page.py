from grab_page import grab_emails


def test_sciencemag_org():
    emails = grab_emails("http://stke.sciencemag.org/cgi/content/abstract/sigtrans;6/302/ra100?view=abstract")
    assert('gelvin@purdue.edu' in emails)
