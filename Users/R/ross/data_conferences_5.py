import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.kdnuggets.com/meetings/")
root = lxml.html.fromstring(html)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

for row in root.cssselect('li'):
    details = row.text_content().strip()
   # print details[:3]
    if details[:3] in months:
        date = details.split(',')[0].strip()
        title = details.split(',')[1].strip()
        location = str(details.split(',')[2:]).replace('[','').replace(']','').replace("'","").replace('.','').replace('\\r\\n','').strip()
    else: 
        date = "Not given"
        title = details.split(',')[0].strip()
        location = str(details.split(',')[1:]).replace('[','').replace(']','').replace("'","").replace('.','').replace('\\r\\n','').strip()

    link = row.cssselect("a")[0].attrib.get('href')

    data = {'Date': date, 'Name': title, 'Location': location, 'URL': link}
    print data
    scraperwiki.sqlite.save(['URL'], data)