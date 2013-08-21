# austrian schools
# http://www.schule.at/index.php?url=schuleNew&startseite=&start=1&anzahl=1&typ=AH

require 'mechanize'
require 'nokogiri'

start = 1
# TODO: read this from page
number_of_schools = 307

agent = Mechanize.new

until start > number_of_schools
search_url = "http://www.schule.at/index.php?url=schuleNew&startseite=&start=#{start}&anzahl=1&typ=AH"
  search_page = agent.get(search_url)
  
  links = search_page.search("div.schoolName a")
  links.each do |link|
    puts link
    result = {}
    page = agent.get("http://www.schule.at" + link['href'])
    result['name'] = link.content.strip
    page.search("td.tdLeft").each do |left|
      key = left.content.strip.downcase
      value = left.next_element.content.strip
      if key =~ /E\-?Mail/i
        # it's in javascript
        value =~ /var ema1l = "(.*?)"/
        user = $1
        value =~ /var ema1lHost = "(.*?)"/
        domain = $1
        result[key] = "#{user}@#{domain}"
      else
        result[key] = value
      end
    end
    ScraperWiki.save(result.keys, result)
  end
  
  start = start + 15
end
