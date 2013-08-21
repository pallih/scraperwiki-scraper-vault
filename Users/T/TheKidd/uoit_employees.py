import scraperwiki
import lxml.html

start = scraperwiki.sqlite.get_var("pos", 0)

html = scraperwiki.scrape("http://ssbprod1.aac.mycampus.ca/pls/prod/www_directory.directory_uoit.p_ShowPeople")
root = lxml.html.fromstring(html)
employees = root.cssselect("table[cellspacing=2] tr.regularText td a")
employees = employees[start:]

for pos, employee in enumerate(employees):
    url = employee.get('href')
    id = ''.join(i for i in url if i.isdigit())
    
    html = scraperwiki.scrape("http://ssbprod1.aac.mycampus.ca/pls/prod/%s" % url)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table[cellspacing=2] tr.regularText td:nth-child(2)")
    
    columns = ["name", "position", "department", "extension", "location", "building", "email"]
    data = {'id': id}
    for row_num, row in enumerate(rows):
        data[columns[row_num]] = row.text_content()
    print data
        
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    scraperwiki.sqlite.save_var("pos", start+pos)

scraperwiki.sqlite.save_var("pos", 0)