import re
import scraperwiki
base = 'http://members.cox.net';
html = scraperwiki.scrape(base+'/govdocs/govspeak.html')

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

# /govdocs/govspeak/a.html, /govdocs/govspeak/b.html, /govdocs/govspeak/c.html
for a in soup.findAll('a'):

    if a.has_key('href') and re.match('/govdocs/govspeak/a.html', a['href']):
        print base+a['href']   # http://members.cox.net/govdocs/govspeak/a.html
        ahtml = scraperwiki.scrape(base+a['href'])
        asoup = BeautifulSoup(ahtml)
        for tr in asoup.findAll('tr'):

            if len(tr.findAll('td')) == 0: continue
            print tr

            ACK       = tr.findAll('td')[0].string;

            if len(tr.findAll('td')) > 1:

                notelessA = tr.findAll('td')[1].findAll('a',recursive=False);
                if len(notelessA):
                    link      = notelessA[0]['href'];
                    expansion = notelessA[0].string;
                    note      = '';
                    note_link = '';

                linklessI = tr.findAll('td')[1].findAll('i',recursive=False);
                if len(linklessI):
                    link      = " - - - - - - linklessI - - - - - - ";
                    expansion = tr.findAll('td')[1].contents[0].string;
                    note      = linklessI[0].string;
                    note_link = '';
                    if linklessI[0].findAll('i') and linklessI[0].findAll('i').has_key('href'):
                        note_link = linklessI.findAll('i').has_key('href');

            print ACK + " " + link + " " + expansion

            record = { "ACK" : ACK, "Link" : link, "Expansion" : expansion, "Note" : note ,  "Note Link" : note_link}
            scraperwiki.datastore.save(["ACK","Link","Expansion","Note","Note Link"], record)
import re
import scraperwiki
base = 'http://members.cox.net';
html = scraperwiki.scrape(base+'/govdocs/govspeak.html')

from BeautifulSoup import BeautifulSoup
soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object

# /govdocs/govspeak/a.html, /govdocs/govspeak/b.html, /govdocs/govspeak/c.html
for a in soup.findAll('a'):

    if a.has_key('href') and re.match('/govdocs/govspeak/a.html', a['href']):
        print base+a['href']   # http://members.cox.net/govdocs/govspeak/a.html
        ahtml = scraperwiki.scrape(base+a['href'])
        asoup = BeautifulSoup(ahtml)
        for tr in asoup.findAll('tr'):

            if len(tr.findAll('td')) == 0: continue
            print tr

            ACK       = tr.findAll('td')[0].string;

            if len(tr.findAll('td')) > 1:

                notelessA = tr.findAll('td')[1].findAll('a',recursive=False);
                if len(notelessA):
                    link      = notelessA[0]['href'];
                    expansion = notelessA[0].string;
                    note      = '';
                    note_link = '';

                linklessI = tr.findAll('td')[1].findAll('i',recursive=False);
                if len(linklessI):
                    link      = " - - - - - - linklessI - - - - - - ";
                    expansion = tr.findAll('td')[1].contents[0].string;
                    note      = linklessI[0].string;
                    note_link = '';
                    if linklessI[0].findAll('i') and linklessI[0].findAll('i').has_key('href'):
                        note_link = linklessI.findAll('i').has_key('href');

            print ACK + " " + link + " " + expansion

            record = { "ACK" : ACK, "Link" : link, "Expansion" : expansion, "Note" : note ,  "Note Link" : note_link}
            scraperwiki.datastore.save(["ACK","Link","Expansion","Note","Note Link"], record)
