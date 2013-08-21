import scraperwiki
import re
import json
from BeautifulSoup import BeautifulSoup

# Get bills given chamber and topic
def scrape_bill_nums(chamber, topic):
    url = 'https://www.revisor.mn.gov/bills/status_result.php?body=' + chamber + '&search=basic&session=0882013&location=House&bill=&bill_type=bill&rev_number=&keyword_type=all&keyword=&keyword_field_text=1&topic%5B%5D=' + topic + '&submit_topic=GO&titleword='
    
    soup = BeautifulSoup(scraperwiki.scrape(url))    
    bills = []    
    rows = soup('tr')
    for row in rows:
        contents = BeautifulSoup(str(row))
        try:
            bill = contents('td')[1].a.contents
            bills.append(str(bill[0]))
        except:
            pass
    return bills

# Format bill so that OS like is "SF 123"
def open_states_format(bill):
    if bill[2] == '0':
        if bill[3] == '0':
            if bill[4] == '0':
                append = " " + bill[5:]
            else:
                append = " " + bill[4:]
        else:
            append = " " + bill[3:]
        result = bill[0:2] + append
    else:
        result = bill
    return result

# Get topic list for a chamber
def get_topics_list(chamber):
    topics = []
    url = 'https://www.revisor.mn.gov/bills/status_search.php?body=' + chamber
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html)
    select = soup('select')[4] #lame, but that should be the categories select
    options = BeautifulSoup(str(select))
    for option in options('option'):
        billnumber = re.findall(r'\d+', option.contents[0])
        if billnumber == []:
            billnumber = 0
        else:
            billnumber = int(billnumber[0])
        paren1 = option.contents[0].find('(')
        topics.append([option['value'],option.contents[0][0:paren1-1],billnumber])
    return topics


# Add bill counts
def combine_bill_count(id):
    row = scraperwiki.sqlite.select("* FROM swdata WHERE topic = ? LIMIT 1", data = [id])
    if row is not None and row[0]:
        row = row[0]
        row['bill_count_upper'] = int(row['bill_count_upper']) if 'bill_count_upper' in row and row['bill_count_upper'] is not None else 0
        row['bill_count_lower'] = int(row['bill_count_lower']) if 'bill_count_lower' in row and row['bill_count_lower'] is not None else 0
        row['bill_count'] = int(row['bill_count_upper']) + int(row['bill_count_lower'])
        scraperwiki.sqlite.save(unique_keys=['topic'], data = row)


# Process a chamber
def process_chamber(chamber):
    # A basic way to store our place in the topic list by
    # using a counter
    topic_counter = 0
    topic_placeholder = scraperwiki.sqlite.get_var('topic_placeholder', 0)
    if topic_placeholder is None:
        topic_placeholder = 0
    else: 
        topic_placeholder = int(topic_placeholder)

    # Get topics
    topics = get_topics_list(chamber)

    print 'Last topic counter is: %s of %s' % (topic_placeholder, len(topics))

    for topic in topics:
        # Check place
        if (topic_placeholder > topic_counter):
            topic_counter = topic_counter + 1
            continue

        topic_counter = topic_counter + 1
        scraperwiki.sqlite.save_var('topic_placeholder', topic_counter)

        # Get bills
        bills = scrape_bill_nums(chamber, topic[0])
        
        for i in range(0,len(bills)):
            bills[i] = open_states_format(bills[i])
        
        # Save data
        if chamber == 'House': 
            data = {
                'topic': topic[1],
                'bills_lower': bills,
                'topic_id_lower': topic[0],
                'bill_count_lower': len(bills)
            }
        if chamber == 'Senate':
            data = {
                'topic': topic[1],
                'bills_upper': bills,
                'topic_id_upper': topic[0],
                'bill_count_upper': len(bills)
            }
            
        scraperwiki.sqlite.save(unique_keys=['topic'], data = data)
        
        # Get bill count by adding the two values
        combine_bill_count(topic[1])


try:
    chambers = ['Senate', 'House']
    last_chamber = scraperwiki.sqlite.get_var('chamber', 'Senate')
    if (last_chamber is not None and last_chamber == 'House'):
        chambers = ['House', 'Senate']

    print 'Last chamber scraped is: ' + last_chamber

    for chamber in chambers:
        print 'Getting data for: ' + chamber

        # If not the first chamber, then start topic placeholder
        # over
        if last_chamber != chamber:
            scraperwiki.sqlite.save_var('topic_placeholder', 0)

        # As this script takes time and power, we need to save our
        # state so that we can make it through everything.
        scraperwiki.sqlite.save_var('chamber', chamber)
        process_chamber(chamber)

except scraperwiki.CPUTimeExceededError:
    # This just makes sure the scraper is not marked
    # as erroring even if it times out
    pass