print "Hello world"
import urllib
import urlparse
import re
import scraperwiki
scraperwiki.cache(True)
    #http://www.merseyside.police.uk/index.aspx?articleid=1304
districtpolice = {"aigburth-mossley-hill": [1304,],
     "allerton": [1342],
     "anfield-walton": [1041,],
     "childwall-netherley": [1302,],
     "croxteth-fazakerley": [1110, 1105],
     "halewood": [686],
     "huyton-prescot": [624, 625, 626, 627, 654, 655, 656, 657, 684],
     "kirkby": [580, 581, 582, 601, 602, 603],
     "speke-garston": [1370, 1371],
     "st-helens": [716, 725, 726, 727, 770, 774, 775, 815, 816, 817, 818, 851, 852, 854, 856],
     "toxteth-wavertree": [1227],
     "west-derby-tuebrook": [1112, 1072],
     "woolton": [1341]}

for district in districtpolice:
    print "***", district
    for number in districtpolice[district]:
        html = urllib.urlopen("http://www.merseyside.police.uk/index.aspx?articleid=%d"%number).read()
        mlocalofficers = re.search('<a href="(http://www.merseyside.police.uk/index.aspx\?articleid=\d+)"\s*class="heading"\s*title="Local officers">', html)
        localoffurl = mlocalofficers.group(1)
        localoffhtml = urllib.urlopen(localoffurl).read()
          
        plodlist = re.findall('(?s)<li>\s*<a class="img" href="(http://www.merseyside.police.uk/index.aspx\?.*?)" title="(.*?)">(.*?)<strong class="contactdetail">(.*?)</strong>', localoffhtml)
        for plodlink, plodtitle, plodimg, plodcontact in plodlist:
            plodpic = re.findall('src="(.*?)"', plodimg)
            plodimglink = ""
            if plodpic:
                plodimglink = urlparse.urljoin(localoffurl, plodpic[0])
            print plodcontact, plodimglink 
            plodlink = re.sub("&amp;", "&", plodlink); 
            scraperwiki.datastore.save(unique_keys=["contact", "district"], data={"district":district, "contact":plodcontact, "img":plodimglink, "plodlink":plodlink})
            

print "Hello world"
import urllib
import urlparse
import re
import scraperwiki
scraperwiki.cache(True)
    #http://www.merseyside.police.uk/index.aspx?articleid=1304
districtpolice = {"aigburth-mossley-hill": [1304,],
     "allerton": [1342],
     "anfield-walton": [1041,],
     "childwall-netherley": [1302,],
     "croxteth-fazakerley": [1110, 1105],
     "halewood": [686],
     "huyton-prescot": [624, 625, 626, 627, 654, 655, 656, 657, 684],
     "kirkby": [580, 581, 582, 601, 602, 603],
     "speke-garston": [1370, 1371],
     "st-helens": [716, 725, 726, 727, 770, 774, 775, 815, 816, 817, 818, 851, 852, 854, 856],
     "toxteth-wavertree": [1227],
     "west-derby-tuebrook": [1112, 1072],
     "woolton": [1341]}

for district in districtpolice:
    print "***", district
    for number in districtpolice[district]:
        html = urllib.urlopen("http://www.merseyside.police.uk/index.aspx?articleid=%d"%number).read()
        mlocalofficers = re.search('<a href="(http://www.merseyside.police.uk/index.aspx\?articleid=\d+)"\s*class="heading"\s*title="Local officers">', html)
        localoffurl = mlocalofficers.group(1)
        localoffhtml = urllib.urlopen(localoffurl).read()
          
        plodlist = re.findall('(?s)<li>\s*<a class="img" href="(http://www.merseyside.police.uk/index.aspx\?.*?)" title="(.*?)">(.*?)<strong class="contactdetail">(.*?)</strong>', localoffhtml)
        for plodlink, plodtitle, plodimg, plodcontact in plodlist:
            plodpic = re.findall('src="(.*?)"', plodimg)
            plodimglink = ""
            if plodpic:
                plodimglink = urlparse.urljoin(localoffurl, plodpic[0])
            print plodcontact, plodimglink 
            plodlink = re.sub("&amp;", "&", plodlink); 
            scraperwiki.datastore.save(unique_keys=["contact", "district"], data={"district":district, "contact":plodcontact, "img":plodimglink, "plodlink":plodlink})
            

