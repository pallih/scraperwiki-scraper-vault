"""""""""""""""""""""""""""""""""""""""""""""""""""
SCRAPE ATTEMPT 2: In: Query | Out: Monitor Database 
"""""""""""""""""""""""""""""""""""""""""""""""""""

import scraperwiki
import urlparse
import lxml.html
import re
import urllib2
from lxml.html import tostring


mapping = {'LCD1990SX-BK':'N82E16824002353',
'N194WA-BF':'N82E16824005214',
'LCD195WXM-BK':'N82E16824002371',
'AS191-BK':'N82E16824002496',
'AS191WM-BK':'N82E16824002497',
'VH198T':'N82E16824236072',
'E1920X':'N82E16824001382',
'HW-191APB':'N82E16824254023',
'P2050':'N82E16824001375',
'E2011H':'N82E16824260023',
'B2030':'N82E16824001383',
'2011x':'N82E16824176200',
'2010i':'N82E16824176157',
'W2040T-PN':'N82E16824005146',
'VH202T-P':'N82E16824236063',
'S201HLbd':'N82E16824009256',
'U2211H':'N82E16824260019',
'2211x':'N82E16824176199',
'EX2220X':'N82E16824001390',
'B2230':'N82E16824001385',
'U2211H':'N82E16824260019',
'VX2250wm-LED':'N82E16824116442',
'LE2201w':'N82E16824176115',
'F22':'N82E16824160051',
'E2360V-PN':'N82E16824005196',
'PX2370':'N82E16824001414',
'VH236H':'N82E16824236059',
'G235HAbd':'N82E16824009266',
'LP2475w':'N82E16824176104',
'U2410':'N82E16824260020',
'ZR24w':'N82E16824176165',
'2443BWT-TAA-1':'N82E16824001409',
'EA241WM-BK':'N82E16824002462',
'FX2490HD':'N82E16824001443',
'VH242H':'N82E16824236052',
'2511x':'N82E16824176194',
'HF-259HPB':'N82E16824262007',
'PA271W-BK':'N82E16824002543',
'DS-275W':'N82E16824185011',
'M2780D-PU':'N82E16824005194',
'E2750VR-SN':'N82E16824005203',
'2711x':'N82E16824176195',
'VE276Q':'N82E16824236091',
'P2770HD':'N82E16824001392',
'LCD3090WQXi-BK':'N82E16824002419',
'U3011':'N82E16824260028',
'ZR30w':'N82E16824176177',
'DS-305W':'N82E16824185012',
'XL2370-1':'N82E16824001380',
'E2243FW':'N82E16824160056',
'B2330HD':'N82E16824001424',
'EX231W-BK':'N82E16824002574',
'2311x':'N82E16824176198',
'BX2350':'N82E16824001420',
'H233Hbmid':'N82E16824009162'}

monitors = ['px2370','vh236h','u2410','fx2490hd','ve276q','p2770hd','u3011','zr30w','xl2370-1','e2243fw','b2330hd','bx2350','e231w-bk','2311x','h233hbmid','vp2365wb','p221w-bk','p2370hd-1']

other = ['PX2370','VH236H','U2410','FX2490HD','PA271W-BK','VE276Q','P2770HD','U3011','ZR30w','XL2370-1','E2243FW','B2330HD','EX231W-BK','2311x','BX2350','H233Hbmid','LCD1990SX-Bk','N194WA','195WXM-BK','AS191-BK','AS191WM-BK','VH198T','E1920X','HW-191APB','P2050','E2011H','B2030','2011x','2010i','W2040T-PN','VH202T-P','S201HLbd','U2211H','2211x','EX2220X','B2230','U2211H','VX2250wm-LED','LE2201w','F22','PX2370','VH236H','G235Habd','LP2475W','U2410','ZR24w','2443BWT','EA241WM-BK','FX2490HD','VH242H','2511x','HF-259HPB','PA271W','DS-275W','M2780D','E2750VR-SN','2711x','VE276Q','P2770HD','LCD3090WQXi-BK','U3011','ZR30w','DS-305W','xl2370','e2243fw','b2330hd','e231w','2310e','bx2350','h233h']

broken = ['W1934S','BX2050','x22LED','2233RZ','BX2250','2240S-PN''V223W','SP2309W','E2311H','E2340S-PN','2436Vw','iH254DPB','2509m','MC007LL/A','B273H','lp2275w','l997','e2350v','f2380','AW2310','U2711','lp3065','m237md']                    

no_data = []
i = 1

for monitor in monitors:

    # initialize record
    record = {}

    """""""""""""""
    Newegg Scrape
    """""""""""""""
    
    monitor = monitor.replace(" ","+")

    # search for product page
    search_result = 'http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&Order=BESTMATCH&Description=' + monitor
    
    # turn search page HTML into lxml object
    html = scraperwiki.scrape(search_result)
    root = lxml.html.fromstring(html)

    # get item number
    try:
        # if no direct product page
        if root.cssselect("h2.pageTitle")[0].text == 'Search Results': 
            # if no results found
            if root.cssselect("h3.alert"): 
                print "No result found for: " + monitor
                no_data.append(monitor)
                continue
            # if multiple results found
            else:  
                print 'Multiple results found for ' + monitor
                uls = root.cssselect('div[id="cellItem1"] ul')
                z = uls[1].cssselect("ul.featureList li")
                item_number = tostring(z[5])[19:34]
    # search yielded direct product page
    except: 
        print 'Found direct item page for ' + monitor
        item_number = root.cssselect("div.v660 em")
        item_number = item_number[0].text
    record['item'] = item_number
    
    
    # navigate to direct product page
    product_page = 'http://www.newegg.com/Product/Product.aspx?Item=' + item_number
    record['link'] = product_page

    # turn product page HTML into lxml object
    html = scraperwiki.scrape(product_page)
    root = lxml.html.fromstring(html)

    # TO-DO get price
    #root.cssselect("input[type='radio']")
       

    # get rating
    ratings = root.cssselect("div.objReviewSummary span.count")
    score = 0
    reviews = 0
    stars = 5
    for count in ratings:
        count = int(count.text.replace(',',''))
        score += count * stars
        reviews += count
        stars -= 1
    if reviews == 0:
        score = 0.0
    else:
        score = round(float(score) / float(reviews), 1)
    record['N_rating'] = score     # add new_egg rating to record
    record['N_reviews'] = reviews  # add new_egg reviews to record


    # Get specified tech specs
    techspecs = ['Model','Brand','Screen_Size','Recommended_Resolution','Viewing_Angle','Pixel_Pitch','Display_Colors','Brightness','Contrast_Ratio','Response_Time']

    dls = root.cssselect("div.Details_Content dl") # Get <dl> tags in class="Details_Content">
    for dl in dls:
        spec = dl[0].text
        spec = spec.replace('.','_')
        spec = spec.replace('+','_')
        spec = spec.replace(' ','_')
        value = dl[1].text
        if spec in techspecs:
            record[spec] = value # add tech spec to record

    """""""""
    CNET Scrape
    """""""""

    # search for product page
    search_result = 'http://reviews.cnet.com/1770-5_7-0.html?query=' + monitor + '&tag=srch&searchtype=products'
    html = scraperwiki.scrape(search_result)
    root = lxml.html.fromstring(html)

    editor_rating = root.cssselect("ul.data")
    if editor_rating:
        editor_rating = editor_rating[0].text[16:19]
        record['C_editor_rating'] = editor_rating

    user_rating = root.cssselect("div.userRate span")
    if user_rating:
        user_rating = user_rating[0].text
        record['C_user_rating'] = user_rating

    user_reviews = root.cssselect("div.userRate div")
    if user_reviews:
        user_reviews = user_reviews[0].text[7:8]
        record['C_user_reviews'] = user_reviews

    bottom_line = root.cssselect("div.resultSummaryCopy p")
    try:
        if bottom_line[0].cssselect("strong")[0].text == "CNET'S bottom line: ":
            text = tostring(bottom_line[0])
            end = text.index('.') + 1
            bottom_line = text[40:end]
            record['C_bottom_line'] = bottom_line
    except:
        pass


    print str(round(float(i) / float(len(monitors)) * 100,2)) + '% done'

    # insert price before
    #gridx + grid y

    record['id'] = i
    i += 1

    scraperwiki.sqlite.save(['Model'],record)



#Print monitors that were not found
print no_data"""""""""""""""""""""""""""""""""""""""""""""""""""
SCRAPE ATTEMPT 2: In: Query | Out: Monitor Database 
"""""""""""""""""""""""""""""""""""""""""""""""""""

import scraperwiki
import urlparse
import lxml.html
import re
import urllib2
from lxml.html import tostring


mapping = {'LCD1990SX-BK':'N82E16824002353',
'N194WA-BF':'N82E16824005214',
'LCD195WXM-BK':'N82E16824002371',
'AS191-BK':'N82E16824002496',
'AS191WM-BK':'N82E16824002497',
'VH198T':'N82E16824236072',
'E1920X':'N82E16824001382',
'HW-191APB':'N82E16824254023',
'P2050':'N82E16824001375',
'E2011H':'N82E16824260023',
'B2030':'N82E16824001383',
'2011x':'N82E16824176200',
'2010i':'N82E16824176157',
'W2040T-PN':'N82E16824005146',
'VH202T-P':'N82E16824236063',
'S201HLbd':'N82E16824009256',
'U2211H':'N82E16824260019',
'2211x':'N82E16824176199',
'EX2220X':'N82E16824001390',
'B2230':'N82E16824001385',
'U2211H':'N82E16824260019',
'VX2250wm-LED':'N82E16824116442',
'LE2201w':'N82E16824176115',
'F22':'N82E16824160051',
'E2360V-PN':'N82E16824005196',
'PX2370':'N82E16824001414',
'VH236H':'N82E16824236059',
'G235HAbd':'N82E16824009266',
'LP2475w':'N82E16824176104',
'U2410':'N82E16824260020',
'ZR24w':'N82E16824176165',
'2443BWT-TAA-1':'N82E16824001409',
'EA241WM-BK':'N82E16824002462',
'FX2490HD':'N82E16824001443',
'VH242H':'N82E16824236052',
'2511x':'N82E16824176194',
'HF-259HPB':'N82E16824262007',
'PA271W-BK':'N82E16824002543',
'DS-275W':'N82E16824185011',
'M2780D-PU':'N82E16824005194',
'E2750VR-SN':'N82E16824005203',
'2711x':'N82E16824176195',
'VE276Q':'N82E16824236091',
'P2770HD':'N82E16824001392',
'LCD3090WQXi-BK':'N82E16824002419',
'U3011':'N82E16824260028',
'ZR30w':'N82E16824176177',
'DS-305W':'N82E16824185012',
'XL2370-1':'N82E16824001380',
'E2243FW':'N82E16824160056',
'B2330HD':'N82E16824001424',
'EX231W-BK':'N82E16824002574',
'2311x':'N82E16824176198',
'BX2350':'N82E16824001420',
'H233Hbmid':'N82E16824009162'}

monitors = ['px2370','vh236h','u2410','fx2490hd','ve276q','p2770hd','u3011','zr30w','xl2370-1','e2243fw','b2330hd','bx2350','e231w-bk','2311x','h233hbmid','vp2365wb','p221w-bk','p2370hd-1']

other = ['PX2370','VH236H','U2410','FX2490HD','PA271W-BK','VE276Q','P2770HD','U3011','ZR30w','XL2370-1','E2243FW','B2330HD','EX231W-BK','2311x','BX2350','H233Hbmid','LCD1990SX-Bk','N194WA','195WXM-BK','AS191-BK','AS191WM-BK','VH198T','E1920X','HW-191APB','P2050','E2011H','B2030','2011x','2010i','W2040T-PN','VH202T-P','S201HLbd','U2211H','2211x','EX2220X','B2230','U2211H','VX2250wm-LED','LE2201w','F22','PX2370','VH236H','G235Habd','LP2475W','U2410','ZR24w','2443BWT','EA241WM-BK','FX2490HD','VH242H','2511x','HF-259HPB','PA271W','DS-275W','M2780D','E2750VR-SN','2711x','VE276Q','P2770HD','LCD3090WQXi-BK','U3011','ZR30w','DS-305W','xl2370','e2243fw','b2330hd','e231w','2310e','bx2350','h233h']

broken = ['W1934S','BX2050','x22LED','2233RZ','BX2250','2240S-PN''V223W','SP2309W','E2311H','E2340S-PN','2436Vw','iH254DPB','2509m','MC007LL/A','B273H','lp2275w','l997','e2350v','f2380','AW2310','U2711','lp3065','m237md']                    

no_data = []
i = 1

for monitor in monitors:

    # initialize record
    record = {}

    """""""""""""""
    Newegg Scrape
    """""""""""""""
    
    monitor = monitor.replace(" ","+")

    # search for product page
    search_result = 'http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&Order=BESTMATCH&Description=' + monitor
    
    # turn search page HTML into lxml object
    html = scraperwiki.scrape(search_result)
    root = lxml.html.fromstring(html)

    # get item number
    try:
        # if no direct product page
        if root.cssselect("h2.pageTitle")[0].text == 'Search Results': 
            # if no results found
            if root.cssselect("h3.alert"): 
                print "No result found for: " + monitor
                no_data.append(monitor)
                continue
            # if multiple results found
            else:  
                print 'Multiple results found for ' + monitor
                uls = root.cssselect('div[id="cellItem1"] ul')
                z = uls[1].cssselect("ul.featureList li")
                item_number = tostring(z[5])[19:34]
    # search yielded direct product page
    except: 
        print 'Found direct item page for ' + monitor
        item_number = root.cssselect("div.v660 em")
        item_number = item_number[0].text
    record['item'] = item_number
    
    
    # navigate to direct product page
    product_page = 'http://www.newegg.com/Product/Product.aspx?Item=' + item_number
    record['link'] = product_page

    # turn product page HTML into lxml object
    html = scraperwiki.scrape(product_page)
    root = lxml.html.fromstring(html)

    # TO-DO get price
    #root.cssselect("input[type='radio']")
       

    # get rating
    ratings = root.cssselect("div.objReviewSummary span.count")
    score = 0
    reviews = 0
    stars = 5
    for count in ratings:
        count = int(count.text.replace(',',''))
        score += count * stars
        reviews += count
        stars -= 1
    if reviews == 0:
        score = 0.0
    else:
        score = round(float(score) / float(reviews), 1)
    record['N_rating'] = score     # add new_egg rating to record
    record['N_reviews'] = reviews  # add new_egg reviews to record


    # Get specified tech specs
    techspecs = ['Model','Brand','Screen_Size','Recommended_Resolution','Viewing_Angle','Pixel_Pitch','Display_Colors','Brightness','Contrast_Ratio','Response_Time']

    dls = root.cssselect("div.Details_Content dl") # Get <dl> tags in class="Details_Content">
    for dl in dls:
        spec = dl[0].text
        spec = spec.replace('.','_')
        spec = spec.replace('+','_')
        spec = spec.replace(' ','_')
        value = dl[1].text
        if spec in techspecs:
            record[spec] = value # add tech spec to record

    """""""""
    CNET Scrape
    """""""""

    # search for product page
    search_result = 'http://reviews.cnet.com/1770-5_7-0.html?query=' + monitor + '&tag=srch&searchtype=products'
    html = scraperwiki.scrape(search_result)
    root = lxml.html.fromstring(html)

    editor_rating = root.cssselect("ul.data")
    if editor_rating:
        editor_rating = editor_rating[0].text[16:19]
        record['C_editor_rating'] = editor_rating

    user_rating = root.cssselect("div.userRate span")
    if user_rating:
        user_rating = user_rating[0].text
        record['C_user_rating'] = user_rating

    user_reviews = root.cssselect("div.userRate div")
    if user_reviews:
        user_reviews = user_reviews[0].text[7:8]
        record['C_user_reviews'] = user_reviews

    bottom_line = root.cssselect("div.resultSummaryCopy p")
    try:
        if bottom_line[0].cssselect("strong")[0].text == "CNET'S bottom line: ":
            text = tostring(bottom_line[0])
            end = text.index('.') + 1
            bottom_line = text[40:end]
            record['C_bottom_line'] = bottom_line
    except:
        pass


    print str(round(float(i) / float(len(monitors)) * 100,2)) + '% done'

    # insert price before
    #gridx + grid y

    record['id'] = i
    i += 1

    scraperwiki.sqlite.save(['Model'],record)



#Print monitors that were not found
print no_data