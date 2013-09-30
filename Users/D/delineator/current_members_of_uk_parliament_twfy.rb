require 'csv'
require 'nokogiri'
require 'mechanize'


uri = 'https://gist.github.com/raw/887730/3263d95655e56db20d07d424380c450ef209ee10/gistfile1.txt'
agent = Mechanize.new
page = agent.get(uri)
eval(page.body)

uri = 'http://www.theyworkforyou.com/mps/?f=csv'
csv = ScraperWiki.scrape(uri)

uris = []

CSV.parse(csv, { :headers => true }) do |row|
  row.each do |key, value|
    if key == 'URI'
      uris << value
    end
  end
end

uris.reverse.each do |uri|
  begin
    agent = Mechanize.new
    page = agent.get(uri)
    html = page.body
    doc = Nokogiri::HTML(html)
    name = doc.at('h2').inner_text
  
    wikipedia_uri = nil
    website_uri = nil
  
    doc.search('a').each do |a|
      if a.inner_text[/Wikipedia/]
        wikipedia_uri = a['href']
        
        if wikipedia_uri
          page_name = wikipedia_uri.split('/').last
          page = Wikipedia.find(page_name)
          if page && (external_uri = page.external_website_uri)
            match = external_uri.detect {|x| ((x.size > 1) && x[1] && x[1][/official/i]) || ((x.size > 2) && x[2] && x[2][/official/i]) }
            unless match
              match = external_uri.detect {|x| ((x.size > 1) && x[1] && x[1][/website/i]) || ((x.size > 2) && x[2] && x[2][/website/i]) }
            end
            website_uri = match.first if match
          end
        end
      end
    end
    
    twitter_uri = nil
    if website_uri
      page = Mechanize.new.get(website_uri)
      links = page.links_with(:href => /twitter\.com\/.+/ )
      links.each do |link|
        if !twitter_uri && !link.href[/http:\/\/twitter.com\/(LibDems|UKLabour|statuses|share)/]
          twitter_uri = link.href.sub('redirect.aspx?ref=','').split('/statuses').first
          twitter_uri = nil if twitter_uri == 'http://twitter.com/'
        end
      end
    end

    record = {'name' => name, 'twfy_uri' => uri, 'wikipedia_uri' => wikipedia_uri, 'website_uri' => website_uri, 'twitter_uri' => twitter_uri}
    puts 'saving ' + record.inspect
    ScraperWiki.save(['twfy_uri'], record)

  rescue Exception => e
    puts e.to_s
    puts e.backtrace.join("\n")
  end
endrequire 'csv'
require 'nokogiri'
require 'mechanize'


uri = 'https://gist.github.com/raw/887730/3263d95655e56db20d07d424380c450ef209ee10/gistfile1.txt'
agent = Mechanize.new
page = agent.get(uri)
eval(page.body)

uri = 'http://www.theyworkforyou.com/mps/?f=csv'
csv = ScraperWiki.scrape(uri)

uris = []

CSV.parse(csv, { :headers => true }) do |row|
  row.each do |key, value|
    if key == 'URI'
      uris << value
    end
  end
end

uris.reverse.each do |uri|
  begin
    agent = Mechanize.new
    page = agent.get(uri)
    html = page.body
    doc = Nokogiri::HTML(html)
    name = doc.at('h2').inner_text
  
    wikipedia_uri = nil
    website_uri = nil
  
    doc.search('a').each do |a|
      if a.inner_text[/Wikipedia/]
        wikipedia_uri = a['href']
        
        if wikipedia_uri
          page_name = wikipedia_uri.split('/').last
          page = Wikipedia.find(page_name)
          if page && (external_uri = page.external_website_uri)
            match = external_uri.detect {|x| ((x.size > 1) && x[1] && x[1][/official/i]) || ((x.size > 2) && x[2] && x[2][/official/i]) }
            unless match
              match = external_uri.detect {|x| ((x.size > 1) && x[1] && x[1][/website/i]) || ((x.size > 2) && x[2] && x[2][/website/i]) }
            end
            website_uri = match.first if match
          end
        end
      end
    end
    
    twitter_uri = nil
    if website_uri
      page = Mechanize.new.get(website_uri)
      links = page.links_with(:href => /twitter\.com\/.+/ )
      links.each do |link|
        if !twitter_uri && !link.href[/http:\/\/twitter.com\/(LibDems|UKLabour|statuses|share)/]
          twitter_uri = link.href.sub('redirect.aspx?ref=','').split('/statuses').first
          twitter_uri = nil if twitter_uri == 'http://twitter.com/'
        end
      end
    end

    record = {'name' => name, 'twfy_uri' => uri, 'wikipedia_uri' => wikipedia_uri, 'website_uri' => website_uri, 'twitter_uri' => twitter_uri}
    puts 'saving ' + record.inspect
    ScraperWiki.save(['twfy_uri'], record)

  rescue Exception => e
    puts e.to_s
    puts e.backtrace.join("\n")
  end
end