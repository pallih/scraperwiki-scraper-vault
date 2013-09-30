'''
Import list of books from GoodReads.
'''
import scraperwiki
from bs4 import BeautifulSoup


URL = "http://www.goodreads.com/list/show/11516.Best_Military_Science_Fiction_Books"

page = scraperwiki.scrape(URL)
soup = BeautifulSoup(page)

table_soup = soup.find("div", {"id": "all_votes"})
all_books = table_soup.find_all("tr", {"itemtype": "http://schema.org/Book"})


books = []
for book_soup in all_books:
    new_book = {}
    new_book['title'] = book_soup.find("span", {"itemprop": "name"}).get_text()
    new_book['author'] = book_soup.find("span", {"itemprop": "author"}).get_text()
    books.append(new_book)

scraperwiki.sqlite.save(['title', 'author'], books, table_name="BestMilitarySF")


    
    '''
Import list of books from GoodReads.
'''
import scraperwiki
from bs4 import BeautifulSoup


URL = "http://www.goodreads.com/list/show/11516.Best_Military_Science_Fiction_Books"

page = scraperwiki.scrape(URL)
soup = BeautifulSoup(page)

table_soup = soup.find("div", {"id": "all_votes"})
all_books = table_soup.find_all("tr", {"itemtype": "http://schema.org/Book"})


books = []
for book_soup in all_books:
    new_book = {}
    new_book['title'] = book_soup.find("span", {"itemprop": "name"}).get_text()
    new_book['author'] = book_soup.find("span", {"itemprop": "author"}).get_text()
    books.append(new_book)

scraperwiki.sqlite.save(['title', 'author'], books, table_name="BestMilitarySF")


    
    