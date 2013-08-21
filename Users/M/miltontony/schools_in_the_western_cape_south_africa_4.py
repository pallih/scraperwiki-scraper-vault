import scraperwiki
import lxml.html

base_url = 'http://wcedemis.pgwc.gov.za/wced/findschoolO.shtml?2'
html = scraperwiki.scrape(base_url)
root = lxml.html.fromstring(html)
tosave = {}


def clean_field(str):
    return '%s' % str.text_content().strip().replace('  ', '').replace('&nbsp;', ' ')

def clean_key(str):
    return '%s' % str.text_content().strip().replace(' ', '').replace('&nbsp;', '').replace('/', '')

last_school = scraperwiki.sqlite.get_var('last_school', None)
resume = False
if not last_school:
    resume = True

resume = True

for o in root.cssselect("select[name='EMIS_NO'] option"):
    school_id = o.get('value')
    tosave['school_id'] = school_id

    if not resume and last_school == school_id:
        resume = True;
    if not resume:
        continue

    #school_id = '0103007277'
    school_id = '0105000876'
    doc_html = scraperwiki.scrape('http://wcedemis.pgwc.gov.za/ibi_apps/WFServlet?IBIF_ex=INERSCHOOLN', {'EMIS_NO': school_id})
    doc = lxml.html.fromstring(doc_html)

    script = clean_field(doc.cssselect("script")[0]).split(';')
    vars = [a.strip().replace(' ','') for a in script if a.strip().replace(' ','').startswith('var')]
    tosave['lat'] = vars[0][vars[0].find("'")+1:vars[0].rfind("'")]
    tosave['long'] = vars[1][vars[1].find("'")+1:vars[1].rfind("'")]
    
    tables = doc.cssselect("table")
    for tr in tables[0].cssselect("tr"):
        tds = tr.cssselect("td")
        if len(tds) == 2:
            tosave[clean_key(tds[0])] = clean_field(tds[1])

    if len(tables) >= 6:
        gender_rows = tables[2].cssselect("tr")
            
        headings_f = ['%s_F'%clean_field(v) for v in gender_rows[2].cssselect("td")]
        headings_m = ['%s_M'%clean_field(v) for v in gender_rows[2].cssselect("td")]
        headings_t = ['%s_T'%clean_field(v) for v in gender_rows[2].cssselect("td")]
    
        fs = [clean_field(v) for v in gender_rows[3].cssselect("td")]
        ms = [clean_field(v) for v in gender_rows[4].cssselect("td")]
        ts = [clean_field(v) for v in gender_rows[5].cssselect("td")]
        tosave = dict(tosave.items() + dict(zip(headings_f, fs)).items())
        tosave = dict(tosave.items() + dict(zip(headings_m, ms)).items())
        tosave = dict(tosave.items() + dict(zip(headings_t, ts)).items())

    rooms_rows = tables[len(tables)-2].cssselect("tr")

    headings = [clean_field(v) for v in rooms_rows[2].cssselect("td")]
    rooms = [clean_field(v) for v in rooms_rows[3].cssselect("td")]
    tosave = dict(tosave.items() + dict(zip(headings, rooms)).items())

    break  # Process 1 schooll only

print tosave
    #scraperwiki.sqlite.save(unique_keys=['school_id'], data=tosave)
    #scraperwiki.sqlite.save_var('last_school', school_id)
