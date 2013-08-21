import scraperwiki
import requests
import urlparse


urls="""http://www.sfgate.com/
http://www.sfexaminer.com/
http://www.sfbg.com/index.php
http://sanfrancisco.cbslocal.com/
http://abclocal.go.com/kgo/index
http://www.kron.com/
http://www.asianweek.com/
http://www.sfbayareaobserver.com/
http://www.ebar.com/
http://www.baycitynews.com/
http://bernalwood.wordpress.com/
http://betweenthelinessf.wordpress.com/
http://www.bignewsnetwork.com/index.php/cat/20134e53b4e12830/
http://www.castrocourier.com/
http://castroonline.com/spectrum/search.html
http://www.catholic-sf.org/
http://www.studycenter.org/test/cce/index.html
http://colevalleyalley.com/
http://district5diary.blogspot.com/
http://www.elreporterosf.com/editions/?q=current
http://eltecolote.org/content/
http://www.fogcityjournal.com/wordpress/
http://foghorn.usfca.edu/
http://www.friendsofdubocepark.org/
http://glenparkassociation.org/
http://www.goldengatexpress.org/
http://www.haightashburystreetfair.org/
http://www.haighteration.com/
http://www.hayesvalleyfarm.com/index.html
http://hoodscope.wordpress.com/
http://www.indiawest.com/
http://www.indybay.org/
http://inglesidelight.com/
http://www.jweekly.com/
http://www.kgoam810.com/default.asp
http://www.kofytv.com/
http://www.ksfo560.com/
http://www.ktsf.com/en/index.html
http://www.ktvu.com/index.html
http://www.lowerhaight.org/
http://www.marinatimes.com/
http://www.missiondispatch.com/news/
http://missionlocal.org/
http://www.missionmission.org/
http://www.msnbc.msn.com/id/3083154/
http://mycastro.com/
http://www.nbcbayarea.com/
http://www.bhnc.org/wordpress/
http://www.nichibei.org/
http://www.nobhillgazette.com/
http://noevalleysf.blogspot.com/
http://www.noevalleyvoice.com/
http://www.northbeachcitizens.org/news/
http://www.northbeachneighbors.org/
http://www.kqed.org/
http://polksheet.com/
http://www.potreroview.net/
http://richmondsfblog.com/
http://sfbayview.com/
http://www.bizjournals.com/sanfrancisco/
http://sanfranciscoglobe.com/
http://www.sanfranmag.com/
http://www.sanfranciscosentinel.com/
http://sfappeal.com/
http://sfcitizen.com/blog/
http://sf.streetsblog.org/
http://www.sfweekly.com/
http://sfist.com/
http://www.sunsetbeacon.com/
http://www.theguardsman.com/
http://newfillmore.com
http://www.sfrichmondreview.com/
http://thetender.us/
http://www.thewesternedition.com/
http://www.topix.com/sf/
http://uptownalmanac.com/
http://westoftwinpeaks.org/
http://www.westsideobserver.com/archives.htm
http://www.worldjournal.com/wjenglishnews"""


def checkurl(url):
    robots=urlparse.urljoin(url, r'/robots.txt')
    print robots
    r=requests.get(robots)
    if r.status_code != 200:
        print r.status_code
        return None
    has_sitemap=False
    for row in r.content.split('\n'):
        if 'Sitemap:' in row:
            print '  '+row
            has_sitemap=True
    return has_sitemap

    
    
for url in urls.split('\n'):
    scraperwiki.sqlite.save(table_name='robots', data={'url': url, 'result': checkurl(url)}, unique_keys=['url'])

