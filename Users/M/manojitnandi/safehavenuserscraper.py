import scraperwiki
import mechanize
import urllib,urllib2
import sys, time, socket
from bs4 import BeautifulSoup
import cookielib

'''
- Login
- Click on http://gabrielle.safe-haven.com/members
- Collect members as links ( a, title ="View Profile")
- On profile page, (a, title = View Friends)
- Friends are (a class='ipsUserPhotoLink', href='<Member Profile>')
- Profile information (li class = 'clear clearfix')
- <Index>: <User>: <Friend> (Multi-way Key)
'''

#Browser
br = mechanize.Browser()

#Set up database
#con = mdb.connect('gladius','mnandi','sazandora','reu2012emotion', charset='utf8', use_unicode=True)

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

#Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0, add Headers
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
br.addheaders = [('User-agent', 'Suffolk REU')]

#Login to the website
url = 'http://gabrielle.self-injury.net/index.php?app=core&module=global&section=login'
response = br.open(url)

list_forms = [ form for form in br.forms() ]
br.select_form(nr=0)

br['ips_username'] = 'Researcher'
br['ips_password'] = 'research'

response = br.submit()

members_url = 'http://gabrielle.self-injury.net/members/'
response = br.open(members_url)

def getMoreProfiles(soup):
    getMore = soup.find('a', attrs={'rel':'next', 'title':' Next page'})
    if getMore is None:
        return None
    else:
        return getMore.get('href')

def getProfiles(response):
    soup = BeautifulSoup(response)
    results = soup.findAll('a', attrs = {'title':'View Profile', 'class': 'ipsUserPhotoLink left'})
    for result in results:
        profile_link = result.get('href')
        profile_link = profile_link.encode('ascii','ignore')
        print 'Examining %s' % (profile_link)
        response = br.open(profile_link)
        time.sleep(20)
        getFriends(response, profile_link)
    moreProfiles = getMoreProfiles(soup)
    if not moreProfiles is None:
        print moreProfiles
        response2 = br.open(moreProfiles)
        getProfiles(response2)

def formatProfileLink(profile_link):
    test = profile_link.rstrip('/')
    num = test.rfind('/')+1
    test = test[num:]
    num2 = test.find('-')
    return (test[:num2], test[num2+1:])

def storeData(output):
    with con:
        cur = con.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute("SET CHARACTER SET utf8")
        cur.execute("SET character_set_connection=utf8")
        cur.execute("CREATE TABLE IF NOT EXISTS SafeHavenMembers(INDEX INTEGER PRIMARY KEY, MemberID INTEGER, UserName TEXT, FriendID INTEGER, FriendName TEXT)")
        memberId = output['MemberID']
        memberName = '\"'+output['UserName']+'\"'
        friendId = output['FriendID']
        friendName = '\"'+output['FriendName']+'\"'
        sql_query = "INSERT INTO SafeHavenMember(MemberId, UserName, FriendID, FriendName) VALUES(%s,%s,%s,%s)" % (memberId,memberName,friendId,friendName)
        try:
            cur.execute(sql_query)
        except mdb.IntegrityError:
            pass

        cur.close()
    con.commit()

def getFriends(profile_page, profile_link):
    soup = BeautifulSoup(profile_page)
    friends = soup.find('div', attrs={'id':'friends_overview'})
    test = formatProfileLink(profile_link)
    if not friends is None:
        friends = friends.findAll('a', attrs={'ipsUserPhotoLink'})
        for friend in friends:
            friend_info = friend.get('href')
            friend_info = friend_info.encode('ascii','ignore')
            friend_info = formatProfileLink(friend_info)
            output = {'MemberID':test[0],'UserName':test[1],'FriendID':friend_info[0],'FriendName':friend_info[1]}
            #storeData(output)
            scraperwiki.sqlite.save(unqiue_keys = 


getProfiles(response)
   


import scraperwiki
import mechanize
import urllib,urllib2
import sys, time, socket
from bs4 import BeautifulSoup
import cookielib

'''
- Login
- Click on http://gabrielle.safe-haven.com/members
- Collect members as links ( a, title ="View Profile")
- On profile page, (a, title = View Friends)
- Friends are (a class='ipsUserPhotoLink', href='<Member Profile>')
- Profile information (li class = 'clear clearfix')
- <Index>: <User>: <Friend> (Multi-way Key)
'''

#Browser
br = mechanize.Browser()

#Set up database
#con = mdb.connect('gladius','mnandi','sazandora','reu2012emotion', charset='utf8', use_unicode=True)

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

#Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0, add Headers
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
br.addheaders = [('User-agent', 'Suffolk REU')]

#Login to the website
url = 'http://gabrielle.self-injury.net/index.php?app=core&module=global&section=login'
response = br.open(url)

list_forms = [ form for form in br.forms() ]
br.select_form(nr=0)

br['ips_username'] = 'Researcher'
br['ips_password'] = 'research'

response = br.submit()

members_url = 'http://gabrielle.self-injury.net/members/'
response = br.open(members_url)

def getMoreProfiles(soup):
    getMore = soup.find('a', attrs={'rel':'next', 'title':' Next page'})
    if getMore is None:
        return None
    else:
        return getMore.get('href')

def getProfiles(response):
    soup = BeautifulSoup(response)
    results = soup.findAll('a', attrs = {'title':'View Profile', 'class': 'ipsUserPhotoLink left'})
    for result in results:
        profile_link = result.get('href')
        profile_link = profile_link.encode('ascii','ignore')
        print 'Examining %s' % (profile_link)
        response = br.open(profile_link)
        time.sleep(20)
        getFriends(response, profile_link)
    moreProfiles = getMoreProfiles(soup)
    if not moreProfiles is None:
        print moreProfiles
        response2 = br.open(moreProfiles)
        getProfiles(response2)

def formatProfileLink(profile_link):
    test = profile_link.rstrip('/')
    num = test.rfind('/')+1
    test = test[num:]
    num2 = test.find('-')
    return (test[:num2], test[num2+1:])

def storeData(output):
    with con:
        cur = con.cursor()
        cur.execute("SET NAMES utf8")
        cur.execute("SET CHARACTER SET utf8")
        cur.execute("SET character_set_connection=utf8")
        cur.execute("CREATE TABLE IF NOT EXISTS SafeHavenMembers(INDEX INTEGER PRIMARY KEY, MemberID INTEGER, UserName TEXT, FriendID INTEGER, FriendName TEXT)")
        memberId = output['MemberID']
        memberName = '\"'+output['UserName']+'\"'
        friendId = output['FriendID']
        friendName = '\"'+output['FriendName']+'\"'
        sql_query = "INSERT INTO SafeHavenMember(MemberId, UserName, FriendID, FriendName) VALUES(%s,%s,%s,%s)" % (memberId,memberName,friendId,friendName)
        try:
            cur.execute(sql_query)
        except mdb.IntegrityError:
            pass

        cur.close()
    con.commit()

def getFriends(profile_page, profile_link):
    soup = BeautifulSoup(profile_page)
    friends = soup.find('div', attrs={'id':'friends_overview'})
    test = formatProfileLink(profile_link)
    if not friends is None:
        friends = friends.findAll('a', attrs={'ipsUserPhotoLink'})
        for friend in friends:
            friend_info = friend.get('href')
            friend_info = friend_info.encode('ascii','ignore')
            friend_info = formatProfileLink(friend_info)
            output = {'MemberID':test[0],'UserName':test[1],'FriendID':friend_info[0],'FriendName':friend_info[1]}
            #storeData(output)
            scraperwiki.sqlite.save(unqiue_keys = 


getProfiles(response)
   


