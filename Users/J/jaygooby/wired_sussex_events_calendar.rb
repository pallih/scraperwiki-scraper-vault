(2011..2012).each do |year|
  puts "Year is: #{year}"

  (1..12).each do |month|
    puts "Month is: #{month}"

    begin

      json_data = ScraperWiki.scrape("http://www.wiredsussex.com/event-calendar/handlers/event-handler.ashx?month=#{month}&year=#{year}")

      puts json_data

      data = JSON.parse(json_data)
      
      events = data['calendarBlocks'].map {|cb| cb['events']}.flatten
    
      ScraperWiki.save(unique_keys=["typeIds", "eventId", "title", "startDateTime", "endDateTime", "startDay", "endDay", "abstract", "description", "cost", "active", "upcoming", "email", "location","venue"], events=events)
    rescue
      puts "No events for #{year}/#{month}"
    end
  end
end

