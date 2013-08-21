require 'nokogiri'

for year in 2000..2010
  html = ScraperWiki.scrape("http://www.socialsecurity.gov/cgi-bin/popularnames.cgi", {"top"=>20, "year"=>2010})

  doc = Nokogiri::HTML(html)
  for v in doc.search("table[@summary='Popularity for top 20'] tr[@align='right']")
    cells = v.search('td')
    data = {
      'year' => year,
      'rank' => cells[0].inner_html,
      'male_name' => cells[1].inner_html,
      'female_name' => cells[2].inner_html
    }
    ScraperWiki.save_sqlite(unique_keys=['year','rank'], data=data) 
  end
end

