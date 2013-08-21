sourcescraper = 'nijobfinder-public-salary'

# This pulls in the data api which lets us connect to the datastore in the other scraper (the one that contains the data)
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

# Some basic variables you need to initialize
limit = 5000
offset = 0

print "<html dir=\"ltr\" lang=\"en\">"
print "<head>"
print "    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>"
print "    <title>General Map Thing</title>"
print "    <style type=\"text/css\" media=\"screen\">p{padding:1px;}</style>"
print "    <script type=\"text/javascript\" src=\"http://maps.google.com/maps/api/js?sensor=false\"></script>"
print "    <script type=\"text/javascript\" src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js\"></script>"
print "</head>"
print ""
print "<body>"
print ""
print "<h2>Money! That's what I want... <span id=\"scrapername\">...</span> <em id=\"message\">...</em></h2>"
print "\
<p>This compares the average level of pay in the public vs private vs voluntary sectors by analysing jobs listed on <a href=\"http://www.nijobfinder.co.uk\">http://www.nijobfinder.co.uk</a> <ul>\
<li>At time of writing, there were many many more private sector jobs listed than public or voluntary. This makes direct comparision of the figures difficult</li>\
<li>Job postings that did not provide a clear numerical salary were ignored</li>\
<li>Where a salary band was provided, we took that average value</li>\
</p>"

print "<p>Here goes... The most important 3 bars in Northern Ireland...</p>"

print "<style type=\"text/css\">"
print "    .graph {"
print "        position: relative; /* IE is dumb */"
print "        width: 200px;"
print "        border: 1px solid #B1D632;"
print "        padding: 2px;"
print "    }"
print "    .graph .bar {"
print "        display: block;"
print "        position: relative;"
print "        background: #B1D632;"
print "        text-align: center;"
print "        color: #333;"
print "        height: 2em;"
print "        line-height: 2em;"
print "    }"
print "    .graph .bar span { position: absolute; left: 1em; }"
print "</style>"
print "<div class=\"graph\" style=\"float: left\">"

# This piece of code here won't be output to the view.
# It's for calculation purposes only
for row in getData(sourcescraper, limit, offset):
    # Note: There's only every one row
    num_private_parsed = int(row['num_private_parsed'])
    num_public_parsed = int(row['num_public_parsed'])
    num_voluntary_parsed = int(row['num_voluntary_parsed'])
    avg_private_salary = int(row['avg_private_salary'])
    avg_public_salary = int(row['avg_public_salary'])
    avg_voluntary_salary = int(row['avg_voluntary_salary'])

combined_avg_salary = avg_private_salary + avg_public_salary + avg_voluntary_salary
private_salary_percentage = float(avg_private_salary) * float(100) / float(combined_avg_salary)
public_salary_percentage = float(avg_public_salary) * float(100) / float(combined_avg_salary)
# Calculating voluntary_salary_percentage in a different manner
# just to be sure to be sure to avoid a 1% rounding error (above float() conversions should guard against this anyway)
voluntary_salary_percentage = 100 - public_salary_percentage - private_salary_percentage

print "Public <strong class=\"bar\" style=\"width: " + str(public_salary_percentage) + "%; background: #cccfff;\">" + str(avg_public_salary) + "</strong>"
print "Private<strong class=\"bar\" style=\"width: " + str(private_salary_percentage) + "%; background: yellow;\">" + str(avg_private_salary) + "</strong>"
print "Voluntary<strong class=\"bar\" style=\"width: " + str(voluntary_salary_percentage) + "%; \">" + str(avg_voluntary_salary) + "</strong>"
print "</div>"
print "<div style=\"float: left; padding-left: 100px\"><br />Number Public sector jobs analysed: " + str(num_public_parsed) + "<br /><br />"
print "Number of Private sector jobs analysed: " + str(num_private_parsed) + "<br /><br />"
print "Number Voluntary sector jobs analysed: " + str(num_voluntary_parsed) + "</div>"
print "</body>"
print "</html>"

