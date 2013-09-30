import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random

urls = [

'http://gmergency.tumblr.com/',
'http://gruntdoc.com/',
'http://guildoffoam.org/',
'http://guitargirlrn.blogspot.com/',
'http://www.hamalrad.com/',
'http://www.hneed.com/',
'http://houseofgodforeclosed.wordpress.com/',
'http://www.hqmeded.com/',
'http://www.impactednurse.com/',
'http://incisionanddrainage.blogspot.com/',
'http://injectableorange.com/',
'http://www.intensivecarenetwork.com/',
'http://iteachem.net/',
'http://spacefan.blogspot.com/',
'http://ivor-kovic.com/blog/',
'http://www.kardioblogie.blogspot.cz/',
'http://keepcaring.wordpress.com/',
'http://keep-caring.com/',
'http://keepingup.vanderbiltem.com/',
'http://ukemigquickhit.wordpress.com/',
'http://kidocs.org/',
'http://ki-docs.com/',
'http://www.emergencydocs.com/blog/',
'http://lifeinthefastlane.com/',
'http://littlemedic.org/',
'http://journals.lww.com/em-news/blog/littlewhitecoats/pages/default.aspx',
'http://journals.lww.com/em-news/blog/M2E/pages/default.aspx',
'http://www.macastat.com/',
'http://www.malatocritico.com/',
'http://mdaware.org/',
'http://www.medicinadurgenza.org/',
'http://medest118.wordpress.com/',
'http://medgadget.com/emergency_medicine',
'http://www.medinuggets.com/',
'http://www.mededmasters.com/',
'http://meritus.kopernika.pl/',
'http://modernem.blogspot.com/',
'http://allbleedingstops.blogspot.com/',
'http://myemergencymedicineblog.blogspot.com/',
'http://www.ozemedicine.com/blog/',
'http://paramedicstory.blogspot.com/',
'http://www.gustavoflores.net/home/',
'http://patersoner.com/',
'http://pedemmorsels.com/',
'http://www.pemcincinnati.com/blog/',
'http://www.pemed.org/',
'http://pemlit.org/',
'http://prehospitalmed.com/',
'http://poranatelesora.wordpress.com/',
'http://practicalevidence.org/',
'http://pricelesselectricalactivity.blogspot.com/',
'http://pulmccm.org/',
'http://www.reanimacion.net/',
'http://www.drhemblog.com/',
'http://residing.tumblr.com/',
'http://resus.me/',
'http://resusreview.com/',
'http://rnshicu.org/blog',
'http://roguemedic.com/',
'http://rollcagemedic.yolasite.com/',
'http://ruralflyingdoc.wordpress.com/',
'http://www.scalpelorsword.blogspot.com.au/',
'http://www.scancrit.com/',
'http://sinaiem.us/',
'http://media.sinaiem.org/',
'http://www.docshazam.com/',
'http://smartem.org/',
'http://socmob.org/',
'http://www.sonospot.com/',
'http://stemlynsblog.org/blog/',
'http://storytellerdoc.blogspot.com/',
'http://suburbanemergency.blogspot.com/',
'http://takeokun.com/',
'http://talesfromtheer.com/',
'http://teachmd.blogspot.com/',
'http://trismus1.wordpress.com/',
'http://thebluntdissection.com/',
'http://bodsblog.wordpress.com/',
'http://journals.lww.com/em-news/blog/TheCaseFiles/pages/default.aspx',
'http://thecentralline.org/',
'http://thechartreview.blogspot.ca/',
'http://theknifeman.blogspot.com/',
'http://medialapproach.com/',
'http://www.thepoisonreview.com/',
'http://thesgem.com/',
'http://thesharpend.org/',
'http://shortcoatsinem.blogspot.com/',
'http://thesonocave.com/',
'http://atencioncontinuada.blogspot.com/',
'http://thoracotomie.com/',
'http://torontoemerg.wordpress.com/',
'http://toxtalk.org/',
'http://regionstraumapro.com/',
'http://www.east.org/resources/traumacast',
'http://www.ultrasoundpodcast.com/',
'https://www.umem.org/res_pearls_browse_cat.php',
'http://underneathem.com/',
'http://urgenciasbidasoa.wordpress.com/',
'http://urgenciashusa.wordpress.com/',
'http://www.epmonthly.com/whitecoat/',
'http://whitecoatrants.wordpress.com/',
'http://wikemerg.ca/',
'http://www.yourerdoc.com/',
]


def data_load(hrefs, url): #Function to store data in sqlite database
    for href in hrefs:
        data = {}
        data['hrefs'] = href
        data['url'] = url
        data['key'] = random.random()
        scraperwiki.sqlite.save(['key'], data) 


def href_find(content, url):#function to grab hrefs
    hrefs = re.findall(r'''href=[\'"]?([^\'" >]+)''', content)
    return data_load(hrefs, url)


def page_load(url): #function to scrape websites
    h = httplib2.Http(".cache")
    try:
        response, content = h.request(url, "GET")
    except: 
        pass
    return href_find(content, url)


for url in urls:
    page_load(url)
    sleep(1)
import scraperwiki
import sys, httplib2, urllib, re
from lxml import etree
from StringIO import StringIO
from time import sleep
import random

urls = [

'http://gmergency.tumblr.com/',
'http://gruntdoc.com/',
'http://guildoffoam.org/',
'http://guitargirlrn.blogspot.com/',
'http://www.hamalrad.com/',
'http://www.hneed.com/',
'http://houseofgodforeclosed.wordpress.com/',
'http://www.hqmeded.com/',
'http://www.impactednurse.com/',
'http://incisionanddrainage.blogspot.com/',
'http://injectableorange.com/',
'http://www.intensivecarenetwork.com/',
'http://iteachem.net/',
'http://spacefan.blogspot.com/',
'http://ivor-kovic.com/blog/',
'http://www.kardioblogie.blogspot.cz/',
'http://keepcaring.wordpress.com/',
'http://keep-caring.com/',
'http://keepingup.vanderbiltem.com/',
'http://ukemigquickhit.wordpress.com/',
'http://kidocs.org/',
'http://ki-docs.com/',
'http://www.emergencydocs.com/blog/',
'http://lifeinthefastlane.com/',
'http://littlemedic.org/',
'http://journals.lww.com/em-news/blog/littlewhitecoats/pages/default.aspx',
'http://journals.lww.com/em-news/blog/M2E/pages/default.aspx',
'http://www.macastat.com/',
'http://www.malatocritico.com/',
'http://mdaware.org/',
'http://www.medicinadurgenza.org/',
'http://medest118.wordpress.com/',
'http://medgadget.com/emergency_medicine',
'http://www.medinuggets.com/',
'http://www.mededmasters.com/',
'http://meritus.kopernika.pl/',
'http://modernem.blogspot.com/',
'http://allbleedingstops.blogspot.com/',
'http://myemergencymedicineblog.blogspot.com/',
'http://www.ozemedicine.com/blog/',
'http://paramedicstory.blogspot.com/',
'http://www.gustavoflores.net/home/',
'http://patersoner.com/',
'http://pedemmorsels.com/',
'http://www.pemcincinnati.com/blog/',
'http://www.pemed.org/',
'http://pemlit.org/',
'http://prehospitalmed.com/',
'http://poranatelesora.wordpress.com/',
'http://practicalevidence.org/',
'http://pricelesselectricalactivity.blogspot.com/',
'http://pulmccm.org/',
'http://www.reanimacion.net/',
'http://www.drhemblog.com/',
'http://residing.tumblr.com/',
'http://resus.me/',
'http://resusreview.com/',
'http://rnshicu.org/blog',
'http://roguemedic.com/',
'http://rollcagemedic.yolasite.com/',
'http://ruralflyingdoc.wordpress.com/',
'http://www.scalpelorsword.blogspot.com.au/',
'http://www.scancrit.com/',
'http://sinaiem.us/',
'http://media.sinaiem.org/',
'http://www.docshazam.com/',
'http://smartem.org/',
'http://socmob.org/',
'http://www.sonospot.com/',
'http://stemlynsblog.org/blog/',
'http://storytellerdoc.blogspot.com/',
'http://suburbanemergency.blogspot.com/',
'http://takeokun.com/',
'http://talesfromtheer.com/',
'http://teachmd.blogspot.com/',
'http://trismus1.wordpress.com/',
'http://thebluntdissection.com/',
'http://bodsblog.wordpress.com/',
'http://journals.lww.com/em-news/blog/TheCaseFiles/pages/default.aspx',
'http://thecentralline.org/',
'http://thechartreview.blogspot.ca/',
'http://theknifeman.blogspot.com/',
'http://medialapproach.com/',
'http://www.thepoisonreview.com/',
'http://thesgem.com/',
'http://thesharpend.org/',
'http://shortcoatsinem.blogspot.com/',
'http://thesonocave.com/',
'http://atencioncontinuada.blogspot.com/',
'http://thoracotomie.com/',
'http://torontoemerg.wordpress.com/',
'http://toxtalk.org/',
'http://regionstraumapro.com/',
'http://www.east.org/resources/traumacast',
'http://www.ultrasoundpodcast.com/',
'https://www.umem.org/res_pearls_browse_cat.php',
'http://underneathem.com/',
'http://urgenciasbidasoa.wordpress.com/',
'http://urgenciashusa.wordpress.com/',
'http://www.epmonthly.com/whitecoat/',
'http://whitecoatrants.wordpress.com/',
'http://wikemerg.ca/',
'http://www.yourerdoc.com/',
]


def data_load(hrefs, url): #Function to store data in sqlite database
    for href in hrefs:
        data = {}
        data['hrefs'] = href
        data['url'] = url
        data['key'] = random.random()
        scraperwiki.sqlite.save(['key'], data) 


def href_find(content, url):#function to grab hrefs
    hrefs = re.findall(r'''href=[\'"]?([^\'" >]+)''', content)
    return data_load(hrefs, url)


def page_load(url): #function to scrape websites
    h = httplib2.Http(".cache")
    try:
        response, content = h.request(url, "GET")
    except: 
        pass
    return href_find(content, url)


for url in urls:
    page_load(url)
    sleep(1)
