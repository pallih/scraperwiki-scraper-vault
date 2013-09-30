from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring, tostring
import datetime

def main():
    Fall2012 ='https://www.american.edu/provost/registrar/schedule/schedule-results.cfm?term=2012FN&subj=&search=&mode=title&stat=ALL&hr=&mn=&ampm=AM&class=Search+Courses'
    Fallpage = urlopen(Fall2012)
    rawtext = Fallpage.read()
    html = fromstring(rawtext)
    print tostring(html)
    
    COURSE_KEYS = ['CourseNum', "Title", "Prerequisite", "Course Description"]
    SECTION_KEYS = ['Status','section','credit','instructor','time']    

    maindivs = html.cssselect(".crs-data")
    for crs in maindivs:
        COURSEdata = []
        header =crs.cssselect('.crs-header')[0]
        secs = crs.cssselect('.sec-details')
        #print tostring(header[0]), tostring(secs[0])
        headerdivs = header.cssselect('div')[1:]
        COURSEdata.extend([div.text_content().strip() for div in headerdivs[:2]])
        
        if len(headerdivs)==5:
            prereq = headerdivs[3].text_content().strip()
            COURSEdata.append(prereq[14:])
        else:
           COURSEdata.append('') 

        descriptionlink = 'https://www.american.edu/provost/registrar/schedule/' + headerdivs[2].cssselect('a')[0].attrib['href']
        descriptionrawtext = fromstring(urlopen(descriptionlink).read())
        try:
            COURSEdata.append(descriptionrawtext.cssselect('.course-header')[0].cssselect('p')[1].text_content().strip())
        except:
            COURSEdata.append('NONE')

        COURSEdata = dict(zip(COURSE_KEYS,COURSEdata))
        #print COURSEdata
        
        for sec in secs:
            SECdata = []
            sectionDivs = sec.cssselect('div')[1:]
            SECdata.append(sectionDivs[0].text_content().strip()) #status
            SECdata.append(sectionDivs[1].text_content().strip()) #sectionNum
            SECdata.append(sectionDivs[3].text_content().strip()) #credits
            SECdata.append(str(sectionDivs[4].text_content().strip())) #professor
            SECdata.append(str(sectionDivs[8].text_content().strip())) #times
            SECdata = dict(zip(SECTION_KEYS,SECdata))
            SECdata = dict(COURSEdata.items() + SECdata.items())
            #SECdata['section'] = int(SECdata['section'])
            #SECdata['credit'] = int(SECdata['credit'])
            SECdata['key'] = SECdata['CourseNum'] + str(SECdata['section']) #used as unique key
            save(['key'],SECdata)
              

main()from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.html import fromstring, tostring
import datetime

def main():
    Fall2012 ='https://www.american.edu/provost/registrar/schedule/schedule-results.cfm?term=2012FN&subj=&search=&mode=title&stat=ALL&hr=&mn=&ampm=AM&class=Search+Courses'
    Fallpage = urlopen(Fall2012)
    rawtext = Fallpage.read()
    html = fromstring(rawtext)
    print tostring(html)
    
    COURSE_KEYS = ['CourseNum', "Title", "Prerequisite", "Course Description"]
    SECTION_KEYS = ['Status','section','credit','instructor','time']    

    maindivs = html.cssselect(".crs-data")
    for crs in maindivs:
        COURSEdata = []
        header =crs.cssselect('.crs-header')[0]
        secs = crs.cssselect('.sec-details')
        #print tostring(header[0]), tostring(secs[0])
        headerdivs = header.cssselect('div')[1:]
        COURSEdata.extend([div.text_content().strip() for div in headerdivs[:2]])
        
        if len(headerdivs)==5:
            prereq = headerdivs[3].text_content().strip()
            COURSEdata.append(prereq[14:])
        else:
           COURSEdata.append('') 

        descriptionlink = 'https://www.american.edu/provost/registrar/schedule/' + headerdivs[2].cssselect('a')[0].attrib['href']
        descriptionrawtext = fromstring(urlopen(descriptionlink).read())
        try:
            COURSEdata.append(descriptionrawtext.cssselect('.course-header')[0].cssselect('p')[1].text_content().strip())
        except:
            COURSEdata.append('NONE')

        COURSEdata = dict(zip(COURSE_KEYS,COURSEdata))
        #print COURSEdata
        
        for sec in secs:
            SECdata = []
            sectionDivs = sec.cssselect('div')[1:]
            SECdata.append(sectionDivs[0].text_content().strip()) #status
            SECdata.append(sectionDivs[1].text_content().strip()) #sectionNum
            SECdata.append(sectionDivs[3].text_content().strip()) #credits
            SECdata.append(str(sectionDivs[4].text_content().strip())) #professor
            SECdata.append(str(sectionDivs[8].text_content().strip())) #times
            SECdata = dict(zip(SECTION_KEYS,SECdata))
            SECdata = dict(COURSEdata.items() + SECdata.items())
            #SECdata['section'] = int(SECdata['section'])
            #SECdata['credit'] = int(SECdata['credit'])
            SECdata['key'] = SECdata['CourseNum'] + str(SECdata['section']) #used as unique key
            save(['key'],SECdata)
              

main()