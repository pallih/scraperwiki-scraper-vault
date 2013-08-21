import scraperwiki
import lxml.html
import string
import unicodedata

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

# data variables
bio = None
type1 = None
type2 = None

base_url = 'http://serebii.net/pokedex/'
ext = '.shtml'

data = dict();

for i in [j+1 for j in range(151)]:
    pokeNum = str(i)
    while(len(pokeNum)<3):
        pokeNum = "0" + pokeNum;
    
    html = scraperwiki.scrape(base_url+str(pokeNum)+ext)
    root = lxml.html.fromstring(html)
    
    # get the bio text
    bioEl = root.cssselect("tr td[colspan=5] font[color=FF0000]")
    if(len(bioEl)):
        bioEl = bioEl[1]       
        bio = string.strip(strip_accents(unicode(bioEl.text)))
    
    # get the type(s)
    type1El = None
    type2El = None
    headings = root.cssselect("b");
    parents = []
    for heading in headings:
        parents.append(heading.getparent())

    if(i<69):   
        for j,el in enumerate(headings):
            if(el.text == "Type 1:"):
                type1El = parents[j].cssselect("div>img")
            elif(el.text == "Type 2:"):
                type2El = parents[j].cssselect("div>img")
        
        if(type1El is not None and len(type1El)):
            type1 = string.strip(strip_accents(unicode(string.split(string.split(type1El[0].attrib['src'],'/')[-1],'.')[0])))
        else:
            type1 = None
        
        if(type2El is not None and len(type2El)):
            type2 = string.strip(strip_accents(unicode(string.split(string.split(type2El[0].attrib['src'],'/')[-1],'.')[0])))
        else:
            type2 = None
    else:
        for j,el in enumerate(headings):
            if(el.text == "Type 1:"):
                type1El = parents[j].cssselect("p")
                if(len(type1El) > 0 and len(type1El[0].getchildren())):
                    type1El = type1El[0].getchildren()
            elif(el.text == "Type 2:"):
                type2El = parents[j].cssselect("p")
                if(len(type2El) > 0 and len(type2El[0].getchildren())):
                    type2El = type2El[0].getchildren()

        
        if(type1El is not None and len(type1El)):
            type1 = string.strip(strip_accents(unicode(type1El[0].text)))
        else:
            type1 = None
        
        if(type2El is not None and len(type2El)):
            type2 = string.strip(strip_accents(unicode(type2El[0].text)))
        else:
            type2 = None

        if(type2 == "N/A"):
            type2 = None
        

    data['pokeNum'] = pokeNum
    data['bio'] = bio
    data['type1'] = type1
    data['type2'] = type2
    scraperwiki.sqlite.save(unique_keys=['pokeNum'],data=data)

for pokeNum,key in enumerate(data):
    print "%i: %s" % (pokeNum,data[key])