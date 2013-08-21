import scraperwiki           
import lxml.html

index = 0
courseState = ""
courseCity = ""
courseTitle = ""
courseInformation = ""
courseType = ""

html = scraperwiki.scrape("http://www.golfcoursesguide.org/unitedstates")
root = lxml.html.fromstring(html)

states = root.cssselect("div[class='col2_center'] table > tr > td > table > tr[valign='TOP'] > td[class='texto'] > a")

for state in states:
    stateURL  = "http://www.golfcoursesguide.org" + state.attrib['href']
    stateName = state.text.replace(" Golf Courses", "")
    courseState = stateName
    html2 = scraperwiki.scrape(stateURL)
    root2 = lxml.html.fromstring(html2)
    
    citys = root2.cssselect("div[class='col2_center'] table > tr > td > table > tr[valign='TOP'] > td[class='texto'] > a")
    for city in citys:
        cityURL  = "http://www.golfcoursesguide.org" + city.attrib['href']
        cityName = city.text.replace(" Golf Courses", "")
        courseCity = cityName 
        html3 = scraperwiki.scrape(cityURL)
        root3 = lxml.html.fromstring(html3)
    
        golfCourses = root3.cssselect("div[class='col2_center'] table > tr > td > table > tr > td > a")
        courseType = root3.cssselect("div[class='col2_center'] table > tr > td > table > tr > td:nth-child(2)")[0].text
        print cityName  + " : " + courseType
        for golfCourse in golfCourses:
            golfCourseName = golfCourse.text_content()
            print golfCourseName 
            courseTitle = golfCourseName 

            clubURL = cityURL + "/" + golfCourse.attrib['href']
            html4 = scraperwiki.scrape(clubURL)
            root4 = lxml.html.fromstring(html4)

            clubinfo = root4.cssselect("div[class='col2_center'] table > tr > td > table > tr[valign='TOP'] > td > center")
            courseInformation = clubinfo[0].text_content()            
            

            index = index + 1
        
            data = {
                "id"      : index,
                "state"   : courseState,
                "city"    : courseCity,
                "courseName" : courseTitle,
                "courseType" : courseType,
                "courseInfo" : courseInformation                           
               }
        
            scraperwiki.sqlite.save(unique_keys=['id'], table_name="GolfCoursesUSA", data=data)

