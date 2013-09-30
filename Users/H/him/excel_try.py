import scraperwiki           
import xlrd
import lxml.html           
xlbin = scraperwiki.scrape("http://www.converge13.com/test/Book1.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)   
for rownumber in range(0, sheet.nrows):
            isbn = str(int(sheet.cell(rownumber,0).value))
            url = ""
            img_url = ""
            title = ""
            mrprice = ""
            fkprice = ""
            authors = ""
            publisher = ""
            publication_year = ""
            isbn_13 = ""
            isbn_10 = ""
            language = ""
            edition = ""
            binding = ""
            no_of_pages = ""
            book_type = ""
            url = "http://www.flipkart.com/search-books?query="+isbn
            html = scraperwiki.scrape(url)
            authors =''
            root = lxml.html.fromstring(html)
            for el in root.cssselect("h1"):   
                 if el.attrib['itemprop']=="name":       
                        title = el.attrib['title']
            for el in root.cssselect("div.nprod-specs div span"):
                if el.text == "Author:" :
                    el = el.getparent()
                    for authorel in el.cssselect("a"):
                        authors += authorel.text + ", "
            
            for el in root.cssselect("span#fk-mprod-list-id"):
                mrprice = el.text
            for el in root.cssselect("span.fk-font-finalprice"):
                fkprice = el.text
            
            for tr in root.cssselect("div#specifications tr"):
                if tr.cssselect("td"):
                    tds = tr.cssselect("td")
                    if tds[0].text_content()=="Publisher":
                        publisher = tds[1].text_content()
                    elif tds[0].text_content()=="Publication Year":
                        publication_year = tds[1].text_content()
                    elif tds[0].text_content()=="ISBN-13":
                        isbn_13 = tds[1].text_content()
                    elif tds[0].text_content()=="ISBN-10":
                        isbn_10 = tds[1].text_content()
                    elif tds[0].text_content()=="Language":
                        language = tds[1].text_content()
                    elif tds[0].text_content()=="Edition":
                        edition = tds[1].text_content()
                    elif tds[0].text_content()=="Binding":
                        binding = tds[1].text_content()
                    elif tds[0].text_content()=="Number of Pages":
                        no_of_pages = tds[1].text_content()
                    elif tds[0].text_content()=="Book Type":
                        book_type = tds[1].text_content()
            
                
            for el in root.cssselect("div.image-wrapper img"):
                img_url = el.attrib['src']
                print img_url
            
            
            data = {
                        'url':url,
                        'img_url':img_url,
                        'title':title,
                        'mrp':mrprice,
                        'fkprice':fkprice,
                        'authors':authors,
                        'publisher':publisher,
                        'publication_year':publication_year,
                        'isbn-13':isbn_13,
                        'isbn-10':isbn_10,
                        'language':language,
                        'edition':edition,
                        'binding':binding,
                        'no_of_pages':no_of_pages,
                        'book_type':book_type
                   }
            
            scraperwiki.sqlite.save(['url'],data)
import scraperwiki           
import xlrd
import lxml.html           
xlbin = scraperwiki.scrape("http://www.converge13.com/test/Book1.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)   
for rownumber in range(0, sheet.nrows):
            isbn = str(int(sheet.cell(rownumber,0).value))
            url = ""
            img_url = ""
            title = ""
            mrprice = ""
            fkprice = ""
            authors = ""
            publisher = ""
            publication_year = ""
            isbn_13 = ""
            isbn_10 = ""
            language = ""
            edition = ""
            binding = ""
            no_of_pages = ""
            book_type = ""
            url = "http://www.flipkart.com/search-books?query="+isbn
            html = scraperwiki.scrape(url)
            authors =''
            root = lxml.html.fromstring(html)
            for el in root.cssselect("h1"):   
                 if el.attrib['itemprop']=="name":       
                        title = el.attrib['title']
            for el in root.cssselect("div.nprod-specs div span"):
                if el.text == "Author:" :
                    el = el.getparent()
                    for authorel in el.cssselect("a"):
                        authors += authorel.text + ", "
            
            for el in root.cssselect("span#fk-mprod-list-id"):
                mrprice = el.text
            for el in root.cssselect("span.fk-font-finalprice"):
                fkprice = el.text
            
            for tr in root.cssselect("div#specifications tr"):
                if tr.cssselect("td"):
                    tds = tr.cssselect("td")
                    if tds[0].text_content()=="Publisher":
                        publisher = tds[1].text_content()
                    elif tds[0].text_content()=="Publication Year":
                        publication_year = tds[1].text_content()
                    elif tds[0].text_content()=="ISBN-13":
                        isbn_13 = tds[1].text_content()
                    elif tds[0].text_content()=="ISBN-10":
                        isbn_10 = tds[1].text_content()
                    elif tds[0].text_content()=="Language":
                        language = tds[1].text_content()
                    elif tds[0].text_content()=="Edition":
                        edition = tds[1].text_content()
                    elif tds[0].text_content()=="Binding":
                        binding = tds[1].text_content()
                    elif tds[0].text_content()=="Number of Pages":
                        no_of_pages = tds[1].text_content()
                    elif tds[0].text_content()=="Book Type":
                        book_type = tds[1].text_content()
            
                
            for el in root.cssselect("div.image-wrapper img"):
                img_url = el.attrib['src']
                print img_url
            
            
            data = {
                        'url':url,
                        'img_url':img_url,
                        'title':title,
                        'mrp':mrprice,
                        'fkprice':fkprice,
                        'authors':authors,
                        'publisher':publisher,
                        'publication_year':publication_year,
                        'isbn-13':isbn_13,
                        'isbn-10':isbn_10,
                        'language':language,
                        'edition':edition,
                        'binding':binding,
                        'no_of_pages':no_of_pages,
                        'book_type':book_type
                   }
            
            scraperwiki.sqlite.save(['url'],data)
import scraperwiki           
import xlrd
import lxml.html           
xlbin = scraperwiki.scrape("http://www.converge13.com/test/Book1.xls")
book = xlrd.open_workbook(file_contents=xlbin)
sheet = book.sheet_by_index(0)   
for rownumber in range(0, sheet.nrows):
            isbn = str(int(sheet.cell(rownumber,0).value))
            url = ""
            img_url = ""
            title = ""
            mrprice = ""
            fkprice = ""
            authors = ""
            publisher = ""
            publication_year = ""
            isbn_13 = ""
            isbn_10 = ""
            language = ""
            edition = ""
            binding = ""
            no_of_pages = ""
            book_type = ""
            url = "http://www.flipkart.com/search-books?query="+isbn
            html = scraperwiki.scrape(url)
            authors =''
            root = lxml.html.fromstring(html)
            for el in root.cssselect("h1"):   
                 if el.attrib['itemprop']=="name":       
                        title = el.attrib['title']
            for el in root.cssselect("div.nprod-specs div span"):
                if el.text == "Author:" :
                    el = el.getparent()
                    for authorel in el.cssselect("a"):
                        authors += authorel.text + ", "
            
            for el in root.cssselect("span#fk-mprod-list-id"):
                mrprice = el.text
            for el in root.cssselect("span.fk-font-finalprice"):
                fkprice = el.text
            
            for tr in root.cssselect("div#specifications tr"):
                if tr.cssselect("td"):
                    tds = tr.cssselect("td")
                    if tds[0].text_content()=="Publisher":
                        publisher = tds[1].text_content()
                    elif tds[0].text_content()=="Publication Year":
                        publication_year = tds[1].text_content()
                    elif tds[0].text_content()=="ISBN-13":
                        isbn_13 = tds[1].text_content()
                    elif tds[0].text_content()=="ISBN-10":
                        isbn_10 = tds[1].text_content()
                    elif tds[0].text_content()=="Language":
                        language = tds[1].text_content()
                    elif tds[0].text_content()=="Edition":
                        edition = tds[1].text_content()
                    elif tds[0].text_content()=="Binding":
                        binding = tds[1].text_content()
                    elif tds[0].text_content()=="Number of Pages":
                        no_of_pages = tds[1].text_content()
                    elif tds[0].text_content()=="Book Type":
                        book_type = tds[1].text_content()
            
                
            for el in root.cssselect("div.image-wrapper img"):
                img_url = el.attrib['src']
                print img_url
            
            
            data = {
                        'url':url,
                        'img_url':img_url,
                        'title':title,
                        'mrp':mrprice,
                        'fkprice':fkprice,
                        'authors':authors,
                        'publisher':publisher,
                        'publication_year':publication_year,
                        'isbn-13':isbn_13,
                        'isbn-10':isbn_10,
                        'language':language,
                        'edition':edition,
                        'binding':binding,
                        'no_of_pages':no_of_pages,
                        'book_type':book_type
                   }
            
            scraperwiki.sqlite.save(['url'],data)
