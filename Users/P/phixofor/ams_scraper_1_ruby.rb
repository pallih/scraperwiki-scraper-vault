# This scraper is a replacement for https://scraperwiki.com/scrapers/rockdale_applications/
# The council da tracker doesn't output rss correctly anymore. So, instead scraping the xml output

require 'mechanize'
require 'json'

url = "http://api.arbetsformedlingen.se/platsannons/"

agent = Mechanize.new


i = 5709621
num = 10249470

while i < num  do
  begin  
    id = i.to_s()
    page = agent.get(url+id)

    sida = page.content
    sida.gsub!(/\A\xEF\xBB\xBF/, '')
    sida.force_encoding 'UTF-8'

    sida = JSON.parse(page.content)

    annonstext = sida["platsannons"]["annons"]["annonstext"]
 
    #puts annonstext

    ScraperWiki::save_sqlite(unique_keys=["a"], data={"a"=>i, "annons"=>annonstext}) 
  
    i +=1
  rescue Exception => e
    page = e.page
    i +=1
  end
end





