require 'nokogiri'

baseurl = "http://www.berlin.de/polizei/presse-fahndung/presse.html"
basehtml = ScraperWiki.scrape(baseurl)
basedoc = Nokogiri::HTML(basehtml)

crimedates = basedoc.xpath("//dt[@class='odd']")

crimedates.each do |crimedate|
  url = crimedate.xpath("following-sibling::*/a").first.attr("href")

  crimehtml = ScraperWiki.scrape("http://www.berlin.de#{url}")
  crimedoc = Nokogiri::HTML(crimehtml)
  
  datetimenode = crimedoc.xpath("//div[@class='datum']")
  date, time = datetimenode.text.gsub('Eingabe: ', '').split(' - ')

  headlinenode = crimedoc.xpath("//h2")
  headline = headlinenode.text
  district = headlinenode.xpath("following-sibling::*").first.text

  textnode = headlinenode.xpath("following-sibling::div[@class='bacontent']").first
  text = textnode.text

  result = {
    'url' => url,
    'date' => date,
    'time' => time,
    'headline' => headline,
    'text' => text
  }

  unique_keys = ['url']
  
  ScraperWiki.save_sqlite(unique_keys, result)
end
