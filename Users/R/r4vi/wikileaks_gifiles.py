import scraperwiki
import lxml.etree

# Blank Python
pages = [scraperwiki.scrape(page) for page in
            ['http://wikileaks.org/gifiles/releasedate/2012-02-27.html',
            'http://wikileaks.org/gifiles/releasedate/2012-02-27-2.html'
            ]
        ]

for page in pages:
    print pageimport scraperwiki
import lxml.etree

# Blank Python
pages = [scraperwiki.scrape(page) for page in
            ['http://wikileaks.org/gifiles/releasedate/2012-02-27.html',
            'http://wikileaks.org/gifiles/releasedate/2012-02-27-2.html'
            ]
        ]

for page in pages:
    print page