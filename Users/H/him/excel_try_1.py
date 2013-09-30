import scraperwiki           
import xlrd
import lxml.html           
import urllib2
import time
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
            check_url = "http://www.flipkart.com/books/pr?sid="
            temp_url = check_url
            url = "http://www.flipkart.com/search-books?query="+isbn
            html = ''
            while check_url in temp_url:
                opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
                request = opener.open(url)
                temp_url = request.url
            data = {'ISBN':isbn,'url':request.url}
            scraperwiki.sqlite.save(['url'],data)
            import scraperwiki           
import xlrd
import lxml.html           
import urllib2
import time
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
            check_url = "http://www.flipkart.com/books/pr?sid="
            temp_url = check_url
            url = "http://www.flipkart.com/search-books?query="+isbn
            html = ''
            while check_url in temp_url:
                opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
                request = opener.open(url)
                temp_url = request.url
            data = {'ISBN':isbn,'url':request.url}
            scraperwiki.sqlite.save(['url'],data)
            import scraperwiki           
import xlrd
import lxml.html           
import urllib2
import time
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
            check_url = "http://www.flipkart.com/books/pr?sid="
            temp_url = check_url
            url = "http://www.flipkart.com/search-books?query="+isbn
            html = ''
            while check_url in temp_url:
                opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
                request = opener.open(url)
                temp_url = request.url
            data = {'ISBN':isbn,'url':request.url}
            scraperwiki.sqlite.save(['url'],data)
            