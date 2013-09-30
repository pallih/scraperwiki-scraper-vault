import scraperwiki
import lxml.html
import logging


def warner(d):
    formats={'onecss':'looked for "{d[selector]}" in tag "{d[tag]}", found "{d[count]}"!',
             'oneattrib':'no attribute "{d[attr]}" on tag "{d[tag]}".'}
    template=formats[d['source']]
    msg=template.format(d=d)
    logging.warn(msg)

subscribers=[warner]

def __notify(self,msg=None):
    try:
        subs=subscribers
    except NameError:
        return None
    for sub in subs:
        sub(msg)
    
lxml.html.HtmlElement.notify=__notify

def __onecss(self, selector):
    """Do or be mildly irked: get the first CSSSelector match"""
    x=self.cssselect(selector)
    if len(x) != 1:
        #self.notify('looked for "%s" in tag "%s", found %d!'%(selector, self.tag, len(x)))
        self.notify({'source':'onecss', 'selector':selector, 'tag':self.tag, 'count':len(x)})
    if len(x)==0:
        return emptyish
    else:
        return x[0]

lxml.html.HtmlElement.onecss=__onecss

def __oneattrib(self,attr):
    """Do or be mildly irked: get HTML attribute"""
    try:
        return self.attrib[attr]
    except KeyError:
        #self.notify('no attribute "%s" on tag "%s".'%(attr, self.tag))
        self.notify({'source':'oneattrib', 'attr':attr, 'tag': self.tag})
        return None

lxml.html.HtmlElement.oneattrib=__oneattrib


emptyish=lxml.html.fromstring ('<none></none>')
root = lxml.html.fromstring ('<html><table><tr><td></td></tr><tr></tr></table></html>')

print root.onecss('tablez').oneattrib('href')

import scraperwiki
import lxml.html
import logging


def warner(d):
    formats={'onecss':'looked for "{d[selector]}" in tag "{d[tag]}", found "{d[count]}"!',
             'oneattrib':'no attribute "{d[attr]}" on tag "{d[tag]}".'}
    template=formats[d['source']]
    msg=template.format(d=d)
    logging.warn(msg)

subscribers=[warner]

def __notify(self,msg=None):
    try:
        subs=subscribers
    except NameError:
        return None
    for sub in subs:
        sub(msg)
    
lxml.html.HtmlElement.notify=__notify

def __onecss(self, selector):
    """Do or be mildly irked: get the first CSSSelector match"""
    x=self.cssselect(selector)
    if len(x) != 1:
        #self.notify('looked for "%s" in tag "%s", found %d!'%(selector, self.tag, len(x)))
        self.notify({'source':'onecss', 'selector':selector, 'tag':self.tag, 'count':len(x)})
    if len(x)==0:
        return emptyish
    else:
        return x[0]

lxml.html.HtmlElement.onecss=__onecss

def __oneattrib(self,attr):
    """Do or be mildly irked: get HTML attribute"""
    try:
        return self.attrib[attr]
    except KeyError:
        #self.notify('no attribute "%s" on tag "%s".'%(attr, self.tag))
        self.notify({'source':'oneattrib', 'attr':attr, 'tag': self.tag})
        return None

lxml.html.HtmlElement.oneattrib=__oneattrib


emptyish=lxml.html.fromstring ('<none></none>')
root = lxml.html.fromstring ('<html><table><tr><td></td></tr><tr></tr></table></html>')

print root.onecss('tablez').oneattrib('href')

