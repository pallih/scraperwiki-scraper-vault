require 'date'
require 'open-uri'
require 'nokogiri'
require 'digest/md5'

YEARS = (1997..2013).to_a
MONTHS = (1..12).to_a.product(YEARS) # [[1,1997], [2,1997]...]

URL_TEMPLATE = "http://www.landtag.sachsen.de/de/aktuelles/sitzungskalender/monat.do?skalender[monat]=%i&skalender[jahr]=%i#tgo-protokolle"

SEL_CONTAINER = "#tgo-protokolle .first-column dl"
SEL_TITLE = "dt"

def fetch(monthyear)
  uri  = URL_TEMPLATE % monthyear
  html = open(uri).read
  doc  = Nokogiri::HTML(html)
end

def get_titles(doc)
  doc.css(SEL_CONTAINER).css(SEL_TITLE).map(&:text)
end

def parse_title(title)
  regex = /\A(.*) vom (\d+\.\d+\.\d+) .*\Z/  # ignores timeranges
  name, date = title.match(regex)[1..2]
  date = if date
    Date.parse(date)
  end
  [name, date]
end

def make_record(title)
  name, date = parse_title(title)
  datepart = date.nil? ? SecureRandom.hex : date.iso8601
  id = Digest::MD5.hexdigest([name, datepart].join("-"))
  {
    :id   => id,
    :name => name,
    :date => (date && date.iso8601) 
  }
end

def parse_month(monthyear)
  doc = fetch(monthyear)
  titles = get_titles(doc)
  titles.map {|title| make_record(title)}
end

def save(record)
  ScraperWiki.save_sqlite(['id'], record)
end

def scrape(monthyear)
  records = parse_month(monthyear)
  # puts records
  records.each {|record| save(record)}
end

MONTHS.each {|m| scrape(m)}

