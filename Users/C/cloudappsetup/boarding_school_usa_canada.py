# Python
#This is a scraper crawling boarding school information from a public organisation website.
#All schools in USA and Canada are included. Main info sections are school name, website, phone number,
#address, school type etc. The script is based on scrapemark, which is a regular expression based scraper...
import string
import scraperwiki
import urllib2
import scrapemark

def getbdschools(url):
    return scrapemark.scrape("""
            {*
                  <table>
                        <tr></tr>
                        <tr></tr>
                        {*
                           <tr>
                               <td><a href='{@{*<div class="contactinfonew"></div><div id="heading3"></div>
                                      <div class="addressbar contactinfonew">
                                      <div><div>{{[saddress]}}</div>
                                                <div>tel:{{[sphone]}}</div>
                                      </div>
                                      <div>
                                                <div><a></a><a href={{[sweb]}} target="new"></a></div>
                                                <div><a></a></div>
                                      </div>
                                      <div><a></a><a></a></div>
                                      <div><br>{{[sbrief]}}</div>
                                </div>*} @}'>{{[sname]}}</a></td>
                               <td><div>{{[stype]}}</div></td>
                               <td><div>{{[sgrade]}}</div></td>
                               <td><div>{{[scity]}}</div></td>
                           </tr>
                        *}
               </table>
            *}
            """,url=url)

allschools=getbdschools('http://www.boardingschoolreview.com/school_overview.php')

dbcity=allschools['scity']
dbname=allschools['sname']
dbweb=allschools['sweb']
dbphone=allschools['sphone']
dbaddress=allschools['saddress']
dbtype=allschools['stype']
dbgrade=allschools['sgrade']
dbbrief=allschools['sbrief']

print 'len(dbname):',len(dbname)
print 'len(dbweb):',len(dbweb)
print 'len(dbphone):',len(dbphone)
print 'len(dbaddress):',len(dbaddress)
print 'len(dbcity):',len(dbcity)
print 'len(dbtype):',len(dbtype)
print 'len(dbgrade):',len(dbgrade)
print 'len(dbbrief):',len(dbbrief)

nums=min(len(dbname),len(dbweb),len(dbphone),len(dbaddress),len(dbcity),len(dbtype),len(dbgrade),len(dbbrief))

id=0
for id in range(nums):
      scraperwiki.sqlite.save(unique_keys=["ID"],data={"ID":id, "City":dbcity[id], "School":dbname[id], "Website":dbweb[id], \
                        "Phone":dbphone[id], "Address":dbaddress[id], "Type":dbtype[id], "BD Grade":dbgrade[id], "Brief":dbbrief[id]})

def cleanaddress(orig):
         nwst=[]
         i=0
         for i in range(len(orig)):
                if orig[i].find("<a href")==-1: nwst[i]=orig[i]
                elif orig[i].find("- <a href")==-1: nwst[i]=orig[i][:orig[i].find("<a href")]
                else: nwst[i]=orig[i][:orig[i].find("- <a href")]
         return nwst

clrAddress=cleanaddress(dbaddress)

id=0
for id in range(nums):
      scraperwiki.sqlite.save(unique_keys=["sID"],data={"sID":id,"clrAddress":clrAddress[id]})

