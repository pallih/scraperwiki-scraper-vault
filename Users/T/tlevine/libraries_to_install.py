from scraperwiki.sqlite import save,execute
import datetime

VERSIONATTRS=(
  '__version__'
, 'version'
)

test = [ ['pycurl','comment1'],['mycurl','nocomment'] ]

# 'library','*comment*'
LIBNAMES=[
   ['pycurl','']
,  ['bs4','https://bitbucket.org/ScraperWiki/scraperwiki/issue/858/beautifulsoup-4-is-not-available']
,  ['gensim','']
,  ['pyparsley','']
,  ['requests','']
,  ['lxml','']
,  ['pyth','']
,  ['pyproj', 'https://bitbucket.org/ScraperWiki/scraperwiki/issue/829/install-pyproj-for-cartographic']
,  ['chardet', 'https://bitbucket.org/ScraperWiki/scraperwiki/issue/718/install-chardet-for-encoding-guessing']
,  ['dstk', 'https://bitbucket.org/ScraperWiki/scraperwiki/issue/448/install-dstk-python-bindings']
,  ['gevent', 'https://bitbucket.org/ScraperWiki/scraperwiki/issue/760/gevent-is-not-installed']
,  ['xmltodict','']
]


DATE=datetime.datetime.now()
DATA_TABLE='https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=libraries_to_install&query=select%20library,date(datetime),version%20from%20`swdata`'

def view():
  print "<h1>Status of a few libraries</h1>"
  print "<ul>"
  for libname in LIBNAMES:
    checklib(libname)
  print "</ul>"
  print '<p>View historical information <a href="%s">here</a>. Empty "version" cells imply that the library was not installed.</p>' % DATA_TABLE


def checklib(libname):
  "Check whether a library is installed. Print its version if it is."
  try:
    lib=__import__(libname[0])
  except ImportError:
    version=None
    print "<li>%s is not installed." % libname[0] 
  else:
    version=None
    for versionattr in VERSIONATTRS:
      if hasattr(lib,versionattr):
        version=getattr(lib,versionattr)
        break
    if version==None: #If we still don't know the version
        version="Installed, dunno what version"
    print "<li>%s is at this version: %s." % (libname[0],version)
  if libname[1] != '':
      print "<b>Comment:</b> ", libname[1], "</li>"
  else:
      print "</li>"
  save([],{"library":libname[0],"version":version,"datetime":DATE})

view()