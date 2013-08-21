###########################################################################################
# We use a ScraperWiki library called pdftoxml to scrape PDFs.
# This is an example of scraping a simple PDF.
###########################################################################################

import scraperwiki
import urllib2
import lxml.etree

lis = ['http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=1',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=1',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=1',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=1',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=1',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=2',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=2',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=2',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=2',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=2',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=2',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=3',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=3',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=3',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=3',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=3',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=3',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=4',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=4',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=4',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=4',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=4',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=4',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=5',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=5',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=5',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=5',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=5',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=5',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=6',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=6',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=6',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=6',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=6',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=6',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=7',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=7',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=7',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=7',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=7',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=7',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=8',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=8',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=8',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=8',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=8',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=8',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=9',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=9',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=9',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=9',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=9',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=9',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=10',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=10',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=10',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=10',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=10',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=10',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=11',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=11',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=11',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=11',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=11',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=11',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=12',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=12',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=12',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=12',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=12',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=12',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=13',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=13',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=13',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=13',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=13',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=13',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=14',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=14',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=14',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=14',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=14',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=14',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=15',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=15',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=15',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=15',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=15',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=15',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=16',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=16',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=16',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=16',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=16',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=16',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=17',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=17',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=17',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=17',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=17',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=17',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=18',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=18',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=18',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=18',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=18',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=18',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=19',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=19',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=19',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=19',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=19',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=19',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=20',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=20',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=20',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=20',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=20',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=20',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=21',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=21',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=21',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=21',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=21',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=21',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=22',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=22',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=22',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=22',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=22',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=22',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=23',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=23',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=23',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=23',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=23',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=23',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=24',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=24',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=24',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=24',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=24',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=24',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=25',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=25',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=25',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=25',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=25',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=25',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=26',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=26',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=26',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=26',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=26',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=26',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=27',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=27',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=27',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=27',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=27',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=27',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=28',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=28',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=28',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=28',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=28',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=28',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=29',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=29',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=29',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=29',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=29',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=29',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=30',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=30',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=30',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=30',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=30',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=30',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=31',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=31',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=31',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=31',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=31',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=31',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Silkeborg IF&code5=dliga&matchday=32',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=32',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Brondby IF&code5=dliga&matchday=32',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=SonderjyskE&code5=dliga&matchday=32',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Randers FC&code5=dliga&matchday=32',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AGF&code5=dliga&matchday=32',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Nordsjaelland&code5=dliga&matchday=33',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=OB&code5=dliga&matchday=33',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AaB&code5=dliga&matchday=33',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Kobenhavn&code5=dliga&matchday=33',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=AC Horsens&code5=dliga&matchday=33',
'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=FC Midtjylland&code5=dliga&matchday=33', 'http://dk.amisco.eu/exploitationlive/editionpdf/livemedia/matchCenter/Danemark/superliga/after/amisco.asp?lequipe=Esbjerg fB&code5=dliga&matchday=1']

i = 0

#this loop isn't working

for words in lis:

    url = lis[i]
    i = i +1
    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)

    xmldata = scraperwiki.pdftoxml(pdfdata)
    print "After converting to xml it has %d bytes" % len(xmldata)
    print "The first 5000 characters are: ", xmldata[:5000]

#    if lxml.etree.fromstring(xmldata) == False:
#        continue
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]


# this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
    def gettext_with_bi_tags(el):
        res = [ ]
        if el.text:
            res.append(el.text)
        for lel in el:
            res.append("<%s>" % lel.tag)
            res.append(gettext_with_bi_tags(lel))
            res.append("</%s>" % lel.tag)
            if el.tail:
                res.append(el.tail)
        return "".join(res)

# print the first hundred text elements from the first page
page0 = pages[0]
ID = 0;
for el in list(page)[:100]:
        print el.tag
        if el.tag == "text":
            print el.attrib, gettext_with_bi_tags(el) 
        record = {}
        record["text"] = gettext_with_bi_tags(el)
        ID = ID+1
        record["ID"] = ID 
        scraperwiki.sqlite.save(["ID"],record)
        print record



# If you have many PDF documents to extract data from, the trick is to find what's similar 
# in the way that the information is presented in them in terms of the top left bottom right 
# pixel locations.  It's real work, but you can use the position visualizer here:
#    http://scraperwikiviews.com/run/pdf-to-html-preview-1/

