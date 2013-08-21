import scraperwiki
from BeautifulSoup import BeautifulSoup
yank=True # pulls out cruft elements
shortoutput=True # doesn't display HTML

scrape = scraperwiki.scrape("http://www.publications.parliament.uk/pa/ld201011/ldbills/019/11019.1-4.html")
soup=BeautifulSoup(scrape)
#soup=soup.html.body.find(id='contentHolder').find(id='mainContents') # find body text
soup=soup.find('tbody') # better alternative which allows no-recurse etc. 

# from http://stackoverflow.com/questions/1765848/remove-a-tag-using-beautifulsoup-but-keeps-its-contents
yanklist=['table','img','font','br','td','img','br','hr','nobr','span','tbody','address','col','a'] # pull all content from these tags
while yank and soup.find(yanklist):
    for tag in soup.findAll(True):
        if tag.name in yanklist:
            tag.replaceWith(tag.renderContents())
    soup=BeautifulSoup(soup.renderContents()) # nasty! better depth-based solution?
    
# right, now take all the individual rows / lines of text and build a dictionary

rows=[]

for row in soup.findAll('tr', recursive=False): # need to walk over differently: get first 
    #if not row.find('tr'):
        rows.append({'html':row})

for row in rows:
    soup=BeautifulSoup(str(row['html'])) # why do I need to stringify?
    
    # get line no and remove para.
    lineno=soup.find(attrs={'class':'lineNumber'})
    try:
        row['lineNumber']=lineno.contents
        lineno.replaceWith('')
    except:
        pass
        
    # get line no and remove para.
    for pageno in soup.findAll(attrs={'class':'para-PageNum-only'}):
        try:
            if pageno.contents:
                row['pageNumber']=pageno.contents
            pageno.replaceWith('')
            #print soup
        except:
            pass
    
    # assertion: all p tags in row now have the same class - write that to row
    paras=soup.findAll('p')
    try:
        c=paras[0]['class']
    except:
        c=None
    if c:
        for para in paras:
            pass
            try:
                assert para['class']==c, 'class %s != %s' % (para['class'],c)
            except:
                pass
                #print paras
        row['class']=c
        
    # add text and paragraph numbers
    if paras:
        row['text']=paras[-1].contents
        if len(paras)==2:
            row['paraNumber']=paras[0].contents
    
    # now put the contents of the p's in.
    # Assumption: last one is actual text: if two, first is para.
    
    row['html']=soup 
    if shortoutput:
        del row['html']

print str(rows)
for i,row in enumerate(rows):
    row['mylineno']=i
    #scraperwiki.datastore.save(unique_keys=['lineno'], data={'lineno':i,'text':row['text'],'class':row['class']})
    scraperwiki.datastore.save(unique_keys=['mylineno'], data=row)
print "%d lines written." % len(rows)