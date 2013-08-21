# Return a configurable HTTP status.

import cgi           
import os

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

# See http://tools.ietf.org/html/rfc2616#section-6
status = paramdict.get('status')


