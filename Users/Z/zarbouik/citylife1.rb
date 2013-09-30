###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'
require 'date'

BASE_URL = 'http://www.citylife.co.uk/whats_on/'
@date=Date.today.strftime("%d/%m/%Y")

# define the order our columns are displayed in the datastore
#mdc = SW_MetadataClient.new
#mdc.save('data_columns', ['Id','Id_Event', 'Link', 'Title', 'LinkVenue', 'Venue', 'Category','Description','Latitude','Longitude','VenueInfo','Address','Tel','Date','Start','End']) 
@i=0

# scrape_event scrapes the event page
def scrape_event(url)
  description=""
  page = Nokogiri::HTML(open(url))
  description=page.css('p#bodytext').inner_text
  description+=' '+page.css('div#listing-details').inner_text.gsub('Details','')
  #linkVenue=page.css('div#listingheader p.nextevent a')[0]['href']
  #puts description
  yield description
end

# scrape_venue scrapes venue info page
def scrape_venue(url,date,eventId)
  latitude=longitude=address=tel=venueInfo=starts=ends=""
  page = Nokogiri::HTML(open(url))
  #puts 'name : '+page.css('div#listingheader h2')[0].inner_text
  scriptMap = page.css('div.venue-map script').inner_text
  scriptMapArray = scriptMap.split(/\n/)
  scriptMapArray.each {|line|
    line=line.split(/"/)
    #puts "latitude : "+line[3] if line[1]=='latitude'
    latitude=line[3] if line[1]=='latitude'
    #puts "longitude : "+line[3] if line[1]=='longitude'
    longitude=line[3] if line[1]=='longitude'
  }
  details = page.css('div#listing-details li').each { |detail|
    detailSplit = detail.inner_text.split(/:/)
    detail=detail.inner_text
    detail.strip!
    detailSplit[0].strip!
    if(detailSplit[0]=='Address')
      #puts "Venue address: "+detail.gsub('Address: ','')
      address=detail.gsub('Address: ','')
    elsif(detailSplit[0]=='Tel')
      #puts "Venue phone number: "+detail.gsub('Tel: ','')
      tel=detail.gsub('Tel: ','')
    else
      #puts "Other info: "+detail
      venueInfo+=detail
    end
  }
  
  allEvents = page.css('table.event-table tr').each {|rowEvent|
    if((rowEvent.css('td')[0].inner_text == date) && (rowEvent.css('td')[3].css('a')[0]['href'].include? eventId.to_s))
      #puts "Start time: "+rowEvent.css('td')[1].inner_text.gsub('Starts ','')
      starts=rowEvent.css('td')[1].inner_text.gsub('Starts ','')
      #puts "End time: "+rowEvent.css('td')[2].inner_text.gsub('Ends ','')
      ends=rowEvent.css('td')[2].inner_text.gsub('Ends ','')
      break
    end
  }

  yield latitude,longitude,address,tel,venueInfo,starts,ends
end

# scrape_table scrapes the search result
def scrape_table(page)
  event_list = page.css('div.listing-search-result').each do |row|
    #puts rows
    record = {}

    record['Link']    = row.css('div.secondary-info a')[0]['href']
    record['Id_event'] = record['Link'][16..20]
    if !record['Id_event'].to_s.empty? 
      record['Title']     = row.css('div.secondary-info a')[0].inner_text
      if(!row.css('div.secondary-info span.venue a').empty?)
        record['LinkVenue'] = row.css('div.secondary-info span.venue a')[0]['href']
        record['Venue'] = row.css('div.secondary-info span.venue a')[0].inner_text
      else
        record['Venue'] = "Multiple Venues"
      end
      record['Category'] = row.css('span.category')[0].inner_text
      record['Id']=@i

      thr_event=Thread.new{
        scrape_event('http://www.citylife.co.uk'+record['Link']) { |description|
          record['Description']=description
        }
      }

      thr_venue=Thread.new{
        if(record['Venue']!='Multiple Venues')
          scrape_venue('http://www.citylife.co.uk'+record['LinkVenue'],@date,record['Id_event']) { |latitude,longitude,address,tel,venueInfo,starts,ends|
          record['Latitude']=latitude
          record['Longitude']=longitude
          record['Address']=address
          record['Tel']=tel
          record['VenueInfo']=venueInfo
          record['Start']=starts
          record['End']=ends
        }
        end
      }

      @i+=1
      #puts record
      # Finally, save the record to the datastore - 'Artist' is our unique key
      
      thr_event.join
      thr_venue.join

      ScraperWiki.save(["Id"], record)
    end
  end
end

#        scrape_and_look_for_next_link(starting_url)

@thr_pages=[]

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    @thr_pages << Thread.new{
      scrape_table(page)
    }
    next_link = page.css('a.pager').each do |pager|
      if pager.inner_text.include?  'Next'
        #puts pager
        next_url = pager['href']
        puts next_url
        #puts 'NEXT PAGE: Waiting 60 secs to avoid IP banning'
        #sleep(60)
        
        nb_thr_alive = 0
        @thr_pages.each do |thr_page|
          if (thr_page.alive?) 
            nb_thr_alive+=1
          end
        end
        if(nb_thr_alive>4) 
          puts 'to many threads, wait for the last to exit'
          @thr_pages.last.join
        end
        
        begin
          scrape_and_look_for_next_link(next_url)
        rescue Timeout::Error
          puts 'Timeout was detected.  Trying again...'
          retry
        end
      end
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL
scrape_and_look_for_next_link(starting_url)

puts 'wait for all threads to end'
@thr_pages.each {|thr_current|
  if(thr_current.alive?) 
    thr_current.join
  end
}
puts 'ok'
###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################
require 'nokogiri'
require 'open-uri'
require 'date'

BASE_URL = 'http://www.citylife.co.uk/whats_on/'
@date=Date.today.strftime("%d/%m/%Y")

# define the order our columns are displayed in the datastore
#mdc = SW_MetadataClient.new
#mdc.save('data_columns', ['Id','Id_Event', 'Link', 'Title', 'LinkVenue', 'Venue', 'Category','Description','Latitude','Longitude','VenueInfo','Address','Tel','Date','Start','End']) 
@i=0

# scrape_event scrapes the event page
def scrape_event(url)
  description=""
  page = Nokogiri::HTML(open(url))
  description=page.css('p#bodytext').inner_text
  description+=' '+page.css('div#listing-details').inner_text.gsub('Details','')
  #linkVenue=page.css('div#listingheader p.nextevent a')[0]['href']
  #puts description
  yield description
end

# scrape_venue scrapes venue info page
def scrape_venue(url,date,eventId)
  latitude=longitude=address=tel=venueInfo=starts=ends=""
  page = Nokogiri::HTML(open(url))
  #puts 'name : '+page.css('div#listingheader h2')[0].inner_text
  scriptMap = page.css('div.venue-map script').inner_text
  scriptMapArray = scriptMap.split(/\n/)
  scriptMapArray.each {|line|
    line=line.split(/"/)
    #puts "latitude : "+line[3] if line[1]=='latitude'
    latitude=line[3] if line[1]=='latitude'
    #puts "longitude : "+line[3] if line[1]=='longitude'
    longitude=line[3] if line[1]=='longitude'
  }
  details = page.css('div#listing-details li').each { |detail|
    detailSplit = detail.inner_text.split(/:/)
    detail=detail.inner_text
    detail.strip!
    detailSplit[0].strip!
    if(detailSplit[0]=='Address')
      #puts "Venue address: "+detail.gsub('Address: ','')
      address=detail.gsub('Address: ','')
    elsif(detailSplit[0]=='Tel')
      #puts "Venue phone number: "+detail.gsub('Tel: ','')
      tel=detail.gsub('Tel: ','')
    else
      #puts "Other info: "+detail
      venueInfo+=detail
    end
  }
  
  allEvents = page.css('table.event-table tr').each {|rowEvent|
    if((rowEvent.css('td')[0].inner_text == date) && (rowEvent.css('td')[3].css('a')[0]['href'].include? eventId.to_s))
      #puts "Start time: "+rowEvent.css('td')[1].inner_text.gsub('Starts ','')
      starts=rowEvent.css('td')[1].inner_text.gsub('Starts ','')
      #puts "End time: "+rowEvent.css('td')[2].inner_text.gsub('Ends ','')
      ends=rowEvent.css('td')[2].inner_text.gsub('Ends ','')
      break
    end
  }

  yield latitude,longitude,address,tel,venueInfo,starts,ends
end

# scrape_table scrapes the search result
def scrape_table(page)
  event_list = page.css('div.listing-search-result').each do |row|
    #puts rows
    record = {}

    record['Link']    = row.css('div.secondary-info a')[0]['href']
    record['Id_event'] = record['Link'][16..20]
    if !record['Id_event'].to_s.empty? 
      record['Title']     = row.css('div.secondary-info a')[0].inner_text
      if(!row.css('div.secondary-info span.venue a').empty?)
        record['LinkVenue'] = row.css('div.secondary-info span.venue a')[0]['href']
        record['Venue'] = row.css('div.secondary-info span.venue a')[0].inner_text
      else
        record['Venue'] = "Multiple Venues"
      end
      record['Category'] = row.css('span.category')[0].inner_text
      record['Id']=@i

      thr_event=Thread.new{
        scrape_event('http://www.citylife.co.uk'+record['Link']) { |description|
          record['Description']=description
        }
      }

      thr_venue=Thread.new{
        if(record['Venue']!='Multiple Venues')
          scrape_venue('http://www.citylife.co.uk'+record['LinkVenue'],@date,record['Id_event']) { |latitude,longitude,address,tel,venueInfo,starts,ends|
          record['Latitude']=latitude
          record['Longitude']=longitude
          record['Address']=address
          record['Tel']=tel
          record['VenueInfo']=venueInfo
          record['Start']=starts
          record['End']=ends
        }
        end
      }

      @i+=1
      #puts record
      # Finally, save the record to the datastore - 'Artist' is our unique key
      
      thr_event.join
      thr_venue.join

      ScraperWiki.save(["Id"], record)
    end
  end
end

#        scrape_and_look_for_next_link(starting_url)

@thr_pages=[]

## scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url)
    page = Nokogiri::HTML(open(url))
    @thr_pages << Thread.new{
      scrape_table(page)
    }
    next_link = page.css('a.pager').each do |pager|
      if pager.inner_text.include?  'Next'
        #puts pager
        next_url = pager['href']
        puts next_url
        #puts 'NEXT PAGE: Waiting 60 secs to avoid IP banning'
        #sleep(60)
        
        nb_thr_alive = 0
        @thr_pages.each do |thr_page|
          if (thr_page.alive?) 
            nb_thr_alive+=1
          end
        end
        if(nb_thr_alive>4) 
          puts 'to many threads, wait for the last to exit'
          @thr_pages.last.join
        end
        
        begin
          scrape_and_look_for_next_link(next_url)
        rescue Timeout::Error
          puts 'Timeout was detected.  Trying again...'
          retry
        end
      end
    end
end

# ---------------------------------------------------------------------------
# START HERE - define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
starting_url = BASE_URL
scrape_and_look_for_next_link(starting_url)

puts 'wait for all threads to end'
@thr_pages.each {|thr_current|
  if(thr_current.alive?) 
    thr_current.join
  end
}
puts 'ok'
