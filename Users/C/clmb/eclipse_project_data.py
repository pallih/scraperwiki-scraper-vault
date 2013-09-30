import urllib
import lxml.html
import re
import urlparse
import scraperwiki

url = "http://www.eclipse.org/projects/listofprojects.php"

html = urllib.urlopen(url).read()
#print html   

root= lxml.html.fromstring(html)

projstack = [] # array for the project

for tr in root.cssselect("div#maincontent table tr")[:]: #go to every <tr> in the table, in order to delimit the number of row by 20, use [:20]
    if tr[0].tag == 'th': #forget the header
        continue
    #print lxml.html.tostring(tr) 
    div = tr[0][0] # think of a tree, you take the first element of <tr>, which is a <td> and the first element within <td> which is <div> 
    assert div.tag == 'div' 
    padding = div.attrib.get('style') #get information inside div, which is the number of pixels, e.g., padding-left:30px
    
    data = {} # define a hashmap
    mpadding = re.match('padding-left:(\d+)px$', padding) #use regex to get the number of pixels in order to determine the project type
    assert mpadding, padding
    data['padding'] = int(mpadding.group(1)) #save the value as integer in data, take the first element of the group because this is the desired value
    a = div[-1]  # last element of list
    data['name'] = a.text.strip() #get the name and delete the spaces around it

    while projstack and projstack[-1][0] >= data['padding']: #as long as the padding value is 
        del projstack[-1] 
    projstack.append([data['padding'], data['name']])

    data['url'] = urlparse.urljoin(url, a.attrib.get('href')) # save the url of the project in data
    #print data
    cols = ['Phase', 'Home', 'Forum', 'Ma', 'Wiki', 'IP'] #define col names
    for i in range(6):
        if list(tr[i+1]):
            src = tr[i+1][0][0].attrib.get('src')
            msrc = re.match('.*/images/(.*?)\.(?:gif|jpg)$', src) # skip the path the the image name, just keep the file name
            assert msrc, [src]
            data[cols[i]] = msrc.group(1) #take the first entry of the regex
    if len(projstack) >= 2:
        data['topproj'] = projstack[0][1] 
    data['fullname'] = '|'.join([e[1]  for e in projstack ])
    scraperwiki.sqlite.save(['fullname'], data) # save the data in sqlite
import urllib
import lxml.html
import re
import urlparse
import scraperwiki

url = "http://www.eclipse.org/projects/listofprojects.php"

html = urllib.urlopen(url).read()
#print html   

root= lxml.html.fromstring(html)

projstack = [] # array for the project

for tr in root.cssselect("div#maincontent table tr")[:]: #go to every <tr> in the table, in order to delimit the number of row by 20, use [:20]
    if tr[0].tag == 'th': #forget the header
        continue
    #print lxml.html.tostring(tr) 
    div = tr[0][0] # think of a tree, you take the first element of <tr>, which is a <td> and the first element within <td> which is <div> 
    assert div.tag == 'div' 
    padding = div.attrib.get('style') #get information inside div, which is the number of pixels, e.g., padding-left:30px
    
    data = {} # define a hashmap
    mpadding = re.match('padding-left:(\d+)px$', padding) #use regex to get the number of pixels in order to determine the project type
    assert mpadding, padding
    data['padding'] = int(mpadding.group(1)) #save the value as integer in data, take the first element of the group because this is the desired value
    a = div[-1]  # last element of list
    data['name'] = a.text.strip() #get the name and delete the spaces around it

    while projstack and projstack[-1][0] >= data['padding']: #as long as the padding value is 
        del projstack[-1] 
    projstack.append([data['padding'], data['name']])

    data['url'] = urlparse.urljoin(url, a.attrib.get('href')) # save the url of the project in data
    #print data
    cols = ['Phase', 'Home', 'Forum', 'Ma', 'Wiki', 'IP'] #define col names
    for i in range(6):
        if list(tr[i+1]):
            src = tr[i+1][0][0].attrib.get('src')
            msrc = re.match('.*/images/(.*?)\.(?:gif|jpg)$', src) # skip the path the the image name, just keep the file name
            assert msrc, [src]
            data[cols[i]] = msrc.group(1) #take the first entry of the regex
    if len(projstack) >= 2:
        data['topproj'] = projstack[0][1] 
    data['fullname'] = '|'.join([e[1]  for e in projstack ])
    scraperwiki.sqlite.save(['fullname'], data) # save the data in sqlite
