import scraperwiki
import lxml.html

do_organisations = False
do_departments = False
do_dept_grants = False

# Organisations page
if do_organisations:
    orgs_page = "http://gow.epsrc.ac.uk/NGBOListOrganisations.aspx"
    
    tree = lxml.html.parse(orgs_page)
    
    organisations = []
    
    for row in tree.xpath('//table/tr')[1:]:
        cols = row.xpath('td')
    
        org_name, num_grants, grants_value, _ = [el.text_content() for el in cols]
    
        grants_value = grants_value.strip()
    
        org_url = cols[0].xpath('a')[0].attrib['href']
    
        org_id = int(org_url[len("NGBOViewOrganisation.aspx?OrganisationId="):])
    
        organisation = {'name': org_name,
                        'id': org_id,}
    
        organisations.append(organisation)
    
    scraperwiki.sqlite.save(unique_keys=["id"], data=organisations, table_name="organisations")
else:
    organisations = scraperwiki.sqlite.select("* from organisations")

if do_departments:
    departments = []
    
    for organisation in organisations:
        org_url = "http://gow.epsrc.ac.uk/NGBOViewOrganisation.aspx?OrganisationId=%s" % organisation['id']
    
        tree = lxml.html.parse(org_url)
    
        for row in tree.xpath('//table/tr')[1:]:
            cols = row.xpath('td')
    
            dept_name, _, _ = [el.text_content() for el in cols]
    
            dept_url = cols[0].xpath('a')[0].attrib['href']
    
            dept_id = dept_url[len("NGBOViewDepartment.aspx?DepartmentId="):]
    
            department = {'name': dept_name,
                           'id': dept_id,
                           'organisation_id': organisation['id'],}
    
            departments.append(department)
    
    scraperwiki.sqlite.save(unique_keys=["id"], data=departments, table_name="departments")
else:
    departments = scraperwiki.sqlite.select("* from departments")

if do_dept_grants:
    grants = []
    
    for department in departments:
        dept_url = "http://gow.epsrc.ac.uk/NGBOViewDepartment.aspx?DepartmentId=%s" % department['id']
    
        tree = lxml.html.parse(dept_url)
    
        for row in tree.xpath('//table/tr')[1:]:
            cols = row.xpath('td')
    
            grant_title, _, _ = [el.text_content() for el in cols]
    
            grant_url = cols[0].xpath('a')[0].attrib['href']
    
            grant_ref = grant_url[len("NGBOViewGrant.aspx?GrantRef="):]
    
            #tree = lxml.html.parse("http://gow.epsrc.ac.uk/NGBOViewGrant.aspx?GrantRef=%s" % grant_ref)
            
            grant = {'title': grant_title,
                     'ref': grant_ref,
                     'department_id': department['id'],}
    
            grants.append(grant)
    
    scraperwiki.sqlite.save(unique_keys=["ref"], data=grants, table_name="grants")
else:
    # grab unscraped grants
    grants = scraperwiki.sqlite.select("* from grants where summary is null")

def grab_row_people(row):
    other_names = [a.text_content() for a in row.xpath('td')[1].xpath('.//a') if 'href' in a.attrib]
    other_urls = [a.attrib['href'] for a in row.xpath('td')[1].xpath('.//a') if 'href' in a.attrib]
    
    people = []
    for i, name in enumerate(other_names):
        if "NGBOViewPerson.aspx" in other_urls[i]:
            person = {'type': 'person',
                      'name': name,
                      'id': other_urls[i][len("NGBOViewPerson.aspx?PersonId="):],}
        elif "NGBOViewPartner.aspx" in other_urls[i]:
            person = {'type': 'partner',
                      'name': name,
                      'id': other_urls[i][len("NGBOViewPartner.aspx?OrganisationId="):],}
        
        people.append(person)

    return people

for grant in grants:
    grant_url = "http://gow.epsrc.ac.uk/NGBOViewGrant.aspx?GrantRef=%s" % grant['ref']

    tree = lxml.html.parse(grant_url)

    rows = tree.xpath("//table[@id='tblFound']/tr")
    
    print grant_url

    PI = grab_row_people(rows[2])
    other_investigators = grab_row_people(rows[3])
    research_coinvestigators = grab_row_people(rows[4])
    project_partners = grab_row_people(rows[5])

    scraperwiki.sqlite.save(unique_keys=["id"], data=PI+other_investigators+research_coinvestigators, table_name="people")
    scraperwiki.sqlite.save(unique_keys=["id"], data=project_partners, table_name="partners")

    scraperwiki.sqlite.save(unique_keys=["person_id", "grant_ref"], data=[{'person_id': person['id'], 'grant_ref': grant['ref'], "relation_type":'PI'} for person in PI], table_name="people_grants")
    scraperwiki.sqlite.save(unique_keys=["person_id", "grant_ref"], data=[{'person_id': person['id'], 'grant_ref': grant['ref'], "relation_type":'OI'} for person in other_investigators], table_name="people_grants")
    scraperwiki.sqlite.save(unique_keys=["person_id", "grant_ref"], data=[{'person_id': person['id'], 'grant_ref': grant['ref'], "relation_type":'CI'} for person in research_coinvestigators], table_name="people_grants")

    scraperwiki.sqlite.save(unique_keys=["partner_id", "grant_ref"], data=[{'partner_id': partner['id'], 'grant_ref': grant['ref']} for partner in project_partners], table_name="partner_grants")

    scheme = rows[8].xpath('td')[1].text_content()

    subrows = rows[9].xpath('td')

    date_start = subrows[1].text_content()
    date_end = subrows[3].text_content()
    value = subrows[5].text_content().replace(',', '')

    topic_classifications = [topic.text_content().strip() for topic in rows[10].xpath('td')[1].xpath('.//td') if len(topic.text_content().strip()) != 0]
    sector_classifications = [sector.text_content().strip() for sector in rows[11].xpath('td')[1].xpath('.//td') if len(sector.text_content().strip()) != 0]
    related_grants = [related_grant.text_content().strip() for related_grant in rows[12].xpath('td')[1].xpath('.//td') if len(related_grant.text_content().strip()) != 0]

    scraperwiki.sqlite.save(unique_keys=['grant_a', 'grant_b'], data=[{'grant_a': grant['ref'], 'grant_b': grant_b} for grant_b in related_grants], table_name='related_grants')

    summary = rows[15].text_content().strip()
    final_report = rows[17].text_content().strip()

    further_information = rows[18].xpath('td')[1].text_content().strip()
    org_website = rows[19].xpath('td')[1].text_content().strip()
    
    grant['date_start'] = date_start
    grant['date_end'] = date_end
    grant['value'] = value
    grant['topics'] = ", ".join(topic_classifications)
    grant['sectors'] = ", ".join(sector_classifications)
    grant['summary'] = summary
    grant['final_report'] = final_report
    grant['further_information'] = further_information
    grant['org_website'] = org_website

    scraperwiki.sqlite.save(unique_keys=['ref'], data=grant, table_name='grants')

