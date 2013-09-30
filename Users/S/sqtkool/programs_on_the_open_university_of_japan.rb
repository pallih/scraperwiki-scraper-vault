# -*- coding: utf-8 -*-

require 'nkf'

$KCODE = 'UTF8' if RUBY_VERSION < '1.9.0'
ENV['TZ'] = 'Asia/Tokyo'

def fetch(date)
  ScraperWiki.scrape(sprintf('http://www.ouj.ac.jp/hp/bangumi2/bangumi.php?month=%d&date=%d', date.month, date.day))
end

def parse(html, date)
  NKF.nkf('-Ew', html).match(/
    (?:document\.open\(\);(.+?)document\.close\(\);)
    .+?
    (?:document\.open\(\);(.+?)document\.close\(\);)
  /mx)[1,2].zip(%w(tv radio)).map {|doc, media|
    parse_programs(doc, media, date)
  }.flatten
end

def parse_programs(doc, media, date)
  programs = []
  channel = 1
  last_time = Time.local(date.year, date.month, date.day, 0, 0)
  doc.split(/^.*?<TD class='content_in_.*$/)[1..-1].each do |lines|
    begin
      lines = lines.strip.split("\n").map {|line| (line.match(/\("(.*)"\)/) || [])[1] }
      time = parse_time(lines[0], date)
      title, link = parse_title(lines[1])
      subtitle, cast = parse_descs(lines[2..-1])
      cast = cast.gsub('担当講師：', '') if cast

      channel += 1 if last_time > time
      last_time = time

      programs << {
        'time' => time.getutc.strftime('%Y-%m-%d %H:%M:%S'),
        'title' => title,
        'link' => link,
        'subtitle' => subtitle,
        'cast' => cast,
        'channel' => channel,
        'media' => media
      }
    rescue
    end
  end
  programs
end

def parse_time(str, date)
  hour, min = str.strip.split(':').map {|n| n.to_i(10) }
  Time.local(date.year, date.month, date.day + (hour >= 24 ? 1 : 0), hour % 24, min)
end

def parse_title(str)
  link = nil
  if m = str.match(/^<a[^>]*?href='([^']+)'/i)
    link = m[1]
  end
  title = str.gsub(/<[^>]+>/, '').strip
  raise if title.empty? 
  [title, link]
end

def parse_descs(lines)
  descs = []
  lines.each do |line|
    break if !line || line.empty? || line.match(/^<\//)
    descs << line.gsub(/<[^>]+>/, '').strip
  end
  descs
end

def save(programs)
  ScraperWiki.save_sqlite(%w(media channel time), programs)
end

tomorrow = Time.now + 60 * 60 * 24
save(parse(fetch(tomorrow), tomorrow))# -*- coding: utf-8 -*-

require 'nkf'

$KCODE = 'UTF8' if RUBY_VERSION < '1.9.0'
ENV['TZ'] = 'Asia/Tokyo'

def fetch(date)
  ScraperWiki.scrape(sprintf('http://www.ouj.ac.jp/hp/bangumi2/bangumi.php?month=%d&date=%d', date.month, date.day))
end

def parse(html, date)
  NKF.nkf('-Ew', html).match(/
    (?:document\.open\(\);(.+?)document\.close\(\);)
    .+?
    (?:document\.open\(\);(.+?)document\.close\(\);)
  /mx)[1,2].zip(%w(tv radio)).map {|doc, media|
    parse_programs(doc, media, date)
  }.flatten
end

def parse_programs(doc, media, date)
  programs = []
  channel = 1
  last_time = Time.local(date.year, date.month, date.day, 0, 0)
  doc.split(/^.*?<TD class='content_in_.*$/)[1..-1].each do |lines|
    begin
      lines = lines.strip.split("\n").map {|line| (line.match(/\("(.*)"\)/) || [])[1] }
      time = parse_time(lines[0], date)
      title, link = parse_title(lines[1])
      subtitle, cast = parse_descs(lines[2..-1])
      cast = cast.gsub('担当講師：', '') if cast

      channel += 1 if last_time > time
      last_time = time

      programs << {
        'time' => time.getutc.strftime('%Y-%m-%d %H:%M:%S'),
        'title' => title,
        'link' => link,
        'subtitle' => subtitle,
        'cast' => cast,
        'channel' => channel,
        'media' => media
      }
    rescue
    end
  end
  programs
end

def parse_time(str, date)
  hour, min = str.strip.split(':').map {|n| n.to_i(10) }
  Time.local(date.year, date.month, date.day + (hour >= 24 ? 1 : 0), hour % 24, min)
end

def parse_title(str)
  link = nil
  if m = str.match(/^<a[^>]*?href='([^']+)'/i)
    link = m[1]
  end
  title = str.gsub(/<[^>]+>/, '').strip
  raise if title.empty? 
  [title, link]
end

def parse_descs(lines)
  descs = []
  lines.each do |line|
    break if !line || line.empty? || line.match(/^<\//)
    descs << line.gsub(/<[^>]+>/, '').strip
  end
  descs
end

def save(programs)
  ScraperWiki.save_sqlite(%w(media channel time), programs)
end

tomorrow = Time.now + 60 * 60 * 24
save(parse(fetch(tomorrow), tomorrow))