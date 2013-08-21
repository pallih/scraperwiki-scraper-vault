import scraperwiki
import lxml.html

print "HARRO WORLD"

html = scraperwiki.scrape("http://www.aucc.ca/canadian-universities/study-programs/")
root = lxml.html.fromstring(html)

sep = "," #split at comma
sep2 = "(" #split at bracket
o_node = ""

discipline = root.get_element_by_id("dcu_disciplines")
for el in discipline.cssselect("li.li_lvl1"):           
    for title in el.cssselect("ul li"):
        n = title.text_content().split(sep, 1)[0].split(sep2, 1)[0].strip(" \t\n\r")
        if n != o_node :
            data = {
                'program': n
            }
            scraperwiki.sqlite.save(unique_keys=['program'], data=data)
            o_node = n
            print n
        
    print "---"


