import scraperwiki
from lxml import html

INDEX = "http://www.parliament.gov.za/live/content.php?Category_ID=97"

def fetch_index():
    document = html.parse(INDEX)
    for row in document.findall(".//tr"):
        tds = row.findall('.//td')
        a = tds[0].find('a')
        if a is None:
            continue
        link = a.get('href')
        if not 'MemberID' in link:
            continue
        data = {
            'member_id': link.rsplit('=', 1)[-1],
            'last_name': tds[0].find('a').text,
            'first_name': tds[2].text,
            'party': tds[4].find('a').text,
            'email': tds[6].find('a').text
            }

        fetch_interests(data)










def fetch_interests(member):
    report = html.parse("http://www.parliament.gov.za/live/content.php?Item_ID=485&MemberID=%s" % member['member_id'])
    tables = report.findall('.//table')
    for table in tables:
        head = table.find('.//td/b')
        if head is None:
            continue
        head = head.text.strip()
        #print head
        if 'Year' == head:
            member['reporting_year'] = table.findall('.//tr')[1].find('td').text.strip()

        if 'Company Name' in head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('.//td')
                if len(tds) != 4:
                    continue
                data = {
                    'company_name': tds[0].text.strip(),
                    'nr_of_shares': tds[1].text.strip(),
                    'nature_of_shares': tds[2].text.strip(),
                    'nominal_value': tds[3].text.strip()
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'company_name', 'nr_of_shares',
                    'nature_of_shares', 'nominal_value'], data=data, table_name='shares')

        if 'Property Description' in head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('.//td')
                if len(tds) != 3:
                    continue
                data = {
                    'description': tds[0].text.strip(),
                    'location': tds[1].text.strip(),
                    'extent': tds[2].text.strip(),
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'description', 'location'],
                    data=data, table_name='property')

        if 'Directorship' == head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('./td')
                if len(tds) != 2:
                    continue
                data = {
                    'company_name': tds[0].text_content().strip(),
                    'business_activity': tds[1].text_content().strip()
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'company_name'],
                    data=data, table_name='directorship')

        if 'Organisation Name' in head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('./td')
                if len(tds) != 2:
                    continue
                data = {
                    'company_name': tds[0].text_content().strip(),
                    'business_activity': tds[1].text_content().strip()
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'company_name'],
                    data=data, table_name='directorship')

        if 'EmployerName' in head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('./td')
                if len(tds) != 2:
                    continue
                data = {
                    'employer_name': tds[0].text_content().strip(),
                    'business_type': tds[1].text_content().strip()
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'employer_name'],
                    data=data, table_name='employment')

        if 'Pension Type' in head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('./td')
                if len(tds) != 2:
                    continue
                data = {
                    'pension_type': tds[0].text_content().strip(),
                    'source': tds[1].text_content().strip()
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'pension_type'],
                    data=data, table_name='employment')

        if 'Gift Description' in head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('./td')
                if len(tds) != 3:
                    continue
                data = {
                    'description': tds[0].text_content().strip(),
                    'source': tds[1].text_content().strip(),
                    'value': tds[2].text_content().strip()
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'description', 'source'],
                    data=data, table_name='gifts')

        if 'Benefit Description' in head:
            for row in table.findall('.//tr')[1:]:
                tds = row.findall('./td')
                if len(tds) != 3:
                    continue
                data = {
                    'description': tds[0].text_content().strip(),
                    'source': tds[1].text_content().strip(),
                    'value': tds[2].text_content().strip()
                    }
                data.update(member)
                scraperwiki.sqlite.save(unique_keys=['member_id', 'reporting_year', 'description', 'source'],
                    data=data, table_name='benefits')


#fetch_interests({'member_id': 547})
#fetch_interests({'member_id': 570})
fetch_index()