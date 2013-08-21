require 'nokogiri' 

def scrape_url(url)
  html = ScraperWiki.scrape(url)
puts "html: #{html}"
  changes = {}
  doc = Nokogiri::HTML(html)
puts "doc: #{doc}"
  doc.css('table.rctable tr').each do |row|
    col1 = row.css('td.rc1')
    col2 = row.css('td.rc2')
    col3 = row.css('td.rc3')

    if col1.css('span.day').empty? 
      page_a = col1.css('a').first
      dump_change(page_a.attribute('href'), page_a.inner_text)
    else
      # FIX: Record the day
    end
  end

end

def dump_change(page_url, page_name)
  # Save data to database
  dump_data = {
    'page_url' => page_url,
    'page_name' => page_name,
  }
  ScraperWiki.save_sqlite(unique_keys=['page_url'], data=dump_data)
end

url = 'http://wiki.tcl.tk/_/recent'
scrape_url(url)


