import scraperwiki
for n in range(50001,52000):
    page = 'http://www.openrice.com/restaurant/sr2.htm?shopid='+str(n)      
    html = scraperwiki.scrape(page)

    import lxml.html
    root = lxml.html.fromstring(html)

    general = root.cssselect("div.breadcrumb a")
    mstatus = root.cssselect("div.title span") 
    maddress = root.cssselect("a.blacklink")
    mphone = root.cssselect("table.addetail b")
    mtype = root.cssselect("span.blacklink a")
    mprice = root.cssselect("span.pricerange")
    mlike = root.cssselect("span.number")
    mgrade = root.cssselect("span.average")
    mimagelink = root.cssselect("div.restinfo img[align='left']")
    noimage = root.cssselect("div.ad_top_bar img")
    
    

    general.append(general[0])
    general.append(general[0])
    general.append(general[0])
    general.append(general[0])
    mstatus.append(general[0])
    mstatus.append(general[0])
    maddress.append(general[0])
    mphone.append(general[0])
    mphone.append(general[0])
    mstatus.append(general[0])
    mstatus.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mprice.append(general[0])
    mlike.append(general[0])
    mlike.append(general[0])
    mlike.append(general[0])
    mgrade.append(general[0])
    mimagelink.append(noimage[0])

    name = general[4].text
    district = general[3].text
    status = mstatus[1].text
    address = maddress[0].tail
    phone = mphone[1].tail[2:]
    type1 = mtype[0].text
    type2 = mtype[1].text
    type3 = mtype[2].text
    type4 = mtype[3].text
    type5 = mtype[4].text
    type6 = mtype[5].text
    type7 = mtype[6].text
    type8 = mtype[7].text
    type9 = mtype[8].text
    type10 = mtype[9].text
    price = mprice[0].text
    like = mlike[0].text
    normal = mlike[1].text
    dislike = mlike[2].text
    grade = mgrade[0].text
    imagelink = mimagelink[0].attrib['src']
    
    data = { 'name' : name, 'district' : district, 'status' : status, 'address' : address, 'phone' : phone, 'type1' : type1, 'type2' : type2, 'type3' : type3, 'type4' : type4, 'type5' : type5, 'type6' : type6, 'type7' : type7, 'type8' : type8, 'type9' : type9, 'type10' : type10, 'price' : price, 'like' : like, 'normal' : normal, 'dislike' : dislike, 'imagelink' : imagelink } 
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)import scraperwiki
for n in range(50001,52000):
    page = 'http://www.openrice.com/restaurant/sr2.htm?shopid='+str(n)      
    html = scraperwiki.scrape(page)

    import lxml.html
    root = lxml.html.fromstring(html)

    general = root.cssselect("div.breadcrumb a")
    mstatus = root.cssselect("div.title span") 
    maddress = root.cssselect("a.blacklink")
    mphone = root.cssselect("table.addetail b")
    mtype = root.cssselect("span.blacklink a")
    mprice = root.cssselect("span.pricerange")
    mlike = root.cssselect("span.number")
    mgrade = root.cssselect("span.average")
    mimagelink = root.cssselect("div.restinfo img[align='left']")
    noimage = root.cssselect("div.ad_top_bar img")
    
    

    general.append(general[0])
    general.append(general[0])
    general.append(general[0])
    general.append(general[0])
    mstatus.append(general[0])
    mstatus.append(general[0])
    maddress.append(general[0])
    mphone.append(general[0])
    mphone.append(general[0])
    mstatus.append(general[0])
    mstatus.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mtype.append(general[0])
    mprice.append(general[0])
    mlike.append(general[0])
    mlike.append(general[0])
    mlike.append(general[0])
    mgrade.append(general[0])
    mimagelink.append(noimage[0])

    name = general[4].text
    district = general[3].text
    status = mstatus[1].text
    address = maddress[0].tail
    phone = mphone[1].tail[2:]
    type1 = mtype[0].text
    type2 = mtype[1].text
    type3 = mtype[2].text
    type4 = mtype[3].text
    type5 = mtype[4].text
    type6 = mtype[5].text
    type7 = mtype[6].text
    type8 = mtype[7].text
    type9 = mtype[8].text
    type10 = mtype[9].text
    price = mprice[0].text
    like = mlike[0].text
    normal = mlike[1].text
    dislike = mlike[2].text
    grade = mgrade[0].text
    imagelink = mimagelink[0].attrib['src']
    
    data = { 'name' : name, 'district' : district, 'status' : status, 'address' : address, 'phone' : phone, 'type1' : type1, 'type2' : type2, 'type3' : type3, 'type4' : type4, 'type5' : type5, 'type6' : type6, 'type7' : type7, 'type8' : type8, 'type9' : type9, 'type10' : type10, 'price' : price, 'like' : like, 'normal' : normal, 'dislike' : dislike, 'imagelink' : imagelink } 
    scraperwiki.sqlite.save(unique_keys=['name'], data=data)