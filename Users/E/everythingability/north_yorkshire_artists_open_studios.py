# See below...
from BeautifulSoup import BeautifulSoup
import scraperwiki, re, urllib, urlparse
print "starting..."

def match(s, reg):
    p = re.compile(reg, re.IGNORECASE| re.DOTALL)
    results = p.findall(s)
    return results

urls = ['http://nyos.org.uk/Artists-Makers.aspx?&fR=0&nR=126',
        'http://nyos.org.uk/Artists-Makers.aspx?&fR=16&nR=126',
        'http://nyos.org.uk/Artists-Makers.aspx?&fR=32&nR=126',
        'http://nyos.org.uk/Artists-Makers.aspx?&fR=48&nR=126',
        'http://nyos.org.uk/Artists-Makers.aspx?&fR=64&nR=126',
        'http://nyos.org.uk/Artists-Makers.aspx?&fR=80&nR=126',
        'http://nyos.org.uk/Artists-Makers.aspx?&fR=96&nR=126',
        'http://nyos.org.uk/Artists-Makers.aspx?&fR=112&nR=126',
        ]

example = '''<div class="artist-card floatLeft"><a href="Artist.aspx?id=152"><img align="left" src="img-artists/Sarah_Denny/Denny_Sarah1.jpg" width="150px" alt="Sarah Denny" /></a><a class="artists-name" href="Artist.aspx?id=152">43 Sarah Denny</a><br />
Sarah Denny is a silversmith committed to hand-making silver vessels using traditional hammering techniques. Her work consists of one-off, sculptural objects, which emphasise the beauty of form in sil ... </div>
'''

pattern = 'Artist\.aspx\?id=[0-9]*'


def get_artists( url ):
    html = scraperwiki.scrape( url )
    item = {'url': url, 'html':html}
    #soup = BeautifulSoup( html )
    #artists = soup.findAll({'class':'artist-card'})
    
    artists_urls = match( html, pattern)

    
    fixed_urls = []
    for a_url in artists_urls:
        fixed_urls.append( urlparse.urljoin(url, a_url) )

    return fixed_urls

items = []    

for url in urls:
    items = items + get_artists( url )





'''    <div id="artists-details">
        <span class="title">17 Val Emmerson</span>
Scar Lodge<br />
Hardy Grange<br />
Grassington<br />North Yorkshire<br />BD23 5AJ<br /><br />

Tel 01756 753388<br /><br />
<span class="title">Websites</span>
<a href="http://www.val-emmerson-art.co.uk" target="_blank">Val Emmerson Art</a><br /><br /><span class="title">Email</span><a href="mailto:val@grassington.plus.com">val@grassington.plus.com</a><br /><br />
<span class="title">Directions</span>From Grassington Square, take small road, Ghylls Fold, down side of folk museum, into Hardy Grange, passing 'private road' sign. Take first left and Scar Lodge is on right.<br /><br />
<span class="title">Parking</span>On site for six cars, other parking in village.<br /><br />
<span class="title">Price Range</span>&#163;2 to &#163;600<br /><br />

<span class="title">Statement</span>After a twenty-year nursing career, Val fulfilled an ambition by attending art school, taking a foundation course at Hornsey College of Art &amp; Design and a degree in textiles, with printmaking and drawing, at West Surrey College of Art &amp; Design. A move to Hong Kong followed, where she produced artwork for the Samaritans. Although she is mainly painting, textiles are always hovering, and she uses different surfaces and media to find ways of interpreting what is around her.<br /><br />
</div>'''

artists = []
saved_urls = []
for url in items:
    try:
        print "Getting URL:%s" % url

        artist = {'url' :url} 
        html = scraperwiki.scrape( url )
        img = match( html, ' src="(img-artists/(.*?)\.jpg)"' )
        print img
        img = img[0][0]

        img = urlparse.urljoin(url, img)
        print "img:", img
        img_src = '<img src="%s" alt="image"/>' % img

        chunk = match(html, ' <div id="artists-details">[0-9]*?(.*?)</div>')[0]

        title = match(chunk, '<span class="title">[0-9]* (.*?)</span>')[0]
        address = match(chunk, '/span>(.*?)</span')[0].strip()
        
        artist['title'] = title
        
        # Crapola, this needs tidying!

        address = address.replace('<span class="title">Websites','')
        address = address.replace('<span class="title">Email', '')
        address = address.replace('\r', '<br /> ')
        address = address.replace('\n', '<br /> ')
        address = address.replace('<br /> ', '<br />') 
        address = address.replace('<br /><br />', '<br />')
        address = address.replace('<br /><br />', '<br />')
        address = address.replace(',', '<br /> ')
        address = address.strip()
        


        artist['address'] = address
        
        artists.append( artist )
        if url not in saved_urls:
            print url
            print title,":", img, address, url
            scraperwiki.sqlite.save(unique_keys=["url"], data={"url":url, "title":title, 'address':address, 'img': img, 'img_src':img_src })
            saved_urls.append(url)
    except Exception, err:
        print err




'''

The intention is that this gets pumped at ...

    http://pipes.yahoo.com/pipes/pipe.info?_id=8d8db199d0238a32c025d7345da6a00e

...and so then can be shown on a map. Here's hoping

'''



    
    


    
     
    

