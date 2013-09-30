ScraperWiki.attach("wired_sussex_events_calendar")

data = ScraperWiki.select(    
    "* from wired_sussex_events_calendar.swdata 
    order by startDateTime"
)

class String
  def crlf
    self.gsub(/$/, "\r\n")
  end
end

def to_ical_timestamp(datetime)
  # Go from 2011-01-02T09:00:00+00:00 to 20110102T090000Z
  DateTime.parse(datetime).to_s.gsub(/[-:]/,'').gsub(/(\+.*)/,'Z')
end



puts "BEGIN:VCALENDAR".crlf
puts "PRODID:-//Apple Inc.//iCal 4.0.3//EN".crlf
puts "VERSION:2.0".crlf
puts "CALSCALE:GREGORIAN".crlf
puts "METHOD:PUBLISH".crlf
puts "X-WR-CALNAME:Wired Sussex events calendar".crlf
puts "X-WR-CALDESC:Wired Sussex events calendar".crlf

puts "X-WR-TIMEZONE:Europe/London".crlf

data.each do |event|

  puts "BEGIN:VEVENT".crlf
  puts "UID:#{to_ical_timestamp(event['startDateTime']) rescue '00000000T000000Z'}-#{event['eventId']}@wiredsussex.com".crlf

  puts "DTSTAMP:#{to_ical_timestamp(event['startDateTime']) rescue '00000000T000000Z'}".crlf 
  puts "DTSTART:#{to_ical_timestamp(event['startDateTime']) rescue '00000000T000000Z'}".crlf 
  puts "DTEND:#{to_ical_timestamp(event['endDateTime']) rescue '00000000T000000Z'}".crlf

  puts "X-TITLE:#{event['title']}".gsub(/[\r\n]/,' ').crlf

  puts "SUMMARY:#{event['title']} - #{event['abstract']}".gsub(/[\r\n]/,' ').crlf
  puts "DESCRIPTION:#{event['description']}".gsub(/[\r\n]/,' ').crlf
 
  location_or_venue = event['location'] || event['venue']
  puts "LOCATION:#{event['location_or_venue']}".gsub(/[\r\n]/,' ').crlf unless location_or_venue.empty? 
        
  puts "END:VEVENT".crlf
end

puts "END:VCALENDAR".crlfScraperWiki.attach("wired_sussex_events_calendar")

data = ScraperWiki.select(    
    "* from wired_sussex_events_calendar.swdata 
    order by startDateTime"
)

class String
  def crlf
    self.gsub(/$/, "\r\n")
  end
end

def to_ical_timestamp(datetime)
  # Go from 2011-01-02T09:00:00+00:00 to 20110102T090000Z
  DateTime.parse(datetime).to_s.gsub(/[-:]/,'').gsub(/(\+.*)/,'Z')
end



puts "BEGIN:VCALENDAR".crlf
puts "PRODID:-//Apple Inc.//iCal 4.0.3//EN".crlf
puts "VERSION:2.0".crlf
puts "CALSCALE:GREGORIAN".crlf
puts "METHOD:PUBLISH".crlf
puts "X-WR-CALNAME:Wired Sussex events calendar".crlf
puts "X-WR-CALDESC:Wired Sussex events calendar".crlf

puts "X-WR-TIMEZONE:Europe/London".crlf

data.each do |event|

  puts "BEGIN:VEVENT".crlf
  puts "UID:#{to_ical_timestamp(event['startDateTime']) rescue '00000000T000000Z'}-#{event['eventId']}@wiredsussex.com".crlf

  puts "DTSTAMP:#{to_ical_timestamp(event['startDateTime']) rescue '00000000T000000Z'}".crlf 
  puts "DTSTART:#{to_ical_timestamp(event['startDateTime']) rescue '00000000T000000Z'}".crlf 
  puts "DTEND:#{to_ical_timestamp(event['endDateTime']) rescue '00000000T000000Z'}".crlf

  puts "X-TITLE:#{event['title']}".gsub(/[\r\n]/,' ').crlf

  puts "SUMMARY:#{event['title']} - #{event['abstract']}".gsub(/[\r\n]/,' ').crlf
  puts "DESCRIPTION:#{event['description']}".gsub(/[\r\n]/,' ').crlf
 
  location_or_venue = event['location'] || event['venue']
  puts "LOCATION:#{event['location_or_venue']}".gsub(/[\r\n]/,' ').crlf unless location_or_venue.empty? 
        
  puts "END:VEVENT".crlf
end

puts "END:VCALENDAR".crlf