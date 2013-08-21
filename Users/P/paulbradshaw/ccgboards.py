import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_divs(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
#MAY BE BETTER TO USE     rows = root.cssselect("article div")  
#ALSO CAN THEN ADD alltext = row[0].text_content()
    #line below selects all <div class="block size3of4"> - note that because there is a space in the value of the div class, we need to put it in inverted commas as a string
    rows = root.cssselect("div.'block size3of4'")  
    for row in rows:
        # Set up our data record - we'll need it later
        print row
        record = {}
        #initialise the variables here, otherwise they won't exist if the 'if' tests aren't met below, and an error will be generated
        membername = ""
        membertitle = ""
        memberbiog = ""
        #grab all <h4> tags within our <div>
        h4s = row.cssselect("h4")
        print h4s        


ccglist = ['www.brentccg.nhs.uk/', 'www.ealingccg.nhs.uk/', 'www.hounslowccg.nhs.uk/', 'www.westlondonccg.nhs.uk/', 'www.centrallondonccg.nhs.uk/', 'www.harrowccg.nhs.uk/', 'www.hammersmithfulhamccg.nhs.uk/']
for ccg in ccglist:
    scrape_divs('http://'+ccg+'about-us/board.aspx')
