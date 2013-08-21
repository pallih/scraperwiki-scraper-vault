# code based on the scraperwiki.utils.swimport(name) function written here:
# https://bitbucket.org/ScraperWiki/scraperwiki/src/6035e7c30b29/scraperlibs/python/scraperwiki/utils.py#cl-115

# Function: Downloads the code and executes it as a module.  

# raw code from github:
url = "https://raw.github.com/tulsawebdevs/okdata/master/python/thd_food_inspections.py"

import urllib, imp, tempfile

modulecode = urllib.urlopen(url).read() + "\n"
modulefile = tempfile.NamedTemporaryFile(suffix='.py')
modulefile.write(modulecode)
modulefile.flush()
fp = open(modulefile.name)
print fp.read()
code = imp.load_module("code", fp, modulefile.name, (".py", "U", 1))
