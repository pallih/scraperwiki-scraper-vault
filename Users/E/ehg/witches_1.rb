require 'nokogiri'


BASE_URL = "http://webdb.ucs.ed.ac.uk/witches/"
PARAMS = {'Date' => '1000', 'Enddate' => '2000',
            'char' => 'any', 'char_op' => 'AND',
            'Ritual_object' => 'any', 'rit_op' => 'AND',
            'Calendar_custom' => 'any', 'cal_op' => 'AND',
            'Non_natural_being' => 'any', 'nnb_op' => 'AND',
            'Demonic_pact' => 'any', 'pact_op' => 'AND'}

def scrape_list
  html = ScraperWiki.scrape "#{BASE_URL}index.cfm?fuseaction=home.searchcase", PARAMS
  doc = Nokogiri::HTML html
  doc.search('ul li').each do |c|
    link = c.search('a').first
    scrape_case link.attr :href unless link.nil? 
  end
end

def scrape_case(href)
  html = ScraperWiki.scrape(BASE_URL + href)
  doc = Nokogiri::HTML html
  
  doc.search('table.case table').each do |table|
    table.search('tr').each do |cell|
      th = cell.search('th')
      td = cell.search('td')
      
      name = td.text.strip if th.text == "The accused"
      start_date = td.text.strip if th.text == "Start date"
      end_date = td.text.strip if th.text == "End date"
      chars_td = td if th.text == "Characterisation"
      chars_td.search('br').each { |br| br.replace "|" } unless chars_td.nil? 
      chars = chars_td.text.gsub(/\r\n?/, '').gsub('\t', '').strip if chars_td

      process_chars chars unless chars.nil? or chars.empty? or chars == "Not enough information"
    end
  end
end

def process_chars(chars)
  chars.gsub! 'Not enough information', ''
  chars.split("|").each do |char|
    char.strip!
    ScraperWiki.save_sqlite [], { 'Characterisation' => char } if char and !char.empty? 
  end
end

scrape_list
require 'nokogiri'


BASE_URL = "http://webdb.ucs.ed.ac.uk/witches/"
PARAMS = {'Date' => '1000', 'Enddate' => '2000',
            'char' => 'any', 'char_op' => 'AND',
            'Ritual_object' => 'any', 'rit_op' => 'AND',
            'Calendar_custom' => 'any', 'cal_op' => 'AND',
            'Non_natural_being' => 'any', 'nnb_op' => 'AND',
            'Demonic_pact' => 'any', 'pact_op' => 'AND'}

def scrape_list
  html = ScraperWiki.scrape "#{BASE_URL}index.cfm?fuseaction=home.searchcase", PARAMS
  doc = Nokogiri::HTML html
  doc.search('ul li').each do |c|
    link = c.search('a').first
    scrape_case link.attr :href unless link.nil? 
  end
end

def scrape_case(href)
  html = ScraperWiki.scrape(BASE_URL + href)
  doc = Nokogiri::HTML html
  
  doc.search('table.case table').each do |table|
    table.search('tr').each do |cell|
      th = cell.search('th')
      td = cell.search('td')
      
      name = td.text.strip if th.text == "The accused"
      start_date = td.text.strip if th.text == "Start date"
      end_date = td.text.strip if th.text == "End date"
      chars_td = td if th.text == "Characterisation"
      chars_td.search('br').each { |br| br.replace "|" } unless chars_td.nil? 
      chars = chars_td.text.gsub(/\r\n?/, '').gsub('\t', '').strip if chars_td

      process_chars chars unless chars.nil? or chars.empty? or chars == "Not enough information"
    end
  end
end

def process_chars(chars)
  chars.gsub! 'Not enough information', ''
  chars.split("|").each do |char|
    char.strip!
    ScraperWiki.save_sqlite [], { 'Characterisation' => char } if char and !char.empty? 
  end
end

scrape_list
