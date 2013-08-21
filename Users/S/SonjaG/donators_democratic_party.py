import scraperwiki
import re

# This function applies the regex to the page

for page in range(1, 116):
    # Adress to scrape
    url = 'http://www.ds.org.rs/o-nama/finansijski-izvestaji/izvestaj/strana-' + str(page) + ''

    # opens the URL
    html = scraperwiki.scrape(url)
    # Extracts the HTML
    print html

    pattern = '<tr>[^\r]\s*<td width="35%">(.*)</td>[^\r]\s*<td width="18%">(.*)</td>[^\r]\s*<td width="18%">(.*)</td>[^\r]\s*<td width="28%">(.*)</td>[^\r]\s*</tr>'
    
    regex = re.compile(pattern)
       
    matches = regex.findall(html)
    
    x = 0

    for match in matches:
        x+=1
        data = {}
        data['id'] = str(page) + "-" + str(x)
        data['name'] = match[0]
        data['city'] = match[1]
        data['amount'] = match[2]
        data['date'] = match[3]
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
