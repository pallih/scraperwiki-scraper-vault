import mechanize
import httplib
import re
import scraperwiki
import xml.sax.saxutils as saxutils
import json
import urllib2
import urllib
import time
from BeautifulSoup import BeautifulSoup


# Useful stuff for parsing
rcs_pattern = re.compile("[0-9]{3} [0-9]{3} [0-9]{3}")
name_pattern = re.compile("Nom commercial :")    
count_pattern = re.compile("([1-9][0-9]*) entreprises")


def expand_task_queue(name, dept):
    '''
    Expand the tasks queue for this name in the departement
    Concretely, add a new a-z at the end of name and append
    '''
    for extra_letter in range(ord('a'),ord('z')+1):
        if chr(extra_letter) != name[-1]:
            create_task(name + chr(extra_letter), dept)


def load_task_queue():
    '''
    Get the queue of tasks
    Returns a list of {name, dept} pairs
    '''
    try:
        # Here we don't expect to have the time to deal with more than 500 tasks per run
        tasks = scraperwiki.sqlite.select("dept,name from tasks where done=0 limit 800")
    except:
        return []
    return tasks


def init_task_queue():
    '''
    Initialise the queue of tasks
    Fetch the list of departements and fill the table with {a-z, dept} pairs
    '''
    # Get the list of departements from an other scraper
    depts = json.loads(scraperwiki.scrape("http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=french-departments&query=select%20name%2Cnumber%20from%20swdata"))
    for dept_index in range(scraperwiki.sqlite.get_var('index', 0), len(depts)):
        for name in range(ord('a'),ord('z')+1):
            create_task(chr(name), depts[dept_index]['number'])


def create_task(name, dept):
    '''
    Creates a new task
    '''
    record = {'name' : name, 'dept' : dept, 'done' : False}
    scraperwiki.sqlite.save(['name', 'dept'], record, table_name="tasks")


def mark_task_done(name, dept, results):
    '''
    Mark a task as done and save the number of results
    '''
    record = {'name' : name, 'dept' : dept, 'done' : True, 'number_records' : results}
    scraperwiki.sqlite.save(['name', 'dept'], record, table_name="tasks")


def get_page(br, page, params = None):
    '''
    Fetch a page using the globally defined browser "br"
    '''
    #start = time.time()
    if params != None:
        params = urllib.urlencode(params)
    response = br.open(page, params)
    document = BeautifulSoup(response.get_data())
    #print "Get page = %d seconds" % (time.time()-start)
    return document


def get_companies(br, name, dept):
    '''
    Issue the search for all the companies in "dept" having "name" as part of their name
    '''
    # Issue the search
    document = get_page(br, "http://www.infogreffe.fr/infogreffe/newRechercheEntreprise.xml", {"denomination" : name, "departement" : dept})

    # Process pages until there is no next page
    count = 0
    stop = False
    while not stop:
        # Process all the companies listed on the page
        for entreprise in document.findAll('td', attrs={'class':'entreprise'}):
            process_entreprise(dept, entreprise)
            count = count + 1
    
        # Get the next page if there is one
        stop = True
        links = [l for l in br.links(text_regex=r"Suivant")]
        if len(links) > 0:
            offset=re.sub(r'javascript:switchPage\(([0-9]*)\)', '\g<1>', links[0].url)
            document = get_page(br, "http://www.infogreffe.fr/infogreffe/includeEntrepListe.do?_=&entrepGlobalIndex=%s&index=rcs&tri=PERTINENCE" % offset)
            stop = False

    # Return the number of results fetched (maximum is 100)
    return count



def process_entreprise(dept, entreprise):
    '''
    Process an HTML block with the description of the entreprise and store a new record for it
    '''
    # Create the record and get the name of the company and the url
    record = {}
    record['CompanyName'] = re.sub(r'[\t\r\n]', '', entreprise.contents[1].text)
    record['RegistryUrl'] = 'http://www.infogreffe.fr' + entreprise.contents[1].get('href')

    # Process all the other data in the description
    for i in range(2,len(entreprise.contents)):
        item = re.sub(r'[\t\r\n]', '', saxutils.unescape(str(entreprise.contents[i]), entities = {'&egrave;' : 'è', '&amp;' : '&', '&quot;' : '"', '&nbsp;' : ''}))

        # Get the company number
        if rcs_pattern.search(item):
            record['CompanyNumber'] = re.sub(r' ', '', re.findall(r'[0-9]{3} [0-9]{3} [0-9]{3}', item)[0])
            blocks = item.split('R.C.S. ')
            if len(blocks) == 2:
                record['RegistrationCity'] = blocks[1]

        # Get its location
        zipcode_pattern = re.compile(dept + "[0-9]{3} ")
        if zipcode_pattern.search(item):
            address=item.split(' - ')
            record['Location'] = re.sub(r' {2,30}', '', address[0])
            if len(address) == 2:
                record['BuildingAtLocation'] = re.sub(r' {2,30}', '', address[1])

        # Get its activity (last info when it is not an address)
        if i==len(entreprise.contents)-1 and zipcode_pattern.search(item) == None:
            record['EntityType'] = item

        # Get its commercial name
        if name_pattern.search(item):
            record['CommercialName'] = re.sub(r' {2,30}', '', item.replace('Nom commercial :', ''))
        
    # Save the new record
    if 'CompanyNumber' in record.keys():
        scraperwiki.sqlite.save(["CompanyNumber"], record)


def go():
    '''
    Main procedure of the scraper. Creates a browser, load the list of tasks and execute them
    '''
    try:
        # Prepare the browser
        cookies = mechanize.CookieJar()
        opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
        mechanize.install_opener(opener)
        br = mechanize.Browser()
        br.set_handle_robots(False)
        br.set_handle_refresh(False)
        br.set_handle_referer(False)
        br.open("http://www.infogreffe.fr/infogreffe/process.do")
    
        # Get the list of tasks
        tasks = load_task_queue()
        if len(tasks) == 0:
            # If there is no task to execute, init/reset the table
            init_task_queue()
            tasks = load_task_queue()
    
        for task in tasks:
            try:
                # Execute the task
                results = get_companies(br, task['name'], task['dept'])
        
                # If we hit the soft limit, add more refined searches to the queue
                if results == 100:
                    print "Limit reached for %s in %s, adding new tasks" % (task['name'], task['dept'])
                    expand_task_queue(task['name'], task['dept'])
    
                # Mark the task as done 
                mark_task_done(task['name'], task['dept'], results)
            except Exception as detail:
                # We may get an exception for using too much CPU time.
                print "Exception raised", detail 
    except Exception as detail:
        # If we can't open the browser, just skip running the scraper
        print "Failed starting browser ", detail



#
# Run the scraper
#
go()


#results = get_companies(br, "a", "95")
#print "Got %d results " % results

