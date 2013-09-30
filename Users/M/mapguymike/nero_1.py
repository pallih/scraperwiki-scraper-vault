import requests
import re

url = 'http://www.nero.noaa.gov/hcd/STATES4/Gulf_of_Maine_1%28eastern_part%29/Gulf_of_Maine_1%28eastern_part%29/44406700.html'

html = requests.get(url).text
print re.search('<P>Square Description.+&#9;(.+)</P>', html).group(1)





    



import requests
import re

url = 'http://www.nero.noaa.gov/hcd/STATES4/Gulf_of_Maine_1%28eastern_part%29/Gulf_of_Maine_1%28eastern_part%29/44406700.html'

html = requests.get(url).text
print re.search('<P>Square Description.+&#9;(.+)</P>', html).group(1)





    



