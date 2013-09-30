import scraperwiki
import lxml.html


id = 0
for page in range(1, 21):
    print page
    count = 0
    html =  scraperwiki.scrape("http://www.doaj.org/doaj?func=subject&p=1&cpid=19&uiLanguage=en&page={0}".format(page))
    root = lxml.html.fromstring(html)
    titlestrings = ['ISSN/EISSN:',  'Subject:', 'Country:', 'Language:', 'year', 'fee:']
    dictstrings = ['ssn',  'subject', 'country', 'language', 'year', 'fee']
    for data in list(root.cssselect("div.data")):
        rowdata = {'id': id, 'count': count, 'page': page}
        rowdata['title'] = list(data)[0].text_content()
        for url in data.cssselect('a'):
            if 'Further Information' in unicode(url.text_content()):
                rowdata['further_information'] = url.get('href')
                break
        tabledata = list(data)[2].text_content().split()
        titleindex = [tabledata.index(x) for x in titlestrings]
        for i in range(0, len(titleindex)):
            if i == (len(titleindex) -1):
                try:
                    rowdata[dictstrings[i]] = ' '.join([tabledata[x] for x in range(titleindex[i]+1, titleindex[i] +2)])
                except:
                    print tabledata
            else:
                rowdata[dictstrings[i]] = ' '.join([tabledata[x] for x in range(titleindex[i]+1, titleindex[i+1])])
        rowdata['year'] = rowdata['year'][0:4]
        scraperwiki.sqlite.save(unique_keys=['id'], data=rowdata)
        id += 1
        count += 1



import scraperwiki
import lxml.html


id = 0
for page in range(1, 21):
    print page
    count = 0
    html =  scraperwiki.scrape("http://www.doaj.org/doaj?func=subject&p=1&cpid=19&uiLanguage=en&page={0}".format(page))
    root = lxml.html.fromstring(html)
    titlestrings = ['ISSN/EISSN:',  'Subject:', 'Country:', 'Language:', 'year', 'fee:']
    dictstrings = ['ssn',  'subject', 'country', 'language', 'year', 'fee']
    for data in list(root.cssselect("div.data")):
        rowdata = {'id': id, 'count': count, 'page': page}
        rowdata['title'] = list(data)[0].text_content()
        for url in data.cssselect('a'):
            if 'Further Information' in unicode(url.text_content()):
                rowdata['further_information'] = url.get('href')
                break
        tabledata = list(data)[2].text_content().split()
        titleindex = [tabledata.index(x) for x in titlestrings]
        for i in range(0, len(titleindex)):
            if i == (len(titleindex) -1):
                try:
                    rowdata[dictstrings[i]] = ' '.join([tabledata[x] for x in range(titleindex[i]+1, titleindex[i] +2)])
                except:
                    print tabledata
            else:
                rowdata[dictstrings[i]] = ' '.join([tabledata[x] for x in range(titleindex[i]+1, titleindex[i+1])])
        rowdata['year'] = rowdata['year'][0:4]
        scraperwiki.sqlite.save(unique_keys=['id'], data=rowdata)
        id += 1
        count += 1



