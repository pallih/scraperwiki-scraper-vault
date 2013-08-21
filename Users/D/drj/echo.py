# Echo
# Prints the CGI arguments.

import scraperwiki

import cgi
import os

scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')
print os.getenv("QUERY_STRING", "")
qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
print "QUERY_STRING parameters are:"
for k,v in qs.iteritems():
    print k, '=', v
print "And that's all"