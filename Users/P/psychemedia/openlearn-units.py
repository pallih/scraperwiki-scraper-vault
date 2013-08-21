###############################################################################
# Basic scraper
###############################################################################

import scraperwiki,urllib
from xml.etree.ElementTree import ElementTree
url='http://openlearn.open.ac.uk/rss/file.php/stdfeed/1/full_opml.xml'
#Load the file in from the URL
f=urllib.urlopen(url)
#set up an XML flavoured object
tree = ElementTree()
#parse loaded file as an XML doc and generate an XML flavoured object
tree.parse(f)

#Search the object for body/outline elements, and return all of them along with their child nodes 
sections =tree.findall('body/outline')
#each section corresponds to a body/outline block in the original doc
for section in sections:
    #we're going to look at each section in turn; note that Python uses whitespace/indentation to define code blocks where other langs might use {}
    topic=section.attrib['text']
    #look for the text attribute of section, ie body/outline[@text] elements
    courses= section.findall('outline')
    #within each section (ie each body/outline element) find all the child outline blocks (all the body/outline/outline blocks)
    for course in courses:
        #for each of these child outline blocks, check to see if the htmlUrl attribute is there (so we're checking body/outline/outline[@htmlUrl]
        # and also check that the body/outline/outline[@text] attibute starts unit;
        if 'htmlUrl' in course.attrib and course.attrib['text'].startswith('Unit'):
            #Thus far, we know we have a block <body><outline><outline htmlURL="SOMETHING" text="Unit foo">STUFF MAYBE</outline></outline></body>
            course.attrib['text']=course.attrib['text'].replace('Unit content for ','')
            #without checking, i guess url is of form http://example.com?name=whatever_itis, or similar
            uc=course.attrib['htmlUrl'].split('?')[1].replace('name=','')
            #split the string about the ? and grab the the second (index 1, start at 0) part (so name=whatever_itis)
            #replace the name= with '', so now we have uc=whatever_itis
            pc=uc.split('_')[0]
            #split the string on the underscore and grab the first part, so pc is set to whatever
            print topic,uc, pc,course.attrib['text'],course.attrib['htmlUrl'],course.attrib['xmlUrl']
            record = { 'topic':topic,'unitcode':uc, 'parentCourseCode':pc,'name':course.attrib['text'],'url':course.attrib['htmlUrl'],'xml':course.attrib['xmlUrl']}
            scraperwiki.datastore.save(["unitcode"], record) 

'''
THIS STUFF IS ALL COMMENTED OUT
# retrieve a page
starting_url = 'http://scraperwiki.com/hello_world.html'
html = scraperwiki.scrape(starting_url)
print html
soup = BeautifulSoup(html)

# use BeautifulSoup to get all <td> tags
tds = soup.findAll('td') 
for td in tds:
    print td
    record = { "td" : td.text }
    # save records to the datastore
    scraperwiki.datastore.save(["td"], record) 
'''