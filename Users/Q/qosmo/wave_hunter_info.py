import scraperwiki
import mechanize 
import lxml.html
import datetime

br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_referer(False)

# login form
login_url = "http://www.wavehunter.jp/wh/wavehunter/frame_left2.php"
response = br.open(login_url)
br.select_form(nr=0)
br["Email"] = "nao.tokui@gmail.com"
br["Password"] = "mogemoge"
response = br.submit()

####### read info
info_url = "http://www.wavehunter.jp/wh/premium/nami2.0.php?area=05" 
response2 = br.open(info_url)
info_html = response2.read()
## print info_html

####### extract info
root = lxml.html.fromstring(info_html)
links = root.xpath('//tr/td')
count = 0
point = -1;
people = -1;
datestr = ""

for link in links:
    try:
        if link.attrib['width'] == "13%" and link.attrib['height'] == "16":  # 日付
            count  = count + 1
            if count == 5: 
                datestr   = link.text.strip()
        if link.attrib['width'] == "15%" and link.attrib['height'] == "38":
#   print link.text 
            if count == 5 and people == -1: # TODO:　5番目の要素を抜き出す (もっといい方法があるはず)
                s = link.text.strip()
                people =  s[:len(s)-1]
            elif count == 5 and people != -1 and point == -1: # TODO:　5番目の要素を抜き出す (もっといい方法があるはず)
                s = link.text.strip()
                point =  s[1:]
    except:
        pass


###### sunrise
info_url = "http://time.unitarium.com/sunrise/104141" 
response2 = br.open(info_url)
info_html = response2.read()
print info_html

root = lxml.html.fromstring(info_html)
links = root.xpath("//td[@style='font-size:20px;color:rgb(215,254,190)']")
sunrise = ""

for link in links:
    if link.text.strip() == "Sunrise:":
        sunrise = link.getnext().text

d = datetime.datetime.today()
today = '%s/%s/%s ' % (d.year, d.month, d.day)
sundate = datetime.datetime.strptime(today + sunrise, "%Y/%m/%d %H:%M:%S")

####### store
day  = datestr[:10]  # TODO:　全角スペースをのぞく... 
time = datestr[12:]
datestr = day + " " + time
print datestr + " - " + point + " - " + people + " people   sunrise:" + str(sundate)

date = datetime.datetime.strptime(datestr, "%Y/%m/%d %H:%M")
data = {"date": date, "wavepoint": point, "people": people, "sunrise": sundate}
scraperwiki.sqlite.save(unique_keys=['date'], data=data)


