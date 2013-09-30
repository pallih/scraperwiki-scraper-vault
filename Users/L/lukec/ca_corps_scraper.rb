require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
@br = Mechanize.new do |br|
  br.user_agent_alias = 'Mac Safari'
  br.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

def scrape_table(page_body)
  doc = Nokogiri::HTML(page_body)
  summary = doc.at_css('div.summary')
  if summary.inner_text =~ /(\d+) results were found/
    puts $1 + " results found."
    return if $1 == 0
  end

  doc.css('#searchResultsList li').collect do |row|
    desc = row.inner_text.squeeze(" ").strip
    if desc =~ /^(.+?)\s+Status:\s+(.+?)\s+Corporation Number:\s+(\S+)\s+Business Number:\s+(?:(\w+)|Not Available)\s*$/
      name, status, corpNum, busNum = $1, $2, $3, $4
      puts "Found #{name} #{status} #{corpNum} #{busNum}"
      record = {}
      record['CompanyNumber'] = corpNum
      record['CompanyName'] = name
      record['Status'] = status
      record['BusinessNumber'] = busNum
      record['date_scraped'] = Time.now
      num = corpNum.sub(/-/, '')
      record['RegistryUrl'] = 'https://www.ic.gc.ca/app/scr/cc/CorporationsCanada/fdrlCrpDtls.html?corpId=' + num
      begin
        ScraperWiki.save(["CompanyNumber"], record)
      rescue Exception => e
        puts "Exception (#{e.inspect}) raised saving company record #{record.inspect}"
      end 
    end
  end
end

def search_for(search_term, retries)
  begin
    @br.post('https://www.ic.gc.ca/app/scr/cc/CorporationsCanada/fdrlCrpSrch.html?locale=en_CA',
      {
        'V_SEARCH.docsStart' => 1,
        'V_SEARCH.baseURL' => "fdrlCrpSrch.html",
        'V_SEARCH.command' => 'search',
        'corpNumber' => search_term,
      }
    );
    scrape_table(@br.page.body)
  rescue Exception, Timeout::Error => e
    retries -= 1
    puts "Exception raised during POST: #{e.inspect} - retries #{retries}"
    if retries > 0 
      sleep 1
      search_for(search_term, retries)
    end
  end
end

MinCorpNum = 10
MaxCorpNum = 99999
MaxRetries = 5

# ScraperWiki.save_var 'last_finished', 79999

start = ScraperWiki.get_var 'last_finished', MinCorpNum - 1
start += 1
start = MinCorpNum if start > MaxCorpNum

for num in (start .. MaxCorpNum)
  search_term = sprintf("%05i", num)
  puts "Searching for '#{search_term}'"
  search_for(search_term, MaxRetries)
  ScraperWiki.save_var 'last_finished', num
endrequire 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
@br = Mechanize.new do |br|
  br.user_agent_alias = 'Mac Safari'
  br.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

def scrape_table(page_body)
  doc = Nokogiri::HTML(page_body)
  summary = doc.at_css('div.summary')
  if summary.inner_text =~ /(\d+) results were found/
    puts $1 + " results found."
    return if $1 == 0
  end

  doc.css('#searchResultsList li').collect do |row|
    desc = row.inner_text.squeeze(" ").strip
    if desc =~ /^(.+?)\s+Status:\s+(.+?)\s+Corporation Number:\s+(\S+)\s+Business Number:\s+(?:(\w+)|Not Available)\s*$/
      name, status, corpNum, busNum = $1, $2, $3, $4
      puts "Found #{name} #{status} #{corpNum} #{busNum}"
      record = {}
      record['CompanyNumber'] = corpNum
      record['CompanyName'] = name
      record['Status'] = status
      record['BusinessNumber'] = busNum
      record['date_scraped'] = Time.now
      num = corpNum.sub(/-/, '')
      record['RegistryUrl'] = 'https://www.ic.gc.ca/app/scr/cc/CorporationsCanada/fdrlCrpDtls.html?corpId=' + num
      begin
        ScraperWiki.save(["CompanyNumber"], record)
      rescue Exception => e
        puts "Exception (#{e.inspect}) raised saving company record #{record.inspect}"
      end 
    end
  end
end

def search_for(search_term, retries)
  begin
    @br.post('https://www.ic.gc.ca/app/scr/cc/CorporationsCanada/fdrlCrpSrch.html?locale=en_CA',
      {
        'V_SEARCH.docsStart' => 1,
        'V_SEARCH.baseURL' => "fdrlCrpSrch.html",
        'V_SEARCH.command' => 'search',
        'corpNumber' => search_term,
      }
    );
    scrape_table(@br.page.body)
  rescue Exception, Timeout::Error => e
    retries -= 1
    puts "Exception raised during POST: #{e.inspect} - retries #{retries}"
    if retries > 0 
      sleep 1
      search_for(search_term, retries)
    end
  end
end

MinCorpNum = 10
MaxCorpNum = 99999
MaxRetries = 5

# ScraperWiki.save_var 'last_finished', 79999

start = ScraperWiki.get_var 'last_finished', MinCorpNum - 1
start += 1
start = MinCorpNum if start > MaxCorpNum

for num in (start .. MaxCorpNum)
  search_term = sprintf("%05i", num)
  puts "Searching for '#{search_term}'"
  search_for(search_term, MaxRetries)
  ScraperWiki.save_var 'last_finished', num
end