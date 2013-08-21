import scraperwiki
import mechanize
import re
import time
import cookielib
from BeautifulSoup import BeautifulSoup
# TO-DO:
# Seeding this database looks to be difficult
# because of number of pages needed to be
# scraped. Need to figure out how to speed
# everything up so it doesn't exceed CPU time.



# Initialize browser and set details.
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# All the states and the associated links to the petitions.
# Testing with DE because The First State rocks.
STATES = [
    # {'name': "AL",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-alabama-withdraw-united-states-america-and-create-its-own-new-government/2TvhJSSC",
    # ]},
    # {'name': 'AK','urls':[
    #     "https://petitions.whitehouse.gov/petition/allow-alaskans-free-and-open-election-decide-whether-or-not-alaska-should-secede-united-states/T7mz4lzx",
    # ]},
    # {'name': "AZ",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-arizona-withdraw-united-states-america-and-create-its-own-new-government/GrZPNqcX",
    # ]},
    # {'name': 'AR','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-arkansas-withdraw-united-states-and-create-its-own-new-government/k6LhPsBX",
    # ]},
    # {'name': "CA",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-california-withdraw-united-states-america-and-create-its-own-new-government/Rfg4ZhhC",
    # ]},
    # {'name': 'CO','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-colorado-withdraw-united-states-america-and-create-its-own-new-government/lWDshfl3",
    # ]},
    # {'name': "CT",'urls': None},
    {'name': 'DE','urls': [
        "https://petitions.whitehouse.gov/petition/peacefully-grant-state-delaware-withdraw-united-states-america-and-create-its-own-new-government/Mbz8QFQr",
    ]},
    # {'name': "FL",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-florida-withdraw-united-states-america-and-create-its-own-new-government/D87Rv7yJ",
    # ]},
    # {'name': 'GA','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-georgia-withdraw-united-states-america-and-create-its-own-new-government/pgJ9JLY3",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-georgia-withdraw-united-states-america-and-create-its-own-new-government/zXYY751D",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-georgia-withdraw-united-states-america-and-create-its-own-new-government/QKgYGBgZ"
    # ]},
    # {'name': "HI",'urls': None},
    # {'name': 'ID','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-idaho-withdraw-united-states-america-and-create-its-own-new-government/wqKSjw5P",
    # ]},
    # {'name': "IL",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-illinois-withdraw-united-states-america-and-create-its-own-new-government/3D1qh2hg",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-illinois-withdraw-united-states-america-and-create-its-own-new-government/95d2JNCj"
    # ]},
    # {'name': 'IN','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-indiana-withdraw-united-states-america-and-create-its-own-new-government/51jYVZ5L",
    # ]},
    # {'name': "IA",'urls': None},
    # {'name': 'KS','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-kansas-withdraw-united-states-america-and-create-its-own-new-government/k96nJrY6",
    #     "https://petitions.whitehouse.gov/petition/petition-peaceful-secession/zmshT35Q"
    # ]},
    # {'name': "KY",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-kentucky-withdraw-united-states-america-and-create-its-own-new-government/RskKYzB6",
    # ]},
    # {'name': 'LA','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-louisiana-withdraw-united-states-america-and-create-its-own-new-government/1wrvtngl",
    # ]},
    # {'name': "ME",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-maine-withdraw-united-states-america-and-create-its-own-new-government/JZv4N6HN",
    # ]},
    # {'name': 'MD','urls': None},
    # {'name': "MA",'urls': None},
    # {'name': 'MI','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-michigan-withdraw-united-states-america-and-create-its-own-new-government/022SsMWp",
    # ]},
    # {'name': "MN",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-minnesota-withdraw-united-states-america-and-create-its-own-new-government/bzct9Ypl",
    # ]},
    # {'name': 'MS','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-mississippi-withdraw-united-states-america-and-create-its-own-new-governmen/9M9rdL8n",
    # ]},
    # {'name': "MO",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-missouri-withdraw-united-states-america-and-create-its-own-new-government/Vd92R3YG",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-missouri-withdraw-united-states-america-and-create-its-own-new-government/JMknspGz"
    # ]},
    # {'name': 'MT','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-montana-withdraw-united-states-america-and-create-its-own-new-government/l76dWhwN",
    # ]},
    # {'name': "NE",'urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-nebraska-withdraw-united-states-and-create-its-own-new-government/Jf5xVXrS",
    # ]},
    # {'name': 'NV','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-nevada-withdraw-united-states-america-and-create-its-own-new-government/3ff8v0HR",
    # ]},
    # {'name': "NH",'urls': [
    #     "https://petitions.whitehouse.gov/petition/grant-state-new-hampshire-withdraw-united-states-america-and-create-its-own-new-government/hdTc6HPn",
    # ]},
    # {'name': 'NJ','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-new-jersey-withdraw-united-states-america-and-create-its-own-new-government/RYvjgdDT",
    # ]},
    # {'name': 'NM','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-new-mexico-withdraw-united-states-america-and-create-its-own-new-government/mzXG7MtY",
    # ]},
    # {'name': 'NY','urls': [
    #     "https://petitions.whitehouse.gov/petition/allow-new-york-secede-united-state-goverment-peacefully-and-allow-it-form-its-own-government/fvr0tjBZ",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-new-york-withdraw-united-states-america-and-create-its-own-new-government/RSBkpCf9"
    # ]},
    # {'name': 'NC','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-north-carolina-withdraw-united-states-and-create-its-own-new-government/rx1KDYTs",
    # ]},
    # {'name': 'ND','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-north-dakota-withdraw-usa-and-create-its-own-new-government/lqPGbvVl",
    # ]},
    # {'name': 'OH','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-republic-ohio-withdraw-united-states-america-and-create-its-own-new-government/cNKXQpjG",
    #     "https://petitions.whitehouse.gov/petition/allow-peaceful-withdrawal-ohio-united-states-america-such-it-becomes-its-own-free-nation/xKLK11kk"
    # ]},
    # {'name': 'OK','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-oklahoma-withdraw-united-states-america-and-create-its-own-new-government/p5whtmhh",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-oklahoma-withdraw-united-states-america-and-create-its-own-new-government/Z0G2vNtF"
    # ]},
    # {'name': 'OR','urls': [
    #     "https://petitions.whitehouse.gov/petition/allow-oregon-vote-and-leave-union-peacefully-and-remain-ally-nation/X3kWX8kF",
    # ]},
    # {'name': 'PA','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-pennsylvania-withdraw-united-states-america-and-create-new-government/kT8FL7Ng",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-pennsylvania-withdraw-united-states-america-and-create-its-own-new-government/0d7vMsmb"
    # ]},
    # {'name': 'RI','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-allow-state-rhode-island-secede-united-states-america-and-create-new-government/6Wfk18XN",
    # ]},
    # {'name': 'SC','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-sc-withdraw-united-states-america-and-create-its-own-new-government/KL6qrls8",
    #     "https://petitions.whitehouse.gov/petition/state-south-carolina-secede-union-and-form-its-own-government-sovereign-state/LFzSJVkP"
    # ]},
    # {'name': 'SD','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-south-dakota-withdraw-united-states-america-and-create-its-own-new-government/FDs7lQJZ",
    # ]},
    # {'name': 'TN','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-tennessee-withdraw-united-states-america-and-create-its-own-new-government/7xsNwkJ8",
    # ]},
    # {'name': 'TX','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-texas-withdraw-united-states-america-and-create-its-own-new-government/BmdWCP8B",
    # ]},
    # {'name': 'UT','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-utah-withdraw-united-states-america-and-create-its-own-new-government/5wcYddXK",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-utah-withdraw-united-states-america-and-create-its-own-new-government/8TlFpQS3"
    # ]},
    # {'name': 'VT','urls': None},
    # {'name': 'VA','urls': [
    #     "https://petitions.whitehouse.gov/petition/allow-state-virginia-vote-peacefully-leaving-united-states/9b73XTSr",
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-virginia-withdraw-united-states-america-and-create-its-own-new-government/pBLTRmfR"
    # ]},
    # {'name': 'WA','urls': None},
    # {'name': 'WV','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-west-virginia-withdraw-united-states-america-and-create-its-own-new-govern/VkP6lCFT",
    # ]},
    # {'name': 'WI','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-allow-state-wisconsin-withdraw-united-states-america-and-create-its-own-new-government/421C1h6t",
    # ]},
    # {'name': 'WY','urls': [
    #     "https://petitions.whitehouse.gov/petition/peacefully-grant-state-wyoming-withdraw-united-states-america-and-create-its-own-new-government/BLQnDS9w",
    # ]},
]

def follow_link(link):
    """
        This is my attempt at dealing with
        503 errors that pop up every so often:
            sleep for 5 secs. and try again.
    """
    try:
        br.follow_link(link)
    except mechanize.HTTPError, e:
        print "Caught http error ", e.code
        time.sleep(5)
        follow_link(link)
    except mechanize.URLError, e:
        print "Url Error: ", e.reason

def get_details(signature):
    """
        Returns the details for each signature.
    """
    name = signature.find('div', attrs={'class': 'name'}).text.strip().encode('utf8', 'replace') # No encoding = fails.
    details = signature.find('div', attrs={'class': 'details'}).contents  # Location, date and signature number, separated by <br>
    sig_num = int(details[4].split("#")[1].strip().replace(",", ""))
    location = details[0].lstrip(' \n').encode('utf8', 'replace')
    date = details[2].lstrip(' \n').encode('utf8', 'replace')
    return name, sig_num, location, date

def get_signatures(html):
    """
        Each signature has a class of
        "entry entry-reg"
    """
    soup = BeautifulSoup(html)
    signatures = soup.findAll('div', attrs={'class': re.compile(r'\bentry-\b')})
    return signatures

for state in STATES:
    if state['urls'] is None:
        pass
    else:
        for url in state['urls']:
            scrape = True
            all_sig_nums = []
            url_id = url.split("/")[-1]
            
            try:
                last_highest = scraperwiki.sqlite.get_var(url_id)
            except:
                last_highest = 0

            try:
                br.open(url)
            except mechanize.HTTPError, e:
                print "Caught error: ", e.code
            except mechanize.URLError, e:
                print "URL error: ", e.reason

            link = br.find_link(url_regex="\?page=")
            
            while link and scrape:
                signatures = get_signatures(br.response().read())
                for signature in signatures:
                    name, sig_num, location, date = get_details(signature)
                    if sig_num == 1:
                        pass
                    else:
                        all_sig_nums.append(sig_num)
                    uid = str(sig_num) + "_" + url_id
                    entry = {'uid':uid, 'pstate': state["name"], 'name': name, 'location': location, 'date': date, 'number': sig_num, 'link': url}
                    scraperwiki.sqlite.save(['uid'], entry, table_name=state['name'], verbose=0)   
                
                follow_link(link)
                
                try:
                    link = br.find_link(url_regex="\?page=")  # Pages have scrollspy that hit a link with this in url. We just follow it.
                except:
                    link = None
                
                if min(all_sig_nums) <= last_highest:
                    scrape = False
                

            scraperwiki.sqlite.save_var(url_id, max(all_sig_nums))
