from scraperwiki.sqlite import attach,select,save,execute,commit
from json import loads
from urllib2 import urlopen
from lxml.html import fromstring,tostring

def copyUrlsDb():
  attach('scraperwiki_scraper_urls')
  save(['url'],select('url,0 as "scraped" from scraper_urls'),'urls')

def getUrls():
  urls=select('url from urls where `scraped`=0;')
  return [row['url'] for row in urls]

def getScraperSlug(url):
  if url[0:7]=="/views/":
    return url[7:-1]
  elif url[0:10]=="/scrapers/":
    return url[10:-1]
  else:
    raise ValueError

def getScraperOwners(scraper_slug):
  json=urlopen("https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name="+scraper_slug+"&version=-1&quietfields=code%7Crunevents%7Cdatasummary%7Chistory").read()
  d=loads(json)

  if 1!=len(d):
    print d
    raise ValueError

  return d[0]['userroles']['owner']

def getUsernames(nullcol="bio"):
  usernames=select('username from users where `%s` is null;' % nullcol)
  return [row['username'] for row in usernames]

def getUserProfile(username):
  s=urlopen("https://scraperwiki.com/profiles/%s/" % username).read()
  xml=fromstring(s)
  divs=xml.cssselect("#divContent div.profilebio")

  if len(divs)!=1:
    raise ValueError

  return tostring(divs[0])

def main():
  for url in getUrls():
    slug=getScraperSlug(url)
    try:
      owners=getScraperOwners(slug)
    except:
      save(['url'],{"url":url},'errors')
    else:
      for owner in owners:
        save(['username'],{"username":owner},'users')
    save(['url'],{"url":url,"scraped":True},'urls')

  print 'Add bio html'
  if "`bio` TEXT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `bio` TEXT;")

  for username in getUsernames("bio"):
    bio=getUserProfile(username)
    save(['username'],{"username":username,"bio":bio},'users')

  print 'Add biotext'
  if "`biotext` TEXT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `biotext` TEXT;")

  for username in getUsernames("biotext"):
    bio=select('`bio` FROM `users` WHERE `username`=?',[username])[0]["bio"]
    biotext=getBioText(bio)
    save(['username'],{"username":username,"bio":bio,"biotext":biotext},'users')

  print 'Add code roles'
  if "`owns` INT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `owns` INT;")
    execute("ALTER TABLE `users` ADD COLUMN `edits` INT;")

  for username in getUsernames("owns"):
    d=getCodeRoles(username)
    execute("UPDATE `users` SET owns=?,edits=? WHERE username=?",[d["owns"],d["edits"],username])
    commit()

  print 'Add title variation'
  if "`distinct_title_tokens_count` INT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `distinct_title_tokens_count` INT;")
    execute("ALTER TABLE `users` ADD COLUMN `title_tokens` TEXT;")

  for username in getUsernames("distinct_title_tokens_count"):
    json=getUserJSON(username)
    d=titleVariation(json)
    execute("""
      UPDATE `users` SET distinct_title_tokens_count=?,title_tokens_count=?,title_tokens=?
      WHERE username=?;
      """,[d["distinct_count"],d["total_count"],d["text"],username]
    )
    commit()



def getCodeRoles(username):
  user=getUserJSON(username)
  coderoles=user["coderoles"]
  d={}
  for listkey,countkey in (("owner","owns"),("editor","edits")):
    if listkey in coderoles:
      d[countkey]=len(coderoles[listkey])
    else:
      d[countkey]=0
  return d

def getUserJSON(username):
  json=urlopen("https://api.scraperwiki.com/api/1.0/scraper/getuserinfo?format=jsondict&username=%s"%username).read()
  d=loads(json)
  if len(d)!=1:
    raise ValueError
  else:
    return d[0]

def titleVariation(userjson):
  if 'owner' in userjson['coderoles']:
    tokens=reduce(lambda a,b:a+b.split('_'),userjson['coderoles']['owner'],[])
  else:
    tokens=[]
  distinct_tokens=set(tokens)
  return {
    "distinct_count":len(distinct_tokens)
  , "total_count":len(tokens)
  , "text":'_'.join(tokens)
  }

def getBioText(biohtml):
  xml=fromstring(biohtml)
  p=xml.cssselect('p:not(.emailers)')

  if len(p)!=1:
    raise ValueError

  elif p[0].text==None:
    return ""
  else:
    return p[0].text


#-------------------------------------


#json=getUserJSON('tlevine')
#print titleVariation(json)

main()


#Because there's no console
#copyUrlsDb()
#execute("ALTER TABLE `users` ADD COLUMN `distinct_title_tokens_count` INT;")
#execute("UPDATE `users` set distinct_title_tokens_count=title_tokens_count;")
#commit()from scraperwiki.sqlite import attach,select,save,execute,commit
from json import loads
from urllib2 import urlopen
from lxml.html import fromstring,tostring

def copyUrlsDb():
  attach('scraperwiki_scraper_urls')
  save(['url'],select('url,0 as "scraped" from scraper_urls'),'urls')

def getUrls():
  urls=select('url from urls where `scraped`=0;')
  return [row['url'] for row in urls]

def getScraperSlug(url):
  if url[0:7]=="/views/":
    return url[7:-1]
  elif url[0:10]=="/scrapers/":
    return url[10:-1]
  else:
    raise ValueError

def getScraperOwners(scraper_slug):
  json=urlopen("https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name="+scraper_slug+"&version=-1&quietfields=code%7Crunevents%7Cdatasummary%7Chistory").read()
  d=loads(json)

  if 1!=len(d):
    print d
    raise ValueError

  return d[0]['userroles']['owner']

def getUsernames(nullcol="bio"):
  usernames=select('username from users where `%s` is null;' % nullcol)
  return [row['username'] for row in usernames]

def getUserProfile(username):
  s=urlopen("https://scraperwiki.com/profiles/%s/" % username).read()
  xml=fromstring(s)
  divs=xml.cssselect("#divContent div.profilebio")

  if len(divs)!=1:
    raise ValueError

  return tostring(divs[0])

def main():
  for url in getUrls():
    slug=getScraperSlug(url)
    try:
      owners=getScraperOwners(slug)
    except:
      save(['url'],{"url":url},'errors')
    else:
      for owner in owners:
        save(['username'],{"username":owner},'users')
    save(['url'],{"url":url,"scraped":True},'urls')

  print 'Add bio html'
  if "`bio` TEXT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `bio` TEXT;")

  for username in getUsernames("bio"):
    bio=getUserProfile(username)
    save(['username'],{"username":username,"bio":bio},'users')

  print 'Add biotext'
  if "`biotext` TEXT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `biotext` TEXT;")

  for username in getUsernames("biotext"):
    bio=select('`bio` FROM `users` WHERE `username`=?',[username])[0]["bio"]
    biotext=getBioText(bio)
    save(['username'],{"username":username,"bio":bio,"biotext":biotext},'users')

  print 'Add code roles'
  if "`owns` INT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `owns` INT;")
    execute("ALTER TABLE `users` ADD COLUMN `edits` INT;")

  for username in getUsernames("owns"):
    d=getCodeRoles(username)
    execute("UPDATE `users` SET owns=?,edits=? WHERE username=?",[d["owns"],d["edits"],username])
    commit()

  print 'Add title variation'
  if "`distinct_title_tokens_count` INT" not in execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'users' AND type = 'table'")['data'][0][0]:
    execute("ALTER TABLE `users` ADD COLUMN `distinct_title_tokens_count` INT;")
    execute("ALTER TABLE `users` ADD COLUMN `title_tokens` TEXT;")

  for username in getUsernames("distinct_title_tokens_count"):
    json=getUserJSON(username)
    d=titleVariation(json)
    execute("""
      UPDATE `users` SET distinct_title_tokens_count=?,title_tokens_count=?,title_tokens=?
      WHERE username=?;
      """,[d["distinct_count"],d["total_count"],d["text"],username]
    )
    commit()



def getCodeRoles(username):
  user=getUserJSON(username)
  coderoles=user["coderoles"]
  d={}
  for listkey,countkey in (("owner","owns"),("editor","edits")):
    if listkey in coderoles:
      d[countkey]=len(coderoles[listkey])
    else:
      d[countkey]=0
  return d

def getUserJSON(username):
  json=urlopen("https://api.scraperwiki.com/api/1.0/scraper/getuserinfo?format=jsondict&username=%s"%username).read()
  d=loads(json)
  if len(d)!=1:
    raise ValueError
  else:
    return d[0]

def titleVariation(userjson):
  if 'owner' in userjson['coderoles']:
    tokens=reduce(lambda a,b:a+b.split('_'),userjson['coderoles']['owner'],[])
  else:
    tokens=[]
  distinct_tokens=set(tokens)
  return {
    "distinct_count":len(distinct_tokens)
  , "total_count":len(tokens)
  , "text":'_'.join(tokens)
  }

def getBioText(biohtml):
  xml=fromstring(biohtml)
  p=xml.cssselect('p:not(.emailers)')

  if len(p)!=1:
    raise ValueError

  elif p[0].text==None:
    return ""
  else:
    return p[0].text


#-------------------------------------


#json=getUserJSON('tlevine')
#print titleVariation(json)

main()


#Because there's no console
#copyUrlsDb()
#execute("ALTER TABLE `users` ADD COLUMN `distinct_title_tokens_count` INT;")
#execute("UPDATE `users` set distinct_title_tokens_count=title_tokens_count;")
#commit()