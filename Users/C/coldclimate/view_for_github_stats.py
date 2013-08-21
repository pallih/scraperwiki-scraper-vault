# Blank Python
sourcescraper = ''
import cgi, os           
paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
print paramdict
