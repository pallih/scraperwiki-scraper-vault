import re
import time
import scraperwiki
from BeautifulSoup import BeautifulSoup

def extract_book_title(text):
    result = False    
    
    #try and match "title BY author"
    m = re.search('(?:\s*[A-Z]\w+?)* (?:by|BY|-)(?:\s*[A-Z][\w]*)*', text.contents[0].string)
    if m:
        full_title =  m.group(0)       
        #can't seem to access the submatches, so split up manually
        split = re.split('by|BY|-', full_title)
        if split[0] and split[1] and split[0] != '' and split[1] != ''  and split[0] != ' ' and split[1] != ' ':
            result = {'title': split[0].strip(), 'author': split[1].strip()}
    
    #try and match "author - title"
    else:
        m = re.search('(?:\s*[A-Z]\w+?)* (?:by|BY|-)(?:\s*[A-Z][\w]*)*', text.contents[0].string)        
        if m:
            full_title =  m.group(0)       
            #can't seem to access the submatches, so split up manually
            split = re.split('by|BY|-', full_title)
            if split[0] and split[1] and split[0] != '' and split[1] != ''  and split[0] != ' ' and split[1] != ' ':
                result = {'title': split[1].strip(), 'author': split[0].strip()}
    return result


def scrape_page(thread_page_url):
    print "scraping " + thread_page_url
    html = scraperwiki.scrape(thread_page_url)
    soup = BeautifulSoup(html)


    #find all the posts
    posts = soup.findAll('li', {'class': 'postbitlegacy postbitim postcontainer'})
    for post in posts:
    
        #remove any quotes
        quote = post.find('div', {'class': 'quote_container'})
        if quote:
            quote.extract()
    
        #get the post text
        post_text = post.find('div', {'class': re.compile(r'\postrow\b')}).find('blockquote')

        #get the book and author
        book_info = extract_book_title(post_text)
    
        #get the username
        #user_name = post.find('div', {'class': 'username_container'}).find('a').contents[0].string
    
        #get a link back to the original post
        url = 'http://www.urban75.net/vbulletin/' + post.find('a', {'class': 'postcounter'})['href']
    
    
        if book_info:
            #save to datastore    
            scraperwiki.datastore.save(unique_keys=['url',], data={'url': url, 'title': book_info['title'], 'author': book_info['author']})  


def main():
    
    #add new threads here
    thread_urls = ['http://www.urban75.net/vbulletin/threads/13543-*What-book-are-you-reading', 'http://www.urban75.net/vbulletin/threads/253591-*What-book-are-you-reading-%28part-2%29']
    
    for thread_url in thread_urls:
        print thread_url
        thread_html = scraperwiki.scrape(thread_url)
        thread_soup = BeautifulSoup(thread_html)


        #get the number of pages

        pagination_element = thread_soup.findAll('a', {'class': 'popupctrl'})
        max_page = int(pagination_element[2].string.split(' of ')[1])
        print "Found " + str(max_page) + " pages"

        page_number = 1
        #sanity check
        if max_page <= 300:
            while page_number <= max_page:
                scrape_page(thread_url + '/page' + str(page_number))
    
                #sleep for a couple of secs to we don't break anything
                time.sleep(5)
    
                #next page
                page_number = page_number + 1
    
main()