import scraperwiki
#trial to import taoabao price list for one defined page
#http://list.taobao.com/market/baobao.htm?spm=1.67805.107645.2&cat=50032654&atype=b&style=list&isprepay=1&viewIndex=1&yp4p_page=0&isnew=2&olu=yes&mSelect=true&commend=all&age=0

html = scraperwiki.scrape("http://www.amazon.com/s/ref=sr_nr_n_0?sf=sbc&rh=n%3A165796011%2Cn%3A%21165797011%2Cn%3A166777011%2Ck%3Ainfant+formula%2Cn%3A166789011%2Cn%3A16323111%2Cn%3A16323121&bbn=16323111&sort=salesrank&keywords=infant+formula&ie=UTF8&qid=1328236098&rnid=16323111")
print html
import lxml.html           
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
print root
tds = root.cssselect(div[class='Brand']) # get all the <ul> tags
print tds
for div in tds:
    print lxml.html.tostring(div) # the full HTML tag
    print div.text                # just the text inside the HTML tag


#for tr in root.cssselect(): #loop starting  trying to get ul#J_ListView.list-view
 

#    tds = tr.cssselect("td")
#    data = {
#      'country' : tds[0].text_content(),
#      'years_in_school' : int(tds[4].text_content())
#    }
#    scraperwiki.sqlite.save(unique_keys=['country'], data=data)
