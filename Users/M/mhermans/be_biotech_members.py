# Scraping members of bio.be

from lxml import html

greenurl = 'http://www.bio.be/content.asp?menu_id=199&id=361&langue_id=1'
redurl = 'http://www.bio.be/content.asp?menu_id=200&id=360&langue_id=1'
whiteurl = 'http://www.bio.be/content.asp?menu_id=201&id=359&langue_id=1'
associatedurl = 'http://www.bio.be/content.asp?menu_id=202&id=362&langue_id=1'

root = html.parse(greenurl).getroot()
for line in root.xpath('//li'):
    print line.xpath('a')
# Scraping members of bio.be

from lxml import html

greenurl = 'http://www.bio.be/content.asp?menu_id=199&id=361&langue_id=1'
redurl = 'http://www.bio.be/content.asp?menu_id=200&id=360&langue_id=1'
whiteurl = 'http://www.bio.be/content.asp?menu_id=201&id=359&langue_id=1'
associatedurl = 'http://www.bio.be/content.asp?menu_id=202&id=362&langue_id=1'

root = html.parse(greenurl).getroot()
for line in root.xpath('//li'):
    print line.xpath('a')
