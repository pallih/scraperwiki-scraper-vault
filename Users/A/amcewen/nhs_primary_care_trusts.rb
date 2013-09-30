# Scraper to get the websites for all the Primary Care Trusts in the NHS
require 'nokogiri'
require 'open-uri'

DB_NAME = "nhs_trusts_primary_care"
index_url = "http://www.nhs.uk/ServiceDirectories/Pages/PrimaryCareTrustListing.aspx"

def find_trust_website(info_url)
  begin
    info_page = ScraperWiki.scrape(info_url)
    info_doc = Nokogiri::HTML(info_page, nil, 'utf-8')
    record = { 'name' => info_doc.css("h1.pct").inner_text }

    # Extract the website address
    info_doc.css(".panel-content p").each do |para|
      if para.inner_text.match(/visit our website/i)
        unless para.css("a").empty? 
          record['URI'] = para.css("a")[0]['href']
        else
          puts "Couldn't find link in "+para.to_s
          puts "URI is currently "+record['URI'].inspect
        end
      end
    end

    unless record['URI'].nil? 
      ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
    else
      puts "### Couldn't find URL for "+record["name"]+"in page at "+info_url
    end
  rescue Timeout::Error
    puts "### Getting #{info_url} timed out"
  end
end

index_page = ScraperWiki.scrape(index_url)
index_doc = Nokogiri::HTML(index_page, nil, 'utf-8')
parsed_index_uri = URI.parse(index_url)

# Find all the links to trusts
index_doc.css(".trust-list li a").each do |trust|
  if trust['class'] != "back-to-top"
    puts trust.inner_text
    find_trust_website(parsed_index_uri.merge(trust['href']).to_s)
  end
end

# Scraper to get the websites for all the Primary Care Trusts in the NHS
require 'nokogiri'
require 'open-uri'

DB_NAME = "nhs_trusts_primary_care"
index_url = "http://www.nhs.uk/ServiceDirectories/Pages/PrimaryCareTrustListing.aspx"

def find_trust_website(info_url)
  begin
    info_page = ScraperWiki.scrape(info_url)
    info_doc = Nokogiri::HTML(info_page, nil, 'utf-8')
    record = { 'name' => info_doc.css("h1.pct").inner_text }

    # Extract the website address
    info_doc.css(".panel-content p").each do |para|
      if para.inner_text.match(/visit our website/i)
        unless para.css("a").empty? 
          record['URI'] = para.css("a")[0]['href']
        else
          puts "Couldn't find link in "+para.to_s
          puts "URI is currently "+record['URI'].inspect
        end
      end
    end

    unless record['URI'].nil? 
      ScraperWiki.save_sqlite(['URI'], record, DB_NAME)
    else
      puts "### Couldn't find URL for "+record["name"]+"in page at "+info_url
    end
  rescue Timeout::Error
    puts "### Getting #{info_url} timed out"
  end
end

index_page = ScraperWiki.scrape(index_url)
index_doc = Nokogiri::HTML(index_page, nil, 'utf-8')
parsed_index_uri = URI.parse(index_url)

# Find all the links to trusts
index_doc.css(".trust-list li a").each do |trust|
  if trust['class'] != "back-to-top"
    puts trust.inner_text
    find_trust_website(parsed_index_uri.merge(trust['href']).to_s)
  end
end

