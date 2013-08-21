import lxml.html
import scraperwiki
url = "http://jobsearch.monsterindia.com/searchresult.html?fts=websphere&loc=199&loc=5&mne=6&mxe=&ind=65&jbc=22&ctp=0&day=30&srt=pst"
root = lxml.html.parse(url).getroot()

# alternatively you can use:
#   html = urllib2.urlopen(url).read()
#   root = lxml.html.fromstring(html)

#divs = root.cssselect("table.results")
#for br_with_tail in root.cssselect('table.results > tr > td > a + span + br'):
    #print br_with_tail.tail
for el in root.cssselect("table.results"):    
 #print el.tag    
 for el2 in el: #tr tags
   # print "--", el2.tag, el2.attrib 
  for e13 in el2:#td tags
   #print e13.tag   
    for e14 in e13:#child elements of td
      if ( e14.tag == 'a') :
         print "keyword: ",e14.text_content()
      if (e14.tag == 'span'):
         print "date: ",e14.text_content()
      if (e14.tag == 'br'):
          if(e14.tail ):
            print "company: ",e14.tail
      if(e14.tag == 'div'):
         for e15 in e14.cssselect('span.txt_green'):
             print "location, yrs : ",e15.text_content()
        
   
#print "There are %d elements with tag style in this page" % len(divs)
#print "Their corresponding attributes are:", [divs.text]

#crdiv = root.cssselect("div#divCopyright")[0]
#print "The copyright message is: ", lxml.html.tostring(crdiv)

# Click on "Quick help" and select lxml cheat sheet for more advice

