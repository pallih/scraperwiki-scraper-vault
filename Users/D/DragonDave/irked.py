import lxml.html
import logging

last=-1 # number of items from last call.

emptyish=lxml.html.fromstring('<none></none>')

def warner(d):
    formats={'onecss':'looked for "{d[selector]}" in tag "{d[tag]}", found {d[count]}!',
             'oneattrib':'no attribute "{d[attr]}" on tag "{d[tag]}".',
             'onexpath':'looked for "{d[xpath]}" in tag "{d[tag]}", found {d[count]}!',
             'oneid':'no id "{d[id]}" found.'}
    template=formats[d['source']]
    msg=template.format(d=d)
    logging.warn(msg)

subscribers=[warner]


def __notify(self,msg=None):
    """Send a message to all subscribers."""
    try:
        subs=subscribers
    except NameError:
        return None
    for sub in subs:
        sub(msg)
    
lxml.html.HtmlElement.notify=__notify

def __onecss(self, selector, silent=False):
    """Do or be mildly irked: get the first CSSSelector match"""
    x=self.cssselect(selector)
    if len(x) != 1 and not silent:
        #self.notify('looked for "%s" in tag "%s", found %d!'%(selector, self.tag, len(x)))
        self.notify({'source':'onecss', 'selector':selector, 'tag':self.tag, 'count':len(x)})
    last=len(x)
    if len(x)==0:
        return emptyish
    else:
        return x[0]

lxml.html.HtmlElement.onecss=__onecss

def __oneattrib(self,attr,silent=False):
    """Do or be mildly irked: get HTML attribute"""
    try:
        last = 1
        return self.attrib[attr]
    except KeyError:
        #self.notify('no attribute "%s" on tag "%s".'%(attr, self.tag))
        last = 0
        if not silent: self.notify({'source':'oneattrib', 'attr':attr, 'tag': self.tag})
        return None

lxml.html.HtmlElement.oneattrib=__oneattrib

def __oneid(self,id,silent=False):
    """Do or be mildly irked: get_element_by_id"""
    try:
        last = 1
        return self.get_element_by_id(id)
    except KeyError:
        last = 0
        if not silent: self.notify({'source':'oneid', 'id':id})
        return emptyish

lxml.html.HtmlElement.oneid=__oneid

def __onexpath(self, xpath, silent=False):
    """Do or be mildly irked: get xpath item"""
    try:
        x=self.xpath(xpath)
    except SyntaxError: # this should never happen
        raise() # untested
        x=''
    last=len(x)
    if len(x) != 1 and not silent:
        self.notify({'source':'onexpath', 'xpath':xpath, 'tag': self.tag, 'count':len(x)})
    if len(x) == 0:
        # guess at correct type, string or element
        if xpath[-2:]=='()' or re.search('@[^/\[\]]*$', xpath): # this will break :(
            return ''
        else:
            return emptyish
    else:
        return x[0]

lxml.html.HtmlElement.onexpath=__onexpath
