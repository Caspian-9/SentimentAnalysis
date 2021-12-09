"""
Contains the spiders in the scrapy project. There are 3 classes,
CBCSpider, GlobalSpider, and TheStarSpider which will crawl and
retrieve articles from CBC, Global news, and the Star respectively.

The initial search query used is 'covid-19', so not all retrieved
articles will be related to businesses or even Canada.

Note, this file won't run on its own. If you want to run the spiders in this
file, you will need to create a separate scrapy project and run the command
'scrapy crawl <name>' where <name> is the name of the spider. There's no workaround
to this since scrapy depends on the directory structure, which we can't submit in
MarkUs. Please follow https://docs.scrapy.org/en/latest/intro/tutorial.html#creating-a-project
for detailed instructions on how to create a scrapy project, and which file to paste this
code into.
"""
import scrapy
import json


class CBCSpider(scrapy.Spider):
    """
    A spider that recursively extracts title, date, and description from CBC articles
    related to covid-19.

    Instance Attributes:
    - name: The name of the spider
    - page: The number of the next page to be searched
    - headers: Headers to create a cUrl request
    - cookies: Cookies to create a cUrl request
    """
    name = 'cbc'
    page = 1
    headers = {
        "authority": "www.cbc.ca",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"",
        "sec-ch-ua-mobile": "?0",
        "user-agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"),
        "sec-ch-ua-platform": "\"Linux\"",
        "accept": "*/*",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": ("https://www.cbc.ca/search?q=%23covid-19&section=news"
                    "&sortOrder=relevance&media=all"),
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8"
    }
    cookies = {
        "s_ecid": "MCMID%7C72675209331303054871157517612837995608",
        "referrerPillar": "feed",
        "cbc_privacy_notification": "1",
        "_cc_id": "d5d73c9fd6b5a360fb4e7d266eedce4",
        "cX_P": "kvbsahwlpv9oy67r",
        "_cb_ls": "1",
        "_cb": "K6DBcCW0p1rBXjK85",
        "_v__chartbeat3": "CqWQZJB8UM4K0i-au",
        "cX_G": "cx%3A15e8ac322fl2e1h9tou4ez0nmj%3A3j9c4hr6ml1ub",
        "cbc_visitor": "7661375d-cb9f-4eb9-82df-c0313ccbb02e",
        "avcaff_volume": "null",
        "avcaff_autodockdisable": "null",
        "avcaff_captions": "false",
        "referringDepartment": "noReferrer",
        "bm_mi": ("0F958BC1CA5F0C70CD5F45D67960448D~u7Yaa7XOsM09kRBlF2qQi1CMr5FQiWv9Mq2kaXn8+"
                  "4wZZccHvB2PZtiDR2UblKTdRN+1VFN+mATFWl5pvJcGu5TegegnU541ASsqGNQnggm0oaR5TLQXY3"
                  "rPlJzieUsky/td/nVSIdVbnoSQAYs+vYEvBLc98t1osXSrgz7OLE/pICk4z3mLhlVJGw47+0y8PIW"
                  "M15FZcbyemT9gSeUqQ6291BoZgTyob0GF8R9r9xSdmdsdBa0yI7JlLUcSuKH+GIlp9T2XVoylFKA"
                  "kc2M4MWpmf5nnL6eT8kjsmgD5Ke8="),
        "cbc-session": "1637376406",
        "NSC_mcwt-ttm-onxfcdbdif": "ffffffff0983169445525d5f4f58455e445a4a423660",
        "AMCVS_951720B3535680CB0A490D45%40AdobeOrg": "1",
        "s_cc": "true",
        "cX_S": "kw77mx4sr9tosdxn",
        "_vfz": ("www%2Ecbc%2Eca.00000000-0000-4000-8000-082f79d5b829.1637376407.1.medium="
                 "direct|source=|sharer_uuid=|terms="),
        "_vfa": ("www%2Ecbc%2Eca.00000000-0000-4000-8000-082f79d5b829.0c442285-8184-4af1-"
                 "85ea-d1375fe83202.1635476182.1636163351.1637376407.5"),
        "_cb_svref": "null",
        "AMCV_951720B3535680CB0A490D45%40AdobeOrg": ("1585540135%7CMCIDTS%7C18952%7CMCMID%7"
                                                     "C726752093313030548711575176128379956"
                                                     "08%7CMCAAMLH-1637981206%7C7%7CMCAAMB-"
                                                     "1637981206%7CRKhpRz8krg2tLO6pguXWp5ol"
                                                     "kAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOU"
                                                     "T-1637383606s%7CNONE%7CMCAID%7CNONE%7"
                                                     "CMCSYNCSOP%7C411-18959%7CvVersion%7C4"
                                                     ".4.0%7CMCCIDH%7C-82759145"),
        "cbc_ppid": "7661375d-cb9f-4eb9-82df-c0313ccbb02e",
        "ak_bmsc": ("E1EA4BCBF4357F30A98929C230C7099A~000000000000000000000000000000~YAAQxy"
                    "v2SFiSnC99AQAAwTY9Ow3JV5Ma0aPo4+yEFR+5X7SM+nk64S5K3Ev0ezjz2GFiiFgs7wof"
                    "8wVNH1ZGJm0xrF4VV8tzNBAzexBYhwq1WaXSssHPH6NaaQuh5hLt5aG0exXJuqtL4tiQmyr"
                    "K/R7+JNIX2hlhhmcY+ZPkLcFCLm/37Md6mwolJ6W5EDIVkLFcyLFMbLPrPklNjdBhhLHK+"
                    "UelYVzkcl3+ES5MIqkT/U3dMr2Lw1BXO2Nxp4rtxqIX3qKJsSDk3W8XfmkGUqg3m1QeeJ"
                    "BEi9fgdito9yu8xE+vppSKUSfcDojr/0N9H2qdX/w9fMDvNcP1h+YGtf+NwrjcB+xOIPHw"
                    "f7ZJuZR3MGjCfnU+dSyE0BNgVO+ZpcYBsF4P+0GQs5DiBUPp3+Rmuow6MvSZdqKS67Q/Ir"
                    "MoW6AWmn8FIw=="),
        "cbc_app_version": "d06b6c2ad59ebe455fe9bd0321b21532f01d4609",
        "stats_experiment_ids": "%5B%22a-uoIkAhyJUH%22%5D",
        "stats_experiment_variants": "%5B%22a-uoIkAhyJUH%7CA%22%5D",
        "RT": ("\"z=1&dm=cbc.ca&si=c54c344a-cc80-4ced-a0eb-4af924d170dd&ss=kw77mw4a&sl=2&tt"
               "=1ik&bcn=%2F%2F68794905.akstat.io%2F&ld=ilu&nu=1r4sypk1&cl=iaf\""),
        "amplitude_id_f5b7aa101ec24385b731affd4a2f5ed0_statscbc.ca": ("eyJkZXZpY2VJZCI6Ijc2N"
                                                                      "jEzNzVkLWNiOWYtNGViOS"
                                                                      "04MmRmLWMwMzEzY2NiYjAy"
                                                                      "ZSIsInVzZXJJZCI6bnVsbCw"
                                                                      "ib3B0T3V0IjpmYWxzZSwi"
                                                                      "c2Vzc2lvbklkIjoxNjM3M"
                                                                      "zc2NDA2MjAwLCJsYXN0RXZ"
                                                                      "lbnRUaW1lIjoxNjM3Mzc2NDI"
                                                                      "5NDAwLCJldmVudElkIj"
                                                                      "o2MywiaWRlbnRpZnlJZC"
                                                                      "I6MTM3LCJzZXF1ZW5jZU51"
                                                                      "bWJlciI6MjAwfQ=="),
        "_chartbeat2": (".1635476181695.1637376429414.0100000000000001.CeD55WB"
                        "KRCc1ByZizHCN4XcnBYVtrj.2"),
        "_vfb": "www%2Ecbc%2Eca.00000000-0000-4000-8000-082f79d5b829.3.10.1637376407....",
        "bm_sv": ("33A771EA7572144CDDE9EED25EB02558~8aAmtu7LND1AEnaIvM+R4qkAFsSfPCi2PYMxxfnY"
                  "hWcvHii2QvE8Zo4Au9Ck15yAN5gk6RrNKTuA/TQfLYAjg2z0oDsxXijlT0HEn9xZefXL9RhkAa"
                  "IDpsr3CfgGaIK8dNVJp3MUx0++R5BkEtOgg/p/Q8RguIjYRyzXU1RBy0o="),
        "s_sq": ("cbc-production%3D%2526pid%253Dsearch%25253Aindex%2526pidt%253D1%2526oid%253"
                 "Dfunctionsn%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT"),
        "SC_LINKS": ("%7B%20%22pageName%22%3A%20%22search%3Aindex%22%2C%20%22linkName%22%3A"
                     "%20%22Loading...%22%2C%20%22concatValue%22%3A%20%22search%3Aindex%20%"
                     "7C%20Loading...%22%2C%20%22linkPosition%22%3A%20%22loadmore1%22%20%7D")
    }

    def start_requests(self) -> list[scrapy.Request]:
        """
        Returns a scrapy.Request in list format overriding the default behaviour.
        """
        url = ('https://www.cbc.ca/search_api/v1/search?q=%23covid-19&sortOrder=relevance&'
               'section=news&media=all&boost-cbc-keywords=7&boost-cbc-keywordscollections'
               '=7&boost-cbc-keywordslocation=4&boost-cbc-keywordsorganization=3&boost-cb'
               'c-keywordsperson=5&boost-cbc-keywordssubject=7&boost-cbc-publishedtime=30'
               '&page=1&fields=feed')
        request = scrapy.Request(
            url=url,
            cookies=self.cookies,
            headers=self.headers,
            method='GET',
            dont_filter=True,
            callback=self.parse
        )
        return [request]

    def parse(self, response, **kwargs):
        """
        Retrieves articles from CBC with the inital search query 'covid-19'.
        """
        data = json.loads(response.text)
        for article in data:
            if 'description' in article and 'title' in article and 'publishtime' in article:
                title = article['title']
                desc = article['description']
                publish_time = article['publishtime']
                yield {'title': title, 'description': desc, 'publish_time': publish_time}

        if len(data) > 1:
            self.page += 1
            url = (f'https://www.cbc.ca/search_api/v1/search?q=%23covid-19&sortOrder=relev'
                   f'ance&section=news&media=all&boost-cbc-keywords=7&boost-cbc-keywordsc'
                   f'ollections=7&boost-cbc-keywordslocation=4&boost-cbc-keywordsorganiza'
                   f'tion=3&boost-cbc-keywordsperson=5&boost-cbc-keywordssubject=7&boost-'
                   f'cbc-publishedtime=30&page={self.page}&fields=feed')
            yield scrapy.Request(
                url=url,
                cookies=self.cookies,
                headers=self.headers,
                method='GET',
                dont_filter=True,
                callback=self.parse
            )


class TheStarSpider(scrapy.Spider):
    """
    A spider that recursively extracts title, date, and body from The Star articles
    related to covid-19.

    Instance Attributes:
    - name: The name of the spider
    - start_urls: The url of the first page to be searched
    """
    name = 'star'
    start_urls = ['https://www.thestar.com/search.html?q=covid-19']

    def parse(self, response, **kwargs):
        """
        Retrieves articles from Toronto Star using the initial search query 'covid-19'.
        """
        # filter out the actual articles
        hits = response.css('div.c-search-results-item')
        # follow the links of each article so that you can extract the body
        for hit in hits:
            links = hit.css('a::attr(href)').getall()
            if len(links) > 0:
                yield from response.follow_all(links, self.extract_body)

        next_page = response.css('div.c-search-paging a::attr(href)').getall()[-1]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def extract_body(self, response) -> dict[str, str]:
        """
        Extract the body of an article from TheStar news.
        """
        body = ' '.join(response.css('p.text-block-container::text').getall())
        date = response.css('span.article__published-date::text').get()
        title = response.css('head title::text').get()
        if body and date and title:
            yield {'title': title, 'publish_time': date, 'body': body}


class GlobalSpider(scrapy.Spider):
    """
    A spider that recursively extracts title, date, and body from Global news articles
    related to covid-19 in Canada.

    Instance Attributes:
    - name: The name of the spider
    - page: The number of the next page to be searched
    - headers: Headers used to create a cUrl request
    - url: The first url to be searched
    """
    name = 'global'
    page = 1
    headers = {
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\"",
        "Accept": "*/*",
        "Referer": "https://globalnews.ca/search/covid-19/",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/96.0.4664.45 Safari/537.36"),
        "sec-ch-ua-platform": "\"Linux\""
    }
    url = ('https://globalnews.ca/gnca-ajax/search-results/%7B%22term%22:%22covid-19%22'
           ',%22type%22:%22news%22,%22page%22:1%7D/')

    def start_requests(self):
        request = scrapy.Request(
            url=self.url,
            headers=self.headers,
            method='GET',
            dont_filter=True,
            callback=self.parse
        )
        return [request]

    def parse(self, response, **kwargs):
        """
         Retrieves articles from Global news with the initial search query 'covid-19'.
        """
        # filter out the actual articles
        hits = response.css('div.story')
        # follow the links of each article so that you can extract the body
        for hit in hits:
            link = hit.css('div.search-thumb-large a::attr(href)').get()
            if link is not None:
                yield response.follow(link, self.extract_body)

        if len(hits) > 0:
            self.page += 1
            next_page = (f'https://globalnews.ca/gnca-ajax/search-results/%7B%22term%22'
                         f':%22covid-19%22,%22type%22:%22news%22,%22page%22:{self.page}%7D/')
            yield response.follow(next_page, callback=self.parse)

    def extract_body(self, response) -> dict[str, str]:
        """
        Extract the body of an article from TheStar news.
        """
        date = response.css('div.c-byline__dates span::text').get()
        title = response.css('head title::text').get()
        body = ' '.join(response.css('article.l-article__text p::text').getall())
        if body and date and title:
            yield {'title': title, 'publish_time': date, 'body': body}


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['scrapy', 'json'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

