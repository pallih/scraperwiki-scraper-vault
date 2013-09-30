# (c) 2013, Dane Summers <dsummers@pinedesk.biz>
#
# This work is licensed under the Creative Commons Attribution 3.0 Unported
# License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by/3.0/.

import argparse
import contextlib
import logging
import lxml.etree
import lxml.html
import mechanize
import re
import scraperwiki
import urllib2

logging.basicConfig()
logger = logging.getLogger('NC')

class Scraper:
  def __init__(self):
    self.br = mechanize.Browser()
    self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  def scrape(self):
    pass

  def urlopen(self,url):
    return self.br.open(url)

class MasterDetailScraper(Scraper):
  def scrape(self):
    results = []
    for url in self.scrapemaster():
      logger.info("Scraping: %s" % url)
      result = self.scrapedetail(url)
      results.append(result)
    return results

  def scrapemaster(self):
    """ Return a list of urls to pass to detail. """
    pass
  def scrapedetail(self,url):
    """ Return a list of results for one detail page. """
    pass

class NCRepScraper(MasterDetailScraper):
  urlpath = "http://www.nclm.org/resource-center/municipalities/Pages"
  url = "%s/Default.aspx" % urlpath

  def scrapemaster(self):
    # sometimes the server is sensitive to this information
    response = self.urlopen(self.url)
    root = lxml.html.fromstring(response.read())
    msvbs = root.cssselect('.ms-vb > a')
    results = []
    for vb in msvbs:
      cityURL = "%s/%s" % (self.urlpath,vb.get('href'))
      results.append(cityURL)
    return results

  def scrapedetail(self,url):
    # sometimes the server is sensitive to this information
    response = self.urlopen(url)

    results = {
      'City': None,
      'Source': url,
      'Population': None,
      'Website': None,
      'Phone': None,
      'County': None,
      'Officials': None
    }

    root = lxml.html.fromstring(response.read())
    city = root.cssselect('#WebPartWPQ2 h1')
    vals = root.cssselect('#WebPartWPQ2 tr')
    results['City'] = city[0].text
    logger.debug(vals)
    for v in vals:
      logger.debug(lxml.etree.tostring(v))
      logger.debug("%s = %s" % (v.xpath('td[1]/h3')[0].text,v.xpath('td[2]')[0].text))
      key = v.xpath('td[1]/h3')[0].text
      value = v.xpath('td[2]')[0].text
      if key == 'Population':
        value = int(value.replace(',',''))
      elif key == 'Phone':
        value = value.encode('ascii','ignore')
      elif key == 'County' and value:
        value = [x.title() for x in value.encode('ascii','ignore').split(',')]
      elif key == 'Website':
        value = v.xpath('td[2]/a')[0].text
      elif key == 'Officials':
        officials = {}
        value = []
        for c in v.xpath('td[2]'):
          if c.text: value.append(c.text)
          for s in c:
            if s.text: value.append(s.text)
            if s.tail: value.append(s.tail)
        # take the array of officials, and split by the LAST comma:
        #  First Name, Jr., Mayor
        #  XXXXXXXXXXXXXXX,YYYYYY
        for name in value:
          parts = name.split(',')
          # if the len > 2 then there are additional commas in the rep's name...
          if len(parts) > 2:
            officials[parts[-1].strip()] = ','.join(parts[0:-1])
          else:
            officials[parts[1].strip()] = parts[0]
        value = officials
      results[key] = value
    return results


# the name is scraper when run on scraperwiki.com
if __name__ == '__main__' or __name__ == 'scraper':
  # Parse any command line options, and react accordingly
  parser = argparse.ArgumentParser( \
      description='Parse NC Cities & Towns website.', \
      epilog='Written by Dane Summers (dsummers@pinedesk.biz).')
  loglevelchoices = ['none','info','debug']
  parser.add_argument('--loglevel', choices=loglevelchoices,help='Log level to display.')
  parser.add_argument('--test',action='store_true',help='Do non-destructive test parse (not a full parse).')
    # these two options are used by scraperwiki.com
  parser.add_argument('--script',help='the location of the script (optional)')
  parser.add_argument('--scraper',help='the name of the scraper (optional)')
  args = parser.parse_args()

  if args.loglevel in loglevelchoices:
    attr = logging.NOTSET
    if args.loglevel != 'none':
      attr = getattr(logging,args.loglevel.upper())
    logger.setLevel(attr)
  else:
    logger.setLevel(logging.INFO)

  scraper = NCRepScraper()

  if args.test:
    alltowns = scraper.scrapemaster()
    logger.info("Got all towns (%d total)" % len(alltowns))
    logger.info("Getting details for: %s" % alltowns[0])
    logger.info("Details = %s" % scraper.scrapedetail(alltowns[0]))
  else:
    alltowns = scraper.scrapemaster()
    logger.info("Got all towns (%d total)" % len(alltowns))
    cnt = 1
    for town in alltowns:
      logger.info("%d/%d Getting details for: %s" % (cnt,len(alltowns),town))
      data = scraper.scrapedetail(town)
      logger.debug("Details = %s" % data)
      #data['Officials'] = ' -- '.join([str(x) for x in data['Officials']])
      towndata = {
        'City'       : data['City'],
        'Source'     : data['Source'],
        'Population' : data['Population'],
        'Website'    : data['Website'],
        'Phone'      : data['Phone']
      }
      scraperwiki.sqlite.save(unique_keys=['Source'], data=towndata,table_name="cities")
      for k,v in data['Officials'].items():
        repdata = {
          'Source': data['Source'],
          'City': data['City'],
          'Title': k,
          'Name': v
        }
        scraperwiki.sqlite.save(unique_keys=['Source','Title','Name'], data=repdata,table_name="reps")
      if data['County']:
        for c in data['County']:
          cdata = {
            'Source': data['Source'],
            'County': c
          }
          scraperwiki.sqlite.save(unique_keys=['Source','County'], data=cdata,table_name="counties")
      cnt += 1
# (c) 2013, Dane Summers <dsummers@pinedesk.biz>
#
# This work is licensed under the Creative Commons Attribution 3.0 Unported
# License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by/3.0/.

import argparse
import contextlib
import logging
import lxml.etree
import lxml.html
import mechanize
import re
import scraperwiki
import urllib2

logging.basicConfig()
logger = logging.getLogger('NC')

class Scraper:
  def __init__(self):
    self.br = mechanize.Browser()
    self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

  def scrape(self):
    pass

  def urlopen(self,url):
    return self.br.open(url)

class MasterDetailScraper(Scraper):
  def scrape(self):
    results = []
    for url in self.scrapemaster():
      logger.info("Scraping: %s" % url)
      result = self.scrapedetail(url)
      results.append(result)
    return results

  def scrapemaster(self):
    """ Return a list of urls to pass to detail. """
    pass
  def scrapedetail(self,url):
    """ Return a list of results for one detail page. """
    pass

class NCRepScraper(MasterDetailScraper):
  urlpath = "http://www.nclm.org/resource-center/municipalities/Pages"
  url = "%s/Default.aspx" % urlpath

  def scrapemaster(self):
    # sometimes the server is sensitive to this information
    response = self.urlopen(self.url)
    root = lxml.html.fromstring(response.read())
    msvbs = root.cssselect('.ms-vb > a')
    results = []
    for vb in msvbs:
      cityURL = "%s/%s" % (self.urlpath,vb.get('href'))
      results.append(cityURL)
    return results

  def scrapedetail(self,url):
    # sometimes the server is sensitive to this information
    response = self.urlopen(url)

    results = {
      'City': None,
      'Source': url,
      'Population': None,
      'Website': None,
      'Phone': None,
      'County': None,
      'Officials': None
    }

    root = lxml.html.fromstring(response.read())
    city = root.cssselect('#WebPartWPQ2 h1')
    vals = root.cssselect('#WebPartWPQ2 tr')
    results['City'] = city[0].text
    logger.debug(vals)
    for v in vals:
      logger.debug(lxml.etree.tostring(v))
      logger.debug("%s = %s" % (v.xpath('td[1]/h3')[0].text,v.xpath('td[2]')[0].text))
      key = v.xpath('td[1]/h3')[0].text
      value = v.xpath('td[2]')[0].text
      if key == 'Population':
        value = int(value.replace(',',''))
      elif key == 'Phone':
        value = value.encode('ascii','ignore')
      elif key == 'County' and value:
        value = [x.title() for x in value.encode('ascii','ignore').split(',')]
      elif key == 'Website':
        value = v.xpath('td[2]/a')[0].text
      elif key == 'Officials':
        officials = {}
        value = []
        for c in v.xpath('td[2]'):
          if c.text: value.append(c.text)
          for s in c:
            if s.text: value.append(s.text)
            if s.tail: value.append(s.tail)
        # take the array of officials, and split by the LAST comma:
        #  First Name, Jr., Mayor
        #  XXXXXXXXXXXXXXX,YYYYYY
        for name in value:
          parts = name.split(',')
          # if the len > 2 then there are additional commas in the rep's name...
          if len(parts) > 2:
            officials[parts[-1].strip()] = ','.join(parts[0:-1])
          else:
            officials[parts[1].strip()] = parts[0]
        value = officials
      results[key] = value
    return results


# the name is scraper when run on scraperwiki.com
if __name__ == '__main__' or __name__ == 'scraper':
  # Parse any command line options, and react accordingly
  parser = argparse.ArgumentParser( \
      description='Parse NC Cities & Towns website.', \
      epilog='Written by Dane Summers (dsummers@pinedesk.biz).')
  loglevelchoices = ['none','info','debug']
  parser.add_argument('--loglevel', choices=loglevelchoices,help='Log level to display.')
  parser.add_argument('--test',action='store_true',help='Do non-destructive test parse (not a full parse).')
    # these two options are used by scraperwiki.com
  parser.add_argument('--script',help='the location of the script (optional)')
  parser.add_argument('--scraper',help='the name of the scraper (optional)')
  args = parser.parse_args()

  if args.loglevel in loglevelchoices:
    attr = logging.NOTSET
    if args.loglevel != 'none':
      attr = getattr(logging,args.loglevel.upper())
    logger.setLevel(attr)
  else:
    logger.setLevel(logging.INFO)

  scraper = NCRepScraper()

  if args.test:
    alltowns = scraper.scrapemaster()
    logger.info("Got all towns (%d total)" % len(alltowns))
    logger.info("Getting details for: %s" % alltowns[0])
    logger.info("Details = %s" % scraper.scrapedetail(alltowns[0]))
  else:
    alltowns = scraper.scrapemaster()
    logger.info("Got all towns (%d total)" % len(alltowns))
    cnt = 1
    for town in alltowns:
      logger.info("%d/%d Getting details for: %s" % (cnt,len(alltowns),town))
      data = scraper.scrapedetail(town)
      logger.debug("Details = %s" % data)
      #data['Officials'] = ' -- '.join([str(x) for x in data['Officials']])
      towndata = {
        'City'       : data['City'],
        'Source'     : data['Source'],
        'Population' : data['Population'],
        'Website'    : data['Website'],
        'Phone'      : data['Phone']
      }
      scraperwiki.sqlite.save(unique_keys=['Source'], data=towndata,table_name="cities")
      for k,v in data['Officials'].items():
        repdata = {
          'Source': data['Source'],
          'City': data['City'],
          'Title': k,
          'Name': v
        }
        scraperwiki.sqlite.save(unique_keys=['Source','Title','Name'], data=repdata,table_name="reps")
      if data['County']:
        for c in data['County']:
          cdata = {
            'Source': data['Source'],
            'County': c
          }
          scraperwiki.sqlite.save(unique_keys=['Source','County'], data=cdata,table_name="counties")
      cnt += 1
