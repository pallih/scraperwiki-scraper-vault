import scraperwiki
import lxml.html
import re
url = "http://www.cvqo.org/dnn/2/Newsevents/National/tabid/1986/ItemID/8424/View/Details/language/en-GB/Default.aspx"
regex = "\<input type.*"
regex1 = "\<img id.*\<p"
regex_div_first = '\<div style.*?normal.>'
regex_div_start = "\<div.*?\>"
regex_div_end = "\<\/div\>"
regex_dql = "\&\#226\;\&\#128\;\&\#156\;"
regex_sq = "&#226;&#128;&#153;"
regex_hyphen = "\&\#226\;\&\#128\;\&\#147\;"
regex_dqr = "\&\#226\;\&\#128\;\&\#157\;"
regex_span_start = "\<span.*?\>"
regex_span_end = "\<\/span\>"
regex_pnbsp = "\<p\>\&\#160\;\<\/p\>"
regex_nbsp = "\&\#160\;"
regex_twop = "\<p\>\s.*?\<p\>"
regex_br = "\<br\>"
regex_newline = "\n"
regex_returnline = "\r"
regex_tab = "\t"
regex_spaces = "\s{2,}"
regex_doublep = "\<p\>\<p\>"
regex_doubleendp = "\<\/p\>\<\/p\>"


html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

pelement = root.cssselect("div.normal")[0]
phtml = lxml.html.tostring(pelement)
phtml = re.sub(regex,"", phtml)
phtml = re.sub(regex1,"<p", phtml)
phtml = re.sub(regex_div_first,"", phtml)
phtml = re.sub(regex_div_start,"<p>", phtml)
phtml = re.sub(regex_div_end,"</p>", phtml)
phtml = re.sub(regex_dql,'"', phtml)
phtml = re.sub(regex_sq,"'", phtml)
phtml = re.sub(regex_hyphen,"-", phtml)
phtml = re.sub(regex_dqr,'"', phtml)
phtml = re.sub(regex_span_start,'', phtml)
phtml = re.sub(regex_span_end,'', phtml)
phtml = re.sub(regex_pnbsp,'', phtml)
phtml = re.sub(regex_nbsp,'', phtml)
phtml = re.sub(regex_br,'', phtml)
phtml = re.sub(regex_newline,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_tab,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_returnline,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_spaces,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_doublep,'<p>', phtml)
phtml = re.sub(regex_doubleendp,'</p>', phtml)
phtml = phtml.strip()
print phtmlimport scraperwiki
import lxml.html
import re
url = "http://www.cvqo.org/dnn/2/Newsevents/National/tabid/1986/ItemID/8424/View/Details/language/en-GB/Default.aspx"
regex = "\<input type.*"
regex1 = "\<img id.*\<p"
regex_div_first = '\<div style.*?normal.>'
regex_div_start = "\<div.*?\>"
regex_div_end = "\<\/div\>"
regex_dql = "\&\#226\;\&\#128\;\&\#156\;"
regex_sq = "&#226;&#128;&#153;"
regex_hyphen = "\&\#226\;\&\#128\;\&\#147\;"
regex_dqr = "\&\#226\;\&\#128\;\&\#157\;"
regex_span_start = "\<span.*?\>"
regex_span_end = "\<\/span\>"
regex_pnbsp = "\<p\>\&\#160\;\<\/p\>"
regex_nbsp = "\&\#160\;"
regex_twop = "\<p\>\s.*?\<p\>"
regex_br = "\<br\>"
regex_newline = "\n"
regex_returnline = "\r"
regex_tab = "\t"
regex_spaces = "\s{2,}"
regex_doublep = "\<p\>\<p\>"
regex_doubleendp = "\<\/p\>\<\/p\>"


html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)

pelement = root.cssselect("div.normal")[0]
phtml = lxml.html.tostring(pelement)
phtml = re.sub(regex,"", phtml)
phtml = re.sub(regex1,"<p", phtml)
phtml = re.sub(regex_div_first,"", phtml)
phtml = re.sub(regex_div_start,"<p>", phtml)
phtml = re.sub(regex_div_end,"</p>", phtml)
phtml = re.sub(regex_dql,'"', phtml)
phtml = re.sub(regex_sq,"'", phtml)
phtml = re.sub(regex_hyphen,"-", phtml)
phtml = re.sub(regex_dqr,'"', phtml)
phtml = re.sub(regex_span_start,'', phtml)
phtml = re.sub(regex_span_end,'', phtml)
phtml = re.sub(regex_pnbsp,'', phtml)
phtml = re.sub(regex_nbsp,'', phtml)
phtml = re.sub(regex_br,'', phtml)
phtml = re.sub(regex_newline,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_tab,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_returnline,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_spaces,'', phtml, flags=re.MULTILINE)
phtml = re.sub(regex_doublep,'<p>', phtml)
phtml = re.sub(regex_doubleendp,'</p>', phtml)
phtml = phtml.strip()
print phtml