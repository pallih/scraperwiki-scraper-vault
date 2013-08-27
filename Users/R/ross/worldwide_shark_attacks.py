import scraperwiki
import lxml.html  
import math

errors = []

regional = {
"Middle America" : "MapMiddle.htm",
"Asia" : "MapAsia.htm",
"Australia" : "MapAU.htm",
"New Zealand" : "MapZE.htm",
"Hawaii" : "mapHawaii.htm",
"Pacific Islands" : "MapOceania.htm",
"Bermuda" : "mapBermuda.htm",
"Europe" : "MapEurope.htm",
"Africa" : "MapAfric.htm",
"USA" : "mapusa.htm",
} 

global_style_page = {
  "Antilles and Bahamas" : "http://www.flmnh.ufl.edu/fish/sharks/statistics/gattack/Caribbean.htm",
}

def calc(ys,xs ):
    c = float(xs)/float(ys)
    return int(math.ceil(c * 100))

def year_or_blank(val):
    try:
        i = int(val.strip())
        return val
    except:
        return ''
       
#Territory,Total Attacks,Fatal Attacks,Last Fatality
def process_block(block, name):
    if len(cells) != 4 or cells[1].text is None or cells[1].text.strip() == '':
        return

    record = {
        'Territory':cells[0][0].text.strip(),
        'Total Attacks': cells[1].text.strip(),
        'Fatal Attacks': cells[2].text.strip(),
        'Last Fatality': year_or_blank(cells[3].text),
        'Approximate percentage fatal' : calc(cells[1].text.strip(), cells[2].text.strip())
    }
    
    try:
        scraperwiki.sqlite.save(unique_keys=['Territory'], data=record, table_name=name)
        print 'Worked'
    except Exception, e:
        print 'Failed'
        msg = str(e)
        if not msg in errors: errors.append(msg) 

print 'Starting processing'

root = lxml.html.parse("http://www.flmnh.ufl.edu/fish/sharks/statistics/GAttack/World.htm").getroot()
print 'Processing world'
if root is not None:
    table = root.cssselect("table[width='720']")[0]
    for row in table.cssselect('tr')[2:]:
        cells = row.cssselect('td')[0:5]
        cells[0] = cells[0].cssselect('font b')
        process_block(cells, name="Worldwide")

        cells = row.cssselect('td')[5:10]
        cells[0] = cells[0].cssselect('font b')
        process_block(cells, name="Worldwide")
    

for k,v in regional.items():
    print 'Processing %s' % k
    root = lxml.html.parse("http://www.flmnh.ufl.edu/fish/sharks/statistics/gattack/%s" % v).getroot()
    if root is not None:
        table = root.cssselect("table[align='center']")[6]
        rows = table.cssselect('tr')[1:]
        for row in rows:
            cells = row.cssselect('td')
            cells[0] = cells[0].cssselect('font')
            try:
                process_block(cells, name=k)
            except IndexError:
                pass


print '*' * 80
print 'Errors'
print '*' * 80
for e in errors:
    print eimport scraperwiki
import lxml.html  
import math

errors = []

regional = {
"Middle America" : "MapMiddle.htm",
"Asia" : "MapAsia.htm",
"Australia" : "MapAU.htm",
"New Zealand" : "MapZE.htm",
"Hawaii" : "mapHawaii.htm",
"Pacific Islands" : "MapOceania.htm",
"Bermuda" : "mapBermuda.htm",
"Europe" : "MapEurope.htm",
"Africa" : "MapAfric.htm",
"USA" : "mapusa.htm",
} 

global_style_page = {
  "Antilles and Bahamas" : "http://www.flmnh.ufl.edu/fish/sharks/statistics/gattack/Caribbean.htm",
}

def calc(ys,xs ):
    c = float(xs)/float(ys)
    return int(math.ceil(c * 100))

def year_or_blank(val):
    try:
        i = int(val.strip())
        return val
    except:
        return ''
       
#Territory,Total Attacks,Fatal Attacks,Last Fatality
def process_block(block, name):
    if len(cells) != 4 or cells[1].text is None or cells[1].text.strip() == '':
        return

    record = {
        'Territory':cells[0][0].text.strip(),
        'Total Attacks': cells[1].text.strip(),
        'Fatal Attacks': cells[2].text.strip(),
        'Last Fatality': year_or_blank(cells[3].text),
        'Approximate percentage fatal' : calc(cells[1].text.strip(), cells[2].text.strip())
    }
    
    try:
        scraperwiki.sqlite.save(unique_keys=['Territory'], data=record, table_name=name)
        print 'Worked'
    except Exception, e:
        print 'Failed'
        msg = str(e)
        if not msg in errors: errors.append(msg) 

print 'Starting processing'

root = lxml.html.parse("http://www.flmnh.ufl.edu/fish/sharks/statistics/GAttack/World.htm").getroot()
print 'Processing world'
if root is not None:
    table = root.cssselect("table[width='720']")[0]
    for row in table.cssselect('tr')[2:]:
        cells = row.cssselect('td')[0:5]
        cells[0] = cells[0].cssselect('font b')
        process_block(cells, name="Worldwide")

        cells = row.cssselect('td')[5:10]
        cells[0] = cells[0].cssselect('font b')
        process_block(cells, name="Worldwide")
    

for k,v in regional.items():
    print 'Processing %s' % k
    root = lxml.html.parse("http://www.flmnh.ufl.edu/fish/sharks/statistics/gattack/%s" % v).getroot()
    if root is not None:
        table = root.cssselect("table[align='center']")[6]
        rows = table.cssselect('tr')[1:]
        for row in rows:
            cells = row.cssselect('td')
            cells[0] = cells[0].cssselect('font')
            try:
                process_block(cells, name=k)
            except IndexError:
                pass


print '*' * 80
print 'Errors'
print '*' * 80
for e in errors:
    print eimport scraperwiki
import lxml.html  
import math

errors = []

regional = {
"Middle America" : "MapMiddle.htm",
"Asia" : "MapAsia.htm",
"Australia" : "MapAU.htm",
"New Zealand" : "MapZE.htm",
"Hawaii" : "mapHawaii.htm",
"Pacific Islands" : "MapOceania.htm",
"Bermuda" : "mapBermuda.htm",
"Europe" : "MapEurope.htm",
"Africa" : "MapAfric.htm",
"USA" : "mapusa.htm",
} 

global_style_page = {
  "Antilles and Bahamas" : "http://www.flmnh.ufl.edu/fish/sharks/statistics/gattack/Caribbean.htm",
}

def calc(ys,xs ):
    c = float(xs)/float(ys)
    return int(math.ceil(c * 100))

def year_or_blank(val):
    try:
        i = int(val.strip())
        return val
    except:
        return ''
       
#Territory,Total Attacks,Fatal Attacks,Last Fatality
def process_block(block, name):
    if len(cells) != 4 or cells[1].text is None or cells[1].text.strip() == '':
        return

    record = {
        'Territory':cells[0][0].text.strip(),
        'Total Attacks': cells[1].text.strip(),
        'Fatal Attacks': cells[2].text.strip(),
        'Last Fatality': year_or_blank(cells[3].text),
        'Approximate percentage fatal' : calc(cells[1].text.strip(), cells[2].text.strip())
    }
    
    try:
        scraperwiki.sqlite.save(unique_keys=['Territory'], data=record, table_name=name)
        print 'Worked'
    except Exception, e:
        print 'Failed'
        msg = str(e)
        if not msg in errors: errors.append(msg) 

print 'Starting processing'

root = lxml.html.parse("http://www.flmnh.ufl.edu/fish/sharks/statistics/GAttack/World.htm").getroot()
print 'Processing world'
if root is not None:
    table = root.cssselect("table[width='720']")[0]
    for row in table.cssselect('tr')[2:]:
        cells = row.cssselect('td')[0:5]
        cells[0] = cells[0].cssselect('font b')
        process_block(cells, name="Worldwide")

        cells = row.cssselect('td')[5:10]
        cells[0] = cells[0].cssselect('font b')
        process_block(cells, name="Worldwide")
    

for k,v in regional.items():
    print 'Processing %s' % k
    root = lxml.html.parse("http://www.flmnh.ufl.edu/fish/sharks/statistics/gattack/%s" % v).getroot()
    if root is not None:
        table = root.cssselect("table[align='center']")[6]
        rows = table.cssselect('tr')[1:]
        for row in rows:
            cells = row.cssselect('td')
            cells[0] = cells[0].cssselect('font')
            try:
                process_block(cells, name=k)
            except IndexError:
                pass


print '*' * 80
print 'Errors'
print '*' * 80
for e in errors:
    print e