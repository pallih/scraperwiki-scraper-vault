# sogedial
require 'nokogiri' 
  
sogedial_base = ["http://www.sogedial.fr/pics_produit/permanant/bio/","http://www.sogedial.fr/pics_produit/permanant/arc-callens/","http://www.sogedial.fr/pics_produit/permanant/discount/","http://www.sogedial.fr/pics_produit/permanant/halal/","http://www.sogedial.fr/pics_produit/permanant/jouets/","http://www.sogedial.fr/pics_produit/permanant/mcbride/"]

sogedial_base.each do |url|
 html = ScraperWiki::scrape(url)               
 doc = Nokogiri::HTML html
 puts doc
 ref= doc.xpath('/html/body/pre/a')
 ref.each do |t|
   img = t['href']
   total_url = url + img
   ean = img[0..-5]
   if(ean.size == 13)
     ScraperWiki::save_sqlite(unique_keys=["ean"], data={"ean"=>ean, "url"=>total_url})
   end
 end
end# sogedial
require 'nokogiri' 
  
sogedial_base = ["http://www.sogedial.fr/pics_produit/permanant/bio/","http://www.sogedial.fr/pics_produit/permanant/arc-callens/","http://www.sogedial.fr/pics_produit/permanant/discount/","http://www.sogedial.fr/pics_produit/permanant/halal/","http://www.sogedial.fr/pics_produit/permanant/jouets/","http://www.sogedial.fr/pics_produit/permanant/mcbride/"]

sogedial_base.each do |url|
 html = ScraperWiki::scrape(url)               
 doc = Nokogiri::HTML html
 puts doc
 ref= doc.xpath('/html/body/pre/a')
 ref.each do |t|
   img = t['href']
   total_url = url + img
   ean = img[0..-5]
   if(ean.size == 13)
     ScraperWiki::save_sqlite(unique_keys=["ean"], data={"ean"=>ean, "url"=>total_url})
   end
 end
end