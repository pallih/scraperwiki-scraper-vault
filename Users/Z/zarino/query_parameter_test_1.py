import cgi
import os

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
print paramdictimport cgi
import os

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
print paramdict