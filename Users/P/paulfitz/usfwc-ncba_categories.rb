require 'json'
require 'nokogiri'           

html = ScraperWiki::scrape("http://www.cooperateusa.coop/")           
doc = Nokogiri::HTML(html)
doc.search("select[@name='industry'] option").each do |opt|
  val = opt["value"]
  next if val == ""
  txt = opt.search("text()")[0]
  url = "http://www.cooperateusa.coop/get_sub_categories.php?id=#{val}&sub_catid=undefined"
  subcat = ScraperWiki::scrape(url)
  subcat = "<select>#{subcat}</select>"
  doc2 = Nokogiri::HTML(subcat)
  doc2.search("option").each do |opt2|
    val2 = opt2["value"]
    next if val2 == ""
    txt2 = opt2.search("text()")[0]
    p "#{val} #{txt} #{val2} #{txt2}"
    ScraperWiki::save_sqlite([:id,:sub_id], { :id => val.to_i, :sub_id => val2.to_i, :category => txt, :subcategory => txt2 }) 
  end
end

