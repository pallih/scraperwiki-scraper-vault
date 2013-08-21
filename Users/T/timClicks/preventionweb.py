from lxml import html

import scraperwiki

# Blank Python

root = 'http://www.preventionweb.net'
base = 'http://www.preventionweb.net/english/professional/contacts/'

scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS orgs (name string, uri string, preventionweb_id int) ;')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS graph (subject string, predicate string, object string); ')

def do_section(predicate, type_of_ref, refs):
    org_uri = org['uri']
    def rumble(refs, type_of_ref):
        for ref in refs:
            name = ref.text
            ref_uri = root + ref.attrib['href']
            yield to_triple(org_uri, predicate, ref_uri)
            yield to_triple(ref_uri, 'name', name)
            yield to_triple(ref_uri, 'type', type_of_ref)
            scraperwiki.sqlite.save(['uri'],  {'uri':ref_uri, 'name': name}, table_name=type_of_ref+'s')
    return [t for t in rumble(refs, type_of_ref)]

def clean_org_detail(key, val):
    key = key.strip(':')
    val = val.strip()
    if key == 'URL':
        key = 'home_url'
    key = key.lower().replace(' ', '_')
    return key, val

def to_triple(sub, pred, obj):
    return {'subject': sub, 'predicate': pred, 'object': obj}

def save_triples(triples):
    scraperwiki.sqlite.save(['subject', 'predicate', 'object'], triples, table_name='graph')

def save_orgs(orgs):
    scraperwiki.sqlite.save(['uri'], orgs, table_name='orgs')

orgs = html.parse(base).getroot().cssselect('ul.horizontal li ul li a')
orgs = [{'name': org.text, 'uri': root + org.attrib['href'], 'preventionweb_id': int(org.attrib['href'].rsplit('id=')[1])} for org in orgs]
save_orgs(orgs)
save_triples([to_triple(o['uri'], 'name', o['name']) for o in orgs])

for org in orgs:
    url = org['uri']
    org_page = html.parse(url)
    
    for el in org_page.xpath("//div[@id='details']"): #yes, there's 2
        triples = []
        for li in el.cssselect('li'):
             # ('URL', 'http://www.aberdeencity.gov.uk')
             # ('Address', 'Ground Floor, St. Nicholas House, Broad Street')
             # ('Postal Code', 'AB10 1AR')
             # ('City', 'Aberdeen')
             # ('Country', 'United Kingdom')
             # ('Telephone', '+44 1224523188')
             # ('Email', 'glawther@aberdeencity.gov.uk')
            key = li[0].text
            try:
                val = li[1].text_content()
            except IndexError:
                val = li[0].tail
            if key and val:
                key, val = clean_org_detail(key, val)
                org[key] = val
                triples.append(to_triple(org['uri'], key, val))
            else:
                print 'WEIRD', key, val
                print  
        save_triples(triples)
    save_orgs([org])

    for el in org_page.xpath("//div[@class='moduleHead']"):
        triples = []
        section= el.text_content().strip()
        refs = el.xpath("following-sibling::div[@class='moduleBody']/ul/li/a")
        if section == 'Other Governmental Organizations':
            triples.extend([to_triple(org['uri'], 'is_associated_with', root + ref.attrib['href']) for ref in refs])

        elif section == 'Organization Contacts':
            triples.extend([to_triple(org['uri'], 'has_relationship_with', root + ref.attrib['href']) for ref in refs])

        elif section == 'News & Announcements':
            triples.extend(do_section('wrote_news', 'news_item', refs))

        elif section == 'Academic Programmes':
            triples.extend(do_section('has_academic_programme', 'academic_programme', refs))

        elif section == 'Educational Materials':
            triples.extend(do_section('produced_educational_material', 'educational_material', refs))

        elif section == 'Training & Events':
            triples.extend(do_section('held_training', 'training', refs))

        elif section == 'Jobs':
            triples.extend(do_section('advertised_job', 'job', refs))

        elif section == 'National Policy, Plans & Statements':
            triples.extend(do_section('produced_national_policy', 'national_policy', refs))

        elif section == 'Documents & Publications':
            triples.extend(do_section('produced_publication', 'publication', refs))

        elif section == 'Multimedia':
            triples.extend(do_section('produced_multimedia', 'multimedia', refs))

        elif section == 'Maps':
            triples.extend(do_section('produced_map', 'map', refs))

        elif section == 'Statements & Presentations':
            statements = do_section('gave_presentation', 'presentation', refs)
            triples.extend(statements)

        elif section in ['Working Areas', 'Subjects Covered']:
            for area in el.xpath("following-sibling::div[@class='moduleBody']/ul"):
                if area[0].text == 'Themes':
                    triples.extend( [to_triple(org['uri'], 'works_under_theme', theme.text) for theme in area[1:]])
                elif area[0].text == 'Hazards':
                    triples.extend( [to_triple(org['uri'], 'works_with_hazard', hazard.text) for hazard in area[1:]])
                else:
                    print 'NOT CAPTURED: Working area', area[0].text, org['uri']
        elif section in ['Tools']: pass
        else: 
            print 'NOT CAPTURED: Section', section, org['uri']
        save_triples(triples)

