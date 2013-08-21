import scraperwiki
import lxml.html, lxml.etree
import string

# List Flims from the site http://www.tamilmp3world.com

pages = [ 'http://www.tamilmp3world.com/1-list.html','http://www.tamilmp3world.com/a-list.htm', 'http://www.tamilmp3world.com/b-list.htm', 'http://www.tamilmp3world.com/c-list.htm', 'http://www.tamilmp3world.com/d-list.htm', 'http://www.tamilmp3world.com/e-list.htm', 'http://www.tamilmp3world.com/f-list.htm', 'http://www.tamilmp3world.com/g-list.htm', 'http://www.tamilmp3world.com/h-list.htm', 'http://www.tamilmp3world.com/i-list.htm', 'http://www.tamilmp3world.com/j-list.htm', 'http://www.tamilmp3world.com/k-list.htm', 'http://www.tamilmp3world.com/l-list.htm', 'http://www.tamilmp3world.com/m-list.htm', 'http://www.tamilmp3world.com/n-list.htm', 'http://www.tamilmp3world.com/o-list.htm', 'http://www.tamilmp3world.com/p-list.htm',  'http://www.tamilmp3world.com/r-list.htm', 'http://www.tamilmp3world.com/s-list.htm', 'http://www.tamilmp3world.com/t-list.htm', 'http://www.tamilmp3world.com/u-list.htm', 'http://www.tamilmp3world.com/v-list.htm', 'http://www.tamilmp3world.com/w-list.htm', 'http://www.tamilmp3world.com/y-list.htm' ];

#pages = [ 'http://www.tamilmp3world.com/n-list.htm']

uchars = [' ','&nbsp;','\n',u'\t',u'\xa0']

def removeUchars(string):
    ''' Removes unwanted chracters from the strings '''
    for uchar in uchars:
        string = string.replace(uchar,'')
    return string

def getName(row):
    ''' This function gets a lxml.html element row and returns Film name '''
    return removeUchars(row.text_content())

def getLink(row):
    ''' The getLink function gets a row and returns link '''
    link = row.cssselect('a')
    return link[0].get('href')

def getArtist(row):
    ''' This function returns the Artist '''
    tag = row.cssselect('span[class="maintextheadings"]')[0]
    return removeUchars(tag.text_content())

def getMusic(row):
    ''' This function returns the Music Director '''
    try:
        tag = row.cssselect('span[class="maintextheadings"]')[0]
        text = removeUchars(tag.text_content())
    except IndexError:
        text = 'Error'    
    return text

# Main script

for page in pages:
    html = scraperwiki.scrape(page)
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table[width='95%']")
    for table in tables:
        # Dictionary to store the links
        film ={ 'name' : '', 'link' : '', 'artist': '', 'music': ''}
        trs = table.cssselect("tr")
        film['name'] = getName(trs[0])
        film['link'] = getLink(trs[0])
        film['artist'] = getArtist(trs[1])
        film['music'] = getMusic(trs[2])
        #print film
        scraperwiki.sqlite.save(unique_keys=['name'], data=film)
