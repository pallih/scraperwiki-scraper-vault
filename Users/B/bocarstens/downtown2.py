import scraperwiki
html = scraperwiki.scrape("http://downtown.dk/kbh/deals")
print html
import lxml.html
root = lxml.html.fromstring(html)
for strtext in root.cssselect("div.text_container a"):
    for strvalue in root.cssselect("div.value span"):
        for strsave in root.cssselect("div.savings span"):
            data = {
            'title' : strtext.text,
            'value' : strvalue.text,
            'save' : strsave.text,
            }
            print data
            scraperwiki.sqlite.save(unique_keys=['title'], data=data)
k1 = 0
k2 = 0
k3 = 0
k4 = 0
k5 = 0
k6 = 0
list = [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9]
for el2 in root.cssselect("td.savings"):
    k5 = k5 + 1
    k6 = k6 + 1
    continue
    for strsave in root.cssselect("div.save"):
        if k3 == 0:
            list[7] = strsave.text[5:]
        if k3 == 1:
            list[8] = strsave.text[5:]
        if k3 == 2:
            list[9] = strsave.text[5:]
        k3 = k3 + 1
        for el in root.cssselect("div.title"):
            if k5 > 2:
                k5 = k5 - 1
                continue
            if k1 == 0:
                list[0] = el.text
            elif k1 == 1:
                list[1] = el.text
            elif k1 == 2:
                list[2] = el.text
            k1 = k1 + 1
            for strvalue in root.cssselect("div.value"):
                if k6 > 2:
                    k6 = k6 - 1
                    continue
                if k2 == 1:
                    list[4] = strvalue.text[8:]
                if k2 == 2:
                    list[5] = strvalue.text[8:]
                if k2 == 3:
                    list[6] = strvalue.text[8:]
                k2 = k2 + 1
while k4 < 3 :
    data = {
    'title' : list[k4],
    'value' : list[k4 + 4],
    'save' : list[k4 + 7]
    }
    print data
    scraperwiki.sqlite.save(unique_keys=['title'], data=data)
    k4 = k4 + 1
