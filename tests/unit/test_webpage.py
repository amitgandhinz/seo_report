import bs4
import ddt
import testtools

from seo_report import webpage


@ddt.ddt
class WebpageTests(testtools.TestCase):

    def setUp(self):
        super(WebpageTests, self).setUp()

        self.titles = {}
        self.descriptions = {}

    def soup_file(self, html):
        soup = bs4.BeautifulSoup(html, "html.parser")
        return soup

    @ddt.file_data('data_html_positive.json')
    def test_analyze_positive(self, data):
        html = data[0]
        expected_achievement = data[1]

        self.wp = webpage.Webpage(
            "https://www.drawbuildplay.com",
            html,
            self.titles,
            self.descriptions)

        self.wp.report()

        # title should have achieved the following
        if expected_achievement != "":
            self.assertTrue(any(earned.startswith(expected_achievement)
                                for earned in self.wp.achieved),
                            "{0} not found".format(expected_achievement))

    @ddt.file_data('data_html_negative.json')
    def test_analyze_negative(self, data):
        html = data[0]
        expected_error = data[1]

        self.wp = webpage.Webpage(
            "https://www.drawbuildplay.com",
            html,
            self.titles,
            self.descriptions)

        self.wp.report()
        self.assertTrue(any(issue.startswith(expected_error)
                            for issue in self.wp.issues),
                        "{0} not found in issues".format(expected_error))

    @ddt.file_data('data_html_negative_url.json')
    def test_analyze_negative_url(self, data):
        url = data[0]
        expected_error = data[1]
        html = ""

        self.wp = webpage.Webpage(
            url, html, self.titles, self.descriptions)

        self.wp.report()
        self.assertTrue(any(issue.startswith(expected_error)
                            for issue in self.wp.issues),
                        "{0} not found in issues".format(expected_error))

        pass

    @ddt.file_data('data_visible_tags.json')
    def test_visible_tags(self, data):
        html = ""
        self.wp = webpage.Webpage(
            "https://www.drawbuildplay.com",
            html,
            self.titles,
            self.descriptions)

        soup = self.soup_file(data[0])
        elements = soup.findAll(text=True)
        for tag in elements:
            result = self.wp.visible_tags(tag)
            self.assertEqual(result, data[1])

    @ddt.file_data('data_duplicates_negative.json')
    def test_analyze_duplicates_negative(self, page):
        html = page[0]
        expected_error = page[1]

        report = {"pages": []}
        for i in range(0, 2):
            self.wp = webpage.Webpage(
                "https://www.drawbuildplay.com/page{0}.html".format(i),
                html,
                self.titles,
                self.descriptions)

            page_report = self.wp.report()
            report['pages'].append(page_report)

        # warn about duplicate information
        self.assertTrue(any(issue.startswith(expected_error)
                            for p in report['pages'] for issue in p['issues']),
                        "{0} not found in issues {1} {2}".format(
                            expected_error,
                            self.titles,
                            self.descriptions))
