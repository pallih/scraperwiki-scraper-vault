# -*- coding: utf-8 -*-
# Tokyo OperaCity Hall Event Calendar

require 'date'
require 'json'

DEBUG = false

BASE_URL = 'http://www.operacity.jp/contents/performance/calendar/ja'
BASE_URL_OF_DETAILS = 'http://www.operacity.jp'

# creates a context.
#
# This method never returns nil.
#
def create_context
  urls = []

  d = Date::today
  for i in 1..4
    urls << '%s/%04d/%02d' % [BASE_URL, d.year, d.month]
    d = d >> 1
  end

  {:urls => urls}
end

# retrieves a text refered by 'url'
#
def get_page(url)
  return nil if url.nil? 

  puts ("DEBUG: " + url) if DEBUG

  sleep 2
  ScraperWiki.scrape(url)
end

# parses a given text and returns the list of objects extracted from the text.
# In this program, the text is in the form of JSON.
#
def parse_a_page(ctx, page_text)
  return nil if ctx.nil? 
  return nil if page_text.nil? 

  perf_cal = JSON.parse(page_text, :symbolize_names => true)

  perfs = []
  perf_cal[:weeks].each do |perfs_of_week|
    perfs_of_week.each do |perfs_of_day|

      perfs_of_day[:performances].each do |perf|
        perfs << {
          :DATETIME => perf[:date] + ' ' + perf[:time],
          :TITLE => perf[:title],
          :HALL => (perf[:hall] == '1' ? 'C' : 'R'),
          :DETAILS => (perf[:is_available_detail] ? 
            BASE_URL_OF_DETAILS + perf[:detail_link_uri] : nil)
        }
      end
    end
  end

  return perfs
end

# saves performance data in the DB.
#
def save_perfs(perfs)
  return if perfs.nil? 

  perfs.each do |perf|
    ScraperWiki.save_sqlite(unique_keys=['DATETIME', 'HALL'], data=perf, tablename='event')
  end

end

# delete all data in the DB.
#
def clear_db()
  ScraperWiki.sqliteexecute('DELETE FROM event')
end

def manage_db
   #ScraperWiki.sqliteexecute("CREATE TABLE event (DATETIME, TITLE, HALL, DETAILS)")
   #ScraperWiki.sqliteexecute("DROP TABLE if exists event")
end

# main method.
#
def main

  ctx = create_context()

  perfs = []
  for url in ctx[:urls]
    page_text = get_page(url)

    perfs += parse_a_page(ctx, page_text)
  end

  if !perfs.nil? and 0 < perfs.length then
    clear_db()
    save_perfs(perfs)
  end

end

main
#manage_db

# -*- coding: utf-8 -*-
# Tokyo OperaCity Hall Event Calendar

require 'date'
require 'json'

DEBUG = false

BASE_URL = 'http://www.operacity.jp/contents/performance/calendar/ja'
BASE_URL_OF_DETAILS = 'http://www.operacity.jp'

# creates a context.
#
# This method never returns nil.
#
def create_context
  urls = []

  d = Date::today
  for i in 1..4
    urls << '%s/%04d/%02d' % [BASE_URL, d.year, d.month]
    d = d >> 1
  end

  {:urls => urls}
end

# retrieves a text refered by 'url'
#
def get_page(url)
  return nil if url.nil? 

  puts ("DEBUG: " + url) if DEBUG

  sleep 2
  ScraperWiki.scrape(url)
end

# parses a given text and returns the list of objects extracted from the text.
# In this program, the text is in the form of JSON.
#
def parse_a_page(ctx, page_text)
  return nil if ctx.nil? 
  return nil if page_text.nil? 

  perf_cal = JSON.parse(page_text, :symbolize_names => true)

  perfs = []
  perf_cal[:weeks].each do |perfs_of_week|
    perfs_of_week.each do |perfs_of_day|

      perfs_of_day[:performances].each do |perf|
        perfs << {
          :DATETIME => perf[:date] + ' ' + perf[:time],
          :TITLE => perf[:title],
          :HALL => (perf[:hall] == '1' ? 'C' : 'R'),
          :DETAILS => (perf[:is_available_detail] ? 
            BASE_URL_OF_DETAILS + perf[:detail_link_uri] : nil)
        }
      end
    end
  end

  return perfs
end

# saves performance data in the DB.
#
def save_perfs(perfs)
  return if perfs.nil? 

  perfs.each do |perf|
    ScraperWiki.save_sqlite(unique_keys=['DATETIME', 'HALL'], data=perf, tablename='event')
  end

end

# delete all data in the DB.
#
def clear_db()
  ScraperWiki.sqliteexecute('DELETE FROM event')
end

def manage_db
   #ScraperWiki.sqliteexecute("CREATE TABLE event (DATETIME, TITLE, HALL, DETAILS)")
   #ScraperWiki.sqliteexecute("DROP TABLE if exists event")
end

# main method.
#
def main

  ctx = create_context()

  perfs = []
  for url in ctx[:urls]
    page_text = get_page(url)

    perfs += parse_a_page(ctx, page_text)
  end

  if !perfs.nil? and 0 < perfs.length then
    clear_db()
    save_perfs(perfs)
  end

end

main
#manage_db

