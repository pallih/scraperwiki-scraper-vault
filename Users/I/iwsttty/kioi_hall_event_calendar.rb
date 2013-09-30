# -*- encoding: utf-8 -*-
# KIOI Hall Event Calendar

require 'nokogiri'

$now = Time.now

TARGETS =
  [{'HALL' => 'H', # means Hall
     'REGEX_MONTH' => '(\d+)月.',
     'REGEX_DATETIME' => '(\d+)（.*）(?:(\d\d?):(\d\d?))?',
     'REGEX_PLAYERS' => '^■(.+)$',
     'REGEX_PROGRAM' => '^●(.+)$',
     'REGEX_CONTACT' => '^☎.(.+)$',
     'REGEX_FEE' => '^◆(.+)$',
     'URL' =>  "http://www.kioi-hall.or.jp/calendar/index_h.html"},
   {'HALL' => 'S', # means Small hall
     'REGEX_MONTH' => '(\d+)月.',
     'REGEX_DATETIME' => '(\d+)（.*）\s*(?:(\d\d?)時(?:(\d\d?)分)?)?',
     'REGEX_PLAYERS' => '出演(.+)$',
     'REGEX_PROGRAM' => '(?:曲目|演目)(.+)$',
     'REGEX_CONTACT' => '^お問合せ\s+(.+)$',
     'REGEX_FEE' => '(全席.*)$',
     'URL' => 'http://www.kioi-hall.or.jp/calendar/index_s.html'}]

#
# returns DOM object of the page pointed by "url".
#
def get_document(url)
  if url.nil? then
    return nil
  end
  
  return Nokogiri::HTML::Document.parse(ScraperWiki.scrape(url), url, "Shift_JIS")
end

#
# make datetime string in the format of "yyyy-mm-dd HH:MM:SS"
# from a month digit and a string in the datetime node.
#
def make_datetime(ctx, node_datetime, month)
  if node_datetime.nil?  then
    return nil
  end

  if /#{ctx['REGEX_DATETIME']}/ !~ node_datetime.text then
    return nil
  end

  now_year = $now.year
  if month < $now.month
    now_year += 1
  end

  if $2.nil? then
    return sprintf('%d-%d-%d', now_year, month, $1)
  elsif $3.nil? then
    return sprintf('%d-%d-%d %s:00:00', now_year, month, $1, $2)
  else
    return sprintf('%d-%d-%d %s:%s:00', now_year, month, $1, $2, $3)
  end
end

#
# parses TD node to get an event information.
#
def parse_event_info(ctx, node_td)
  if node_td.nil? then
    return nil
  end

  event_info = {}

  lines = node_td.children()
  lines.shift # skip first line

  title = node_td.xpath('./font[1]').text
  title = title.gsub(/\r|\n/, '')
  event_info['TITLE'] = title.strip

  lines.each do |l|
    info_line = l.text.strip
    if 0 == info_line.length then
      next
    end

    case info_line
    when /#{ctx['REGEX_PLAYERS']}/
      event_info['PLAYERS'] = $1.strip
    when /#{ctx['REGEX_PROGRAM']}/
      event_info['PROGRAM'] = $1.strip
    when /#{ctx['REGEX_CONTACT']}/
      event_info['CONTACT'] = $1.strip
    when /#{ctx['REGEX_FEE']}/
      event_info['FEE'] = $1.strip
    end
  end

  event_info['HALL'] = ctx['HALL']

  return event_info
end

#
# parses a calendar table of a month.
#
def parse_calendar_table(ctx, node_table, month)
  if node_table.nil? then
    return
  end

  event_infos = []
  node_table.xpath('./tr').each do |node_tr|
    event_datetime = make_datetime(ctx, node_tr.children()[0], month)
    if event_datetime.nil? then
      next
    end

    event_info = parse_event_info(ctx, node_tr.children()[2])
    if !event_info.nil? and 0 < event_info['TITLE'].length then
      event_info['DATETIME'] = event_datetime
      event_infos << event_info
    end
  end

  return event_infos
end

#
# parses all calendars in a page and makes an array containing all event informations.
#
def parse_calendar_page(ctx, doc)
  is_table_found = false
  parsed_month = -1

  all_programs = []
  doc.xpath('//table').each do |node_table|
    if is_table_found == true then
      programs = parse_calendar_table(ctx, node_table, parsed_month)
      all_programs = all_programs + programs
      is_table_found = false
      next
    end

    nodes_month = node_table.xpath('./tr/td/a/font/b')
    if 0 < nodes_month.size and /#{ctx['REGEX_MONTH']}/ =~ nodes_month[0].text then
      parsed_month = $1.to_i
      is_table_found = true
    end
  end

  return all_programs
end

#
# saves the event informations to the SQLite.
#
def save_event_infos(infos)
  if infos.nil? then
    return
  end

  infos.each do |p|
    ScraperWiki.save_sqlite(unique_keys=['DATETIME', 'HALL'], data=p, tablename='events')
  end
end

#
# gets the HTML document and parses it.
#
def main

  TARGETS.each do |target|
    warn('URL:' << target['URL'])
    doc = get_document(target['URL'])
    if doc.nil? then
      warn('no data from ' << target['URL'])
      next
    end

    infos = parse_calendar_page(target, doc)
    save_event_infos(infos)
  end
end

def maintain_db
  #ScraperWiki.sqliteexecute("create table concert (DATETIME, TITLE, PROGRAM, PLAYERS, CONTACT, FEE)")
  #ScraperWiki.sqliteexecute("drop table if exists concert")
  #ScraperWiki.sqliteexecute("delete from concert")
end

main
#maintain_db

# -*- encoding: utf-8 -*-
# KIOI Hall Event Calendar

require 'nokogiri'

$now = Time.now

TARGETS =
  [{'HALL' => 'H', # means Hall
     'REGEX_MONTH' => '(\d+)月.',
     'REGEX_DATETIME' => '(\d+)（.*）(?:(\d\d?):(\d\d?))?',
     'REGEX_PLAYERS' => '^■(.+)$',
     'REGEX_PROGRAM' => '^●(.+)$',
     'REGEX_CONTACT' => '^☎.(.+)$',
     'REGEX_FEE' => '^◆(.+)$',
     'URL' =>  "http://www.kioi-hall.or.jp/calendar/index_h.html"},
   {'HALL' => 'S', # means Small hall
     'REGEX_MONTH' => '(\d+)月.',
     'REGEX_DATETIME' => '(\d+)（.*）\s*(?:(\d\d?)時(?:(\d\d?)分)?)?',
     'REGEX_PLAYERS' => '出演(.+)$',
     'REGEX_PROGRAM' => '(?:曲目|演目)(.+)$',
     'REGEX_CONTACT' => '^お問合せ\s+(.+)$',
     'REGEX_FEE' => '(全席.*)$',
     'URL' => 'http://www.kioi-hall.or.jp/calendar/index_s.html'}]

#
# returns DOM object of the page pointed by "url".
#
def get_document(url)
  if url.nil? then
    return nil
  end
  
  return Nokogiri::HTML::Document.parse(ScraperWiki.scrape(url), url, "Shift_JIS")
end

#
# make datetime string in the format of "yyyy-mm-dd HH:MM:SS"
# from a month digit and a string in the datetime node.
#
def make_datetime(ctx, node_datetime, month)
  if node_datetime.nil?  then
    return nil
  end

  if /#{ctx['REGEX_DATETIME']}/ !~ node_datetime.text then
    return nil
  end

  now_year = $now.year
  if month < $now.month
    now_year += 1
  end

  if $2.nil? then
    return sprintf('%d-%d-%d', now_year, month, $1)
  elsif $3.nil? then
    return sprintf('%d-%d-%d %s:00:00', now_year, month, $1, $2)
  else
    return sprintf('%d-%d-%d %s:%s:00', now_year, month, $1, $2, $3)
  end
end

#
# parses TD node to get an event information.
#
def parse_event_info(ctx, node_td)
  if node_td.nil? then
    return nil
  end

  event_info = {}

  lines = node_td.children()
  lines.shift # skip first line

  title = node_td.xpath('./font[1]').text
  title = title.gsub(/\r|\n/, '')
  event_info['TITLE'] = title.strip

  lines.each do |l|
    info_line = l.text.strip
    if 0 == info_line.length then
      next
    end

    case info_line
    when /#{ctx['REGEX_PLAYERS']}/
      event_info['PLAYERS'] = $1.strip
    when /#{ctx['REGEX_PROGRAM']}/
      event_info['PROGRAM'] = $1.strip
    when /#{ctx['REGEX_CONTACT']}/
      event_info['CONTACT'] = $1.strip
    when /#{ctx['REGEX_FEE']}/
      event_info['FEE'] = $1.strip
    end
  end

  event_info['HALL'] = ctx['HALL']

  return event_info
end

#
# parses a calendar table of a month.
#
def parse_calendar_table(ctx, node_table, month)
  if node_table.nil? then
    return
  end

  event_infos = []
  node_table.xpath('./tr').each do |node_tr|
    event_datetime = make_datetime(ctx, node_tr.children()[0], month)
    if event_datetime.nil? then
      next
    end

    event_info = parse_event_info(ctx, node_tr.children()[2])
    if !event_info.nil? and 0 < event_info['TITLE'].length then
      event_info['DATETIME'] = event_datetime
      event_infos << event_info
    end
  end

  return event_infos
end

#
# parses all calendars in a page and makes an array containing all event informations.
#
def parse_calendar_page(ctx, doc)
  is_table_found = false
  parsed_month = -1

  all_programs = []
  doc.xpath('//table').each do |node_table|
    if is_table_found == true then
      programs = parse_calendar_table(ctx, node_table, parsed_month)
      all_programs = all_programs + programs
      is_table_found = false
      next
    end

    nodes_month = node_table.xpath('./tr/td/a/font/b')
    if 0 < nodes_month.size and /#{ctx['REGEX_MONTH']}/ =~ nodes_month[0].text then
      parsed_month = $1.to_i
      is_table_found = true
    end
  end

  return all_programs
end

#
# saves the event informations to the SQLite.
#
def save_event_infos(infos)
  if infos.nil? then
    return
  end

  infos.each do |p|
    ScraperWiki.save_sqlite(unique_keys=['DATETIME', 'HALL'], data=p, tablename='events')
  end
end

#
# gets the HTML document and parses it.
#
def main

  TARGETS.each do |target|
    warn('URL:' << target['URL'])
    doc = get_document(target['URL'])
    if doc.nil? then
      warn('no data from ' << target['URL'])
      next
    end

    infos = parse_calendar_page(target, doc)
    save_event_infos(infos)
  end
end

def maintain_db
  #ScraperWiki.sqliteexecute("create table concert (DATETIME, TITLE, PROGRAM, PLAYERS, CONTACT, FEE)")
  #ScraperWiki.sqliteexecute("drop table if exists concert")
  #ScraperWiki.sqliteexecute("delete from concert")
end

main
#maintain_db

