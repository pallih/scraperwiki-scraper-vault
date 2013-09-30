import scraperwiki
import sys
from bs4 import BeautifulSoup
#searches = ["http://www.cheapbeachbikes.com/product/700-1130_Firmstrong-Urban-20%22-Beach-Cruiser-Girl"]
searches = ["http://www.cheapbeachbikes.com/product/700-1130_Firmstrong-Urban-20%22-Beach-Cruiser-Girl","http://www.cheapbeachbikes.com/product/700-1120_Firmstrong-Urban-20%22-Beach-Cruiser-Boy","http://www.cheapbeachbikes.com/product/700-1080-0_Firmstrong-Urban-Boutique-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1200_Firmstrong-Bella-Classic-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1445_Firmstrong-Diva-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-2000-1-0-0_Firmstrong-Comfort-21-spd-26%22-Mountain-Bike-Unisex","http://www.cheapbeachbikes.com/product/700-1010_Firmstrong-Urban-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1080_Firmstrong-Urban-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-2020_Firmstrong-Urban-Alloy-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-2020-0_Firmstrong-Urban-Alloy-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1078-0_Firmstrong-Bruiser-Prestige-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1077_Firmstrong-Urban-LRD-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1200-1_Firmstrong-Bella-Fashionista-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1100_Firmstrong-Urban-Jr--24%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1103_Firmstrong-Urban-Jr-24%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1010-0_Firmstrong-Urban-Limited-26%22-w/-Shimano-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1010-0-0_Firmstrong-Urban-26%22-w/-Shimano-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-2000-1-0-1-0_Firmstrong-Traveler-18-spd-26%22-Mountain-Bike-Lady","http://www.cheapbeachbikes.com/product/700-2000-1-0-1_Firmstrong-Traveler-18-spd-26%22-Mountain-Bike-Man","http://www.cheapbeachbikes.com/product/700-2000_Firmstrong-Chief-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-2000-0_Firmstrong-Chief-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1060_Firmstrong-Urban-7-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1065_Firmstrong-Urban-7-spd-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1447_Firmstrong-CA520-7-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-2000-1_Firmstrong-Chief-26%22-3-spd-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1110_Firmstrong-Urban-Nexus-3-spd-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1115_Firmstrong-Urban-Nexus-3-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1200-0_Firmstrong-Bella-Nexus-3-spd-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1100-0_Firmstrong-Urban-Nexus-3-spd-Jr--24%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1040_Firmstrong-Urban-Delux-Stretch-Cruiser","http://www.cheapbeachbikes.com/product/700-1446_Firmstrong-Rebel-Stretch-Cruiser","http://www.cheapbeachbikes.com/product/700-1448_Firmstrong-Bruiser-Prestige-7-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1450_Firmstrong-Bella-Fashionista-7-spd-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-4000_20-21-Speed-Mountain-Bikes","http://www.cheapbeachbikes.com/product/700-5000_20-Single-Speed-Beach-Cruisers","http://www.cheapbeachbikes.com/product/700-5307-1212_20-Bruiser-Bikes---HOT-NEW-CRUISER-BIKE","http://www.cheapbeachbikes.com/product/700-5300_20-3-Speed-Nexus-Beach-Cruisers","http://www.cheapbeachbikes.com/product/BCT-709i-10_10-Tandems---7-Speed-Independent-Pedaling","http://www.cheapbeachbikes.com/product/700-5001_20-Single-Speed-Beach-Cruisers-w/-Accessories-Pkg","http://www.cheapbeachbikes.com/product/700-5301_20-3-Speed-Beach-Cruisers-w/-Accessories-Pkg","http://www.cheapbeachbikes.com/product/700-6000_100-Single-Speed-Beach-Cruisers-w/-Accessories-Pkg","http://www.cheapbeachbikes.com/product/700-1120-609268182_20-Kids-Bikes---Single-Speed-20%22-Beach-Cruisers"]


for search in searches:
    try:
        html = scraperwiki.scrape(search)
    except scraperwiki.CPUTimeExceededError:
        print "CPU exception caught"
    except:
        print "Error, unexpected exception"
    soup = BeautifulSoup(html)
    #print soup
    maindiv = soup.find_all('td',{"class":"centercontainer"})
    #print maindiv
    if maindiv:
        pr = maindiv[0].find('span', {"class":"priceparts"}).text
    if pr:
        print pr
        data = {}
        data['URL'] = search
        data['price'] = pr
        scraperwiki.sqlite.save(unique_keys=["URL"], data={"URL":search, "price":pr}) 
    else:
        print 'nodata'
        data = {}
        data['URL'] = search
        data['price'] = 'nodata'
        scraperwiki.sqlite.save(data={"URL":search, "price":pr}) #unique_keys=["URL"],        

print scraperwiki.sqlite.show_tables()

#for link in pr:
        #url = link["href"]
#        print link
        #data = {"URL":url}
        #scraperwiki.sqlite.save(["URL"], data)
import scraperwiki
import sys
from bs4 import BeautifulSoup
#searches = ["http://www.cheapbeachbikes.com/product/700-1130_Firmstrong-Urban-20%22-Beach-Cruiser-Girl"]
searches = ["http://www.cheapbeachbikes.com/product/700-1130_Firmstrong-Urban-20%22-Beach-Cruiser-Girl","http://www.cheapbeachbikes.com/product/700-1120_Firmstrong-Urban-20%22-Beach-Cruiser-Boy","http://www.cheapbeachbikes.com/product/700-1080-0_Firmstrong-Urban-Boutique-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1200_Firmstrong-Bella-Classic-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1445_Firmstrong-Diva-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-2000-1-0-0_Firmstrong-Comfort-21-spd-26%22-Mountain-Bike-Unisex","http://www.cheapbeachbikes.com/product/700-1010_Firmstrong-Urban-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1080_Firmstrong-Urban-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-2020_Firmstrong-Urban-Alloy-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-2020-0_Firmstrong-Urban-Alloy-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1078-0_Firmstrong-Bruiser-Prestige-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1077_Firmstrong-Urban-LRD-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1200-1_Firmstrong-Bella-Fashionista-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1100_Firmstrong-Urban-Jr--24%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1103_Firmstrong-Urban-Jr-24%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1010-0_Firmstrong-Urban-Limited-26%22-w/-Shimano-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1010-0-0_Firmstrong-Urban-26%22-w/-Shimano-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-2000-1-0-1-0_Firmstrong-Traveler-18-spd-26%22-Mountain-Bike-Lady","http://www.cheapbeachbikes.com/product/700-2000-1-0-1_Firmstrong-Traveler-18-spd-26%22-Mountain-Bike-Man","http://www.cheapbeachbikes.com/product/700-2000_Firmstrong-Chief-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-2000-0_Firmstrong-Chief-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1060_Firmstrong-Urban-7-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1065_Firmstrong-Urban-7-spd-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1447_Firmstrong-CA520-7-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-2000-1_Firmstrong-Chief-26%22-3-spd-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1110_Firmstrong-Urban-Nexus-3-spd-26%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1115_Firmstrong-Urban-Nexus-3-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1200-0_Firmstrong-Bella-Nexus-3-spd-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1100-0_Firmstrong-Urban-Nexus-3-spd-Jr--24%22-Beach-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-1040_Firmstrong-Urban-Delux-Stretch-Cruiser","http://www.cheapbeachbikes.com/product/700-1446_Firmstrong-Rebel-Stretch-Cruiser","http://www.cheapbeachbikes.com/product/700-1448_Firmstrong-Bruiser-Prestige-7-spd-26%22-Beach-Cruiser-Man","http://www.cheapbeachbikes.com/product/700-1450_Firmstrong-Bella-Fashionista-7-spd-26%22-Cruiser-Lady","http://www.cheapbeachbikes.com/product/700-4000_20-21-Speed-Mountain-Bikes","http://www.cheapbeachbikes.com/product/700-5000_20-Single-Speed-Beach-Cruisers","http://www.cheapbeachbikes.com/product/700-5307-1212_20-Bruiser-Bikes---HOT-NEW-CRUISER-BIKE","http://www.cheapbeachbikes.com/product/700-5300_20-3-Speed-Nexus-Beach-Cruisers","http://www.cheapbeachbikes.com/product/BCT-709i-10_10-Tandems---7-Speed-Independent-Pedaling","http://www.cheapbeachbikes.com/product/700-5001_20-Single-Speed-Beach-Cruisers-w/-Accessories-Pkg","http://www.cheapbeachbikes.com/product/700-5301_20-3-Speed-Beach-Cruisers-w/-Accessories-Pkg","http://www.cheapbeachbikes.com/product/700-6000_100-Single-Speed-Beach-Cruisers-w/-Accessories-Pkg","http://www.cheapbeachbikes.com/product/700-1120-609268182_20-Kids-Bikes---Single-Speed-20%22-Beach-Cruisers"]


for search in searches:
    try:
        html = scraperwiki.scrape(search)
    except scraperwiki.CPUTimeExceededError:
        print "CPU exception caught"
    except:
        print "Error, unexpected exception"
    soup = BeautifulSoup(html)
    #print soup
    maindiv = soup.find_all('td',{"class":"centercontainer"})
    #print maindiv
    if maindiv:
        pr = maindiv[0].find('span', {"class":"priceparts"}).text
    if pr:
        print pr
        data = {}
        data['URL'] = search
        data['price'] = pr
        scraperwiki.sqlite.save(unique_keys=["URL"], data={"URL":search, "price":pr}) 
    else:
        print 'nodata'
        data = {}
        data['URL'] = search
        data['price'] = 'nodata'
        scraperwiki.sqlite.save(data={"URL":search, "price":pr}) #unique_keys=["URL"],        

print scraperwiki.sqlite.show_tables()

#for link in pr:
        #url = link["href"]
#        print link
        #data = {"URL":url}
        #scraperwiki.sqlite.save(["URL"], data)
