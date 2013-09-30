import scraperwiki
#import inspect
import lxml.html 
import re

#Load the html of the Conference service physics page
html = scraperwiki.scrape("http://www.conference-service.com/conferences/physics.html") 
root = lxml.html.fromstring(html) 


subjectlinks = root.cssselect("a.subjectlinks")





for link in subjectlinks :



    html2 = scraperwiki.scrape("http://www.conference-service.com/conferences/"+link.get('href')   )  
    root2 = lxml.html.fromstring(html2)
    
    
    #Kind of weird, there seems to be 3 table.conferencelist, each containing an arbitrary number of conferences
    conflist = root2.cssselect('table.conferencelist')
    trlist = []
    for clist in conflist :
        trlisttemp = clist.cssselect('tr')

        for tr in trlisttemp :
            trlist.append(tr)
    


    

    trclass = [tr.get('class') for tr in trlist ] 
    tbindex = [i for i, x in enumerate(trclass) if x == "conflist_titlebar"]

#Apparently not a good Python way of doing things, but whatever...
    for i in range(0,len(tbindex)-1) :
        
        #Search for stuff in the tr's between tr(tbindex(i)) and tr(tbindex(i+1))
        #First get the name, this is always easy
        name = trlist[tbindex[i]].cssselect('td.conflist_title')[0].text_content()

        #Next tr has the date
        date = trlist[tbindex[i]+1].cssselect('td.conflist_date')[0].text_content()

        #Next tr has location
        location = trlist[tbindex[i]+2].cssselect('td.conflist_date')[0].text_content()

        #One of the remaining tr before next titlebar may contain a Weblink:
    
        j = tbindex[i]+3
        if i < len(tbindex)-1 :
            jlim = tbindex[i+1]
        else :
            jlim = len(trlist)
        while j < jlim :
            url = ''
            urltag = trlist[j].cssselect('a')
            if urltag != [] :
                url = urltag[0].get('href')
                break
            j =j+1

        print 'Name: '+name+', Date: '+date+', Location: '+location+', URL: '+url


#    for clist in conflist :
#        conferences = clist.cssselect('td.conflist_title')
#        confdates = clist.cssselect('td.conflist_date')
#        conflink = clist.cssselect('td.conflist_left a')
 #       print 'Length of conferencenames is '+str(len(conferences))
 #       print 'Length of conferencedates is '+str(len(confdates))
 #       print 'Length of conferencelinks is '+str(len(conflink))   
        
#        for index, event in enumerate(conferences) :     
#
#            confname = event.text_content()
#            date = confdates[index*2].text_content()
#            location = confdates[index*2+1].text_content()
#            try:
#                url = conflink[index].get('href')
#            except:
#                url = ''
#            print 'Name: '+confname+', Date: '+date+', Location: '+location+', URL: '+url
#    
#    break
'''

    confname_css = eventinfo.cssselect('span[id="eventNameHeader"]')[0]
    confname = confname_css.text_content()
    
    date_css = eventinfo.cssselect('span[id="eventDate"]')[0]
    date = date_css.text_content()


    venue_css = eventinfo.cssselect('span[id="eventCountry"]')[0]
    venue = venue_css.text_content()
    

    url_css = eventinfo.cssselect('span[id="eventWebsite"]')[0]
    url = url_css.cssselect('a')[0].get('href')
    

        


    
    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url, 'venue':venue, 'date':date})           
    

'''


import scraperwiki
#import inspect
import lxml.html 
import re

#Load the html of the Conference service physics page
html = scraperwiki.scrape("http://www.conference-service.com/conferences/physics.html") 
root = lxml.html.fromstring(html) 


subjectlinks = root.cssselect("a.subjectlinks")





for link in subjectlinks :



    html2 = scraperwiki.scrape("http://www.conference-service.com/conferences/"+link.get('href')   )  
    root2 = lxml.html.fromstring(html2)
    
    
    #Kind of weird, there seems to be 3 table.conferencelist, each containing an arbitrary number of conferences
    conflist = root2.cssselect('table.conferencelist')
    trlist = []
    for clist in conflist :
        trlisttemp = clist.cssselect('tr')

        for tr in trlisttemp :
            trlist.append(tr)
    


    

    trclass = [tr.get('class') for tr in trlist ] 
    tbindex = [i for i, x in enumerate(trclass) if x == "conflist_titlebar"]

#Apparently not a good Python way of doing things, but whatever...
    for i in range(0,len(tbindex)-1) :
        
        #Search for stuff in the tr's between tr(tbindex(i)) and tr(tbindex(i+1))
        #First get the name, this is always easy
        name = trlist[tbindex[i]].cssselect('td.conflist_title')[0].text_content()

        #Next tr has the date
        date = trlist[tbindex[i]+1].cssselect('td.conflist_date')[0].text_content()

        #Next tr has location
        location = trlist[tbindex[i]+2].cssselect('td.conflist_date')[0].text_content()

        #One of the remaining tr before next titlebar may contain a Weblink:
    
        j = tbindex[i]+3
        if i < len(tbindex)-1 :
            jlim = tbindex[i+1]
        else :
            jlim = len(trlist)
        while j < jlim :
            url = ''
            urltag = trlist[j].cssselect('a')
            if urltag != [] :
                url = urltag[0].get('href')
                break
            j =j+1

        print 'Name: '+name+', Date: '+date+', Location: '+location+', URL: '+url


#    for clist in conflist :
#        conferences = clist.cssselect('td.conflist_title')
#        confdates = clist.cssselect('td.conflist_date')
#        conflink = clist.cssselect('td.conflist_left a')
 #       print 'Length of conferencenames is '+str(len(conferences))
 #       print 'Length of conferencedates is '+str(len(confdates))
 #       print 'Length of conferencelinks is '+str(len(conflink))   
        
#        for index, event in enumerate(conferences) :     
#
#            confname = event.text_content()
#            date = confdates[index*2].text_content()
#            location = confdates[index*2+1].text_content()
#            try:
#                url = conflink[index].get('href')
#            except:
#                url = ''
#            print 'Name: '+confname+', Date: '+date+', Location: '+location+', URL: '+url
#    
#    break
'''

    confname_css = eventinfo.cssselect('span[id="eventNameHeader"]')[0]
    confname = confname_css.text_content()
    
    date_css = eventinfo.cssselect('span[id="eventDate"]')[0]
    date = date_css.text_content()


    venue_css = eventinfo.cssselect('span[id="eventCountry"]')[0]
    venue = venue_css.text_content()
    

    url_css = eventinfo.cssselect('span[id="eventWebsite"]')[0]
    url = url_css.cssselect('a')[0].get('href')
    

        


    
    scraperwiki.sqlite.save(unique_keys=['name'], data={'name':confname,'url':url, 'venue':venue, 'date':date})           
    

'''


