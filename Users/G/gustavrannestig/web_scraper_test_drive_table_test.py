import scraperwiki
import scraperwiki 
import mechanize
import lxml.html
import re
import urlparse

# Web Scraper Test Drive!
#Table test

base_url = "http://testing-ground.extract-web-data.com/table"
test1_url = "http://testing-ground.extract-web-data.com/table?products=1&years=1&quarters=1"
test2_url = "http://testing-ground.extract-web-data.com/table?products=4&years=3&quarters=2"
test3_url = "http://testing-ground.extract-web-data.com/table?products=10&years=10&quarters=4"
def scrape(url):
    br = mechanize.Browser()
    response = br.open(url)

    html = response.read()

    root = lxml.html.fromstring(html)

    #Uncomment to create db-tables
    scraperwiki.sqlite.execute("create table years (year string, result string)")
    scraperwiki.sqlite.execute("create table quarters (quarter string, year string, result string)")
    scraperwiki.sqlite.commit()  

    tableheaderrows = root.cssselect("thead tr")
    tablebodyrows = root.cssselect("tbody tr")

    #Structure of the table, first table header with Quarter,x number of products,Total ammount
    # Then next table header row with item,ammount * number of products
    #the rows start with the quarter and en with the total ammount for that quarter
    #the last row of every year is the total ammount for that year

    #Find out how many products there are in the table by looking how many th:s there are in the first row of the thead
    ths1 = tableheaderrows[0].cssselect("th")
    num_of_prod = len(ths1) - 2

    #create a list with names of the product
    productlist = []
    counter = 0
    while counter != num_of_prod:
        productlist.append(ths1[counter + 1].text_content())
        counter += 1
    
    #two variables to hold the year and quarter as we itterate through the table
    year = ""
    quarter = ""
    
    #go trough every row in the tablebody
    for row in tablebodyrows:
        tds = row.cssselect("td")
        
        #See if the coolspan of the first element in the row is not None, then we probably deal with the row that holds the year
        colspan = tds[0].get("colspan")
        if colspan != None:
            if int(colspan) == (len(productlist)*2 + 2):
                year = tds[0].text_content()
        
        #if the number of td:s are more than 2, then we probably deal with the rows listing product information
        if len(tds) > 2:
            
            #the first td holds the quarter
            quarter = tds[0].text_content()
        
            #for every product extract the info on this row, 
            counter = 0
            for product in productlist:
                #if we got through the second to last td we can stop since the last hold info about the total for the quarter
                if counter == (len(tds) - 2):                
                    break
                
                #if there is no colspan there is probably information to get
                if tds[counter + 1].get("colspan") == None:
                    #as long as there is no rowspan :)
                    if tds[counter + 1].get("rowspan") == None:
                        data = { 
                                'product' : product,
                                'items' : tds[counter + 1].text_content(),
                                'amount' : tds[counter + 2].text_content(),
                                'year' : year,
                                'quarter' : quarter,
                                }
                        scraperwiki.sqlite.save(["year","quarter","product"], data)
                        counter += 2
                    else:
                        counter += 2
                else:
                    counter += 1
            #when we get to the last td we save the total for the quarter
            data = {
                    'quarter' : quarter,
                    'year' : year,
                    'result' : tds[counter + 1].text_content()             
                    }
            scraperwiki.sqlite.execute("insert or replace into quarters values (:quarter, :year, :result)", data)
            scraperwiki.sqlite.commit() 
        
        #when we find a row where there's no colspan on the first td but only two tds we know that we can get the total for the year
        elif colspan == None:
            data = {
                    'year' : year,
                    'result' : tds[1].text_content()
                   }
            scraperwiki.sqlite.execute("insert or replace into years values (:year, :result)", data)
            scraperwiki.sqlite.commit()  
        
scrape(test3_url)                   

