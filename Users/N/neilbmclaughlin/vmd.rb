#https://groups.google.com/forum/#!searchin/scraperwiki/javascript$20mechanize/scraperwiki/Fs-tKVMgdJQ/sodPpm7jFCwJ

require 'rubygems'
require 'mechanize'
require 'date'

module VMDScraper
 
  class Scraper < Mechanize   
    private
    def date_scraped
      @date_scraped ||= Date.today.strftime("%Y-%m-%d")
    end

    def clean_whitespace(str) 
      str.gsub(/\s+/, ' ').strip
    end
  end

  class ProductInformationDatabaseScraper < Scraper
    def starting_page
      @starting_page ||= URI.parse("http://www.vmd.defra.gov.uk/ProductInformationDatabase/")
    end

    def get_records
      puts "Getting records from #{starting_page}..."
      page = get(starting_page)


      form = page.form("aspnetForm")
      form.add_field!('__EVENTARGUMENT', '')
      form.add_field!('__EVENTTARGET', 'ctl00$ctl00$VMDMaster$lbtnAll')
      page = submit(form)

      #form = page.form("aspnetForm")
      #form.add_field!('__EVENTARGUMENT', '')
      #form.add_field!('__EVENTTARGET', 'ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPage2')
      #page = submit(form)

      p page.title()

      #p page.parser.xpath('//table')

      records = 
      page.parser.xpath('//table[@id="x:1453027887.5:mkr:dataTbl.hdn"]/tbody/tr').collect{ |product|

        product_name = product.xpath('td[@class="ig2d2816fe"]').text #.collect #.collect(&:inner_html)
        supplier_name = product.xpath('td[@class="ig2d2816ff"]').text #.collect #.collect(&:inner_html)

        if product_name != ""
          {
            "name"=> clean_whitespace(product_name),
            "supplier"=> clean_whitespace(supplier_name )
          }
        end
      }

      #next_link = page.links.detect { |l|
      #        l.attributes.keys.include?('title') && l.attributes['title'].match(/Next page set./)
      #}

      #p next_link


      #p records
      return records

      #scrape(page)

    end


    private
    def scrape(page)
        records = page.parser.xpath('//table[@id="x:1453027887.10:mkr:headerContent.hdn"//tr').collect { |record|
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
        l.attributes.keys.include?('title') && l.attributes['title'].match(/Next page/)
      }
      #p next_link
      p records.collect { |r| r['council_reference'] }
      #records
      next_link ? records + scrape_and_follow_next_link(click(next_link)) : records
    end
  end
end

def scraper
  VMDScraper::ProductInformationDatabaseScraper .new
end

if DEBUG = __FILE__ == $0
  # When running from the command line
  require 'terminal-table/import'
  cols = %w(council_reference info_url date_received description address comment_url status)
  rows = scraper.get_records.collect { |record| cols.map { |col| record[col] } }
  puts table cols, *rows
else
  # When running in ScraperWiki
  #ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS `vmdData` (`h1` text, `h2` text)")

  scraper.get_records.each { |record|
    p record
    #ScraperWiki.save_sqlite(['h1'], record)
  }
end

