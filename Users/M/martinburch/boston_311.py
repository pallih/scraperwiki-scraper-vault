import scraperwiki
from urllib2 import urlopen
from json import load

hostname = "data.cityofboston.gov"
endpoint = "awu8-dc52"
query = "select+case_enquiry_id,open_dt,case_title,subject,reason,type,latitude,longitude+where+(closure_reason+IS+NULL+and+case_status+=+%27Open%27)"
startRow = 0
numRows = 2000
appToken = "ZUwuxNW2shEOQQzt4T4H0AwQh"

http://%s/resource/%s.json?$$app_token=%s&$query=%s+offset++limit+%s

hostname, endpoint, appToken, query, str(

while True:
    url = "http://%s/api/views/%s/rows.json?method=getRows&$offset=%s&$limit=%s" % (hostname, viewID, str(startRow), str(numRows))
    response = urlopen(url)
    rows = load(response)
    numRowsRcvd = len(rows)
    if numRowsRcvd == 0:
        break
    print '\n====== %s ROWS DOWNLOADED:  ======' % (numRowsRcvd)
    for row in rows:
        print row    # rowID for ward number
    startRow += numRows
