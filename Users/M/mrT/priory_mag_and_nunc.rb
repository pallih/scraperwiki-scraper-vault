require 'nokogiri'
require 'mechanize'
agent = Mechanize.new

list_page = agent.get("http://www.prioryrecords.co.uk/searchcat.php?category=MagNunc");
list_page.links_with(:text => "More Information").each{ |link|
  x = link.click
  artist = x.search("div[@id='itemartist']").inner_html
  artist.sub!(/Artist:.{4}/,"");
  i=1
  x.search("div[@id='tracklisting'] table tr").each{ |track|
     items = track.search("td")
     track_no = items[0].inner_text.sub!(/\./,"")
     setting = items[1].inner_text
     composor = items[2].inner_text
     item = {:key=>artist+track_no,:track_no=>track_no,:setting=>setting,:composor=>composor,:artist=>artist}
     ScraperWiki::save_sqlite(['key'],item)
  }
}

