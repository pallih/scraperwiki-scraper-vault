# This won't work yet as ScraperWiki doesn't have Selenium support :)

# Example of screen scraping with Selenium.

# Download Selenium 2 and run its remote backend:
#   java -jar selenium-server-standalone-2.0b1.jar 
# Install Python bindings (docs here: http://pypi.python.org/pypi/selenium/2.0-dev)
#   pip install -U selenium

# TODO:
# Make sure it kills any left over sessions somehow. See:
# http://stackoverflow.com/questions/1317844/how-to-close-a-browser-on-a-selenium-rc-server-which-lost-its-client
# Maybe just brutally kill any long running firefox processes?

import sys
from selenium import selenium

# Don't try google-chrome, doesn't work: http://jira.openqa.org/browse/SRC-740
s = selenium("localhost", 4444, "*firefox", "http://localhost/")
s.start()

# Demonstrate it on a fancy ASP example with Javascript
s.open("http://recognition.ncqa.org/PSearchResults.aspx?state=NY&rp=")

while 1:
    # Print page number we are on
    s.wait_for_page_to_load(30000) # timeout in milliseconds
    print s.get_text("css=//span[id=ProviderSearchResultsTable1_lblPhysicianCount]")

    # Can save source here or use in BeautifulSoup etc. - can't work out how to
    # loop over elements in Selenium, even Selenium 2. Answers here might help:
    # http://stackoverflow.com/questions/3943997/get-text-from-all-elements-matching-a-pattern-in-selenium
    # s.get_html_source()

    # Go to next page
    try:
        s.click("//a[contains(text(),'Next Page')]")
    except Exception:
        print "Next Page link not found"
        sys.exit()
