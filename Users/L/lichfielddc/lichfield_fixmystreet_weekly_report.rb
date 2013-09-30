ScraperWiki::attach('lichfield_district_council_fixmystreet_reports')

reports = ScraperWiki::select("* from `swdata` WHERE swdata.updated > '#{(Date.today-7).strftime('%F')}'")

puts "Welcome to this week's FixMyStreet weekly update. Here are all the reports which have been updated this week:\r\n"

reports.each do |report|
  
  puts "#{report['description']}\r\n"

  puts "Reported: #{Date.parse(report['requested']).strftime('%d %B %Y')}\r\n"
  puts "Last Updated: #{Date.parse(report['updated']).strftime('%d %B %Y')}\r\n"
  puts "Status: #{report['status']}"

  comments = ScraperWiki::select("* from `comments` WHERE problemid = '#{report['uid']}'")

  if comments.count > 0
    
    puts "Comments"

    comments.each do |comment|

      puts "From: #{comment['author']}"

      puts "\"#{comment['comment']}\""

      puts "Date made: #{Date.parse(comment['date']).strftime('%d %B %Y')} at #{comment['time']}"
      puts "-------------------------------------"

    end

  end

  puts "Address: #{report['url']}"
  
  puts "\r\n=======================================\r\n"

endScraperWiki::attach('lichfield_district_council_fixmystreet_reports')

reports = ScraperWiki::select("* from `swdata` WHERE swdata.updated > '#{(Date.today-7).strftime('%F')}'")

puts "Welcome to this week's FixMyStreet weekly update. Here are all the reports which have been updated this week:\r\n"

reports.each do |report|
  
  puts "#{report['description']}\r\n"

  puts "Reported: #{Date.parse(report['requested']).strftime('%d %B %Y')}\r\n"
  puts "Last Updated: #{Date.parse(report['updated']).strftime('%d %B %Y')}\r\n"
  puts "Status: #{report['status']}"

  comments = ScraperWiki::select("* from `comments` WHERE problemid = '#{report['uid']}'")

  if comments.count > 0
    
    puts "Comments"

    comments.each do |comment|

      puts "From: #{comment['author']}"

      puts "\"#{comment['comment']}\""

      puts "Date made: #{Date.parse(comment['date']).strftime('%d %B %Y')} at #{comment['time']}"
      puts "-------------------------------------"

    end

  end

  puts "Address: #{report['url']}"
  
  puts "\r\n=======================================\r\n"

end