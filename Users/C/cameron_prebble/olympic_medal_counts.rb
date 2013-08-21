require 'rubygems'
require 'hpricot'

html = ScraperWiki::scrape("http://m.london2012.com/medals/medal-count/") 
doc = Hpricot(html)
doc.search('//*[@id="overall_medals"]/table/tbody/tr').each do |row|
  country = {
    :name   => row.search("/td[2]/div/text()").first.to_plain_text,
    :gold   => row.search(".or-gold").first.inner_html.to_i,
    :silver => row.search(".or-silver").first.inner_html.to_i,
    :bronze => row.search(".or-bronze").first.inner_html.to_i,
    :total  => row.search(".or-total").first.inner_html.to_i
  }
  ScraperWiki::save_sqlite(['name'], country)
end
