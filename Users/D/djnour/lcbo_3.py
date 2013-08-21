import scraperwiki
import lxml.html
from lxml.html.clean import clean_html


# Blank Python
key = 'a'
string = ''
apv = 0
apvtup=[0,0]
apvtop=0
x = 0
x = scraperwiki.sqlite.get_var(key, x)
while x < 999947:
    category = ''
    null= 0
    volumeb = 0
    priceb = 0
    alcb = 0
    apv = 0
    a= "http://www.lcbo.com/lcbo-ear/lcbo/product/details.do?language=EN&itemNumber="+str(x)
    html = scraperwiki.scrape(a)
    string =''
    
    root = lxml.html.fromstring(html)
    tds = root.cssselect('td br,b')
    for td in tds:
        string = lxml.html.tostring(td)
        string = clean_html(string)
        namest = string.find('<span class="titlefont">')
        
        if namest != -1:
            nameend = string.find('</span>')
            name = string[namest+24:nameend]
        mlp = string.find('mL')
        if mlp != -1:
            volumea = string[mlp-10:mlp]
            volumea = volumea[::-1]
            volumeb = 0
            mult = 0
            dec = 1
            dec2 = 1
            xdidnt = 'True'
            if 'x' in volumea:
                for char in volumea:
                    if xdidnt == 'True':
                        if char in ('1234567890'):
                            volumeb += (int(char)*dec)
                            dec *= 10
                        if char == 'x':
                            xdidnt = 'False'
                    if xdidnt == 'False':
                        if char in ('1234567890'):
                                mult += (int(char)*dec2)
                                dec2 *= 10
            volumeb = volumeb * mult
                   
                    
            if 'x' not in volumea:
                for char in volumea:
                    if char in ('1234567890'):
                        volumeb += (int(char)*dec)
                        dec *= 10
        price = string.find('$')
        if price != -1:
            pricea = string[price+1:price+11]
            pricea = pricea[::-1]
            priceb = 0
            dec = 0.01
            for char in pricea:
                if char in ('1234567890'):
                    priceb += (int(char)*dec)
                    dec *= 10
        alc = string.find('%')
        if alc != -1:
            alca = string[alc-4:alc]
            alca = alca[::-1]
            alcb = 0
            dec = 0.1
            for char in alca:
                if char in ('1234567890'):
                    alcb += (int(char)*dec)
                    dec *= 10
        for word in ['Ale','Armagnac','Bags','Bar Accessories','Beer Coolers','Boxes','Brandy','Champagne','Charity Donations','Ciders','Cognac','Cork Screws','Dessert Wine','Eau-de-Vie','Fortifieds','Gift Certificate','Gift Of The Month','Gin','Glassware','Gluten Free','Icewine','Lager','Liqueur/Liquor','Misc-seasonal Items','Mixed Wine Products','Mixed/Taster Packs','Non-alcohol','One Pour Cocktails','Product Knowledge','Publications','Red Wine','Rosé Wine','Rum','Sake','Scotch Whisky','Sparkling Wine','Specialty Wines/Other','Spirit Coolers','Tequila','Vessels','Vodka','Whisky/Whiskey','White Wine','Wine Coolers','Wine Racks','Beer']:
            if word in string:
                category = word + " / " + category

    if alcb != 0:
        apv = ((alcb/100)*volumeb)/priceb
    if apv != 0:
        scraperwiki.sqlite.save(unique_keys=["a"], data={'a':[x,name,apv,category]})
        
    if apv > apvtop:
        apvtop = apv
        apvtup = [x,name,apv,category]
        print apvtup
    scraperwiki.sqlite.save_var(key, x)
    x += 1
    
