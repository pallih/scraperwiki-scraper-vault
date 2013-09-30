require 'nokogiri'
require 'uri'

page = 1
finished = false

ministers = ['Andrew Mitchell','Alan Duncan','Stephen O’Brien',"Stephen O'Brien"]

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

while !finished do
  url = "http://www.dfid.gov.uk/Media-Room/Speeches-and-articles/?q=&t=&c=&p=&page=#{page}"
  base_url = URI.parse(url)
  puts "scraping index page: #{page}"

  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)

  permalinks = doc.search('a').inject([]) do |list, a|
    is_speech_or_article = a['href'] && a['href'][/Media-Room\/Speeches-and-articles\/\d\d\d\d/]  

    if is_speech_or_article
      speech_or_article_url = base_url.merge(a['href']).to_s
      list << speech_or_article_url
    end
    list
  end

  permalinks.each do |permalink|
    puts "scraping: #{permalink}"

    begin
      html = ScraperWiki.scrape(permalink)
    rescue Exception => e
      puts e.to_s
      html = nil
    end

    if html
      doc = Nokogiri::HTML(html, nil, 'utf-8') # hard code correct encoding
  
      title = doc.at('.h1_bot h1').inner_text
      date = ( doc.at('.notabstext .date') ? doc.at('.notabstext .date').inner_text : doc.at('.text .date').inner_text )
      content = ( doc.at('.notabstext .date') ? doc.at('.notabstext .date').parent : doc.at('.text .date').parent )
      body = content.inner_html
  
      description = doc.at('.h1_bot p') ? doc.at('.h1_bot p').inner_text : nil
  
      minister_name = 'unknown'
      ministers.each do |minister|
        minister_name = minister if title[/#{minister}/] || (description && description[/#{minister}/])
      end
  
      if minister_name == 'unknown'
        ministers.each do |minister|      
          minister_name = minister if body[/#{minister}/]
        end
      end
    
      where = find_where(description || title)
      h3 = content.at('h3')
      where = find_where h3 if where == 'unknown'
      where = find_where doc.at('.notabstext .date').parent.at('p') if where == 'unknown' && !h3
      where = find_where doc.at('.notabstext .date').parent.search('p')[1] if where == 'unknown' && !h3
  
      puts "where: " + where
  
      record = {'title' => title, 'permalink' => permalink, 'minister_name' => minister_name, 'given_on' => date, 'body' => body, 'department' => 'Department for International Development', 'where' => where}
  
      puts "#{minister_name} - #{title}"
      ScraperWiki.save(['permalink'], record)
    end
  
    finished = true
    finished = false if doc.at('img[name="pagenavNext"]')
  
    page = page + 1
  end
end
require 'nokogiri'
require 'uri'

page = 1
finished = false

ministers = ['Andrew Mitchell','Alan Duncan','Stephen O’Brien',"Stephen O'Brien"]

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

while !finished do
  url = "http://www.dfid.gov.uk/Media-Room/Speeches-and-articles/?q=&t=&c=&p=&page=#{page}"
  base_url = URI.parse(url)
  puts "scraping index page: #{page}"

  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)

  permalinks = doc.search('a').inject([]) do |list, a|
    is_speech_or_article = a['href'] && a['href'][/Media-Room\/Speeches-and-articles\/\d\d\d\d/]  

    if is_speech_or_article
      speech_or_article_url = base_url.merge(a['href']).to_s
      list << speech_or_article_url
    end
    list
  end

  permalinks.each do |permalink|
    puts "scraping: #{permalink}"

    begin
      html = ScraperWiki.scrape(permalink)
    rescue Exception => e
      puts e.to_s
      html = nil
    end

    if html
      doc = Nokogiri::HTML(html, nil, 'utf-8') # hard code correct encoding
  
      title = doc.at('.h1_bot h1').inner_text
      date = ( doc.at('.notabstext .date') ? doc.at('.notabstext .date').inner_text : doc.at('.text .date').inner_text )
      content = ( doc.at('.notabstext .date') ? doc.at('.notabstext .date').parent : doc.at('.text .date').parent )
      body = content.inner_html
  
      description = doc.at('.h1_bot p') ? doc.at('.h1_bot p').inner_text : nil
  
      minister_name = 'unknown'
      ministers.each do |minister|
        minister_name = minister if title[/#{minister}/] || (description && description[/#{minister}/])
      end
  
      if minister_name == 'unknown'
        ministers.each do |minister|      
          minister_name = minister if body[/#{minister}/]
        end
      end
    
      where = find_where(description || title)
      h3 = content.at('h3')
      where = find_where h3 if where == 'unknown'
      where = find_where doc.at('.notabstext .date').parent.at('p') if where == 'unknown' && !h3
      where = find_where doc.at('.notabstext .date').parent.search('p')[1] if where == 'unknown' && !h3
  
      puts "where: " + where
  
      record = {'title' => title, 'permalink' => permalink, 'minister_name' => minister_name, 'given_on' => date, 'body' => body, 'department' => 'Department for International Development', 'where' => where}
  
      puts "#{minister_name} - #{title}"
      ScraperWiki.save(['permalink'], record)
    end
  
    finished = true
    finished = false if doc.at('img[name="pagenavNext"]')
  
    page = page + 1
  end
end
