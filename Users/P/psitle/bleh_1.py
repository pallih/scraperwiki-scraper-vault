import scraperwiki
from lxml.etree import tostring
import re
import lxml.html

#find the locations of all the target
def findall(target,string):
    list=[]
    beg = 0
    var = 1
    while var == 1:
        item = string.find(target,beg,len(string))
        if item  == -1:
            break
        else:
            list.append(item)
            beg = item + 1
    return list


html = scraperwiki.scrape("http://www.minecraftwiki.net/wiki/Blocks")
#root = lxml.html.fromstring(html)
#print(tostring(root,pretty_print=True).strip())


lists = findall('<h2>',html)
print lists
print lists[0]
print len(lists)






import scraperwiki
from lxml.etree import tostring
import re
import lxml.html

#find the locations of all the target
def findall(target,string):
    list=[]
    beg = 0
    var = 1
    while var == 1:
        item = string.find(target,beg,len(string))
        if item  == -1:
            break
        else:
            list.append(item)
            beg = item + 1
    return list


html = scraperwiki.scrape("http://www.minecraftwiki.net/wiki/Blocks")
#root = lxml.html.fromstring(html)
#print(tostring(root,pretty_print=True).strip())


lists = findall('<h2>',html)
print lists
print lists[0]
print len(lists)






