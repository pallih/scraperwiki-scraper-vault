import scraperwiki
import os
import tempfile

def pdftotext(pdfdata):
    """converts pdf file to text"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    textin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmptext = textin.name
    cmd = '/usr/bin/pdftohtml -xml "%s" "%s"' % (pdffout.name, tmptext)
    cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    text = textin.read()
    textin.close()
    return text

pdfurl = "http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"
a = scraperwiki.scrape(pdfurl)
print pdftotext(a)