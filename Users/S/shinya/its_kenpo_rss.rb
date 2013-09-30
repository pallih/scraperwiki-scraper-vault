# coding: utf-8

require 'rss/maker'
require 'locale'

def get_last_ctime()
  ScraperWiki.select('distinct ctime from its_kenpo_1.vacancy').each do |row|
    return row['ctime']
  end
end

def get_ctimes()
  ctimes = []
  ScraperWiki.select('distinct ctime from its_kenpo_1.changes order by ctime desc').each do |row|
    ctimes << row['ctime']
  end
  return ctimes
end

def get_changes(ctime)
  wd = ['日', '月', '火', '水', '木', '金', '土']
  changes = {}
  ScraperWiki.select('name, date from its_kenpo_1.changes where ctime = ?', [ctime]).each do |row|
    name = row['name']
    changes[name] = [] if !changes.has_key? (name)
    t = Time.parse(row['date'])
    changes[name] << t.strftime("%m月%d日(#{%w(日 月 火 水 木 金 土)[t.wday]})")
  end
  return changes
end

url = 'http://yoyaku.its-kenpo.or.jp/its_rsvestab/vacant/its_w_vacant_frame.asp'
begin
  ScraperWiki.attach('its_kenpo_1')

  last_ctime = get_last_ctime()
  raise if last_ctime.nil? 

  rss = RSS::Maker.make('2.0') do |maker|
    maker.channel.title = 'ITS健保 保養施設空室発生状況'
    maker.channel.description = 'ITS健保 保養施設の空室発生状況をお知らせします。'
    maker.channel.link = url
    maker.channel.language = 'ja'
    maker.channel.pubDate = Time.at(last_ctime).strftime('%a, %d %b %Y %H:%M:%S %z')

    get_ctimes().each do |ctime|
      changes = get_changes(ctime)
      next if changes.empty? 

      maker.items.new_item do |item|
        item.title = Time.at(ctime).strftime('%Y年%m月%d日の空室発生状況')
        item.link = url
        description = '<p>次の施設で空室が発生しました。</p>'
        changes.each do |name, dates|
          description += '<p><div>' + name + '</div><div>' + dates.join(', ') + '</div></p>'
        end
        description += '<p><a href="http://yoyaku.its-kenpo.or.jp/its_rsvestab/vacant/its_w_vacant_frame.asp">保養所空室状況</a></p>'
        item.description = description
        item.date = Time.at(ctime).strftime('%a, %d %b %Y %H:%M:%S %z')
      end
    end
  end

  ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )
  puts rss
rescue Exception => err
  puts err
end
# coding: utf-8

require 'rss/maker'
require 'locale'

def get_last_ctime()
  ScraperWiki.select('distinct ctime from its_kenpo_1.vacancy').each do |row|
    return row['ctime']
  end
end

def get_ctimes()
  ctimes = []
  ScraperWiki.select('distinct ctime from its_kenpo_1.changes order by ctime desc').each do |row|
    ctimes << row['ctime']
  end
  return ctimes
end

def get_changes(ctime)
  wd = ['日', '月', '火', '水', '木', '金', '土']
  changes = {}
  ScraperWiki.select('name, date from its_kenpo_1.changes where ctime = ?', [ctime]).each do |row|
    name = row['name']
    changes[name] = [] if !changes.has_key? (name)
    t = Time.parse(row['date'])
    changes[name] << t.strftime("%m月%d日(#{%w(日 月 火 水 木 金 土)[t.wday]})")
  end
  return changes
end

url = 'http://yoyaku.its-kenpo.or.jp/its_rsvestab/vacant/its_w_vacant_frame.asp'
begin
  ScraperWiki.attach('its_kenpo_1')

  last_ctime = get_last_ctime()
  raise if last_ctime.nil? 

  rss = RSS::Maker.make('2.0') do |maker|
    maker.channel.title = 'ITS健保 保養施設空室発生状況'
    maker.channel.description = 'ITS健保 保養施設の空室発生状況をお知らせします。'
    maker.channel.link = url
    maker.channel.language = 'ja'
    maker.channel.pubDate = Time.at(last_ctime).strftime('%a, %d %b %Y %H:%M:%S %z')

    get_ctimes().each do |ctime|
      changes = get_changes(ctime)
      next if changes.empty? 

      maker.items.new_item do |item|
        item.title = Time.at(ctime).strftime('%Y年%m月%d日の空室発生状況')
        item.link = url
        description = '<p>次の施設で空室が発生しました。</p>'
        changes.each do |name, dates|
          description += '<p><div>' + name + '</div><div>' + dates.join(', ') + '</div></p>'
        end
        description += '<p><a href="http://yoyaku.its-kenpo.or.jp/its_rsvestab/vacant/its_w_vacant_frame.asp">保養所空室状況</a></p>'
        item.description = description
        item.date = Time.at(ctime).strftime('%a, %d %b %Y %H:%M:%S %z')
      end
    end
  end

  ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )
  puts rss
rescue Exception => err
  puts err
end
