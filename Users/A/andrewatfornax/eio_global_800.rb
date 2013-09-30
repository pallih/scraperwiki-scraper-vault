# Environmental Investment Organisation Global 800 Carbon Ranking
require 'nokogiri'

EIO_GLOBAL_800_URL = "http://www.eio.org.uk/etindex.php?page=overview1&ranking=Global_800"


eio_global_800_html = ScraperWiki::scrape(EIO_GLOBAL_800_URL)
eio_global_800_doc = Nokogiri::HTML eio_global_800_html
eio_global_800_doc.search("table#eio_rankings tr.eio_company").each do |company_row|
  company_cells = company_row.search("td")
  if company_cells.count == 11
    company_data = {
      eio_800_rank:            company_cells[0].search("span").inner_html,
      company_name:            Nokogiri::HTML(company_cells[1].inner_html).text,
      country_code:            company_cells[2].inner_html,
      market_value:            company_cells[3].inner_html.to_f,
      scope_1_and_2_emissions: company_cells[4].inner_html.gsub(/,/, ""), 
        # Scope 1 & 2 emissions not converted to an integer with to_i above,
        # as some data rows contain the text "Incomplete" or "No Data" 
      scope_1_and_2_intensity: company_cells[5].inner_html.to_f
    }
    ScraperWiki::save_sqlite(['company_name', 'country_code'], company_data) 
  end
end
# Environmental Investment Organisation Global 800 Carbon Ranking
require 'nokogiri'

EIO_GLOBAL_800_URL = "http://www.eio.org.uk/etindex.php?page=overview1&ranking=Global_800"


eio_global_800_html = ScraperWiki::scrape(EIO_GLOBAL_800_URL)
eio_global_800_doc = Nokogiri::HTML eio_global_800_html
eio_global_800_doc.search("table#eio_rankings tr.eio_company").each do |company_row|
  company_cells = company_row.search("td")
  if company_cells.count == 11
    company_data = {
      eio_800_rank:            company_cells[0].search("span").inner_html,
      company_name:            Nokogiri::HTML(company_cells[1].inner_html).text,
      country_code:            company_cells[2].inner_html,
      market_value:            company_cells[3].inner_html.to_f,
      scope_1_and_2_emissions: company_cells[4].inner_html.gsub(/,/, ""), 
        # Scope 1 & 2 emissions not converted to an integer with to_i above,
        # as some data rows contain the text "Incomplete" or "No Data" 
      scope_1_and_2_intensity: company_cells[5].inner_html.to_f
    }
    ScraperWiki::save_sqlite(['company_name', 'country_code'], company_data) 
  end
end
