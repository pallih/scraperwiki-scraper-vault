# Markmail
require 'open-uri'
require 'nokogiri'

years = ['2009', '2010', '2011']
base_url = "http://markmail.org/browse/?q=emergya+-from:emergya+-type:checkins+-from:juanje%2Eojeda+-from:gloob+opt:noquote+date:"

years.each do |year|
  url = base_url + year
  doc = Nokogiri::HTML(open url)
  doc.xpath('//tr/td[@align = "right"]').each do |row|
    data = {
      'list' => row.previous_element.text,
      'mails' => row.text.to_i,
      'year' => year
    }
    ScraperWiki.save(unique_keys=['list'], data=data)
  end
end
# Markmail
require 'open-uri'
require 'nokogiri'

years = ['2009', '2010', '2011']
base_url = "http://markmail.org/browse/?q=emergya+-from:emergya+-type:checkins+-from:juanje%2Eojeda+-from:gloob+opt:noquote+date:"

years.each do |year|
  url = base_url + year
  doc = Nokogiri::HTML(open url)
  doc.xpath('//tr/td[@align = "right"]').each do |row|
    data = {
      'list' => row.previous_element.text,
      'mails' => row.text.to_i,
      'year' => year
    }
    ScraperWiki.save(unique_keys=['list'], data=data)
  end
end
