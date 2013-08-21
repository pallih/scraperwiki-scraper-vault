from BeautifulSoup import BeautifulSoup
import scraperwiki
import time
import re

# Username
username = 'avholloway'

# Base URL
url = 'https://supportforums.cisco.com/people/' + username + '/'

# Get the current timestamp
scrape_datetime  = int(time.mktime(time.localtime()))
    
# Grab the web page
html_resp = scraperwiki.scrape(url)
    
# Use BeautifulSoup to parse the HTML and create a tree
html_tree = BeautifulSoup(html_resp)
    
# Extract the points
points_raw = str(html_tree.find('span', {'class': 'jive-cisco-user-points'}).contents[1])

points_match = re.findall(r'\((.+)\)', points_raw)

if points_match:
  points = int(points_match[0].replace(",", ""))
else:
  points = 0

#print scrape_datetime, username, points
scraperwiki.sqlite.save(['timestamp', 'username', 'points'], {'timestamp' : scrape_datetime, 'username' : username, 'points' : points})