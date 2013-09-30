require 'nokogiri'
require 'mechanize'
require 'uri'

def scrape_consultation uri
  puts uri
  doc = nil
  begin
    html = ScraperWiki.scrape(uri)
    doc = Nokogiri::HTML(html)
  rescue Exeption => e
    puts e.to_s
    puts e.backttrace.join("\n")
  end

  return if doc.nil? 

  title = if doc.at('h2[@property="dc:title"]')
    doc.at('h2[@property="dc:title"]').inner_text.strip
  elsif doc.at('.publicationIntro')
    doc.at('.publicationIntro > h2').inner_text
  else
    ''
  end

  closing = if doc.at('td[@property="dc:valid"]')
    doc.at('td[@property="dc:valid"]')['content']
  else
    ''
  end

  published = if doc.at('td[@property="dc:issued"]')
    doc.at('td[@property="dc:issued"]')['content']
  elsif doc.at('#Page').at('th[text()="Published"]').parent.at('td')
    doc.at('#Page').at('th[text()="Published"]').parent.at('td').inner_text.strip
  else
    ''
  end

  description = []
  summary = doc.at('#Page').at('h3[text()="Summary"]').next

  while summary && summary.name != 'h3' && summary.inner_text != 'Order'
    description << ((summary.name == 'text') ? summary.inner_text : summary.inner_html)
    summary = summary.next
  end

  description = description.map {|x| x.strip}
  description.delete_if {|x| x.nil? || x.size == 0}

  documents = if doc.at('.downloadList')
    doc.search('.downloadList > li').collect do |li|
      if li.at('a')
        parts = li.at('div') ? li.at('div').inner_text.split(',') : ['','']

        title = li.at('a').inner_text
        doc_uri = URI.parse(uri).merge(li.at('a')['href']).to_s
        format = parts[0].strip
        size = parts[1].strip

        record = {
          'consultation' => uri,
          'title' => title,
          'URI' => doc_uri,
          'format' => format,
          'size' => size
        }
        ScraperWiki.save_sqlite(['URI'], record, 'documents')
        [title, doc_uri, format, size]
      else
        ['','','','']
      end
    end
  else
    []
  end

  record = {
    'department' => 'Department for Communities and Local Government',
    'title' => title,
    'published_date' => published,
    'end_date' => closing,
    'URI' => uri,
    'description' => '<p>' + description.join("</p><p>") + '</p>',
    'start_date' => '',
    'sponsor' => '',
    'agency' => '',
    'documents' => [documents, documents.size].inspect
  }
  
  ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  nil
end

def find_consulations page, base_url, index=1, consultation_uris=[]
  doc = Nokogiri::HTML(page.body.gsub('&nbsp;',' '))
  
  doc.search('.searchResultList > li').each do |li|
    closing_year = nil
    li.search('ul > li').each do |sub_li|
      if sub_li.inner_text[/Closing date:.+\s(\d\d\d\d)/]
        closing_year = $1.to_i
        puts closing_year.to_s
      end
    end

    if closing_year && closing_year < 2010
      #ignore
    else
      a = li.at('h4').at('a')
      uri = base_url.merge(a['href']).to_s
      puts uri
      consultation_uris << uri
    end
  end

  if next_link = page.link_with(:text => /Next/)
    puts "clicking #{next_link.to_s}"
    begin
      next_page = next_link.click
      find_consulations(next_page, base_url, index+1, consultation_uris)
    rescue Exception => e
      puts e.to_s
      begin
        next_page = next_link.click
        find_consulations(next_page, base_url, index+1, consultation_uris)
      rescue Exception => e
        puts e.to_s
      end
    end
  end

  consultation_uris
end


url = "http://www.communities.gov.uk/planningandbuilding/publications/consultations/"
base_url = URI.parse(url)

agent = Mechanize.new
page = agent.get(url)

consultation_uris = find_consulations page, base_url

consultation_uris.each {|uri| scrape_consultation uri}require 'nokogiri'
require 'mechanize'
require 'uri'

def scrape_consultation uri
  puts uri
  doc = nil
  begin
    html = ScraperWiki.scrape(uri)
    doc = Nokogiri::HTML(html)
  rescue Exeption => e
    puts e.to_s
    puts e.backttrace.join("\n")
  end

  return if doc.nil? 

  title = if doc.at('h2[@property="dc:title"]')
    doc.at('h2[@property="dc:title"]').inner_text.strip
  elsif doc.at('.publicationIntro')
    doc.at('.publicationIntro > h2').inner_text
  else
    ''
  end

  closing = if doc.at('td[@property="dc:valid"]')
    doc.at('td[@property="dc:valid"]')['content']
  else
    ''
  end

  published = if doc.at('td[@property="dc:issued"]')
    doc.at('td[@property="dc:issued"]')['content']
  elsif doc.at('#Page').at('th[text()="Published"]').parent.at('td')
    doc.at('#Page').at('th[text()="Published"]').parent.at('td').inner_text.strip
  else
    ''
  end

  description = []
  summary = doc.at('#Page').at('h3[text()="Summary"]').next

  while summary && summary.name != 'h3' && summary.inner_text != 'Order'
    description << ((summary.name == 'text') ? summary.inner_text : summary.inner_html)
    summary = summary.next
  end

  description = description.map {|x| x.strip}
  description.delete_if {|x| x.nil? || x.size == 0}

  documents = if doc.at('.downloadList')
    doc.search('.downloadList > li').collect do |li|
      if li.at('a')
        parts = li.at('div') ? li.at('div').inner_text.split(',') : ['','']

        title = li.at('a').inner_text
        doc_uri = URI.parse(uri).merge(li.at('a')['href']).to_s
        format = parts[0].strip
        size = parts[1].strip

        record = {
          'consultation' => uri,
          'title' => title,
          'URI' => doc_uri,
          'format' => format,
          'size' => size
        }
        ScraperWiki.save_sqlite(['URI'], record, 'documents')
        [title, doc_uri, format, size]
      else
        ['','','','']
      end
    end
  else
    []
  end

  record = {
    'department' => 'Department for Communities and Local Government',
    'title' => title,
    'published_date' => published,
    'end_date' => closing,
    'URI' => uri,
    'description' => '<p>' + description.join("</p><p>") + '</p>',
    'start_date' => '',
    'sponsor' => '',
    'agency' => '',
    'documents' => [documents, documents.size].inspect
  }
  
  ScraperWiki.save_sqlite(['URI'], record, 'consultations')
  nil
end

def find_consulations page, base_url, index=1, consultation_uris=[]
  doc = Nokogiri::HTML(page.body.gsub('&nbsp;',' '))
  
  doc.search('.searchResultList > li').each do |li|
    closing_year = nil
    li.search('ul > li').each do |sub_li|
      if sub_li.inner_text[/Closing date:.+\s(\d\d\d\d)/]
        closing_year = $1.to_i
        puts closing_year.to_s
      end
    end

    if closing_year && closing_year < 2010
      #ignore
    else
      a = li.at('h4').at('a')
      uri = base_url.merge(a['href']).to_s
      puts uri
      consultation_uris << uri
    end
  end

  if next_link = page.link_with(:text => /Next/)
    puts "clicking #{next_link.to_s}"
    begin
      next_page = next_link.click
      find_consulations(next_page, base_url, index+1, consultation_uris)
    rescue Exception => e
      puts e.to_s
      begin
        next_page = next_link.click
        find_consulations(next_page, base_url, index+1, consultation_uris)
      rescue Exception => e
        puts e.to_s
      end
    end
  end

  consultation_uris
end


url = "http://www.communities.gov.uk/planningandbuilding/publications/consultations/"
base_url = URI.parse(url)

agent = Mechanize.new
page = agent.get(url)

consultation_uris = find_consulations page, base_url

consultation_uris.each {|uri| scrape_consultation uri}