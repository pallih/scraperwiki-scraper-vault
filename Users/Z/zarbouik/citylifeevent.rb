# CityLife event scraping


require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.citylife.co.uk/whats_on/event/71783_don_broco'

def scrape_event(url,id)
  puts "Id = #{id}"
  page = Nokogiri::HTML(open(url))
  description=page.css('p#bodytext').inner_text
  description+=' '+page.css('div#listing-details').inner_text.gsub('Details','')
  puts description
end

#scrape_event(BASE_URL,1)

BASE_VENUE = 'http://www.citylife.co.uk/whats_on/venue/111643_roadhouse'

def scrape_venue(url,id,date,eventId)
  puts "Id = #{id}"
  page = Nokogiri::HTML(open(url))
  puts 'name : '+page.css('div#listingheader h2')[0].inner_text
  scriptMap = page.css('div.venue-map script').inner_text
  scriptMapArray = scriptMap.split(/\n/)
  scriptMapArray.each {|line|
    line=line.split(/"/)
    puts "latitude : "+line[3] if line[1]=='latitude'
    puts "longitude : "+line[3] if line[1]=='longitude'
  }
  details = page.css('div#listing-details li').each { |detail|
    detailSplit = detail.inner_text.split(/:/)
    detail=detail.inner_text
    detail.strip!
    detailSplit[0].strip!
    if(detailSplit[0]=='Address')
      puts "Venue address: "+detail.gsub('Address: ','')
    elsif(detailSplit[0]=='Tel')
      puts "Venue phone number: "+detail.gsub('Tel: ','')
    else
      puts "Other info: "+detail
    end
  }
  
  allEvents = page.css('table.event-table tr').each {|rowEvent|
    if((rowEvent.css('td')[0].inner_text == date) && (rowEvent.css('td')[3].css('a')[0]['href'].include? eventId.to_s))
      puts "Start time: "+rowEvent.css('td')[1].inner_text.gsub('Starts ','')
      puts "End time: "+rowEvent.css('td')[2].inner_text.gsub('Ends ','')
      break
    end
  }
end

scrape_venue(BASE_VENUE,1,'21/02/2011',71783)