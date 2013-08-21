import scraperwiki
import urlparse
import lxml.html

from lxml import etree

base_url = 'http://gui.ie/clubs_info.asp?id='
max_id = 10

def getPageRoot(id):
    parser = etree.XMLParser(remove_blank_text=True)

    url = generateUrl(id)
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    return root;

def scrapeCourse(id):
    root = getPageRoot(id);
    courseInfo1 = root.cssselect('div#clubCol1')[0];
    courseInfo2 = root.cssselect('div#clubCol2')[0];

    info = getMainInfo(courseInfo1)

    if(len(info) == 0):
        return
    else:
        info['id'] = id
        #teeInfo = getTeeboxInfo(courseInfo2, id)
        info = getExtraCourseInfo(courseInfo2, info)

        #for tee in teeInfo:
            #print tee
            #scraperwiki.sqlite.save(['name', 'courseid'], tee, table_name='teesbox')

        print info
        #scraperwiki.sqlite.save(['phone', 'name'], info, table_name='course')

def generateUrl(id):
    return base_url + str(id)

def getCourseName(root):
    h1 = root.cssselect('h1')[0]
    return h1.text

def getAddressSeparateIndex(root):
    for idx,el in enumerate(root):
        if el.tail is None:
            return idx

def formatCounty(county):
    return county.replace('Co. ', '').replace('Co ', '')

def getMainInfo(root):
    info = {}
    name = getCourseName(root)
    if name is not None:
        info['name'] = name.strip()
        ps = root.cssselect('p')[0]
        psbrs = ps.cssselect('br')
        idx = getAddressSeparateIndex(psbrs)

        # if break index is 1 - we have 1 address line (presumably county)
        if idx == 1:
            info['address'] = ''
            info['town'] = ps.text
            info['county'] = formatCounty(psbrs[0].tail)
        
        # otherwise we have 2 address lines (town, county)
        if idx == 2:
            info['address'] = ps.text.strip()
            info['town'] = psbrs[0].tail
            info['county'] = formatCounty(psbrs[1].tail)

        info = getContactInfo(psbrs, info)
        info = getWebsiteEmail(ps, info)

    return info

def searchContactInfo(search, value):
  if value.tail is not None and value.tail.find(search) is not -1:
        return value.tail.replace(search, '').replace(':', '').strip()
  else:
    return ''

def getContactInfo(root, info):
    phone = ''
    fax = ''

    for el in root:
        _phone = searchContactInfo('(P)', el)
        _fax = searchContactInfo('(F)', el)

        if _phone is not '':
            phone = _phone

        if _fax is not '':
            fax = _fax

    info['phone'] = phone
    info['fax'] = fax

    return info

def getWebsiteEmail(root, info):
    website = ''
    email = ''
    ass = root.cssselect('a')
    for a in ass:
        if a.text.find('@') is not -1:
            email  = a.text
        else:
            if a.text.find('www') is not -1 or a.text.find('.ie') is not -1 or a.text.find('.com') is not -1:
                if a.text.find('www') is not -1:
                    website = a.text
                else:
                    website = 'www.' + a.text

    info['website'] = website
    info['email'] = email

    return info

def getTeeboxInfo(root, id):
    info = []

    tables = root.cssselect('table')
    tees = tables[0]
    teetrs = tees.cssselect('tr')
    for tr in teetrs:
        trtds = tr.cssselect('td')
        if len(trtds) == 4:
            tee = {}
            tee ['courseid'] = id
            tee ['name'] = trtds[0].text
            tee ['distance'] = trtds[1].text
            tee ['par'] = trtds[2].text
            tee ['sss'] = trtds[3].text
            info.append(tee)

    return info

def getExtraCourseInfo(root, info):
    tables = root.cssselect('table')
    content = tables[1]
    trs = content.cssselect('tr')

    _type = trs[0].cssselect('td')[0].text
    _holes = trs[1].cssselect('td')[0].text
    _spikes = trs[2].cssselect('img')[0].tag

    info['type'] = _type
    info['holes'] = _holes

    return info


def scrapeAllCourses():
    for i in range(max_id):
        scrapeCourse(i+1)


# scrape just one course (for testing)
scrapeCourse(88)
#scrapeCourse(411)

# scrape all courses
#scrapeAllCourses()

