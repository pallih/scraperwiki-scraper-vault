import re

import scraperwiki           
html = scraperwiki.scrape("http://www.coopdirectory.org/directory.htm")

import lxml.html           
root = lxml.html.fromstring(html)

state = None
coop = None
txt = []

def cleanup(s):
    s = s.replace("\r\n","")
    s = re.sub(r'(?i)phone:',"",s)
    s = re.sub(r'(?i)fax:',"",s)
    s = re.sub(r'  +'," ",s)
    s = s.lstrip()
    s = s.rstrip()
    return s

def finalize_coop():
    global state
    global coop
    global txt
    if coop and len(txt)>0 and state != "International":  # formatting in International section is too irregular to parse
        data = {
          'title' : cleanup(coop),
          'state': state,
        }
        if len(txt)>=1:
            data['address1'] = cleanup(txt[0])
        if len(txt)>=2:
            data['address2'] = cleanup(txt[1])
        for t in txt[2:]:
            if re.search("phone",t,flags=re.IGNORECASE):
                data['phone'] = cleanup(t)
            if re.search("fax",t,flags=re.IGNORECASE):
                data['fax'] = cleanup(t)
            if re.search("@",t):
                data['email'] = cleanup(t)
            if re.search("http://",t):
                data['website'] = cleanup(t)
        print data
        scraperwiki.sqlite.save(unique_keys=['title', 'state'], data=data)
    coop = None
    txt = []

for entry in root.cssselect('span, b, p'):
    set_state = entry.cssselect('a[name]')
    set_coop = entry.cssselect('b')
    if set_state:
        finalize_coop()
        state = set_state[0].get("name")
        # print "STATE", state
    elif set_coop:
        possible_coop = set_coop[0].text_content()
        if re.search("[a-zA-Z0-9]",possible_coop):
            finalize_coop()
            coop = possible_coop
    elif entry.tag == "p":
        content = entry.text_content()
        if re.search("[a-zA-Z0-9]",content):
            content = content.replace(u'\xa0',u'')
            content = content.replace("\r\n","")
            txt.append(content)

finalize_coop()
