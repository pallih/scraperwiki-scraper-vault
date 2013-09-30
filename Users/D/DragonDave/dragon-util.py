def fakeforeign(data, dictname):
    """takes a list and turns it into a dictionary of name_1, name_2, name_3"""
    out={}
    for i,d in enumerate(data):
        out["%s_%d" % (dictname, i+1)] = d
    return out

def urltohtml(url="http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"):
    import scraperwiki, urllib2, lxml.etree
    lazycache=scraperwiki.swimport('lazycache')
    pdfdata = lazycache.lazycache(url)

    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    # this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
    def gettext_with_bi_tags(el):
        res = [ ]
        if el.text:
            res.append(el.text)
        for lel in el:
            res.append("<%s>" % lel.tag)
            res.append(gettext_with_bi_tags(lel))
            res.append("</%s>" % lel.tag)
            if el.tail:
                res.append(el.tail)
        return "".join(res)
    
    # print the first hundred text elements from the first page
    text=[]
    for page in pages:
        for el in list(page)[:100]:
            if el.tag == "text":
                text.append(gettext_with_bi_tags(el))
    return '\n'.join(text)

def fakeforeign(data, dictname):
    """takes a list and turns it into a dictionary of name_1, name_2, name_3"""
    out={}
    for i,d in enumerate(data):
        out["%s_%d" % (dictname, i+1)] = d
    return out

def urltohtml(url="http://www.madingley.org/uploaded/Hansard_08.07.2010.pdf"):
    import scraperwiki, urllib2, lxml.etree
    lazycache=scraperwiki.swimport('lazycache')
    pdfdata = lazycache.lazycache(url)

    xmldata = scraperwiki.pdftoxml(pdfdata)
    root = lxml.etree.fromstring(xmldata)
    pages = list(root)
    
    # this function has to work recursively because we might have "<b>Part1 <i>part 2</i></b>"
    def gettext_with_bi_tags(el):
        res = [ ]
        if el.text:
            res.append(el.text)
        for lel in el:
            res.append("<%s>" % lel.tag)
            res.append(gettext_with_bi_tags(lel))
            res.append("</%s>" % lel.tag)
            if el.tail:
                res.append(el.tail)
        return "".join(res)
    
    # print the first hundred text elements from the first page
    text=[]
    for page in pages:
        for el in list(page)[:100]:
            if el.tag == "text":
                text.append(gettext_with_bi_tags(el))
    return '\n'.join(text)

