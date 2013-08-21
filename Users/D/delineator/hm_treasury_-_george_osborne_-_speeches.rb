require 'nokogiri'
require 'uri'

def find_where text
  if text
    text = text.sub('to the Treasury','')
    where = case text
      when /\sat (.+) (on|\.)/
        $1.split('.').first.split(/\sby\s(\D+)/).first.strip
      when /\sto (.+) (on|in)/
        $1.split('.').first.split(/\sby\s(\D+)/).first.strip
      when /\sat ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      when /\sto ([^\.]+)/
        $1.split(/\sby\s(\D+)/).first.strip
      else
        'unknown'
    end
    where.sub!(/^the /, '')
    where.chomp!(', hosted')
    where = where.split(/Monday|Tuesday|Wednesday|Thursday|Friday/).first.strip.chomp(',')
    where = 'unknown' if where[/^note$/i]
  else
    where = 'unknown'
  end
  where
end

2010.upto(Time.now.year) do |year|

  url = "http://www.hm-treasury.gov.uk/speech_chex_#{year}_index.htm"
  base_url = URI.parse(url)
  puts "scraping year index: #{year}"

  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)

  not_available = doc.at('title').inner_text[/Error/] || doc.at('title').inner_text[/301 Moved Permanently/]

  if not_available
    puts "year #{year} not available"
  else
    permalinks = doc.search('a').inject([]) do |list, a|
      is_speech = a['href'] && a['href'][/speech_chx_\d+/]  
  
      if is_speech
        speech_url = base_url.merge(a['href']).to_s
        list << speech_url
      end
      list
    end
  
    permalinks.each do |permalink|
      puts "scraping: #{permalink}"

      begin
        speech_html = ScraperWiki.scrape(permalink)
      rescue Exception => e
        puts e.to_s
        speech_html = nil
      end

      if speech_html
        speech = Nokogiri::HTML(speech_html)
    
        title = speech.at('#primaryContentFull > h1').inner_text
        if title[/George Osborne/]
          puts title
          date = speech.at('meta[name="DC.date.issued"]')['content']
          puts date
      
          body = speech.at('#primaryContentFull').inner_html
  
          where = find_where title
  
          record = {'title' => title, 'permalink' => permalink, 'minister_name' => 'George Osborne', 'given_on' => date, 'body' => body, 'department' => 'HM Treasury', 'where' => where}
  
          ScraperWiki.save(['permalink'], record)
        end
      end
    end
  end
  nil
end