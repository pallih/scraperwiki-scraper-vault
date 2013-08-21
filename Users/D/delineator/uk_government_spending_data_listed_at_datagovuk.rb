# encoding: utf-8
require 'nokogiri'
require 'json'

SPEND_OVER_ENTITY = /^(Transparency )?((Spend|Expenditure|Spending) over) (£?(\d|,|k)+) (made by|in|at|for|by|from) (the )?(.+)$/i
ENTITY_SPEND_OVER = /^(.+) ((Spend|Expenditure|Spending) (data )?over) (£?(\d|,|k)+)( .+)?$/i
ENTITY_SPEND_DATA = /^(.+) (spend data)$/i
ENTITY_DATA_TRANSPARENCY_PORTAL = /^(.+)'s (data transparency portal)$/i
PAYMENTS_TO = /^Payments to suppliers (with a value )?over (£?(\d|,|k)+) (made by|in|at|for|by|from) (the )?(.+)$/i
PAYMENTS_OVER = /^Payments over (£?(\d|,|k)+) (made by|in|at|for|by|from) (the )?(.+)$/i

ENTITY_PAYMENTS = /^(.+) - Payments.* (£?(\d|,|k)+) .*$/i

DATE = /^(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d\d\d\d$/

finished = false
page = 80
debug = false

while !finished
  puts "page: #{page}"
  starting_url = "http://data.gov.uk/opensearch/apachesolr_search/spend%20over?filters=type:ckan_package&page=#{page}"
  page += 1

  items = []
  begin
    xml = ScraperWiki.scrape(starting_url)
    doc = Nokogiri::XML(xml)
    items = doc.search('item')
  rescue Exception => e
    puts e.to_s
    puts e.backtrace.join("\n")
  end

  if items.empty? # try again
    begin
      xml = ScraperWiki.scrape(starting_url)  
      doc = Nokogiri::XML(xml)
      items = doc.search('item')
    rescue Exception => e
      puts e.to_s
      puts e.backtrace.join("\n")
    end
    finished = true if items.empty? 
  end

  items.each do |item|
    title = item.at('title').inner_text.strip
    puts title if debug
    link = item.at('link').inner_text.strip
    spend_over = nil
    entity = nil
  
    case title
      when SPEND_OVER_ENTITY
        spend_over = $4
        entity = $8
      when ENTITY_SPEND_OVER
        entity = $1
        spend_over = $5
      when ENTITY_SPEND_DATA, ENTITY_DATA_TRANSPARENCY_PORTAL
        entity = $1
      when PAYMENTS_TO
        spend_over = $2
        entity = $6
      when PAYMENTS_OVER
        spend_over = $1
        entity = $5
      when ENTITY_PAYMENTS
        spend_over = $2
        entity = $1
      else
        puts title
    end
  
    agency = nil
    domain = nil
    department = nil

    if link
      url = link.sub('dataset', 'api/catalogue/rest/package')
      json = nil
      begin
        json = ScraperWiki.scrape(url)
      rescue Exception => e
        puts e.to_s
        puts e.backtrace.join("\n")
      end

      if json && !json[/DOCTYPE html/] && !json[/Error response/] && (data = JSON::load(json))
        if extras = data['extras']
          agency = extras['agency']
          department = extras['department']
        end
        url = data['url'].to_s.strip.gsub(',','').gsub('£','')
        begin
          url = "http:\/\/#{url}" unless url[ /^http:\/\// ]
          domain = URI.parse(url).host.sub('www.','')
        rescue
          puts "error parsing: #{url}"
        end if url && (url.size != 0)
  
        if !domain && (resources = data['resources'])
          resources = resources.first if resources.is_a?(Array)
          if resources
            url = resources['url'].to_s.strip.gsub(',','').gsub('£','')
            url = "http:\/\/#{url}" unless url[ /^http:\/\// ]
            begin
              domain = URI.parse(url).host.sub('www.','')
            rescue
              puts "error parsing: #{url}"
            end if url && (url.size != 0)
          end
        end
      end
    end

    entity = nil if entity && entity[DATE]

    record = {'spend_over' => spend_over,
        'entity_from_title' => entity,
        'title' => title,
        'agency' => agency,
        'datagovuk_url' => link,
        'domain' => domain,
        'department' => department}
    ScraperWiki.save(['datagovuk_url'], record)
  end
end