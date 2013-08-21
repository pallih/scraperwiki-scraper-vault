require 'nokogiri'
require 'open-uri'
require 'json'

def get_page(url)
  req = open(url)
  data = JSON.parse(req.read)
  return data
end

def main
  # need to fake user agent :/
  #doc = Nokogiri::HTML(open('http://www.jobbnorge.no/employerprofile.aspx?empID=1328', 'User-Agent' => 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1').read)
  page_num = 1
  total_pages = 1

  until page_num > total_pages
    data_container = get_page("http://hotell.difi.no/api/json/difi/etatsbasen/url?page=#{page_num}")
    page_num += 1
    data_container['entries'].each do |entry|
      data = ['tailid' => entry['tailid'], 'language' => entry['language'], 'url' => entry['url']]
      ScraperWiki.save(['tailid', 'language'], data)
    end
    if data_container['pages'] >= total_pages
      total_pages = data_container['pages']
    else
      raise 'Unexcepted total_page'
    end
    puts "Total pages: #{total_pages} Finished: %s" % data_container['page']
  end
end

main