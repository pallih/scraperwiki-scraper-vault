import scraperwiki
import urllib2
import lxml.etree
import StringIO
import subprocess
import tempfile
import os.path
import base64

# Dummy URL load to give ScraperWiki something to screenshot.
urllib2.urlopen("http://www.atoc.org/about-atoc/rail-settlement-plan/routeing-guide")


def pink_pages():
    #
    # Pink pages
    #

    print "Loading pink pages (station to RP mapping)"
    url = "http://www.atoc.org/clientfiles/File/routeing_point_identifier.pdf"

    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)
    print "Converting to XML"

    xmldata = scraperwiki.pdftoxml(pdfdata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    # print "The first 20000 characters are: ", xmldata[:20000]

    print "Parsing XML"
    root = lxml.etree.fromstring(xmldata)

    # Each station is on a single line consisting of the station name and then
    # the various routeing points.

    stncells = root.xpath('//text[@left=37]')

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS routeing_points')
    scraperwiki.sqlite.execute('CREATE TABLE routeing_points (station, routeing_point)')
    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS groups')
    scraperwiki.sqlite.execute('CREATE TABLE groups (station, stngroup)')

    find_other_cells = lxml.etree.XPath('following-sibling::text[@top=$this/@top]')

    print "Extracting station list"
    for stncell in stncells:
        # Find other cells on the same row of the same page.
        othercells = find_other_cells(stncell, this = stncell)
        for othercell in othercells:
            stn, other = stncell.xpath('string()'), othercell.xpath('string()')
            stn = stn.title()
            if other == "Routeing Point":
                other = stn
            if other.endswith(" Routeing Point Member"):
                other = other[:-22]
                scraperwiki.sqlite.execute('INSERT INTO groups VALUES (?, ?)',
                    (str(stn), str(other)), verbose=0)
            scraperwiki.sqlite.execute('INSERT INTO routeing_points VALUES (?, ?)',
                (str(stn), str(other)), verbose=0)

    print "Creating indexes"
    scraperwiki.sqlite.execute('CREATE INDEX points_bystn ON routeing_points(station)')
    scraperwiki.sqlite.execute('CREATE INDEX groups_bystn ON groups(station)')
    print "Committing"
    scraperwiki.sqlite.commit()
    print "Pink pages processed"


def yellow_pages():
    #
    # Yellow pages
    #
    # This file is huge, so we do the XML parsing incrementally.
    #

    print "Loading yellow pages (permitted route list)"
    url = "http://www.atoc.org/clientfiles/File/permitted_route_identifier.pdf"

    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)

    print "Converting to XML"
    xmldata = scraperwiki.pdftoxml(pdfdata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    # print "The first 20000 characters are: ", xmldata[:20000]

    orig = None
    dest = None

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS permitted_routes')
    scraperwiki.sqlite.execute('CREATE TABLE permitted_routes (orig, dest, maps)')

    print "Processing XML"
    # This is horrid, and assumes that the PDF will be in the correct order.
    for _, cell in lxml.etree.iterparse(StringIO.StringIO(xmldata), tag='text'):
        if cell.attrib['height'] == '10':
            if cell.attrib['left'] == '80':
                orig = cell.xpath('string()')
            elif cell.attrib['left'] == '208':
                dest = cell.xpath('string()')
            else:
                scraperwiki.sqlite.execute('INSERT INTO permitted_routes VALUES (?, ?, ?)',
                    (orig, dest, cell.xpath('string()')))
        cell.clear()

    print "Creating index"
    scraperwiki.sqlite.execute('CREATE INDEX routes_bystn ON permitted_routes(orig, dest)')
    print "Committing"
    scraperwiki.sqlite.commit()
    print "Yellow pages done"

def maps():
    url = "http://www.atoc.org/clientfiles/File/Maps.pdf"

    print "Fetching maps"
    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)


    print "Converting to XML"
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 20000 characters are: ", xmldata[:20000]

    print "Converting PDF to PNGs"
    with tempfile.NamedTemporaryFile() as pdffile:
        pdffile.write(pdfdata)
        pdffile.flush()
        tmpdir = tempfile.mkdtemp()

        subprocess.check_call(['pdftoppm', '-r', '75', '-png',
            pdffile.name, os.path.join(tmpdir, 'p')])

    print "Parsing XML"
    root = lxml.etree.fromstring(xmldata)

    print "Processing maps"
    maptitles = root.xpath('//text[@height=100]')

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS maps')
    scraperwiki.sqlite.execute('CREATE TABLE maps (mapname, pageno, data)')

    for maptitle in maptitles:
        pageno = int(maptitle.xpath('string(../@number)'))
        with open(os.path.join(tmpdir, 'p-%03d.png' % (pageno)), 'rb') as f:
            scraperwiki.sqlite.execute('INSERT INTO maps VALUES (?,?,?)',
                (maptitle.xpath('string()'), pageno, base64.b64encode(f.read())))

    print "Creating index"
    scraperwiki.sqlite.execute('CREATE INDEX maps_bymap ON maps(mapname, pageno)')
    print "Committing maps"
    scraperwiki.sqlite.commit()
    print "Maps processed"

def rp_table():
    url = "http://www.atoc.org/clientfiles/File/routeing_points.pdf"

    print "Processing routeing point list"
    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)

    print "Converting to XML"
    xmldata = scraperwiki.pdftoxml(pdfdata)

    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 20000 characters are: ", xmldata[:20000]

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS rp_maps')
    scraperwiki.sqlite.execute('CREATE TABLE rp_maps (routeing_point, mapname)')

    print "Processing XML"
    # This is horrid, and assumes that the PDF will be in the correct order.
    for _, cell in lxml.etree.iterparse(StringIO.StringIO(xmldata), tag='text'):
        if int(cell.attrib['top']) > 100:
            if cell.attrib['left'] == '38':
                rp = cell.xpath('string()').title()
            else:
                for mapname in cell.xpath('string()').split():
                    scraperwiki.sqlite.execute('INSERT INTO rp_maps VALUES (?, ?)',
                        (rp, mapname))
        cell.clear()

    print "Creating indexes"
    scraperwiki.sqlite.execute('CREATE INDEX maps_byrp ON rp_maps(routeing_point)')
    scraperwiki.sqlite.execute('CREATE INDEX rps_bymap ON rp_maps(mapname)')
    print "Committing"
    scraperwiki.sqlite.commit()
    print "Routeing point list processed"

pink_pages()
yellow_pages()
maps()
rp_table()
import scraperwiki
import urllib2
import lxml.etree
import StringIO
import subprocess
import tempfile
import os.path
import base64

# Dummy URL load to give ScraperWiki something to screenshot.
urllib2.urlopen("http://www.atoc.org/about-atoc/rail-settlement-plan/routeing-guide")


def pink_pages():
    #
    # Pink pages
    #

    print "Loading pink pages (station to RP mapping)"
    url = "http://www.atoc.org/clientfiles/File/routeing_point_identifier.pdf"

    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)
    print "Converting to XML"

    xmldata = scraperwiki.pdftoxml(pdfdata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    # print "The first 20000 characters are: ", xmldata[:20000]

    print "Parsing XML"
    root = lxml.etree.fromstring(xmldata)

    # Each station is on a single line consisting of the station name and then
    # the various routeing points.

    stncells = root.xpath('//text[@left=37]')

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS routeing_points')
    scraperwiki.sqlite.execute('CREATE TABLE routeing_points (station, routeing_point)')
    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS groups')
    scraperwiki.sqlite.execute('CREATE TABLE groups (station, stngroup)')

    find_other_cells = lxml.etree.XPath('following-sibling::text[@top=$this/@top]')

    print "Extracting station list"
    for stncell in stncells:
        # Find other cells on the same row of the same page.
        othercells = find_other_cells(stncell, this = stncell)
        for othercell in othercells:
            stn, other = stncell.xpath('string()'), othercell.xpath('string()')
            stn = stn.title()
            if other == "Routeing Point":
                other = stn
            if other.endswith(" Routeing Point Member"):
                other = other[:-22]
                scraperwiki.sqlite.execute('INSERT INTO groups VALUES (?, ?)',
                    (str(stn), str(other)), verbose=0)
            scraperwiki.sqlite.execute('INSERT INTO routeing_points VALUES (?, ?)',
                (str(stn), str(other)), verbose=0)

    print "Creating indexes"
    scraperwiki.sqlite.execute('CREATE INDEX points_bystn ON routeing_points(station)')
    scraperwiki.sqlite.execute('CREATE INDEX groups_bystn ON groups(station)')
    print "Committing"
    scraperwiki.sqlite.commit()
    print "Pink pages processed"


def yellow_pages():
    #
    # Yellow pages
    #
    # This file is huge, so we do the XML parsing incrementally.
    #

    print "Loading yellow pages (permitted route list)"
    url = "http://www.atoc.org/clientfiles/File/permitted_route_identifier.pdf"

    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)

    print "Converting to XML"
    xmldata = scraperwiki.pdftoxml(pdfdata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    # print "The first 20000 characters are: ", xmldata[:20000]

    orig = None
    dest = None

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS permitted_routes')
    scraperwiki.sqlite.execute('CREATE TABLE permitted_routes (orig, dest, maps)')

    print "Processing XML"
    # This is horrid, and assumes that the PDF will be in the correct order.
    for _, cell in lxml.etree.iterparse(StringIO.StringIO(xmldata), tag='text'):
        if cell.attrib['height'] == '10':
            if cell.attrib['left'] == '80':
                orig = cell.xpath('string()')
            elif cell.attrib['left'] == '208':
                dest = cell.xpath('string()')
            else:
                scraperwiki.sqlite.execute('INSERT INTO permitted_routes VALUES (?, ?, ?)',
                    (orig, dest, cell.xpath('string()')))
        cell.clear()

    print "Creating index"
    scraperwiki.sqlite.execute('CREATE INDEX routes_bystn ON permitted_routes(orig, dest)')
    print "Committing"
    scraperwiki.sqlite.commit()
    print "Yellow pages done"

def maps():
    url = "http://www.atoc.org/clientfiles/File/Maps.pdf"

    print "Fetching maps"
    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)


    print "Converting to XML"
    xmldata = scraperwiki.pdftoxml(pdfdata)
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 20000 characters are: ", xmldata[:20000]

    print "Converting PDF to PNGs"
    with tempfile.NamedTemporaryFile() as pdffile:
        pdffile.write(pdfdata)
        pdffile.flush()
        tmpdir = tempfile.mkdtemp()

        subprocess.check_call(['pdftoppm', '-r', '75', '-png',
            pdffile.name, os.path.join(tmpdir, 'p')])

    print "Parsing XML"
    root = lxml.etree.fromstring(xmldata)

    print "Processing maps"
    maptitles = root.xpath('//text[@height=100]')

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS maps')
    scraperwiki.sqlite.execute('CREATE TABLE maps (mapname, pageno, data)')

    for maptitle in maptitles:
        pageno = int(maptitle.xpath('string(../@number)'))
        with open(os.path.join(tmpdir, 'p-%03d.png' % (pageno)), 'rb') as f:
            scraperwiki.sqlite.execute('INSERT INTO maps VALUES (?,?,?)',
                (maptitle.xpath('string()'), pageno, base64.b64encode(f.read())))

    print "Creating index"
    scraperwiki.sqlite.execute('CREATE INDEX maps_bymap ON maps(mapname, pageno)')
    print "Committing maps"
    scraperwiki.sqlite.commit()
    print "Maps processed"

def rp_table():
    url = "http://www.atoc.org/clientfiles/File/routeing_points.pdf"

    print "Processing routeing point list"
    pdfdata = urllib2.urlopen(url).read()
    print "The pdf file has %d bytes" % len(pdfdata)

    print "Converting to XML"
    xmldata = scraperwiki.pdftoxml(pdfdata)

    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 20000 characters are: ", xmldata[:20000]

    scraperwiki.sqlite.execute('DROP TABLE IF EXISTS rp_maps')
    scraperwiki.sqlite.execute('CREATE TABLE rp_maps (routeing_point, mapname)')

    print "Processing XML"
    # This is horrid, and assumes that the PDF will be in the correct order.
    for _, cell in lxml.etree.iterparse(StringIO.StringIO(xmldata), tag='text'):
        if int(cell.attrib['top']) > 100:
            if cell.attrib['left'] == '38':
                rp = cell.xpath('string()').title()
            else:
                for mapname in cell.xpath('string()').split():
                    scraperwiki.sqlite.execute('INSERT INTO rp_maps VALUES (?, ?)',
                        (rp, mapname))
        cell.clear()

    print "Creating indexes"
    scraperwiki.sqlite.execute('CREATE INDEX maps_byrp ON rp_maps(routeing_point)')
    scraperwiki.sqlite.execute('CREATE INDEX rps_bymap ON rp_maps(mapname)')
    print "Committing"
    scraperwiki.sqlite.commit()
    print "Routeing point list processed"

pink_pages()
yellow_pages()
maps()
rp_table()
