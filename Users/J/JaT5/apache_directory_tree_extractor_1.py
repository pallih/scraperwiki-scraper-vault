import urllib, urllib2, urlparse
import lxml.html
import re, os

# Format of svn directory page:
#<html><head><title>Yorkshire - Revision 2383: /mmmmc/conf</title></head>
#<body>
# <h2>Yorkshire - Revision 2383: /mmmmc/conf</h2>
# <ul>
#  <li><a href="../">..</a></li>
#  <li><a href="authz">authz</a></li>
#  <li><a href="passwd">passwd</a></li>
#  <li><a href="svnserve.conf">svnserve.conf</a></li>
# </ul>
# <hr noshade><em>Powered by <a href="http://subversion.tigris.org/">Subversion</a> version 1.6.11 (r934486).</em>
#</body></html>

def ParseSVNRevPage(url):
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return None
    root = lxml.html.fromstring(html)
    assert root.tag == "html" and root[1].tag == "body", html
    h2, ul = root[1][0], root[1][1]
    assert h2.tag == "h2" and ul.tag == "ul", html
    mh2 = re.match("(.*?) - Revision (\d+): (/.*?)$", h2.text)
    assert mh2, html
    res = {"url":url, "svnrepo":mh2.group(1), "rev":int(mh2.group(2)), "dirname":mh2.group(3)}
    if res["dirname"] != '/':
        res["dirname"] += '/'
    assert '//' not in res["dirname"], res
    lis = list(ul)
    if res["dirname"] != '/':   # the up directory .. is not in the top level
        assert lxml.html.tostring(lis[0]).strip() == '<li><a href="../">..</a></li>', html
        del lis[0]
    res["contents"] = [ ]
    for li in lis:
        cres = {"fname":li[0].text, "url":urlparse.urljoin(url, li[0].attrib.get("href"))}
        cres["abspath"] = res["dirname"]+cres["fname"]
        if cres["fname"][-1] == '/':
            cres["name"], cres["ext"] = cres["fname"][:-1], '/'
        else:
            cres["name"], cres["ext"] = os.path.splitext(cres["fname"])
        res["contents"].append(cres)
    return res


# Returns: {'url':, 'rev':2383, 'dirname':'/mmmmc/', 'svnrepo':'Yorkshire', 
#           'contents':[{'url':, 'abspath':, 'fname':'thing.txt', 'name':'thing', 'ext':'.txt'}, ... ]

def ParseSVNRevPageTree(lurl):
    res = ParseSVNRevPage(lurl)
    if not res:
        return None
    urlstack = [ (cres["abspath"], cres["url"])  for cres in res["contents"]  if cres["ext"] == '/' ]
    while urlstack:
        abspath, url = urlstack.pop()
        lres = ParseSVNRevPage(url)
        if not lres:
            continue
        assert (res["svnrepo"], res["rev"]) == (lres["svnrepo"], lres["rev"])
        assert abspath == lres["dirname"]
        res["contents"].extend(lres["contents"])
        urlstack.extend([ (cres["abspath"], cres["url"])  for cres in lres["contents"]  if cres["ext"] == '/' ])
    return res


# Testing
print ParseSVNRevPageTree("http://cave-registry.org.uk/svn/Yorkshire/mmmmc/")


# To do: same again, which can iterate through http://seagrass.goatchurch.org.uk/~expo/


import urllib, urllib2, urlparse
import lxml.html
import re, os

# Format of svn directory page:
#<html><head><title>Yorkshire - Revision 2383: /mmmmc/conf</title></head>
#<body>
# <h2>Yorkshire - Revision 2383: /mmmmc/conf</h2>
# <ul>
#  <li><a href="../">..</a></li>
#  <li><a href="authz">authz</a></li>
#  <li><a href="passwd">passwd</a></li>
#  <li><a href="svnserve.conf">svnserve.conf</a></li>
# </ul>
# <hr noshade><em>Powered by <a href="http://subversion.tigris.org/">Subversion</a> version 1.6.11 (r934486).</em>
#</body></html>

def ParseSVNRevPage(url):
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return None
    root = lxml.html.fromstring(html)
    assert root.tag == "html" and root[1].tag == "body", html
    h2, ul = root[1][0], root[1][1]
    assert h2.tag == "h2" and ul.tag == "ul", html
    mh2 = re.match("(.*?) - Revision (\d+): (/.*?)$", h2.text)
    assert mh2, html
    res = {"url":url, "svnrepo":mh2.group(1), "rev":int(mh2.group(2)), "dirname":mh2.group(3)}
    if res["dirname"] != '/':
        res["dirname"] += '/'
    assert '//' not in res["dirname"], res
    lis = list(ul)
    if res["dirname"] != '/':   # the up directory .. is not in the top level
        assert lxml.html.tostring(lis[0]).strip() == '<li><a href="../">..</a></li>', html
        del lis[0]
    res["contents"] = [ ]
    for li in lis:
        cres = {"fname":li[0].text, "url":urlparse.urljoin(url, li[0].attrib.get("href"))}
        cres["abspath"] = res["dirname"]+cres["fname"]
        if cres["fname"][-1] == '/':
            cres["name"], cres["ext"] = cres["fname"][:-1], '/'
        else:
            cres["name"], cres["ext"] = os.path.splitext(cres["fname"])
        res["contents"].append(cres)
    return res


# Returns: {'url':, 'rev':2383, 'dirname':'/mmmmc/', 'svnrepo':'Yorkshire', 
#           'contents':[{'url':, 'abspath':, 'fname':'thing.txt', 'name':'thing', 'ext':'.txt'}, ... ]

def ParseSVNRevPageTree(lurl):
    res = ParseSVNRevPage(lurl)
    if not res:
        return None
    urlstack = [ (cres["abspath"], cres["url"])  for cres in res["contents"]  if cres["ext"] == '/' ]
    while urlstack:
        abspath, url = urlstack.pop()
        lres = ParseSVNRevPage(url)
        if not lres:
            continue
        assert (res["svnrepo"], res["rev"]) == (lres["svnrepo"], lres["rev"])
        assert abspath == lres["dirname"]
        res["contents"].extend(lres["contents"])
        urlstack.extend([ (cres["abspath"], cres["url"])  for cres in lres["contents"]  if cres["ext"] == '/' ])
    return res


# Testing
print ParseSVNRevPageTree("http://cave-registry.org.uk/svn/Yorkshire/mmmmc/")


# To do: same again, which can iterate through http://seagrass.goatchurch.org.uk/~expo/


