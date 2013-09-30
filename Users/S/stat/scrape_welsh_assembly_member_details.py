# Blank Python

import scraperwiki
import lxml.html
root = lxml.html.parse("http://www.assemblywales.org/memhome/mem-profile.htm").getroot()
nodes=root.cssselect('.box_border_width')

newdataattempt = { "memberName":"Leighton Andrews", "memberURL":"http://www.assemblywales.org/memhome/mem-previous-members/mem-profile/mem-rhondda.htm", "memberImageURL":"http://www.assemblywales.org/memhome/leighton_andrews_.jpg", "constituency":"Rhondda", "politicalParty":"Labour" }
scraperwiki.sqlite.save(unique_keys=["memberName", "memberURL"], data=newdataattempt)

#print lxml.html.tostring(root)
#print root.cssselect(".title_area")
for node in nodes:
    print ''
    #print lxml.html.tostring(node)
    name=node.cssselect('h3')[0].text
  #  print "'memberName': '" + name + "'"
    a=node.cssselect('a')[0]
    child = a.attrib.get('href')
   # print child
    #print "'memberURL': '" + a.attrib.get('href') + "'"
    i=node.cssselect('img')[0]
    image=i.attrib.get('src')
    print image
    #image=image.rstrip('-_profile.jpg')
  #  print "'memberImageURL': 'http://www.assemblywales.org/memhome/" + image# + "_.jpg'"
    smallMemberImage = 'http://www.assemblywales.org/memhome/' + image
# + '_.jpg'
    
    childPage = lxml.html.parse(child).getroot()
    childPageS = childPage.cssselect('.box_txt')
    #print childPageS
    for childPager in childPageS:
        #print lxml.html.tostring(childPager)
        if (childPager.cssselect('h1')):
            constituency=childPager.cssselect('h1')[0].text
           # print "'constituency': '" + constituency + "'"        
        if (childPager.cssselect('h2')):
            party = childPager.cssselect('h2')[0].text
            if (party!='Personal Website'):
                politicalParty = "'politicalParty': '" + party + "'"
                #if (politicalParty != "'politicalParty': 'Video Biography'"):
                  #  print politicalParty

    wagData = { "memberName": name.strip(),
            "memberURL": child,
            "smallMemberImageURL": smallMemberImage,
            "constituency": constituency,
            "politicalParty": party }

    scraperwiki.sqlite.save(unique_keys=['memberName', 'memberURL'], data=wagData)

# Blank Python

import scraperwiki
import lxml.html
root = lxml.html.parse("http://www.assemblywales.org/memhome/mem-profile.htm").getroot()
nodes=root.cssselect('.box_border_width')

newdataattempt = { "memberName":"Leighton Andrews", "memberURL":"http://www.assemblywales.org/memhome/mem-previous-members/mem-profile/mem-rhondda.htm", "memberImageURL":"http://www.assemblywales.org/memhome/leighton_andrews_.jpg", "constituency":"Rhondda", "politicalParty":"Labour" }
scraperwiki.sqlite.save(unique_keys=["memberName", "memberURL"], data=newdataattempt)

#print lxml.html.tostring(root)
#print root.cssselect(".title_area")
for node in nodes:
    print ''
    #print lxml.html.tostring(node)
    name=node.cssselect('h3')[0].text
  #  print "'memberName': '" + name + "'"
    a=node.cssselect('a')[0]
    child = a.attrib.get('href')
   # print child
    #print "'memberURL': '" + a.attrib.get('href') + "'"
    i=node.cssselect('img')[0]
    image=i.attrib.get('src')
    print image
    #image=image.rstrip('-_profile.jpg')
  #  print "'memberImageURL': 'http://www.assemblywales.org/memhome/" + image# + "_.jpg'"
    smallMemberImage = 'http://www.assemblywales.org/memhome/' + image
# + '_.jpg'
    
    childPage = lxml.html.parse(child).getroot()
    childPageS = childPage.cssselect('.box_txt')
    #print childPageS
    for childPager in childPageS:
        #print lxml.html.tostring(childPager)
        if (childPager.cssselect('h1')):
            constituency=childPager.cssselect('h1')[0].text
           # print "'constituency': '" + constituency + "'"        
        if (childPager.cssselect('h2')):
            party = childPager.cssselect('h2')[0].text
            if (party!='Personal Website'):
                politicalParty = "'politicalParty': '" + party + "'"
                #if (politicalParty != "'politicalParty': 'Video Biography'"):
                  #  print politicalParty

    wagData = { "memberName": name.strip(),
            "memberURL": child,
            "smallMemberImageURL": smallMemberImage,
            "constituency": constituency,
            "politicalParty": party }

    scraperwiki.sqlite.save(unique_keys=['memberName', 'memberURL'], data=wagData)

