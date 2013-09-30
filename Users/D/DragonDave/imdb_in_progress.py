# Blank Python
url='http://www.imdb.com/name/nm1476707/' # dizzee rascal

import scraperwiki, re
import BeautifulSoup

# http://stackoverflow.com/questions/4995116/only-extracting-text-from-this-element-not-its-children

html = scraperwiki.scrape(url)
print html

soup = BeautifulSoup.BeautifulSoup(html)

# performances - a list of all performances the star has been in.
performances = soup.findAll("div", { "class" : re.compile("filmo-row .*") })
db=[]
for item in performances:
    data={}
    data['year']=item.find("span", {"class":"year_column"}).text
    data['url']=item.find("a")['href']
    data['name']=item.find("a").text
    # not all entries have episodes associated with them. (TODO there can be multiple episodes)
    try:
        data['episodeurl']=item.find("div", {"class":"filmo-episodes"}).find('a')['href']
        data['episodename']=item.find("div", {"class":"filmo-episodes"}).find('a').text
    except AttributeError:
        pass
    db.append(data)
# print len(performances)

# perfcat - categories for performances (with numbers)
perfcat=soup.findAll("div", {"class": "head"})
pos=0
for item in perfcat:
    catname=item['id'].split('-')[-1]
    catsize=int(item.find(text=re.compile("\(.* title.*\)"))[2:].split(" ")[0])
    for dbitem in range(pos,pos+catsize):
        db[dbitem]['category']=catname
    pos=pos+catsize

# save to store
for item in db:
    scraperwiki.datastore.save(unique_keys=['url'], data=item)

# Blank Python
url='http://www.imdb.com/name/nm1476707/' # dizzee rascal

import scraperwiki, re
import BeautifulSoup

# http://stackoverflow.com/questions/4995116/only-extracting-text-from-this-element-not-its-children

html = scraperwiki.scrape(url)
print html

soup = BeautifulSoup.BeautifulSoup(html)

# performances - a list of all performances the star has been in.
performances = soup.findAll("div", { "class" : re.compile("filmo-row .*") })
db=[]
for item in performances:
    data={}
    data['year']=item.find("span", {"class":"year_column"}).text
    data['url']=item.find("a")['href']
    data['name']=item.find("a").text
    # not all entries have episodes associated with them. (TODO there can be multiple episodes)
    try:
        data['episodeurl']=item.find("div", {"class":"filmo-episodes"}).find('a')['href']
        data['episodename']=item.find("div", {"class":"filmo-episodes"}).find('a').text
    except AttributeError:
        pass
    db.append(data)
# print len(performances)

# perfcat - categories for performances (with numbers)
perfcat=soup.findAll("div", {"class": "head"})
pos=0
for item in perfcat:
    catname=item['id'].split('-')[-1]
    catsize=int(item.find(text=re.compile("\(.* title.*\)"))[2:].split(" ")[0])
    for dbitem in range(pos,pos+catsize):
        db[dbitem]['category']=catname
    pos=pos+catsize

# save to store
for item in db:
    scraperwiki.datastore.save(unique_keys=['url'], data=item)

