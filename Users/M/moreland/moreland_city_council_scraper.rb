require 'rubygems'
require 'mechanize'
require 'date'

module PlanningAlertsScraper  
  class Scraper < Mechanize   
    private
    def date_scraped
      @date_scraped ||= Date.today.strftime("%Y-%m-%d")
    end

    def clean_whitespace(str) 
      str.gsub(/\s+/, ' ').strip
    end
  end

  class MorelandScraper < Scraper
    def starting_page
      @starting_page ||= URI.parse("https://eservices.moreland.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx?ModuleCode=LAP")
    end

    def comment_url
      @comment_url ||= "https://eservices.moreland.vic.gov.au/ePathway/Production/Web/CustomerService/CustomerServiceType.aspx"
    end

    def get_records
      puts "Getting records from #{starting_page}..."
      page = get(starting_page)
      form = page.forms.first 
      form.radiobuttons_with(:name => 'mDataGrid:Column0:Property').first.check
      scrape_and_follow_next_link(form.click_button)
    end

    private
    def scrape_and_follow_next_link(page)
      records = page.parser.xpath('//tr[@class="ContentPanel"]').collect { |record|
        cells = record.xpath('td/*[@class="ContentText"]')#.collect #.collect(&:inner_html)
        # Cells in row
        # <a>Application_number</a>  Date_received  Application_proposal Address Status
        {
          "council_reference"=> clean_whitespace(cells[0].text),
          "info_url"         => starting_page.merge(cells[0].attributes['href'].to_s).to_s,
          "date_received"    => Date.strptime(cells[1].text.strip, '%d/%m/%Y'),
          "description"      => clean_whitespace(cells[2].text),
          "address"          => clean_whitespace(cells[3].text),
          "date_scraped"     => date_scraped,
          "comment_url"      => comment_url,
          "status"           => clean_whitespace(cells[4].text)
        }
      }
      next_link = page.links.detect { |l|
        l.attributes.has_key?('title') && l.attributes['title'].match(/Next page/)
      }
      #p next_link
      p records.collect { |r| r['council_reference'] }
      #records
      next_link ? records + scrape_and_follow_next_link(click(next_link)) : records
    end
  end
end

def scraper
  PlanningAlertsScraper::MorelandScraper.new
end

if DEBUG = __FILE__ == $0
  # When running from the command line
  require 'terminal-table/import'
  cols = %w(council_reference info_url date_received description address comment_url status)
  rows = scraper.get_records.collect { |record| cols.map { |col| record[col] } }
  puts table cols, *rows
else
  # When running in ScraperWiki
  #ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS `swdata` (`date_scraped` text, `description` text, `info_url` text, `date_received` text, `council_reference` text, `address` text, `comment_url` text, `status` text)")
  scraper.get_records.each { |record|
    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  }
end
require 'rubygems'
require 'mechanize'
require 'date'

module PlanningAlertsScraper  
  class Scraper < Mechanize   
    private
    def date_scraped
      @date_scraped ||= Date.today.strftime("%Y-%m-%d")
    end

    def clean_whitespace(str) 
      str.gsub(/\s+/, ' ').strip
    end
  end

  class MorelandScraper < Scraper
    def starting_page
      @starting_page ||= URI.parse("https://eservices.moreland.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx?ModuleCode=LAP")
    end

    def comment_url
      @comment_url ||= "https://eservices.moreland.vic.gov.au/ePathway/Production/Web/CustomerService/CustomerServiceType.aspx"
    end

    def get_records
      puts "Getting records from #{starting_page}..."
      page = get(starting_page)
      form = page.forms.first 
      form.radiobuttons_with(:name => 'mDataGrid:Column0:Property').first.check
      scrape_and_follow_next_link(form.click_button)
    end

    private
    def scrape_and_follow_next_link(page)
      records = page.parser.xpath('//tr[@class="ContentPanel"]').collect { |record|
        cells = record.xpath('td/*[@class="ContentText"]')#.collect #.collect(&:inner_html)
        # Cells in row
        # <a>Application_number</a>  Date_received  Application_proposal Address Status
        {
          "council_reference"=> clean_whitespace(cells[0].text),
          "info_url"         => starting_page.merge(cells[0].attributes['href'].to_s).to_s,
          "date_received"    => Date.strptime(cells[1].text.strip, '%d/%m/%Y'),
          "description"      => clean_whitespace(cells[2].text),
          "address"          => clean_whitespace(cells[3].text),
          "date_scraped"     => date_scraped,
          "comment_url"      => comment_url,
          "status"           => clean_whitespace(cells[4].text)
        }
      }
      next_link = page.links.detect { |l|
        l.attributes.has_key?('title') && l.attributes['title'].match(/Next page/)
      }
      #p next_link
      p records.collect { |r| r['council_reference'] }
      #records
      next_link ? records + scrape_and_follow_next_link(click(next_link)) : records
    end
  end
end

def scraper
  PlanningAlertsScraper::MorelandScraper.new
end

if DEBUG = __FILE__ == $0
  # When running from the command line
  require 'terminal-table/import'
  cols = %w(council_reference info_url date_received description address comment_url status)
  rows = scraper.get_records.collect { |record| cols.map { |col| record[col] } }
  puts table cols, *rows
else
  # When running in ScraperWiki
  #ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS `swdata` (`date_scraped` text, `description` text, `info_url` text, `date_received` text, `council_reference` text, `address` text, `comment_url` text, `status` text)")
  scraper.get_records.each { |record|
    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  }
end
