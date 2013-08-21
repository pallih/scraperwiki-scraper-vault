#!/usr/bin/env ruby

require 'date'
require 'open-uri'
require 'net/http'
require 'uri'
require 'nokogiri'

RFC2822 = '%a, %d %b %Y %H:%M:%S %z'
BASE_URL = 'http://radios.ucr.ac.cr/radio-a-la-carta/de-la-a-a-la-z.html'
MONTHS = {
  "Ene" => 1, "Feb" =>  2, "Mar" =>  3, "Abr" =>  4,
  "May" => 5, "Jun" =>  6, "Jul" =>  7, "Ago" =>  8,
  "Sep" => 9, "Oct" => 10, "Nov" => 11, "Dic" => 12,
}

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

def get_date(title)
  m = title.match(%r{(\d+)/(\w+)/(\d+)})
  return if m.nil? 
  datetime = DateTime.strptime(
    "%d/%d/%d" % [m[1].to_i, MONTHS[m[2]], m[3].to_i],
    "%d/%m/%Y")
  return datetime.strftime('%s').to_i
end

def get_entries(url, show_id)
  entries = []
  doc = Nokogiri::HTML(open(url)) or return nil
  # 
  # tr div.descripcion
  # a.jce_file_custom href="ftp://163.178.18.201/RadioUniversidad/2013/Desayunos/Desayunos-02-07-2013.MP3"
  # tr.descripcion
  doc.css('table.ucrftp_mp3browser').each do |table|
    rows = table.css('tr')
    until rows.empty? 
      r_link = rows.shift
      r_desc = rows.shift
      next if r_link.nil? or r_desc.nil? 
      links = r_link.css('a.jce_file_custom').
        map { |a| URI.join(url, URI.escape(a['href'])).to_s }.
        select { |href| href =~ /\.mp3$/i }
      next if links[0].nil? 
      title = r_link.css('div.descripcion')[0]
      next if title.nil? 
      title = title.content.strip
      m = title.match(%r{(\d+)/(\w+)/(\d+)})
      #info = get_info(links[0])
      #next if info.nil? 
      entries.push({
        :show_id   => show_id,
        :title     => title,
        :audio     => links[0].to_s,
        :desc      => r_desc.content.strip,
        :published => get_date(title),
        #:length    => info[:length]
      })
    end
  end
  return entries
end

def get_shows(url)
  doc = Nokogiri::HTML(open(url)) or return nil
  doc.css('div#id_columna_principal span.title a').
  select {|a| a['href'] =~ %r{/programas/[^/]+/\d+-[^/]+\.html$} }.
  map do |a|
    ref = URI::join(url, a['href'])
    m = %r{/(\d+)-[^/]+\.html$}.match(ref.path)
    title = a.content
    {
      :id    => m[1].to_i,
      :title => title,
      :url   => ref.to_s,
    }
  end
end

# ScraperWiki.sqliteexecute('DELETE FROM audio WHERE length=0')
# ScraperWiki.commit

get_shows(BASE_URL).each do |show|
  ScraperWiki.save_sqlite([:id], show, 'shows')
  get_entries(show[:url], show[:id]).each do |entry|
    ScraperWiki.save_sqlite([:audio], entry, 'audio')
  end
end