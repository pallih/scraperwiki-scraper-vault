import resource
import scraperwiki
import lxml.html
import sys
import re

baseURL = "http://www.chictopia.com"
#Los Angeles / Women-Only
#http://www.chictopia.com/browse/people?g=1&l=5
url = baseURL + "/browse/people?g=1&l=5"

while True:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for post in root.cssselect(".action_photo.large .info_overlay"): 
        infoBox = post.cssselect("div")[2]

        _user = infoBox.cssselect("a")[0]
        userName = _user.text_content()
        userURL = baseURL + _user.attrib.get('href')

        # Visit User Profile Page
        print "Visiting user profile: " + userURL
        _html = scraperwiki.scrape(userURL)
        _root = lxml.html.fromstring(_html)

        friends = _root.cssselect("#bodywrapper .stats")[0].text_content()
        following = _root.cssselect("#bodywrapper .stats")[1].text_content()
        followers = _root.cssselect("#bodywrapper .stats")[2].text_content()

        city = _root.cssselect("#bodywrapper div div > .left > .px11 a")[0].get('alt')

        urlTwitter = False
        urlFacebook = False
        urlInstagram = False
        urlTumblr = False
        urlWebsite = False
        statsTweets = False
        statsFollowing = False 
        statsFollowers = False

        for _link in _root.cssselect("#bodywrapper div div > .left > .px11 > div a"):
            link = _link.get("href")

            if(link.find("twitter.com") > 0):
                urlTwitter = link 
                #htmlTwitter = scraperwiki.scrape(urlTwitter)
                #rootTwitter = lxml.html.fromstring(htmlTwitter)
                #userStats = rootTwitter.cssselect(".js-mini-profile-stats")
                #if len(userStats) > 0:
                    #statsTweets = rootTwitter.cssselect("a[data-element-term=tweet_stats] strong")[0].text_content()
                    #statsFollowing = rootTwitter.cssselect("a[data-element-term=following_stats] strong")[0].text_content()
                    #statsFollowers = rootTwitter.cssselect("a[data-element-term=follower_stats] strong")[0].text_content()
            elif(link.find("facebook.com") > 0):
                urlFacebook = link 
            elif(link.find("instagram.com") > 0):
                urlInstagram = link 
            elif(link.find("tumblr.com") > 0):
                urlTumblr = link 
            else:
                urlWebsite = link      
        data = {
            'userName' : userName,
            'userURL' : userURL,
            'friends' : re.sub("\D", "", friends.strip()),
            'followers' : re.sub("\D", "", followers.strip()),
            'following' : re.sub("\D", "", following.strip()),
            'city' : city,
            'twitter' : urlTwitter,
            'twitterTweets' : statsTweets,
            'twitterFollowers' : statsFollowers,
            'twitterFollowing' : statsFollowing,
            'facebook' : urlFacebook,
            'instagram' : urlInstagram,
            'website' : urlWebsite,
            'tumblr' : urlTumblr
        }
        scraperwiki.sqlite.save(unique_keys=[], data=data)

    url = baseURL + root.cssselect(".next_page_browse a")[0].attrib.get('href')
    print "-- Visiting URL: " + urlimport resource
import scraperwiki
import lxml.html
import sys
import re

baseURL = "http://www.chictopia.com"
#Los Angeles / Women-Only
#http://www.chictopia.com/browse/people?g=1&l=5
url = baseURL + "/browse/people?g=1&l=5"

while True:
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for post in root.cssselect(".action_photo.large .info_overlay"): 
        infoBox = post.cssselect("div")[2]

        _user = infoBox.cssselect("a")[0]
        userName = _user.text_content()
        userURL = baseURL + _user.attrib.get('href')

        # Visit User Profile Page
        print "Visiting user profile: " + userURL
        _html = scraperwiki.scrape(userURL)
        _root = lxml.html.fromstring(_html)

        friends = _root.cssselect("#bodywrapper .stats")[0].text_content()
        following = _root.cssselect("#bodywrapper .stats")[1].text_content()
        followers = _root.cssselect("#bodywrapper .stats")[2].text_content()

        city = _root.cssselect("#bodywrapper div div > .left > .px11 a")[0].get('alt')

        urlTwitter = False
        urlFacebook = False
        urlInstagram = False
        urlTumblr = False
        urlWebsite = False
        statsTweets = False
        statsFollowing = False 
        statsFollowers = False

        for _link in _root.cssselect("#bodywrapper div div > .left > .px11 > div a"):
            link = _link.get("href")

            if(link.find("twitter.com") > 0):
                urlTwitter = link 
                #htmlTwitter = scraperwiki.scrape(urlTwitter)
                #rootTwitter = lxml.html.fromstring(htmlTwitter)
                #userStats = rootTwitter.cssselect(".js-mini-profile-stats")
                #if len(userStats) > 0:
                    #statsTweets = rootTwitter.cssselect("a[data-element-term=tweet_stats] strong")[0].text_content()
                    #statsFollowing = rootTwitter.cssselect("a[data-element-term=following_stats] strong")[0].text_content()
                    #statsFollowers = rootTwitter.cssselect("a[data-element-term=follower_stats] strong")[0].text_content()
            elif(link.find("facebook.com") > 0):
                urlFacebook = link 
            elif(link.find("instagram.com") > 0):
                urlInstagram = link 
            elif(link.find("tumblr.com") > 0):
                urlTumblr = link 
            else:
                urlWebsite = link      
        data = {
            'userName' : userName,
            'userURL' : userURL,
            'friends' : re.sub("\D", "", friends.strip()),
            'followers' : re.sub("\D", "", followers.strip()),
            'following' : re.sub("\D", "", following.strip()),
            'city' : city,
            'twitter' : urlTwitter,
            'twitterTweets' : statsTweets,
            'twitterFollowers' : statsFollowers,
            'twitterFollowing' : statsFollowing,
            'facebook' : urlFacebook,
            'instagram' : urlInstagram,
            'website' : urlWebsite,
            'tumblr' : urlTumblr
        }
        scraperwiki.sqlite.save(unique_keys=[], data=data)

    url = baseURL + root.cssselect(".next_page_browse a")[0].attrib.get('href')
    print "-- Visiting URL: " + url