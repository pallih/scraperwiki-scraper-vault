sourcescraper = 'nijobfinder-public-salary-ruby'

# This pulls in the data api which lets us connect to the datastore in the other scraper (the one that contains the data)
#from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

# Some basic variables you need to initialize
limit = 5000
offset = 0

puts "<html dir=\"ltr\" lang=\"en\">"
puts "<head>"
puts "    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>"
puts "    <title>General Map Thing</title>"
puts "    <style type=\"text/css\" media=\"screen\">p{padding:1px;}</style>"
puts "    <script type=\"text/javascript\" src=\"http://maps.google.com/maps/api/js?sensor=false\"></script>"
puts "    <script type=\"text/javascript\" src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js\"></script>"
puts "</head>"
puts ""
puts "<body>"
puts ""
puts "<h2>Money! That's what I want... <span id=\"scrapername\">...</span> <em id=\"message\">...</em></h2>"

puts "<p>Here goes... The most important 3 bars in Northern Ireland...</p>"

puts "<style type=\"text/css\">"
puts "    .graph {"
puts "        position: relative; /* IE is dumb */"
puts "        width: 200px;"
puts "        border: 1px solid #B1D632;"
puts "        padding: 2px;"
puts "    }"
puts "    .graph .bar {"
puts "        display: block;"
puts "        position: relative;"
puts "        background: #B1D632;"
puts "        text-align: center;"
puts "        color: #333;"
puts "        height: 2em;"
puts "        line-height: 2em;"
puts "    }"
puts "    .graph .bar span { position: absolute; left: 1em; }"
puts "</style>"
puts "<div class=\"graph\" style=\"float: left\">"

# This piece of code here won't be output to the view.
# It's for calculation purposes only
num_private_parsed = nil
num_public_parsed = nil
num_voluntary_parsed = nil
avg_private_salary = nil
avg_public_salary = nil
avg_voluntary_salary = nil

ScraperWiki.getData(sourcescraper, limit, offset).each do |row|
    # Note: There's only every one row
    num_private_parsed = row['num_private_parsed'].to_i
    num_public_parsed = row['num_public_parsed'].to_i
    num_voluntary_parsed = row['num_voluntary_parsed'].to_i
    avg_private_salary = row['avg_private_salary'.to_i]
    avg_public_salary = row['avg_public_salary'].to_i
    avg_voluntary_salary = row['avg_voluntary_salary'].to_i
end

combined_avg_salary = avg_private_salary + avg_public_salary + avg_voluntary_salary
private_salary_percentage = avg_private_salary.to_f * 100.to_f / combined_avg_salary.to_f
public_salary_percentage = avg_public_salary.to_f * 100.to_f / combined_avg_salary.to_f
# Calculating voluntary_salary_percentage in a different manner
# just to be sure to be sure to avoid a 1% rounding error (above to_f() conversions should guard against this anyway)
voluntary_salary_percentage = 100 - public_salary_percentage - private_salary_percentage

puts "Public <strong class=\"bar\" style=\"width: " + public_salary_percentage.to_s + "%; background: #cccfff;\">" + avg_public_salary.to_s + "</strong>"
puts "Private<strong class=\"bar\" style=\"width: " + private_salary_percentage.to_s + "%; background: yellow;\">" + avg_private_salary.to_s + "</strong>"
puts "Voluntary<strong class=\"bar\" style=\"width: " + voluntary_salary_percentage.to_s + "%; \">" + avg_voluntary_salary.to_s + "</strong>"
puts "</div>"
puts "<div style=\"float: left; padding-left: 100px\"><br />Number Public sector jobs analysed: " + num_public_parsed.to_s + "<br /><br />"
puts "Number of Private sector jobs analysed: " + num_private_parsed.to_s + "<br /><br />"
puts "Number Voluntary sector jobs analysed: " + num_voluntary_parsed.to_s + "</div>"
puts "</body>"
puts "</html>"


sourcescraper = 'nijobfinder-public-salary-ruby'

# This pulls in the data api which lets us connect to the datastore in the other scraper (the one that contains the data)
#from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

# Some basic variables you need to initialize
limit = 5000
offset = 0

puts "<html dir=\"ltr\" lang=\"en\">"
puts "<head>"
puts "    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>"
puts "    <title>General Map Thing</title>"
puts "    <style type=\"text/css\" media=\"screen\">p{padding:1px;}</style>"
puts "    <script type=\"text/javascript\" src=\"http://maps.google.com/maps/api/js?sensor=false\"></script>"
puts "    <script type=\"text/javascript\" src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js\"></script>"
puts "</head>"
puts ""
puts "<body>"
puts ""
puts "<h2>Money! That's what I want... <span id=\"scrapername\">...</span> <em id=\"message\">...</em></h2>"

puts "<p>Here goes... The most important 3 bars in Northern Ireland...</p>"

puts "<style type=\"text/css\">"
puts "    .graph {"
puts "        position: relative; /* IE is dumb */"
puts "        width: 200px;"
puts "        border: 1px solid #B1D632;"
puts "        padding: 2px;"
puts "    }"
puts "    .graph .bar {"
puts "        display: block;"
puts "        position: relative;"
puts "        background: #B1D632;"
puts "        text-align: center;"
puts "        color: #333;"
puts "        height: 2em;"
puts "        line-height: 2em;"
puts "    }"
puts "    .graph .bar span { position: absolute; left: 1em; }"
puts "</style>"
puts "<div class=\"graph\" style=\"float: left\">"

# This piece of code here won't be output to the view.
# It's for calculation purposes only
num_private_parsed = nil
num_public_parsed = nil
num_voluntary_parsed = nil
avg_private_salary = nil
avg_public_salary = nil
avg_voluntary_salary = nil

ScraperWiki.getData(sourcescraper, limit, offset).each do |row|
    # Note: There's only every one row
    num_private_parsed = row['num_private_parsed'].to_i
    num_public_parsed = row['num_public_parsed'].to_i
    num_voluntary_parsed = row['num_voluntary_parsed'].to_i
    avg_private_salary = row['avg_private_salary'.to_i]
    avg_public_salary = row['avg_public_salary'].to_i
    avg_voluntary_salary = row['avg_voluntary_salary'].to_i
end

combined_avg_salary = avg_private_salary + avg_public_salary + avg_voluntary_salary
private_salary_percentage = avg_private_salary.to_f * 100.to_f / combined_avg_salary.to_f
public_salary_percentage = avg_public_salary.to_f * 100.to_f / combined_avg_salary.to_f
# Calculating voluntary_salary_percentage in a different manner
# just to be sure to be sure to avoid a 1% rounding error (above to_f() conversions should guard against this anyway)
voluntary_salary_percentage = 100 - public_salary_percentage - private_salary_percentage

puts "Public <strong class=\"bar\" style=\"width: " + public_salary_percentage.to_s + "%; background: #cccfff;\">" + avg_public_salary.to_s + "</strong>"
puts "Private<strong class=\"bar\" style=\"width: " + private_salary_percentage.to_s + "%; background: yellow;\">" + avg_private_salary.to_s + "</strong>"
puts "Voluntary<strong class=\"bar\" style=\"width: " + voluntary_salary_percentage.to_s + "%; \">" + avg_voluntary_salary.to_s + "</strong>"
puts "</div>"
puts "<div style=\"float: left; padding-left: 100px\"><br />Number Public sector jobs analysed: " + num_public_parsed.to_s + "<br /><br />"
puts "Number of Private sector jobs analysed: " + num_private_parsed.to_s + "<br /><br />"
puts "Number Voluntary sector jobs analysed: " + num_voluntary_parsed.to_s + "</div>"
puts "</body>"
puts "</html>"


