require 'nokogiri'

def pageURL(year,event)
  "http://lanyrd.com/#{year}/#{event}/"
end

def fetchSessionsPage(year,event)
  html = ScraperWiki.scrape(pageURL(year,event)) rescue false
  Nokogiri::HTML.parse(html) if html
end

def fetchSessionDetailsPage(url)
  html = ScraperWiki.scrape(url) rescue false
  Nokogiri::HTML.parse(html) if html
end

doc = fetchSessionsPage(2011,'higheredphilly')
sessions = doc.css('#session-list li')

sessions.each do |li|
  title_link = li.css('h3 a')
  session = {}

  #title and url
  session['title'] = title_link.text
  session['url'] = "http://lanyrd.com#{title_link.attr('href').text}"
  
  #scrape session-specific page for its details
  sessionDoc = fetchSessionDetailsPage(session['url'])

  #get speakers
  speakers = ""
  speaker_block = li.css('p')
  speakers = speaker_block.inner_text.to_s if !speaker_block.empty? 
  speakers = speakers[13..speakers.length] if !speaker_block.empty? 
  session['speakers'] = speakers

  #get abstract
  abstract = ""
  abstract_block = sessionDoc.css('.abstract')
  session['abstract'] = abstract_block.inner_html.split.join(' ')

  #get room
  room = ""
  has_room = (session['abstract'][0..8] === "<p>Room: " || session['abstract'] === '<p>room: ')
  room = session['abstract'][9..11] if has_room
  session['abstract'] = session['abstract'][16..session['abstract'].length] if has_room
  session['room'] = room

  #get times
  time_start_block = sessionDoc.css('.session-meta-item .dtstart')
  time_start = ""
  time_start = time_start_block.inner_html if !time_start_block.empty? 
  time_end_block = sessionDoc.css('.session-meta-item .dtend')
  time_end = ""
  time_end = time_end_block.inner_html if !time_end_block.empty? 
  session['start'] = time_start
  session['end'] = time_end

  #save
  ScraperWiki.save_sqlite(unique_keys=['url'], data=session)
end
