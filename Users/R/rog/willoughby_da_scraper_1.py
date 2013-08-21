import scraperwiki
import mechanize
import re
#import sys, logging
#logger = logging.getLogger("mechanize")
#logger.addHandler(logging.StreamHandler(sys.stdout))
#logger.setLevel(logging.DEBUG)

# Session required to do anything, so the best we can do is start and send people here:
preurl = "https://epathway.willoughby.nsw.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx"
commenturl = "mailto:email@willoughby.nsw.gov.au";

br = mechanize.Browser()

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(preurl)

br.select_form(name='aspnetForm')
br.form.set_all_readonly(False)
br['mDataGrid:Column0:Property'] = ['ctl00$MainBodyContent$mDataList$ctl00$mDataGrid$ctl02$ctl00']
response = br.submit(name='ctl00$MainBodyContent$mContinueButton')

# After much mucking about, it turns out submitting a blank search gives you
# a page full of the most recent DAs
br.select_form(name='aspnetForm')
response = br.submit()
html = response.read()
#print "length %d" % len(html)
#for form in br.forms():
#    print form
#print html

import lxml.html
import time
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
rows = root.cssselect('table.ContentPanel tr') # get all the <tr> tags

"""<tr class="ContentPanel">
<td align="left" valign="top" style="width:100px;white-space:nowrap;">
    <div class='ContentText' style='width: 100px; text-overflow: ellipsis; overflow:hidden;'>
        <a href='EnquiryDetailView.aspx?Id=372459'>DA-2011/440</a>
    </div>
</td>
<td align="left" valign="top" style="width:100px;white-space:nowrap;">
    <span class="ContentText">16/09/2011</span>
</td>
<td align="left" valign="top" style="width:500px;white-space:nowrap;">
    <div class='ContentText' style='width: 500px; text-overflow: ellipsis; overflow:hidden;'>
        9 The Citadel, CASTLECRAG NSW 2068.
    </div>
</td>
<td align="left" valign="top" style="width:200px;white-space:nowrap;">
    <div class='ContentText' style='width: 200px; text-overflow: ellipsis; overflow:hidden;'>
    Lodged - Recently submitted to Council
    </div>
</td>
<td align="left" valign="top" style="width:500px;">
    <span class="ContentText">DA for demolition of existing attached & detached garages & 1 storey dwelling at construction of new 2 storey dwelling, detached garage & swimming pool.</span>
</td>
<td align="left" valign="top" style="width:200px;white-space:nowrap;">
<div class='ContentText' style='width: 200px; text-overflow: ellipsis; overflow:hidden;'></div>
</td>
<td align="left" valign="top" style="width:200px;white-space:nowrap;">
<div class='ContentText' style='width: 200px; text-overflow: ellipsis; overflow:hidden;'></div>
</td>
<td>&nbsp;</td>
</tr>"""
def all_text(cell):
    return lxml.html.tostring(cell, method="text", encoding=unicode)

for row in rows[1:]:
    #print lxml.html.tostring(row) # the full HTML tag

    cells = row.cssselect("td")
#    print cells
#    for cell in cells:
#        print lxml.html.tostring(cell, method="text", encoding=unicode)
        
    council_reference = all_text(cells[0])
    if council_reference == "Not on file":
        continue
    address = all_text(cells[2])
    description = all_text(cells[4])
    date_received = time.strftime('%Y-%m-%d', time.strptime(all_text(cells[1]), '%d/%m/%Y'))
    record = {
        'info_url': preurl,
        'comment_url': commenturl,
        'council_reference': council_reference,
        'date_received': date_received,
        'address': address,
        'description': description,
        'date_scraped': time.strftime('%Y-%m-%d')
    }

    scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record)
