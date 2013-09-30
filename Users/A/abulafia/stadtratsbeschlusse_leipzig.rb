require 'nokogiri'
require 'open-uri'
require 'uri'
require 'date'

URL = "http://notes.leipzig.de/APPL/LAURA/WP5/kais02.nsf/WEBBeschlussAusw2?OpenView&RestrictToCategory=2013-----alleEinreicher"

SEL_CONTAINER = "form > table > tbody"
SEL_ROW       = "tr"

def fetch(url=URL)
  doc  = open(url)
  page = Nokogiri::HTML(doc)
end

def parse_date(string)
  begin
    Date.strptime string, "%m/%d/%Y"
  rescue
    nil
  end
end

def build_url(url)
 ["http://notes.leipzig.de", url].join("")
end

def get_rows(page)

  rows = page.search('//form/table/tr[@valign="top"]').map do |row|

    beschlussnr = row.at('./td[1]').content rescue ''
    url         = row.at('./td[1]//a[1]')['href']
    betreff     = row.at('./td[3]').content rescue ''
    datum       = row.at('./td[4]').content rescue ''
    dsnr        = row.at('./td[5]').content rescue ''
    termin      = row.at('./td[6]').content rescue ''
    stand       = row.at('./td[9]').content rescue ''

    {
      beschlussnr: beschlussnr,
      url:         build_url(url),
      betreff:     betreff,
      datum:       parse_date(datum),
      dsnr:        dsnr,
      termin:      parse_date(termin),
      stand:       stand
    }
  end
end

page = fetch(URL)
rows = get_rows(page)

rows.each do |record|
  ScraperWiki.save_sqlite(['beschlussnr'], record)
end

require 'nokogiri'
require 'open-uri'
require 'uri'
require 'date'

URL = "http://notes.leipzig.de/APPL/LAURA/WP5/kais02.nsf/WEBBeschlussAusw2?OpenView&RestrictToCategory=2013-----alleEinreicher"

SEL_CONTAINER = "form > table > tbody"
SEL_ROW       = "tr"

def fetch(url=URL)
  doc  = open(url)
  page = Nokogiri::HTML(doc)
end

def parse_date(string)
  begin
    Date.strptime string, "%m/%d/%Y"
  rescue
    nil
  end
end

def build_url(url)
 ["http://notes.leipzig.de", url].join("")
end

def get_rows(page)

  rows = page.search('//form/table/tr[@valign="top"]').map do |row|

    beschlussnr = row.at('./td[1]').content rescue ''
    url         = row.at('./td[1]//a[1]')['href']
    betreff     = row.at('./td[3]').content rescue ''
    datum       = row.at('./td[4]').content rescue ''
    dsnr        = row.at('./td[5]').content rescue ''
    termin      = row.at('./td[6]').content rescue ''
    stand       = row.at('./td[9]').content rescue ''

    {
      beschlussnr: beschlussnr,
      url:         build_url(url),
      betreff:     betreff,
      datum:       parse_date(datum),
      dsnr:        dsnr,
      termin:      parse_date(termin),
      stand:       stand
    }
  end
end

page = fetch(URL)
rows = get_rows(page)

rows.each do |record|
  ScraperWiki.save_sqlite(['beschlussnr'], record)
end

