# based on https://scraperwiki.com/docs/ruby/ruby_intro_tutorial/ and 
# Mike Subelsky's work at https://github.com/subelsky/baltimore_property/blob/master/lib/real_property_scraper.rb

require 'nokogiri' 
require 'sanitize'

page = "http://newrin.lsc.gov/scripts/LSC/grantpro/pgp1.asp"
html = ScraperWiki::scrape(page)     
        
doc = Nokogiri::HTML html
doc.search("tr").each do |v|
  cells = v.search 'td'
p cells
  if Sanitize.clean(cells[0].inner_html.strip).match("#")
    next
  end

  if cells.count == 18
    data = {
      state: Sanitize.clean(cells[1].inner_html.strip).split("(")[0].strip,
      abbr: Sanitize.clean(cells[1].inner_html.strip).split("(")[1].delete(")").strip,
      CSR07: Sanitize.clean(cells[2].inner_html.strip.delete(",")).to_i,
      CSR07_Per: Sanitize.clean(cells[3].inner_html.strip.delete("%")).to_f,
      CSR08: Sanitize.clean(cells[4].inner_html.strip.delete(",")).to_i,
      CSR08_Per: Sanitize.clean(cells[5].inner_html.strip.delete("%")).to_f,
      CSR09: Sanitize.clean(cells[6].inner_html.strip.delete(",")).to_i,
      CSR09_Per: Sanitize.clean(cells[7].inner_html.strip.delete("%")).to_f,
      CSR10: Sanitize.clean(cells[8].inner_html.strip.delete(",")).to_i,
      CSR10_Per: Sanitize.clean(cells[9].inner_html.strip.delete("%")).to_f,
      CSR11: Sanitize.clean(cells[10].inner_html.strip.delete(",")).to_i,
      CSR11_Per: Sanitize.clean(cells[11].inner_html.strip.delete("%")).to_f,
      Funding07: Sanitize.clean(cells[12].inner_html.strip.delete(",")).to_i,
      Funding08: Sanitize.clean(cells[13].inner_html.strip.delete(",")).to_i,
      Funding09: Sanitize.clean(cells[14].inner_html.strip.delete(",")).to_i,
      Funding10: Sanitize.clean(cells[15].inner_html.strip.delete(",")).to_i,
      Funding11: Sanitize.clean(cells[16].inner_html.strip.delete(",")).to_i,
      Funding12: Sanitize.clean(cells[17].inner_html.strip.delete(",")).to_i
    }
    puts data.to_json
    ScraperWiki::save_sqlite(['state'], data)  
  end
end

   