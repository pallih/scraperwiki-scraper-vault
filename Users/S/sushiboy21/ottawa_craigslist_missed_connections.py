import scraperwiki 
import scraperwiki

import re
import time

# The function that will scrape each index page, parse out the ID numbers for each post, scrape each post, parse them, and save the data
def our_scraper(our_url):
    the_page = scraperwiki.scrape(our_url)
    for every_post in re.finditer('<a href="http://ottawa.en.craigslist.ca/mis/(.+?).html">.+?</a>', the_page):
                
                # Extracts the id number for each hyperlink from the list of Missed Connection postings    
                post_id = every_post.group(1)
                
                # Creates the URL for the full listing of each post. EDIT THIS FOR YOUR CITY'S craigslist URL
                full_listing_url = "http://ottawa.en.craigslist.ca/mis/" + str(post_id) + ".html"
                
                # Scrapes the post    
                full_listing = scraperwiki.scrape(full_listing_url)
                
                # removes the hard returns in the HTML of the post to make it easier to parse
                full_listing = re.sub("\n","",full_listing)

                # Uses regular expression to parse out the title of the post
                post_title = re.search("<h2>(.+?)</h2>", full_listing).group(1)
                
                # Tries a regular expression to pull out the gender designator from the title. If can't find, sets gender variable to "NOT SPECIFIED"
                try:
                    post_gender = re.search("- (\D+4\D+)", post_title).group(1)
                    post_gender = re.sub("-","", post_gender)
                    post_gender = re.sub("\(.+?\)","", post_gender)

                except:
                    post_gender = "NOT SPECIFIED"

                # Pulls out the age of from the title, where specificed
                try:
                    post_age = re.search("- (\d+)", post_title).group(1)
                except:
                    post_age = ""
    

                # Pulls out the date and time from the post listing
                post_date = re.search("<hr>Date: (.+?)<br>", full_listing).group(1)
             
                
                # Pulls out the full text of the post, takes out the HTMT tags
                post_text = re.search('<div id="userbody">(.+?)<!', full_listing).group(1)
                post_text = re.sub("<.+?>"," ", post_text)


                print post_title, post_gender, post_age, post_text, post_date

                # Saves it all to our datastore
                try:
                    scraperwiki.sqlite.save(unique_keys=["post_id"],data={"post_id": post_id, "post_title": post_title, "post_gender": post_gender, "post_age": post_age,"post_date": post_date,"post_text": post_text,})    
                except:
                    pass
                time.sleep(1)

base_link = "http://ottawa.en.craigslist.ca/mis/index"
base_number = 0


# The loop that will call the function with a different URL for each index page of Missed Connection listings   
# Setting the base_number to 500 will scrape 5 pages. You can change it if there are more available for your city

while base_number < 500:
    our_url  =  base_link + str(base_number) + ".html"
    our_scraper(our_url)
    base_number = base_number + 100
    # Puts in a breather to avoid overloading the server
    time.sleep(2)