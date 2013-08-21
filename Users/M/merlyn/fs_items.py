import scraperwiki
#import lxml.etree
import lxml.html
import re

def get_table(page):
    root = lxml.html.parse('http://guide.fallensword.com/index.php?cmd=items&index=' + str(page)).getroot()
    trs = root.cssselect('html>body>table>tr>td>table>tr>td>table>tr')
    index = 1
    for tr in trs:
        if index <> 1 and index <> len(trs) and index % 2 == 1:
            rec = {}
            td = tr.cssselect('td')
            a = td[0].cssselect('a')[0]
            rec ['Name'] = a.text
#            href = a.attrib.get('href')
            rec ['id'] = int(re.search(r'item_id=(\d+)&', a.attrib.get('href')).group(1))
            rec ['Level'] = int(td[1].text)
            rec ['Type'] = td[2].text
            rec ['Rarity'] = td[3].text
            rec ['Attack'] = int(td[4].text)
            rec ['Defense'] = int(td[5].text)
            rec ['Armor'] = int(td[6].text)
            rec ['Damage'] = int(td[7].text)
            rec ['HP'] = int(td[8].text)
#            print rec
            scraperwiki.sqlite.save(unique_keys=['id'], data=rec)
        index += 1


#scraperwiki.sqlite.execute('drop table if exists swdata')
#scraperwiki.sqlite.execute('CREATE TABLE `swdata` (`id` integer, `Name` text, `Level` integer, `Type` text, `Rarity` text, `Attack` integer, `Defense` integer, `Armor` integer, `Damage` integer, `HP` integer)')
#scraperwiki.sqlite.commit()

for i in range(10):
    print i
    get_table(i)



