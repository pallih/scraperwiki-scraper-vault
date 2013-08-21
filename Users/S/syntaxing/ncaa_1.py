import scraperwiki
import lxml.html

  
url = "http://espn.go.com/mens-college-basketball/statistics/team/_/stat/assists"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
    
    

for main in root.cssselect("table.tablehead tr[align='right']"):

    #scraperwiki.sqlite.save(unique_keys=["title"], data={"title":main.text, "link": main.attrib['href']})   
    temp =  main.cssselect("td")


    try:
        temp_array = [temp[0].text, temp[1].cssselect("a")[0].text, temp[2].text, temp[3].text, temp[4].text, temp[5].text,temp[6].text,temp[7].text]
        print temp_array
        scraperwiki.sqlite.save(unique_keys=["RK"], data={"RK":temp_array[0], "TEAM":temp_array[1],"GP":temp_array[2], "AST":temp_array[3], "APG":temp_array[4],"TO":temp_array[5],"TOPG":temp_array[6],"ASTTO":temp_array[7]})
    except IndexError:
        pass


