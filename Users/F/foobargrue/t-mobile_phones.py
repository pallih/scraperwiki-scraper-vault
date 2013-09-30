import scraperwiki
import lxml.html           
import urllib
import re

html        = scraperwiki.scrape("http://store.three.co.uk/view/searchDevice?sort=payMonthlyMinPrice-ascending&viewAll=true&tariff=3046")
root        = lxml.html.fromstring(html)

regex_details     = re.compile(r">(.*?)<", re.DOTALL)
regex_subdetails  = re.compile(r"black|white|purple|blue|pink|(?<!\.)\d+GB", re.IGNORECASE)
regex_upfront     = re.compile(r"(\d+?)\.", re.DOTALL)

for handset in root.cssselect("div.productList_item"):
    phone_details = lxml.html.tostring(handset.cssselect("h4.productList_name")[0])
    match         = regex_details.findall(phone_details)
    phone_name    = match[0].strip()
    phone_variant = match[1].strip()
    if phone_variant.endswith('.'):
        phone_variant = phone_variant[:-1]
    match         = regex_subdetails.findall(phone_variant)
    phone_subdetails = " ".join(match)
    ebay_search   = 'http://www.ebay.co.uk/sch/Mobile-Smart-Phones-/9355/i.html?LH_BIN=1&LH_ItemCondition=1000&_from=R40&_sop=15&LH_PrefLoc=1&_nkw="' + urllib.quote_plus(phone_name + '" ' + phone_subdetails + ' -faulty -spares -repair')
    ebay_html     = scraperwiki.scrape(ebay_search)
    ebay_root     = lxml.html.fromstring(ebay_html)
    try:
        ebay_total    = 0.8 * float(ebay_root.cssselect("div#ResultSetItems div.g-b")[0].text_content().strip()[1:])
    except IndexError:
        ebay_total    = 0

    monthly       = handset.cssselect("a.productList_a")[0].text_content().strip()
    upfront       = handset.cssselect("div.price")[1].text_content().strip()
    upfront_match = regex_upfront.findall(upfront)
    data = {
        'phone name'    : phone_name,
        'phone variant' : phone_variant,
        'subdetails'    : phone_subdetails,
#        'ebay search'   : ebay_search,
        'ebay total'    : ebay_total
    }
    if (monthly.find("-") == -1):
        monthly   = float(monthly[1:])
        upfront   = float(upfront_match[0])
        gross_out = 24*monthly + upfront
        data['monthly']   = monthly
        data['upfront']   = upfront
        data['gross out'] = gross_out
        data['net out']   = gross_out - ebay_total
        data['index']     = phone_name + phone_variant + str(upfront)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
    else:
        monthly_min = float(monthly[1:2])
        monthly_max = float(monthly[-2:])
        upfront_min = float(upfront_match[0])
        upfront_max = float(upfront_match[1])
        gross_out = 24*monthly_min + upfront_max
        data['monthly']   = monthly_min
        data['upfront']   = upfront_max
        data['gross out'] = gross_out
        data['net out']   = gross_out - ebay_total
        data['index']     = phone_name + phone_variant + str(upfront_max)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
        gross_out = 24*monthly_max + upfront_min
        data['monthly']   = monthly_max
        data['upfront']   = upfront_min
        data['gross out'] = gross_out
        data['net out']   = gross_out - ebay_total
        data['index']     = phone_name + phone_variant + str(upfront_min)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
import scraperwiki
import lxml.html           
import urllib
import re

html        = scraperwiki.scrape("http://store.three.co.uk/view/searchDevice?sort=payMonthlyMinPrice-ascending&viewAll=true&tariff=3046")
root        = lxml.html.fromstring(html)

regex_details     = re.compile(r">(.*?)<", re.DOTALL)
regex_subdetails  = re.compile(r"black|white|purple|blue|pink|(?<!\.)\d+GB", re.IGNORECASE)
regex_upfront     = re.compile(r"(\d+?)\.", re.DOTALL)

for handset in root.cssselect("div.productList_item"):
    phone_details = lxml.html.tostring(handset.cssselect("h4.productList_name")[0])
    match         = regex_details.findall(phone_details)
    phone_name    = match[0].strip()
    phone_variant = match[1].strip()
    if phone_variant.endswith('.'):
        phone_variant = phone_variant[:-1]
    match         = regex_subdetails.findall(phone_variant)
    phone_subdetails = " ".join(match)
    ebay_search   = 'http://www.ebay.co.uk/sch/Mobile-Smart-Phones-/9355/i.html?LH_BIN=1&LH_ItemCondition=1000&_from=R40&_sop=15&LH_PrefLoc=1&_nkw="' + urllib.quote_plus(phone_name + '" ' + phone_subdetails + ' -faulty -spares -repair')
    ebay_html     = scraperwiki.scrape(ebay_search)
    ebay_root     = lxml.html.fromstring(ebay_html)
    try:
        ebay_total    = 0.8 * float(ebay_root.cssselect("div#ResultSetItems div.g-b")[0].text_content().strip()[1:])
    except IndexError:
        ebay_total    = 0

    monthly       = handset.cssselect("a.productList_a")[0].text_content().strip()
    upfront       = handset.cssselect("div.price")[1].text_content().strip()
    upfront_match = regex_upfront.findall(upfront)
    data = {
        'phone name'    : phone_name,
        'phone variant' : phone_variant,
        'subdetails'    : phone_subdetails,
#        'ebay search'   : ebay_search,
        'ebay total'    : ebay_total
    }
    if (monthly.find("-") == -1):
        monthly   = float(monthly[1:])
        upfront   = float(upfront_match[0])
        gross_out = 24*monthly + upfront
        data['monthly']   = monthly
        data['upfront']   = upfront
        data['gross out'] = gross_out
        data['net out']   = gross_out - ebay_total
        data['index']     = phone_name + phone_variant + str(upfront)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
    else:
        monthly_min = float(monthly[1:2])
        monthly_max = float(monthly[-2:])
        upfront_min = float(upfront_match[0])
        upfront_max = float(upfront_match[1])
        gross_out = 24*monthly_min + upfront_max
        data['monthly']   = monthly_min
        data['upfront']   = upfront_max
        data['gross out'] = gross_out
        data['net out']   = gross_out - ebay_total
        data['index']     = phone_name + phone_variant + str(upfront_max)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
        gross_out = 24*monthly_max + upfront_min
        data['monthly']   = monthly_max
        data['upfront']   = upfront_min
        data['gross out'] = gross_out
        data['net out']   = gross_out - ebay_total
        data['index']     = phone_name + phone_variant + str(upfront_min)
        scraperwiki.sqlite.save(unique_keys=['index'], data=data)
