from scraperwiki import pdftoxml, swimport
from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.etree import fromstring, tostring
from time import time

DATE = time()

def main():
    pdf = fromstring(pdftoxml(urlopen('http://www.realpeople.co.za/Downloads/COR%200275%20BRANCH%20LIST.pdf').read()))
    d = []
    for page in pdf.xpath('//page'):
        d.extend(parsepage(page))
    for row in d:
        row['date_scraped'] = DATE
    save([], d)

def parsepage(page):
    tops = list(map(int, set(page.xpath('text/@top'))))
    tops.sort()
    tops = map(str, tops)

    header = None
    d = []
    for top in tops:
        cells = page.xpath('text[@top="%s"]' % top)

        try:
            firstcelltext = cells[0].xpath('b/text()')[0]
        except:
            continue

        if len(cells) == 6:
            pass
        elif firstcelltext == '292 SMITH STREET':
            cells = page.xpath('text[@top = "700" or @top = "699"]')
        elif firstcelltext == 'FOX STREET':
            cells = page.xpath('text[@top = "470" or @top = "469"]')
        else:
            continue

        if len(cells) != 6:
            #print [tostring(cell) for cell in cells]
            assert cells[1].attrib['left'] == '100', cells
            cells.pop(1)

        #print [cell.attrib['left'] for cell in cells]
        cell_values = [cell.xpath('b/text()')[0] for cell in cells]
        if header == None:
            header = [v.strip() for v in cell_values]
        else:
            row = dict(zip(header, cell_values))
            addresslines = row['ADDRESS'].split(', ')
            row['street-address'] = '\n'.join(addresslines[:-1])
            row['town'] = addresslines[-1]
            d.append(row)

    return d

main()from scraperwiki import pdftoxml, swimport
from scraperwiki.sqlite import save
from urllib2 import urlopen
from lxml.etree import fromstring, tostring
from time import time

DATE = time()

def main():
    pdf = fromstring(pdftoxml(urlopen('http://www.realpeople.co.za/Downloads/COR%200275%20BRANCH%20LIST.pdf').read()))
    d = []
    for page in pdf.xpath('//page'):
        d.extend(parsepage(page))
    for row in d:
        row['date_scraped'] = DATE
    save([], d)

def parsepage(page):
    tops = list(map(int, set(page.xpath('text/@top'))))
    tops.sort()
    tops = map(str, tops)

    header = None
    d = []
    for top in tops:
        cells = page.xpath('text[@top="%s"]' % top)

        try:
            firstcelltext = cells[0].xpath('b/text()')[0]
        except:
            continue

        if len(cells) == 6:
            pass
        elif firstcelltext == '292 SMITH STREET':
            cells = page.xpath('text[@top = "700" or @top = "699"]')
        elif firstcelltext == 'FOX STREET':
            cells = page.xpath('text[@top = "470" or @top = "469"]')
        else:
            continue

        if len(cells) != 6:
            #print [tostring(cell) for cell in cells]
            assert cells[1].attrib['left'] == '100', cells
            cells.pop(1)

        #print [cell.attrib['left'] for cell in cells]
        cell_values = [cell.xpath('b/text()')[0] for cell in cells]
        if header == None:
            header = [v.strip() for v in cell_values]
        else:
            row = dict(zip(header, cell_values))
            addresslines = row['ADDRESS'].split(', ')
            row['street-address'] = '\n'.join(addresslines[:-1])
            row['town'] = addresslines[-1]
            d.append(row)

    return d

main()