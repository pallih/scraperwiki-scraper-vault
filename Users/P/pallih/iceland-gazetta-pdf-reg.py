import scraperwiki
import os
import tempfile
import re
import urllib2
import lxml.etree

regex = re.compile("Hlutafélagaskrá – nýskráning\n(.*\n)Hlutafélagaskrá – nýskráning",re.DOTALL)
#regex = re.compile(r"Félagið heitir:^(.+)\n((?:\n.+)+)", re.MULTILINE)

def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptext = textin.name
    cmd = '/usr/bin/pdftotext -raw -nopgbrk -enc UTF-8 "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    text = textin.read()
    textin.close()
    #text = text.strip('\t\n\r')
    return text

#pdfurl = "http://logbirtingablad.is/PdfOpen.aspx?StreamID=327644be-82a1-4a70-addb-924829853465"
pdfurl = "http://logbirtingablad.is/PdfOpen.aspx?StreamID=d7aaf458-3312-47e8-9d1e-23ca842e43d1"
a = scraperwiki.scrape(pdfurl)
source = pdftotext(a)
print source
print
print
#what = re.findall(regex,source)
#print "what ",what
#for w in what:
#    print w
hat = re.findall("(?s)Hlutafélagaskrá – nýskráning.*?Hluta", source)
for h in hat:
    #h = h.rstrip('Hluta')
    #h = h.lstrip('Hlutafélagaskrá – nýskráning\n')
    print h
#print what.group(1)
#names = list(re.findall('Félagið heitir:(\s.*)Kt.',source, re.M))
#print names
#ids = list(re.findall('Kt.:(\s.*)Heimili',source))
#addresses = list(re.findall('Heimili og varnarþing:(\s.*)Dagsetning', source, re.M))
#founders = list(re.findall('Stofnendur:(.*)', source, re.M))
#print founders
#for f in founders:
#    print f
#for name in names:
#    print name
#for id in ids:
#    print id
#print source
#for name, id, address, founder in zip(names,ids, addresses, founders):
#    print name, id, address, founder

print
print
import scraperwiki
import os
import tempfile
import re
import urllib2
import lxml.etree

regex = re.compile("Hlutafélagaskrá – nýskráning\n(.*\n)Hlutafélagaskrá – nýskráning",re.DOTALL)
#regex = re.compile(r"Félagið heitir:^(.+)\n((?:\n.+)+)", re.MULTILINE)

def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.txt')
    tmptext = textin.name
    cmd = '/usr/bin/pdftotext -raw -nopgbrk -enc UTF-8 "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    text = textin.read()
    textin.close()
    #text = text.strip('\t\n\r')
    return text

#pdfurl = "http://logbirtingablad.is/PdfOpen.aspx?StreamID=327644be-82a1-4a70-addb-924829853465"
pdfurl = "http://logbirtingablad.is/PdfOpen.aspx?StreamID=d7aaf458-3312-47e8-9d1e-23ca842e43d1"
a = scraperwiki.scrape(pdfurl)
source = pdftotext(a)
print source
print
print
#what = re.findall(regex,source)
#print "what ",what
#for w in what:
#    print w
hat = re.findall("(?s)Hlutafélagaskrá – nýskráning.*?Hluta", source)
for h in hat:
    #h = h.rstrip('Hluta')
    #h = h.lstrip('Hlutafélagaskrá – nýskráning\n')
    print h
#print what.group(1)
#names = list(re.findall('Félagið heitir:(\s.*)Kt.',source, re.M))
#print names
#ids = list(re.findall('Kt.:(\s.*)Heimili',source))
#addresses = list(re.findall('Heimili og varnarþing:(\s.*)Dagsetning', source, re.M))
#founders = list(re.findall('Stofnendur:(.*)', source, re.M))
#print founders
#for f in founders:
#    print f
#for name in names:
#    print name
#for id in ids:
#    print id
#print source
#for name, id, address, founder in zip(names,ids, addresses, founders):
#    print name, id, address, founder

print
print
