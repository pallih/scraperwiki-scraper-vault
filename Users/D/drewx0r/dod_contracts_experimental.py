import scraperwiki                  # To screen scrape
import lxml.html                    # To parse HTML
from lxml.html.clean import Cleaner # To get rid of unneeded HTML tags
import re                           # Gotta have my regex
import time                         # time is on my side. (date operations)
from decimal import *



def scrape_and_move_on(html,starting_url):
    # initialize variables
    company = ''                                                  # variable for the company name. name will be changed to be more professional. 
    amount = ''                                                   # variable for the dollar amount. name will similarly be changed
    branch = ''                                                   # variable for the branch of the military. this is perfectly professional
    cleaner = Cleaner(allow_tags=['p','strong'], remove_unknown_tags=False) # make a vacuum to vacuum out every tag but <p> and <strong>
    supercleaner = Cleaner(allow_tags=['p'], remove_unknown_tags=False)     # make a vacuum to vacuum out every tag but the <p> tag


    # get date
    datestring = re.search(r'\S*\s\d\d, \d\d\d\d', html).group(0) # find the date string on the page
    date = time.strptime(datestring, '%B %d, %Y')                 # encode the date as a date using format Month dd, YYYY
    date = time.strftime('%Y-%m-%d', date)                        # decode that date back into a string of format YYYY-mm-dd

    #parse html
    root = lxml.html.fromstring(html)                             # turn our HTML into an lxml object
    ps = root.cssselect('p')                                      # get all the <p> tags
    for p in ps:                                                  # loop through each <p> tag
        p = supercleaner.clean_html(p)                                 # Clean out all the HTML tags (if you don't, p.text will stop when it hits the first tag)
        newp = p.text                                             # initialize contents of p as a string.
        print lxml.html.tostring(p)
        # find possible branch headings
        if newp and re.sub(r'[\(\)0-9]','',newp.upper()) == newp:  # Eliminating parens gets rid of false positive. I don't think any branches have parens. I'll check.
            if p.text.strip():                          # Make sure the text isn't just whitespace
                branch = p.text.title().strip()                    # Set the branch name to the text of the tag, make it title case, and strip out whitespace

        # parse contract paragraphs for company and amount
        elif newp and len(newp.split()) > 10:         # If it exists, is not a branch heading, and is longer than 10 words (gets rid of cruft)
            newp = newp.strip()                                   # The text of the p tag without any leading or trailing whitespace
            a = re.split(",? is|,? are|,? were|,? was|,? will|,? received|,? has been|,? awarded", newp)   # split the paragraph right after the business name(s) and location.
            if a[1] and len(a[0].split()) <= 5 and ("Air Force" in a[0] or "Missile Defense Agency" in a[0]):
                a = re.split("(?:(?:contract )?(?:,? to |,? with |,? for |,? under |\:(?:\xa0| )))|(?:\.\\xa0 )",a[1])
                if a[1].find(" awarding") == 0:
                    a = re.split(" awarding |(?:[,.] a)",a[1])
                    company = a[1]
                else:
                    company = a[1]
            else:
                company = a[0]                                        # grab the first element of the array (company and location)
            b = re.findall(r"(\$[0-9,.\s]*[0-9](?: million| billion)?)", newp) # search for all dollar amounts and return a list. 
            if b:                                                # if there's anything in the list
                amountarray = [Decimal(re.sub('[^0-9.]','', x)) for x in b]  # strip all non-decimal characters from each string in the list and convert to decimal
                # multiply it by a million or a billion if required
                for i in range(len(b)):
                    if "million" in b[i]: 
                        amountarray[i] = int(amountarray[i] * 1000000)
                    elif "billion" in b[i]:
                        amountarray[i] = int(amountarray[i] * 1000000000)
                maxamount = max(amountarray)                    # find the largest dollar value listed
                minamount = min(amountarray)                    # find the smallest dollar value listed
            else:
                minamount = ""                                     # if the list is empty, just return nothing for the amount.
                maxamount = ""
            findcontract = re.search(r'( firm| fixed| cost| modification .* previously awarded| indefinite| order against).*?( contract| agreement)( to exercise [a-zA-Z0-9 ]* for)?',newp.lower())
            contracttype = ''
            if findcontract:
                contracttype = findcontract.group(0).strip()
            elif "modification" in newp:
                contracttype = "contract modification"

            contractnum = re.findall(r'\((\w{5,6}\s*?[-/].*?)\)',newp)
            if len(contractnum) is 0:
                contractnum = re.findall(r'\w{5,6}\s*?[-/]\s*\w{2}\s*[-/]\s*\w\s*[-/]\s*\w{3,4}', newp) # Ugly regex to find all contract numbers in a paragraph
            contract = ''                                                    # Initialize contract variable
            for i in range(0,len(contractnum)):                              # Loop through each one
                contractnum[i] = re.sub(r'(\d)\s(\d)',r'\1-\2',contractnum[i]) #change whitespace between two digits to a hyphen
                contractnum[i] = re.sub(r'\s','',contractnum[i])             # Strip out whitespace anywhere in the contract number
                contractnum[i] = re.sub(r'/','-',contractnum[i])             # Change / to - to standardize the format
                contract = contract + ' ' + contractnum[i]                   # append each contract number

            # initialize the record data structure and populate it with data
            record = {}                                            
            record["URL"] = starting_url
            record["Company"] = company
            record["MinAmount"] = minamount                           
            record["MaxAmount"] = maxamount                              
            record["Branch"] = branch                              
            record["Date"] = date                                  
            record["Contract"] = contract
            record["Details"] = newp
            record["Type"] = contracttype
            scraperwiki.sqlite.save(["Contract"], record)          # save the record


# Code starts here.
html = scraperwiki.scrape('http://www.defense.gov/contracts')      # scrape the recent contracts page
lastcontracts = re.search('contractid=\d{4,}', html)               # find the number of the most recent contracts day
lastcontracts = int(lastcontracts.group(0).replace('contractid=','')) # isolate the number and make it an integer.

if scraperwiki.sqlite.get_var('last_page') == None:
    firstcontracts = 390
else:
#    firstcontracts = scraperwiki.sqlite.get_var('last_page')
    firstcontracts = 390
if firstcontracts >= lastcontracts:
    pass
    print "no new contracts"
else:
    for x in range(3312+1,3313+1):                                # (the +1 is because python excludes the end of the range.
        base_url = 'http://www.defense.gov/contracts/contract.aspx?contractid='  # the base URL
        starting_url = base_url + str(x)                                         # the base URL with the contract ID tacked on
#        print x
        while True:
            try:
                html = scraperwiki.scrape(starting_url)                           # scrape the contracts page
            except:
                continue
            break
        if "The Official Home of the Department of Defense" not in html:  # make sure we haven't been redirected to defense.gov because the page doesn't exist.
            # The following lines manipulate the HTML in several ways to account for different formatting methods
            html = re.sub("<div><span>","<p>",html)
            html = re.sub('<div align="center"><strong>','<p><strong>',html)
            html = re.sub('div style="MARGIN: 0in 0in 0pt"','p',html)
            html = re.sub(r'<(/?)b>',r'<\1strong>',html)
            html = re.sub(r'(?i)<H(3|4)>(.*)</H\1>',r'<p><strong>\2</strong></p>',html)
            html = re.sub(r'[\n\r]',' ', html)
            html = re.sub('<div STYLE="font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #000000;">','<P>',html)
            scrape_and_move_on(html,starting_url)                                      # this runs the scrape function above
    
#        print html

scraperwiki.sqlite.save_var('last_page', lastcontracts)
print scraperwiki.sqlite.get_var('last_page')