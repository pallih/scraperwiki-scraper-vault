import scraperwiki
import lxml.html
import urllib

sourcescraper = 'schulen-berlin-de-source'
query_args = scraperwiki.utils.GET()

scraperwiki.sqlite.attach(sourcescraper)

fragment = "schulportrait" if not 'fragment' in query_args else urllib.unquote(query_args['fragment'])
where = "" if not 'where' in query_args else " WHERE " + urllib.unquote(query_args['where'])
sql_query = "IDSchulzweig, SchulNr, SchulName, Schulzweig, " + fragment + " FROM schule" + where
school_list = scraperwiki.sqlite.select(sql_query)
css = "" if not 'css' in query_args else urllib.unquote(query_args['css'])

print '''<!DOCTYPE html>
<html>
    <head><title></title></head>
    <body>
        <table border="1">
            <tr>
                <td>IDSchulzweig</td>
                <td>SchulNr</td>
                <td>SchulName</td>
                <td>Schulzweig</td>
                <td>%s</td>
            </tr>''' % fragment

for s in school_list:
    root = lxml.html.fromstring(s[fragment])
    sel = root.cssselect(css)
    elem = "" if not sel else sel[0].text_content()
    print '''
            <tr>
                <td>%i</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>''' % (s['IDSchulzweig'], s['SchulNr'], s['SchulName'], s['Schulzweig'], elem)

print '''
        </table>
    </body>
</html>'''