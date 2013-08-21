import scraperwiki           
html = scraperwiki.scrape("http://www.flipkart.com/dell-vostro-1550-2nd-gen-ci5-4-gb-500-windows-7-home-basic/p/itmd8d663ec8fybp")
print html


from BeautifulSoup import BeautifulSoup

soup = BeautifulSoup(html)
print soup.prettify()