import scraperwiki
import lxml.html

output = []
url=''
record = {}
def uniq(input):
     if input not in output:
        output.append(input)
          
def unique(my_list): 
    return [x for x in my_list if x not in locals()]

UniqList={}
i=0

html=scraperwiki.scrape("http://stoganews.com/")
root=lxml.html.fromstring(html)
divs=root.cssselect("div [class=featuredPost] a")

for div in divs:
     url=div.attrib['href'] 
     url=url.replace("#respond","") 
     uniq(url)

for aurl in output:
    html1=scraperwiki.scrape(aurl)
    root1=lxml.html.fromstring(html1)
    ndvis=root1.cssselect('img')
    for ndiv in ndvis:
        if ".jpg" not in ndiv.attrib["src"]:
            continue
       
        imagename=aurl
        imagename=imagename.replace('http://stoganews.com/','')
        imagename=imagename.replace('/','_')
       
        record["url"] = ndiv.attrib["src"]
        record["ImageName"]=imagename
        scraperwiki.sqlite.save(["url"],record)
        print ndiv.attrib["src"]

