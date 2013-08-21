import lxml.html
import re
import datetime
import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-levels"


def parsepage(url):
    try:
        root = lxml.html.parse(url).getroot()
    except IOError:
        # Page not found or other error, "river level" database probably needs updating.
        return None, None

    na = root.cssselect('div#content div.plain_text p')
    try:
        if len(na) > 0 and re.match('The station that you have selected is not currently active.$', na[0].text):
            return None, None
    except TypeError:
        # Element not found or is wrong type - station probably active.
        pass

    ps = root.cssselect('div#station-detail-left div.panels div.theme1 div.panel div.t div.r div.b div.l div.tr div.tl div.br div.bl p')
    if re.match('Sorry, the last measurement was invalid. We will update the page as soon as possible.$', ps[0].text):
        return None, None

    mriverlevel = re.match("The (?:river )?level at .*? is ([\d.\-]*) m(?:etres)?\.$", ps[0].text)
    assert mriverlevel, ps[0].text
    md = re.match("This measurement was recorded at (\d\d):(\d\d) on (\d\d)/(\d\d)/(\d\d\d\d)\.$", ps[1].text)
    assert md, ps[1].text
    date = datetime.datetime(int(md.group(5)), int(md.group(4)), int(md.group(3)), int(md.group(1)), int(md.group(2)))
    level = float(mriverlevel.group(1))

    typicaldata = { }
    for psl in ps[2:]:
        if not psl.text:
            continue
        mtypical = re.match('The typical river level range for this location is between ([\d\.\-]+) metres and ([\d\.\-]+) metres.$', psl.text)
        mtidelevel = re.match('Highest astronomical tide level for this site is ([\d\.\-]+) m AOD.$', psl.text)
        mhighest = re.match('The highest river level recorded at this location is ([\d\.\-]+) metres and the river level reached ([\d\.\-]+) metres on (\d\d)/(\d\d)/(\d\d\d\d).', psl.text)
        if mtypical:
            typicaldata["typicallowlevel"] = mtypical.group(1)
            typicaldata["typicalhighlevel"] = mtypical.group(2)
        elif mtidelevel:
            typicaldata["highesttide"] = mtidelevel.group(1)
        elif mhighest:
            typicaldata["highestlevel"] = mhighest.group(1)
            typicaldata["highestrecorded"] = mhighest.group(2)
            typicaldata["highestrecordeddate"] = str( datetime.datetime(int(mhighest.group(5)), int(mhighest.group(4)), int(mhighest.group(3))) )
        else:
            assert False, "No match on text: "+psl.text
            
    return str(date), level
    

limit = 2000
offset = 0
scraperwiki.sqlite.attach(sourcescraper) 
sdata = scraperwiki.sqlite.select('* from `%s`.swdata limit %d' % (sourcescraper, limit))
for row in sdata:
    date, level = parsepage(row['url'])
    if date:
        row["level"] = level
        scraperwiki.sqlite.save(unique_keys=['station', 'River'], data=row, date=date)


import lxml.html
import re
import datetime
import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-levels"


def parsepage(url):
    try:
        root = lxml.html.parse(url).getroot()
    except IOError:
        # Page not found or other error, "river level" database probably needs updating.
        return None, None

    na = root.cssselect('div#content div.plain_text p')
    try:
        if len(na) > 0 and re.match('The station that you have selected is not currently active.$', na[0].text):
            return None, None
    except TypeError:
        # Element not found or is wrong type - station probably active.
        pass

    ps = root.cssselect('div#station-detail-left div.panels div.theme1 div.panel div.t div.r div.b div.l div.tr div.tl div.br div.bl p')
    if re.match('Sorry, the last measurement was invalid. We will update the page as soon as possible.$', ps[0].text):
        return None, None

    mriverlevel = re.match("The (?:river )?level at .*? is ([\d.\-]*) m(?:etres)?\.$", ps[0].text)
    assert mriverlevel, ps[0].text
    md = re.match("This measurement was recorded at (\d\d):(\d\d) on (\d\d)/(\d\d)/(\d\d\d\d)\.$", ps[1].text)
    assert md, ps[1].text
    date = datetime.datetime(int(md.group(5)), int(md.group(4)), int(md.group(3)), int(md.group(1)), int(md.group(2)))
    level = float(mriverlevel.group(1))

    typicaldata = { }
    for psl in ps[2:]:
        if not psl.text:
            continue
        mtypical = re.match('The typical river level range for this location is between ([\d\.\-]+) metres and ([\d\.\-]+) metres.$', psl.text)
        mtidelevel = re.match('Highest astronomical tide level for this site is ([\d\.\-]+) m AOD.$', psl.text)
        mhighest = re.match('The highest river level recorded at this location is ([\d\.\-]+) metres and the river level reached ([\d\.\-]+) metres on (\d\d)/(\d\d)/(\d\d\d\d).', psl.text)
        if mtypical:
            typicaldata["typicallowlevel"] = mtypical.group(1)
            typicaldata["typicalhighlevel"] = mtypical.group(2)
        elif mtidelevel:
            typicaldata["highesttide"] = mtidelevel.group(1)
        elif mhighest:
            typicaldata["highestlevel"] = mhighest.group(1)
            typicaldata["highestrecorded"] = mhighest.group(2)
            typicaldata["highestrecordeddate"] = str( datetime.datetime(int(mhighest.group(5)), int(mhighest.group(4)), int(mhighest.group(3))) )
        else:
            assert False, "No match on text: "+psl.text
            
    return str(date), level
    

limit = 2000
offset = 0
scraperwiki.sqlite.attach(sourcescraper) 
sdata = scraperwiki.sqlite.select('* from `%s`.swdata limit %d' % (sourcescraper, limit))
for row in sdata:
    date, level = parsepage(row['url'])
    if date:
        row["level"] = level
        scraperwiki.sqlite.save(unique_keys=['station', 'River'], data=row, date=date)


import lxml.html
import re
import datetime
import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-levels"


def parsepage(url):
    try:
        root = lxml.html.parse(url).getroot()
    except IOError:
        # Page not found or other error, "river level" database probably needs updating.
        return None, None

    na = root.cssselect('div#content div.plain_text p')
    try:
        if len(na) > 0 and re.match('The station that you have selected is not currently active.$', na[0].text):
            return None, None
    except TypeError:
        # Element not found or is wrong type - station probably active.
        pass

    ps = root.cssselect('div#station-detail-left div.panels div.theme1 div.panel div.t div.r div.b div.l div.tr div.tl div.br div.bl p')
    if re.match('Sorry, the last measurement was invalid. We will update the page as soon as possible.$', ps[0].text):
        return None, None

    mriverlevel = re.match("The (?:river )?level at .*? is ([\d.\-]*) m(?:etres)?\.$", ps[0].text)
    assert mriverlevel, ps[0].text
    md = re.match("This measurement was recorded at (\d\d):(\d\d) on (\d\d)/(\d\d)/(\d\d\d\d)\.$", ps[1].text)
    assert md, ps[1].text
    date = datetime.datetime(int(md.group(5)), int(md.group(4)), int(md.group(3)), int(md.group(1)), int(md.group(2)))
    level = float(mriverlevel.group(1))

    typicaldata = { }
    for psl in ps[2:]:
        if not psl.text:
            continue
        mtypical = re.match('The typical river level range for this location is between ([\d\.\-]+) metres and ([\d\.\-]+) metres.$', psl.text)
        mtidelevel = re.match('Highest astronomical tide level for this site is ([\d\.\-]+) m AOD.$', psl.text)
        mhighest = re.match('The highest river level recorded at this location is ([\d\.\-]+) metres and the river level reached ([\d\.\-]+) metres on (\d\d)/(\d\d)/(\d\d\d\d).', psl.text)
        if mtypical:
            typicaldata["typicallowlevel"] = mtypical.group(1)
            typicaldata["typicalhighlevel"] = mtypical.group(2)
        elif mtidelevel:
            typicaldata["highesttide"] = mtidelevel.group(1)
        elif mhighest:
            typicaldata["highestlevel"] = mhighest.group(1)
            typicaldata["highestrecorded"] = mhighest.group(2)
            typicaldata["highestrecordeddate"] = str( datetime.datetime(int(mhighest.group(5)), int(mhighest.group(4)), int(mhighest.group(3))) )
        else:
            assert False, "No match on text: "+psl.text
            
    return str(date), level
    

limit = 2000
offset = 0
scraperwiki.sqlite.attach(sourcescraper) 
sdata = scraperwiki.sqlite.select('* from `%s`.swdata limit %d' % (sourcescraper, limit))
for row in sdata:
    date, level = parsepage(row['url'])
    if date:
        row["level"] = level
        scraperwiki.sqlite.save(unique_keys=['station', 'River'], data=row, date=date)


import lxml.html
import re
import datetime
import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "environment-agency-river-levels"


def parsepage(url):
    try:
        root = lxml.html.parse(url).getroot()
    except IOError:
        # Page not found or other error, "river level" database probably needs updating.
        return None, None

    na = root.cssselect('div#content div.plain_text p')
    try:
        if len(na) > 0 and re.match('The station that you have selected is not currently active.$', na[0].text):
            return None, None
    except TypeError:
        # Element not found or is wrong type - station probably active.
        pass

    ps = root.cssselect('div#station-detail-left div.panels div.theme1 div.panel div.t div.r div.b div.l div.tr div.tl div.br div.bl p')
    if re.match('Sorry, the last measurement was invalid. We will update the page as soon as possible.$', ps[0].text):
        return None, None

    mriverlevel = re.match("The (?:river )?level at .*? is ([\d.\-]*) m(?:etres)?\.$", ps[0].text)
    assert mriverlevel, ps[0].text
    md = re.match("This measurement was recorded at (\d\d):(\d\d) on (\d\d)/(\d\d)/(\d\d\d\d)\.$", ps[1].text)
    assert md, ps[1].text
    date = datetime.datetime(int(md.group(5)), int(md.group(4)), int(md.group(3)), int(md.group(1)), int(md.group(2)))
    level = float(mriverlevel.group(1))

    typicaldata = { }
    for psl in ps[2:]:
        if not psl.text:
            continue
        mtypical = re.match('The typical river level range for this location is between ([\d\.\-]+) metres and ([\d\.\-]+) metres.$', psl.text)
        mtidelevel = re.match('Highest astronomical tide level for this site is ([\d\.\-]+) m AOD.$', psl.text)
        mhighest = re.match('The highest river level recorded at this location is ([\d\.\-]+) metres and the river level reached ([\d\.\-]+) metres on (\d\d)/(\d\d)/(\d\d\d\d).', psl.text)
        if mtypical:
            typicaldata["typicallowlevel"] = mtypical.group(1)
            typicaldata["typicalhighlevel"] = mtypical.group(2)
        elif mtidelevel:
            typicaldata["highesttide"] = mtidelevel.group(1)
        elif mhighest:
            typicaldata["highestlevel"] = mhighest.group(1)
            typicaldata["highestrecorded"] = mhighest.group(2)
            typicaldata["highestrecordeddate"] = str( datetime.datetime(int(mhighest.group(5)), int(mhighest.group(4)), int(mhighest.group(3))) )
        else:
            assert False, "No match on text: "+psl.text
            
    return str(date), level
    

limit = 2000
offset = 0
scraperwiki.sqlite.attach(sourcescraper) 
sdata = scraperwiki.sqlite.select('* from `%s`.swdata limit %d' % (sourcescraper, limit))
for row in sdata:
    date, level = parsepage(row['url'])
    if date:
        row["level"] = level
        scraperwiki.sqlite.save(unique_keys=['station', 'River'], data=row, date=date)


