require 'date'
require 'open-uri'
require 'net/http'
require 'uri'
require 'nokogiri'

RFC2822 = '%a, %d %b %Y %H:%M:%S %z'
BASE_URL = 'http://www.monumental.co.cr/programas/96/Asi-es-la-cosa'

def to_unix_epoch(date)
  datetime = DateTime.strptime(date, RFC2822)
  return datetime.strftime('%s').to_i
end

def get_info(url)
  p url
  uri = URI(url)
  req = Net::HTTP.new(uri.host, uri.port) or return nil
  ans = req.request_head(uri.path)
  return nil if ans.nil? || ans.code_type == Net::HTTPNotFound
  date = to_unix_epoch(ans['last-modified'] || ans['Date'])
  length = ans['content-length'].to_i
  return (date.nil? || length == 0) ? 
    nil :
    {
      :link      => uri.to_s,
      :published => date,
      :length    => length
    }
end

def get_desc(url)
  doc = Nokogiri::HTML(open(url)) or return nil
  desc = doc.css('div#op-content div.content p').map { |p|
    p.inner_text.strip
  }.join('')
  return desc
end

def get_entries(url)
  entries = []
  doc = Nokogiri::HTML(open(url)) or return nil
  doc.css('div.view-Podcasts div.view-content div.item-list ul li').each do |li|
    a_title=li.css('h3.title a').first
    a_audio=li.css('span.link a').first
    next if a_title.nil? || a_audio.nil? 
    link = URI::join(url, a_title['href']).to_s
    title = a_title.inner_text
    audio = URI::join(url, a_audio['href']).to_s
    entries.push({
      :title => title,
      :audio => audio,
      :url   => link
    })
  end
  return entries
end

get_entries(BASE_URL).each do |entry|
  entry[:description] = get_desc(entry[:url]) || 'N/A'
  entry.merge!(get_info(entry[:audio]))
  ScraperWiki.save_sqlite([:audio], entry, 'audio')
endrequire 'date'
require 'open-uri'
require 'net/http'
require 'uri'
require 'nokogiri'

RFC2822 = '%a, %d %b %Y %H:%M:%S %z'
BASE_URL = 'http://www.monumental.co.cr/programas/96/Asi-es-la-cosa'

def to_unix_epoch(date)
  datetime = DateTime.strptime(date, RFC2822)
  return datetime.strftime('%s').to_i
end

def get_info(url)
  p url
  uri = URI(url)
  req = Net::HTTP.new(uri.host, uri.port) or return nil
  ans = req.request_head(uri.path)
  return nil if ans.nil? || ans.code_type == Net::HTTPNotFound
  date = to_unix_epoch(ans['last-modified'] || ans['Date'])
  length = ans['content-length'].to_i
  return (date.nil? || length == 0) ? 
    nil :
    {
      :link      => uri.to_s,
      :published => date,
      :length    => length
    }
end

def get_desc(url)
  doc = Nokogiri::HTML(open(url)) or return nil
  desc = doc.css('div#op-content div.content p').map { |p|
    p.inner_text.strip
  }.join('')
  return desc
end

def get_entries(url)
  entries = []
  doc = Nokogiri::HTML(open(url)) or return nil
  doc.css('div.view-Podcasts div.view-content div.item-list ul li').each do |li|
    a_title=li.css('h3.title a').first
    a_audio=li.css('span.link a').first
    next if a_title.nil? || a_audio.nil? 
    link = URI::join(url, a_title['href']).to_s
    title = a_title.inner_text
    audio = URI::join(url, a_audio['href']).to_s
    entries.push({
      :title => title,
      :audio => audio,
      :url   => link
    })
  end
  return entries
end

get_entries(BASE_URL).each do |entry|
  entry[:description] = get_desc(entry[:url]) || 'N/A'
  entry.merge!(get_info(entry[:audio]))
  ScraperWiki.save_sqlite([:audio], entry, 'audio')
end