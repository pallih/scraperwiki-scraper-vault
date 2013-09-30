#This is a scraper crawling boarding school information from a public organisation website.
#All schools in USA and Canada are included. Main info sections are school name, website, phone number,
#address, school type etc. The script is based on scrapemark, which is a regular expression based scraper.

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
                               <td><a href='{@{*<div class="addressbar contactinfonew">
                                      <div><div>{{[saddress]}}<a></a></div>
                                                <div>{{[sphone]}}</div>
                                      </div>
                                      <div><div style="float:left"><a href={{[sweb]}} target="new"></a></div></div>
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

print 'len(dbname):',len(dbname)
print 'len(dbweb):',len(dbweb)
print 'len(dbphone):',len(dbphone)
print 'len(dbaddress):',len(dbaddress)
print 'len(dbcity):',len(dbcity)
print 'len(dbtype):',len(dbtype)
print 'len(dbgrade):',len(dbgrade)

nums=min(len(dbname),len(dbweb),len(dbphone),len(dbaddress),len(dbcity),len(dbtype),len(dbgrade))

id=0
for id in range(nums):
      scraperwiki.sqlite.save(unique_keys=["ID"],data={"ID":id, "City":dbcity[id], "School":dbname[id], "Website":dbweb[id], \
                        "Phone":dbphone[id], "Address":dbaddress[id], "Type":dbtype[id], "BD Grade":dbgrade[id]})

i = 0
print '<table border=1px>'
print '<tr><td>No.</td><td>City</td><td>School</td><td>Website</td>'
print '<td>Phone</td><td>Address</td><td>Type</td><td>Grades</td></tr>'
for i in range(nums):
    print '<tr>'
    print '<td>'+str(i)+'</td><td>'+dbcity[i]+'</td>'
    print '<td>'+dbname[i]+'</td><td>'+dbweb[i]+'</td>'
    print '<td>'+dbphone[i]+'</td><td>'+dbaddress[i]+'</td>'
    print '<td>'+dbtype[i]+'</td><td>'+dbgrade[i]+'</td>'
    print '</tr>'
print '</table>'

#This is a scraper crawling boarding school information from a public organisation website.
#All schools in USA and Canada are included. Main info sections are school name, website, phone number,
#address, school type etc. The script is based on scrapemark, which is a regular expression based scraper.

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
                               <td><a href='{@{*<div class="addressbar contactinfonew">
                                      <div><div>{{[saddress]}}<a></a></div>
                                                <div>{{[sphone]}}</div>
                                      </div>
                                      <div><div style="float:left"><a href={{[sweb]}} target="new"></a></div></div>
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

print 'len(dbname):',len(dbname)
print 'len(dbweb):',len(dbweb)
print 'len(dbphone):',len(dbphone)
print 'len(dbaddress):',len(dbaddress)
print 'len(dbcity):',len(dbcity)
print 'len(dbtype):',len(dbtype)
print 'len(dbgrade):',len(dbgrade)

nums=min(len(dbname),len(dbweb),len(dbphone),len(dbaddress),len(dbcity),len(dbtype),len(dbgrade))

id=0
for id in range(nums):
      scraperwiki.sqlite.save(unique_keys=["ID"],data={"ID":id, "City":dbcity[id], "School":dbname[id], "Website":dbweb[id], \
                        "Phone":dbphone[id], "Address":dbaddress[id], "Type":dbtype[id], "BD Grade":dbgrade[id]})

i = 0
print '<table border=1px>'
print '<tr><td>No.</td><td>City</td><td>School</td><td>Website</td>'
print '<td>Phone</td><td>Address</td><td>Type</td><td>Grades</td></tr>'
for i in range(nums):
    print '<tr>'
    print '<td>'+str(i)+'</td><td>'+dbcity[i]+'</td>'
    print '<td>'+dbname[i]+'</td><td>'+dbweb[i]+'</td>'
    print '<td>'+dbphone[i]+'</td><td>'+dbaddress[i]+'</td>'
    print '<td>'+dbtype[i]+'</td><td>'+dbgrade[i]+'</td>'
    print '</tr>'
print '</table>'

