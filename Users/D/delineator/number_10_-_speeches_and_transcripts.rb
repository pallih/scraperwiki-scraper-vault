require 'nokogiri'

def find_where text
  if text
    where = case text
      when /\sat (.+) (on|in)/
        $1.split('.').first.split(/\sby\s(\D+)/).first.strip
      when /\sto (.+) (on|in)/
        $1.split('.').first.split(/\sby\s(\D+)/).first.strip
      when /\sat ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      when /\sto ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      when /\sin ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      else
        'unknown'
    end
    where.sub!(/^the /, '')
    where.chomp!(', hosted')
    where = where.split(/Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday/).first.strip.chomp(' on').strip.chomp(',')
    where = where.split(/(on|following) (\d|the)/).first.strip.chomp(',')
    where = where.split('about').first.strip
    where = where.split(/\d\d\s\D+\s\d\d\d\d$/).first.strip.chomp(',')
    where = 'unknown' if where[/^(note$|mark)/i]
    where = 'House of Commons' if where[/House\sof\sCommons/] || where[/House of Commons/]
    where = 'Houses of Parliament' if where[/Houses of Parliament/]
  else
    where = 'unknown'
  end
  where
end

page = 1
finished = false

while !finished do
  url = "http://www.number10.gov.uk/news/speeches-and-transcripts/page/#{page}"
  puts "scraping index page: #{page}"

  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  
  doc.search('.posts_list_post/a').each do |a|
    title = a.inner_text.strip
    permalink = a['href'].to_s

    puts "scraping: #{title}"

    record = {'title' => title, 'permalink' => permalink, 'minister_name' => "David Cameron"}

    speech_or_transcript_html = ScraperWiki.scrape(permalink)
    speech_or_transcript_doc = Nokogiri::HTML(speech_or_transcript_html)

    record['given_on'] = speech_or_transcript_doc.at('.timestamp').inner_text

    body = speech_or_transcript_doc.at('.entry')
    first_paragraph = body.search('p').first.inner_text
    record['body'] = body.inner_html

    record['department'] = "Prime Minister's Office"
    
    where = find_where title
    where = find_where(first_paragraph) if where == 'unknown'
    record['where'] = where

    ScraperWiki.save(['permalink'], record)
  end

  finished = true
  doc.search('a').each do |a|
    has_previous_entries = a.inner_text[/Previous Entries/]
    finished = false if has_previous_entries
  end
  page = page + 1
endrequire 'nokogiri'

def find_where text
  if text
    where = case text
      when /\sat (.+) (on|in)/
        $1.split('.').first.split(/\sby\s(\D+)/).first.strip
      when /\sto (.+) (on|in)/
        $1.split('.').first.split(/\sby\s(\D+)/).first.strip
      when /\sat ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      when /\sto ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      when /\sin ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      else
        'unknown'
    end
    where.sub!(/^the /, '')
    where.chomp!(', hosted')
    where = where.split(/Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday/).first.strip.chomp(' on').strip.chomp(',')
    where = where.split(/(on|following) (\d|the)/).first.strip.chomp(',')
    where = where.split('about').first.strip
    where = where.split(/\d\d\s\D+\s\d\d\d\d$/).first.strip.chomp(',')
    where = 'unknown' if where[/^(note$|mark)/i]
    where = 'House of Commons' if where[/House\sof\sCommons/] || where[/House of Commons/]
    where = 'Houses of Parliament' if where[/Houses of Parliament/]
  else
    where = 'unknown'
  end
  where
end

page = 1
finished = false

while !finished do
  url = "http://www.number10.gov.uk/news/speeches-and-transcripts/page/#{page}"
  puts "scraping index page: #{page}"

  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  
  doc.search('.posts_list_post/a').each do |a|
    title = a.inner_text.strip
    permalink = a['href'].to_s

    puts "scraping: #{title}"

    record = {'title' => title, 'permalink' => permalink, 'minister_name' => "David Cameron"}

    speech_or_transcript_html = ScraperWiki.scrape(permalink)
    speech_or_transcript_doc = Nokogiri::HTML(speech_or_transcript_html)

    record['given_on'] = speech_or_transcript_doc.at('.timestamp').inner_text

    body = speech_or_transcript_doc.at('.entry')
    first_paragraph = body.search('p').first.inner_text
    record['body'] = body.inner_html

    record['department'] = "Prime Minister's Office"
    
    where = find_where title
    where = find_where(first_paragraph) if where == 'unknown'
    record['where'] = where

    ScraperWiki.save(['permalink'], record)
  end

  finished = true
  doc.search('a').each do |a|
    has_previous_entries = a.inner_text[/Previous Entries/]
    finished = false if has_previous_entries
  end
  page = page + 1
end