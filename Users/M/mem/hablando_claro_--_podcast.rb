#!/usr/bin/env ruby

require 'date'
require 'net/http'
require 'uri'
require 'nokogiri'

class DateTime
  def to_i
    self.strftime('%s').to_i
  end
end

MONTHS = %w{
    enero febrero marzo
    abril mayo junio
    julio agosto setiembre
    octubre noviembre diciembre
}
BASE_URL =
  'http://www.hablandoclarocr.com/media/hablando_claro/programas_anteriores/'
URI_FORMAT = BASE_URL + '%02d-%s-%d.mp3'
RSS_URL =
  'http://hablandoclarocr.com/index.php/hablando-claro/programas-columbia?format=feed&type=atom'
DAYS = 10

def get_uri(t)
  URI(URI_FORMAT % [ t.day, MONTHS[t.month-1], t.year ])
end

def get_item(t)
  uri = get_uri(t)
  req = Net::HTTP.new(uri.host, uri.port) or return nil
  ans = req.request_head(uri.path)
  return nil if ans.nil? || ans.code_type == Net::HTTPNotFound
  return {
    :link      => uri.to_s,
    :date      => t.to_i,
    :published => ans['last-modified'],
    :length    => ans['content-length'].to_i
  }
end

def get_date(date, published)
  day = mon = year = nil
  published = DateTime.parse(published)

  if date =~ /^(\d+)\s+de\s+(\w+)$/
    day = $1
    mon = MONTHS.find_index($2)+1
    # date is missing a year, get it from published
    if published
      year = published.year
    end
  elsif date =~ /^(\d+)\s+de\s+(\w+) de (\d+)$/
    day = $1
    mon = MONTHS.find_index($2)+1
    year = $3
  else
    if published
      day, mon, year =
        published.day, published.month, published.year
    end
  end
  date = DateTime.parse('%d/%d/%d' % [ year, mon, day ].map { |v| v.to_i })
  return date.to_i
end

def get_rss(url)
  entries = []
  xml = ScraperWiki.scrape(url) or return nil
  doc = Nokogiri::XML(xml) or return nil
  doc.search('entry').each do |entry|
    data = {}
    %w{link title summary published}.each do |tag|
      if i = entry.at_css(tag)
        case tag
          when 'title'
            data['date'], data['title'] = i.text.split(/:\s*/, 2)
          when 'link'
            data[tag] = i['href']
          else
            data[tag] = i.text
        end
      end
    end
    data['date'] =
      get_date(data['date'], data['published'])
    entries << data
  end
  return entries
end

def process
  t0 = DateTime.parse((DateTime.now - DAYS).strftime('%Y/%m/%d'))
  0.upto(DAYS).each do |day|
    t = t0 + day
    if (1..5).member?(t.wday)
      if data = get_item(t)
        ScraperWiki.save_sqlite([:link], data, 'audio')
      end
    end
  end
  if data = get_rss(RSS_URL)
    ScraperWiki.save_sqlite([:link], data, 'info')
  end
end

process