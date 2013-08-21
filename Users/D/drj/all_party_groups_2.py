import scraperwiki
from lxml import etree
from urllib2 import urlopen
import re
from urlparse import urljoin
from htmllib import HTMLParser

def unescape(data):
    p = HTMLParser(None)
    p.save_bgn()
    p.feed(data)
    return p.save_end()

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return unescape(p.sub('', data))

class AllPartyGroupsScraper(object):
    def __init__(self):
        self.groups = []
        self.base_url = "http://www.publications.parliament.uk/pa/cm/cmallparty/register/"

    def get_page(self, url):
        html = urlopen(urljoin(self.base_url, url)).read()
        html = self.fix_exceptions(html)
        return etree.HTML(html)

    def fix_exceptions(self, html):
        html = html.replace("\r", "")
        html = html.replace("\n", "")
        html = html.replace("<p>Baroness O’Cathain</p>", "<p>Baroness O’Cathain - ???</p>")
        html = html.replace("<p>Baroness Hooper</p>", "<p>Baroness Hooper - ???</p>")
        html = html.replace("<p>Lord Brooke of Sutton Mandeville</p>", "<p>Lord Brooke of Sutton Mandeville - ???</p>")
        html = html.replace("<p>Baroness Miller of Chilthorne Domer</p>", "<p>Baroness Miller of Chilthorne Domer - ???</p>")
        html = html.replace("<p>Lord Garel Jones</p>", "<p>Lord Garel Jones - ???</p>")
        html = html.replace("<p>Lord Naseby</p>", "<p>Lord Naseby - ???</p>")
        html = html.replace("<p>Lord Inglewood</p>", "<p>Lord Inglewood - ???</p>")
        html = html.replace("<p>Lord Bowness</p>", "<p>Lord Bowness - ???</p>")
        html = html.replace("<p>Lord Clement-Jones</p>", "<p>Lord Clement-Jones - ???</p>")
        html = html.replace("<br/>Baroness Ludford</p>", "<br/>Baroness Ludford - ???</p>")
        html = html.replace("<p>Duke of Montrose Con</p>", "<p>Duke of Montrose - Con</p>")
        html = html.replace("<p>Lord Bradshaw LD</p>", "<p>Lord Bradshaw - LD</p>")
        html = html.replace("<p>Lord Newton of Braintree</p>", "<p>Lord Newton of Braintree - ???</p>")
        html = html.replace("<p>Lord Crathorne</p>", "<p>Lord Crathorne - ???</p>")
        html = html.replace("<p>Baroness Noakes</p>", "<p>Baroness Noakes - ???</p>")
        html = html.replace("<p>Baroness Walmsley</p>", "<p>Baroness Walmsley - ???</p>")
        html = html.replace("<p>Lord Mancroft Con</p>", "<p>Lord Mancroft - Con</p>")
        html = html.replace("<p>Lord Lester of Herne Hill</p>", "<p>Lord Lester of Herne Hill - ???</p>")
        html = html.replace("<p>Baroness Neuberger</p>", "<p>Baroness Neuberger - ???</p>")
        html = html.replace("<p>Baroness Thomas of Walliswood</p>", "<p>Baroness Thomas of Walliswood - ???</p>")
        html = html.replace("<p>Baroness Falkner of Margravine</p>", "<p>Baroness Falkner of Margravine - ???</p>")
        html = html.replace("<br/>Baroness Knight</p>", "<br/>Baroness Knight - ???</p>")
        html = html.replace("<p>Baroness Howarth</p>               <p>of Breckland</p>", "<p>Baroness Howarth of Breckland</p>")
        html = html.replace("<p>                  <br/>-</p>", "<p>???</p>")
        html = html.replace("<p>Lord Feldman</p>", "<p>Lord Feldman - ???</p>")
        html = html.replace("<p>Baroness Harris of Richmond</p>", "<p>Baroness Harris of Richmond - ???</p>")
        html = html.replace("<p>Baroness Byford Con</p>", "<p>Baroness Byford - Con</p>")
        html = html.replace("<p>Lord Dholakia</p>", "<p>Lord Dholakia - ???</p>")
        html = html.replace("<p>Lord Jenkin of Roding</p>", "<p>Lord Jenkin of Roding - ???</p>")
        html = html.replace("<p>Lord Soulsby of Swaffham Prior</p>", "<p>Lord Soulsby of Swaffham Prior - ???</p>")
        html = html.replace("<p>Earl of Selbourne</p>", "<p>Earl of Selbourne - ???</p>")
        html = html.replace("<p>Lord Waldegrave of North Hill</p>", "<p>Lord Waldegrave of North Hill - ???</p>")
        html = html.replace("<p>Baroness Sharp of Guildford</p>", "<p>Baroness Sharp of Guildford - ???</p>")
        html = html.replace("<p>Lord Taylor of Warwick</p>", "<p>Lord Taylor of Warwick - ???</p>")
        html = html.replace("<p>Lord Jones of Cheltenham</p>", "<p>Lord Jones of Cheltenham - ???</p>")
        html = html.replace("<p>Lord Harries of </p>               <p>Pentrgarth</p>", "<p>Lord Harries of Pentrgarth</p>")
        return html

    def scrape(self, url):
        doc = etree.HTML(urlopen(url).read())
        for x in doc.xpath('//p[@class="contentsLink"]/a'):
            self.scrape_page(x.text, x.attrib['href'])

    def scrape_page(self, group_name, url):
        group = {'name': group_name, 'members': []}

        doc = self.get_page(url)

        group['title'] = remove_html_tags(etree.tostring(doc.xpath('//tr[1]/td[2]/p')[0])).strip()
        group['purpose'] = remove_html_tags(etree.tostring(doc.xpath('//tr[3]/td[2]/p')[0])).strip()
        group['contact'] = remove_html_tags(etree.tostring(doc.xpath('//tr[16]/td[1]/p')[0])).strip()
        group['benefits'] = remove_html_tags(etree.tostring(doc.xpath('//tr[18]/td[1]/p')[0])).strip()
        try:
            group['employment'] = remove_html_tags(etree.tostring(doc.xpath('//tr[20]/td[1]/p')[0])).strip()
        except:
            group['employment'] = ""

        others = []
        for i, col in enumerate(doc.xpath('//tr[count(td)=5]/td')):
            if i == 1:
                tmp = []
                for lord in col.xpath('p[not(@class="spacer")]'):
                    tmp.append(lord.text)
                    for br in lord.xpath('br'):
                        tmp.append(br.tail)

                for lord in tmp:
                    try:
                        # This one must be first
                        name, party = lord.rsplit(u'\u2013', 1)
                    except:
                        try:
                            name, party = lord.rsplit('-', 1)
                        except ValueError:
                            name, party = lord, '???'
                    group['members'].append({'name': name.strip(), 'party': party.strip()})
            elif i == 2:
                for lord in col.xpath('p[not(@class="spacer")]'):
                    group['members'].append({'name': lord.text.strip(), 'party': 'Lab'})
            elif i == 3:
                for lord in col.xpath('p[not(@class="spacer")]'):
                    others.append(lord.text.strip())
                    for br in lord.xpath('br'):
                        br.tail and others.append(br.tail.strip())
            elif i == 4:
                others_parties = []
                for p in col.xpath('p[not(@class="spacer")]'):
                    others_parties.append(p.text.strip())
                    for br in p.xpath('br'):
                        br.tail and others_parties.append(br.tail.strip())

                if not (len(others) == len(others_parties)):
                    print "assertion would have failed"

                for name, party in zip(others, others_parties):
                    group['members'].append({'name': name, 'party': party})


        self.groups.append(group)

base_url = "http://www.publications.parliament.uk/pa/cm/cmallparty/register/contents.htm"

scraper = AllPartyGroupsScraper()

scraper.scrape(base_url)

for g in scraper.groups:
    for m in g['members']:
        scraperwiki.sqlite.save(['Group', 'Name', 'Party'], data = {'Group': g['name'], 'Name': m['name'], 'Party': m['party']}, table_name='members')

for g in scraper.groups:
    scraperwiki.sqlite.save(['Group'], data={'Group': g['name'], 
                                             'Title': g['title'],
                                             'Purpose': g['purpose'], 
                                             'Contact': g['contact'], 
                                             'Benefits': g['benefits'], 
                                             'Employment':g['employment']},
                                       table_name='groups')
