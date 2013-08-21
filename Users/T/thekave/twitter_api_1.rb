# We use the Flickr API to construct a table
require 'fruttero'

# STARTS HERE: define tag to look for 
tag=Array.[]("aftreden oprotten opstappen ontslag")
record={}

for i in 0..1 do
  for j in 1..50 do
    base_URI="http://search.twitter.com/search.atom?q="+tag[i]+"&page="+ j.to_s()

    xml = ScraperWiki.scrape(base_URI)
    puts xml
    record = {}

    # Next we use Nokogiri to extract the values from the XML returned from the API
    doc = Nokogiri::HTML(xml)
    doc.search('entry').each do |entry|
       puts entry.css ('title')
       puts entry.css ('name')
       record['title']= entry.css ('title')
       record['name']= entry.css ('name')
       record['geo']= entry.css ('twitter:geo')      
       record['published']= entry.css ('published')   
       ScraperWiki.save_sqlite(unique_keys=['title'], record)
    end
  end
end