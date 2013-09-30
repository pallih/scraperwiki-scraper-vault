# Blank Python
import scraperwiki
import os
import cgi
           
paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

if 'table' in paramdict:
    scraperwiki.sqlite.save (table_name=paramdict['table'], data=[paramdict], unique_keys=['link'])
    print "Added to %s."%paramdict['table']
print """

<form method=get>
<input type='hidden' name='apikey' value='%s'><br>
Table:<input type='input' name='table' value=override><br>
Link:<input type='input' name='link'><br>
New Type:<input type='input' name='type'><br>
Parser Arguments:<input type='input' name='parsearg'><br>
<input type='submit'>
</form>

<form method=get>
<input type='hidden' name='apikey' value='%s'><br>
Table:<input type='input' name='table' value='todo'><br>
Link To Process:<input type='input' name='link'><br>
<input type='submit'>
</form>

"""%(paramdict['apikey'], paramdict['apikey'])
# Blank Python
import scraperwiki
import os
import cgi
           
paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

if 'table' in paramdict:
    scraperwiki.sqlite.save (table_name=paramdict['table'], data=[paramdict], unique_keys=['link'])
    print "Added to %s."%paramdict['table']
print """

<form method=get>
<input type='hidden' name='apikey' value='%s'><br>
Table:<input type='input' name='table' value=override><br>
Link:<input type='input' name='link'><br>
New Type:<input type='input' name='type'><br>
Parser Arguments:<input type='input' name='parsearg'><br>
<input type='submit'>
</form>

<form method=get>
<input type='hidden' name='apikey' value='%s'><br>
Table:<input type='input' name='table' value='todo'><br>
Link To Process:<input type='input' name='link'><br>
<input type='submit'>
</form>

"""%(paramdict['apikey'], paramdict['apikey'])
