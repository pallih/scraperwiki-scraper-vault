import scraperwiki
import urllib

sourcescraper = 'lands-tribunal-decisions'
scraperwiki.sqlite.attach(sourcescraper)

categories={
    'service charges' : 'service charges',
    'insurance' : 'insurance',
    'appointment of a manager' : 'manager',
    'right to manage' : 'right to',
    'administration charges' : 'administrative',
    'purchase notices' : 'purchase',
    'breach of covenant' : 'breach',
    'acquisition by tenant of new lease' : 'acquisition',
    'variation of leases' : 'variation',
    'LVT procedure' : 'procedure' }

def make_case_string(name, reference, href):
    return(u'''<b>{name}</b> (<a href="{href}">{reference}</a>)'''.format(name=name, reference=reference, href=href))

def make_category_id(category):
    return(urllib.quote_plus(categories[category]))

small_words=['a', 'of', 'in']
# removes multiple spaces in a string
def make_title(s):
    L=s.split(' ')
    result=[]
    for word in L:
        if word in small_words:
            result.append(word)
        else:
            result.append(word[0].upper() + word[1:])
    return ' '.join(result)

def print_category(category):

    category_pattern=categories[category]
    data = scraperwiki.sqlite.select('''url_summary, respondent, decision_no, notes, lower(subcategory) as subcategory, url_doc, url_pdf, substr(decision_no, -4) as year from 'lands-tribunal-decisions'.summaries where category like "%landlord%" and subcategory like "%{0}%" order by year desc'''.format(category_pattern))

    if len(data)==0:
        print('''<p><emph>None</emph></p>''')

    for row in data:
        #print(u'''<p>{0}</p>'''.format(repr(row)))
        case_string=make_case_string(name=row['respondent'], reference=row['decision_no'], href=row['url_summary'])
        print('''<p />''')
        print(u'''{0} {subcategory}</h3>'''.format(case_string, **row))
        print(u'''<p>{notes}</p>'''.format(**row))
        print('<table>')
        for suffix in ['doc', 'pdf']:
            print(u'''<tr><td>{0}:</td><td><a href="{1}">{1}</a></td></tr>'''.format(suffix, row['url_{0}'.format(suffix)]))
        print('</table>')

def print_heading():
    print('''<h1>Lands Tribunal Decisions</h1>''')
    print('''<p>The Lands Tribunal and Upper Tribunal (Lands Chamber) <a href="http://www.landstribunal.gov.uk/Aspx/Default.aspx">decisions database</a> is fairly horrid to use. In particular because it uses javascript to load in html, it is impossible to use the "back" button properly. This view picks out and organises the decisions relating to landlord and tenant law and attempts to order them by category with the most recent first.</p>''')
    print('''<p>The Lands Tribunal also maintain a table of <a href="http://www.justice.gov.uk/downloads/tribunals/lands/court-appeal-cases.pdf">cases appealed to the court of appeal</a> which I have not yet been able to process automatically.</p>''')

def print_toc():
    print('''<h2>Contents</h2>''')
    print('''<ul>''')
    for category in categories:
        print('''<li><a href="#{0}">{1}</a></li>'''.format(make_category_id(category), make_title(category)))
    print('''</li>''')
    print('''</ul>''')

print_heading()
print_toc()

for category in categories:
    category_string=make_title(category)
    print('''<h2 id="{0}">{1}</h2>'''.format(make_category_id(category), category_string))
    print_category(category)
    import scraperwiki
import urllib

sourcescraper = 'lands-tribunal-decisions'
scraperwiki.sqlite.attach(sourcescraper)

categories={
    'service charges' : 'service charges',
    'insurance' : 'insurance',
    'appointment of a manager' : 'manager',
    'right to manage' : 'right to',
    'administration charges' : 'administrative',
    'purchase notices' : 'purchase',
    'breach of covenant' : 'breach',
    'acquisition by tenant of new lease' : 'acquisition',
    'variation of leases' : 'variation',
    'LVT procedure' : 'procedure' }

def make_case_string(name, reference, href):
    return(u'''<b>{name}</b> (<a href="{href}">{reference}</a>)'''.format(name=name, reference=reference, href=href))

def make_category_id(category):
    return(urllib.quote_plus(categories[category]))

small_words=['a', 'of', 'in']
# removes multiple spaces in a string
def make_title(s):
    L=s.split(' ')
    result=[]
    for word in L:
        if word in small_words:
            result.append(word)
        else:
            result.append(word[0].upper() + word[1:])
    return ' '.join(result)

def print_category(category):

    category_pattern=categories[category]
    data = scraperwiki.sqlite.select('''url_summary, respondent, decision_no, notes, lower(subcategory) as subcategory, url_doc, url_pdf, substr(decision_no, -4) as year from 'lands-tribunal-decisions'.summaries where category like "%landlord%" and subcategory like "%{0}%" order by year desc'''.format(category_pattern))

    if len(data)==0:
        print('''<p><emph>None</emph></p>''')

    for row in data:
        #print(u'''<p>{0}</p>'''.format(repr(row)))
        case_string=make_case_string(name=row['respondent'], reference=row['decision_no'], href=row['url_summary'])
        print('''<p />''')
        print(u'''{0} {subcategory}</h3>'''.format(case_string, **row))
        print(u'''<p>{notes}</p>'''.format(**row))
        print('<table>')
        for suffix in ['doc', 'pdf']:
            print(u'''<tr><td>{0}:</td><td><a href="{1}">{1}</a></td></tr>'''.format(suffix, row['url_{0}'.format(suffix)]))
        print('</table>')

def print_heading():
    print('''<h1>Lands Tribunal Decisions</h1>''')
    print('''<p>The Lands Tribunal and Upper Tribunal (Lands Chamber) <a href="http://www.landstribunal.gov.uk/Aspx/Default.aspx">decisions database</a> is fairly horrid to use. In particular because it uses javascript to load in html, it is impossible to use the "back" button properly. This view picks out and organises the decisions relating to landlord and tenant law and attempts to order them by category with the most recent first.</p>''')
    print('''<p>The Lands Tribunal also maintain a table of <a href="http://www.justice.gov.uk/downloads/tribunals/lands/court-appeal-cases.pdf">cases appealed to the court of appeal</a> which I have not yet been able to process automatically.</p>''')

def print_toc():
    print('''<h2>Contents</h2>''')
    print('''<ul>''')
    for category in categories:
        print('''<li><a href="#{0}">{1}</a></li>'''.format(make_category_id(category), make_title(category)))
    print('''</li>''')
    print('''</ul>''')

print_heading()
print_toc()

for category in categories:
    category_string=make_title(category)
    print('''<h2 id="{0}">{1}</h2>'''.format(make_category_id(category), category_string))
    print_category(category)
    