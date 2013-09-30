require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'iconv'


def save_company_from_element(p)
  return unless p.at('a')[:href] =~ /http:/ # pagination links are relative
  link = p.at('a')
  company_type = p.at('i').next.to_s.scan(/,([\w\s]+),/).flatten.first.strip rescue nil
  record = {'CompanyNumber' => link.inner_text,
            'RegistryUrl'   => link[:href],
            'CompanyType'   => company_type,
            'DateScraped'   => Time.now
           }
  bold_name = p.at('b')
  raw_company_name = bold_name ? bold_name.inner_text : p.children.first.to_s # sometimes name is in bold, sometimes not...
  record['CompanyName'] = raw_company_name.sub(/\bin liquidation/i,'').strip.force_encoding("UTF-8")
  p p if record['CompanyName'].nil? || record['CompanyName'] == ''
  ScraperWiki.save(["CompanyNumber"], record)
end
 
# scrape_page function: gets passed an individual page to scrape
def scrape_page(page, url)
  # clean up page so valid enough for Nokogiri to parse
  page.gsub!('<p />','</p><p>')
  page.sub!('<hr />','<p>')
  page.gsub!('<hr ','</p><hr ')
  doc = Nokogiri.HTML(page)
  doc.search('a[@href*="getHRGHTML"]').each do |a|
    save_company_from_element(a.parent)
  end
rescue Exception => e
  puts "Exception (#{e.inspect}) raised while getting or parsing data (source url=#{url}). Data: #{page.to_s}\n\nBacktrace:\n#{e.backtrace}"
end

def get_results_and_extract_data_for(prefix, search_offset)
  while search_offset do
    url = "http://www.oera.li/WebServices/ZefixFL/ZefixFL.asmx/SearchFirm?name=#{prefix}%20&suche_nach=-&rf=&sitz=&id=&language=4&phonetisch=no&posMin=#{search_offset}"
    response = 
    begin
      html = open(url).read.encode!('utf-8','iso-8859-1')
    rescue Exception, Timeout::Error => e
      puts "Problem getting/parsing data from #{url}: #{e.inspect}"
      nil
    end
    next unless response
    if response.match(/webservices\/HRG/) # check has links to companies
      puts "****Scraping page #{(search_offset+10)/10}"
      scrape_page(response, url)
      ScraperWiki.save_var('search_offset', search_offset)
      search_offset += 10
    else
      search_offset = false
    end
  end
end

prefix = ScraperWiki.get_var('prefix', 'aaa')
saved_search_offset = ScraperWiki.get_var('search_offset', 0)

while prefix != 'aaaa' do
  get_results_and_extract_data_for(prefix, saved_search_offset)
  puts "***** Finished processing #{prefix}"
  prefix = prefix.succ # little-known ruby magic
  saved_search_offset = 0 # reset search_offset
  ScraperWiki.save_var('search_offset', 0) #...and save it
  ScraperWiki.save_var('prefix', prefix) # save prefix in case scraper gets killed
end

ScraperWiki.save_var('prefix','aaa') # start at the beginning next time
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'iconv'


def save_company_from_element(p)
  return unless p.at('a')[:href] =~ /http:/ # pagination links are relative
  link = p.at('a')
  company_type = p.at('i').next.to_s.scan(/,([\w\s]+),/).flatten.first.strip rescue nil
  record = {'CompanyNumber' => link.inner_text,
            'RegistryUrl'   => link[:href],
            'CompanyType'   => company_type,
            'DateScraped'   => Time.now
           }
  bold_name = p.at('b')
  raw_company_name = bold_name ? bold_name.inner_text : p.children.first.to_s # sometimes name is in bold, sometimes not...
  record['CompanyName'] = raw_company_name.sub(/\bin liquidation/i,'').strip.force_encoding("UTF-8")
  p p if record['CompanyName'].nil? || record['CompanyName'] == ''
  ScraperWiki.save(["CompanyNumber"], record)
end
 
# scrape_page function: gets passed an individual page to scrape
def scrape_page(page, url)
  # clean up page so valid enough for Nokogiri to parse
  page.gsub!('<p />','</p><p>')
  page.sub!('<hr />','<p>')
  page.gsub!('<hr ','</p><hr ')
  doc = Nokogiri.HTML(page)
  doc.search('a[@href*="getHRGHTML"]').each do |a|
    save_company_from_element(a.parent)
  end
rescue Exception => e
  puts "Exception (#{e.inspect}) raised while getting or parsing data (source url=#{url}). Data: #{page.to_s}\n\nBacktrace:\n#{e.backtrace}"
end

def get_results_and_extract_data_for(prefix, search_offset)
  while search_offset do
    url = "http://www.oera.li/WebServices/ZefixFL/ZefixFL.asmx/SearchFirm?name=#{prefix}%20&suche_nach=-&rf=&sitz=&id=&language=4&phonetisch=no&posMin=#{search_offset}"
    response = 
    begin
      html = open(url).read.encode!('utf-8','iso-8859-1')
    rescue Exception, Timeout::Error => e
      puts "Problem getting/parsing data from #{url}: #{e.inspect}"
      nil
    end
    next unless response
    if response.match(/webservices\/HRG/) # check has links to companies
      puts "****Scraping page #{(search_offset+10)/10}"
      scrape_page(response, url)
      ScraperWiki.save_var('search_offset', search_offset)
      search_offset += 10
    else
      search_offset = false
    end
  end
end

prefix = ScraperWiki.get_var('prefix', 'aaa')
saved_search_offset = ScraperWiki.get_var('search_offset', 0)

while prefix != 'aaaa' do
  get_results_and_extract_data_for(prefix, saved_search_offset)
  puts "***** Finished processing #{prefix}"
  prefix = prefix.succ # little-known ruby magic
  saved_search_offset = 0 # reset search_offset
  ScraperWiki.save_var('search_offset', 0) #...and save it
  ScraperWiki.save_var('prefix', prefix) # save prefix in case scraper gets killed
end

ScraperWiki.save_var('prefix','aaa') # start at the beginning next time
