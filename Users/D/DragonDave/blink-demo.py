import scraperwiki
import requests
import lxml.html
html2text=scraperwiki.swimport('html2text')

# Blank Python

# get lxml chunks
url='http://online.businesslink.gov.uk/bdotg/action/printguide?r.l1=1079717544&r.l2=1084228483&r.l3=1084228524&r.l4=1084304680&topicId=1084304680'
html=requests.get(url).content
root=lxml.html.fromstring(html)
data={}
maincontent=root.get_element_by_id('maincontent')
addcontent=root.get_element_by_id('additionalContent')
print lxml.html.tostring(maincontent)
print lxml.html.tostring(addcontent)

# parse maincontent
h1=maincontent.cssselect('h1')[0]
data['title']=h1.text
h1.drop_tree()
data['rawhtml']=lxml.html.tostring(maincontent)
data['rawmarkdown']=html2text.html2text(data['rawhtml'])

#parse additionalContent
# http://stackoverflow.com/questions/8050929/select-divs-between-html-comments-in-lxml
help=root.xpath("//*[preceding-sibling::comment()[. = ' Helplines '] and following-sibling::comment()[. = ' Internal Links']]")
data['help']={}
h3=None
for item in help:
    if item.tag=='h3':
        if h3:
            data['help'][h3]=contents
        h3=item.text
        contents=[]
    elif item.tag=='p':
        contents.append(item.text)
    else:
        assert False
data['help'][h3]=contents

external=root.xpath("//p[preceding-sibling::comment()[. = ' External Links ']]")
data['externals']=[]
for item in external:
    b=item.cssselect('b')[0]
    name=b.text
    b.drop_tree()
    data['externals'].append ({'name': name, 'url': item.text_content()})

# rebuild markdown
externalmd='\n\n'.join(['[%s](%s)'%(i['name'],i['url']) for i in data['externals']])
buildhelp=[]
for i in data['help']:
    buildhelp.append( '### %s\n%s'%(i, ', '.join(data['help'][i])))
helpmd='\n\n'.join(buildhelp)
print externalmd

data['markdown']='\n\n'.join(['## Introduction', data['rawmarkdown'], '* * *', '## Further Information', helpmd, externalmd])

print data['markdown']
