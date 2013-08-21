import scraperwiki           
scraperwiki.sqlite.attach("charity_village")

data = scraperwiki.sqlite.select(           
    '''community, jurisdiction, link, startedAt, employer, deadline from swdata order by jurisdiction, community'''
)

print '<div>Jobs from Charity Village - Dates are deadlines</div>'

for item in data :
    jurisdiction = item [ 'jurisdiction' ]
    community = item [ 'community' ]
    link = item [ 'link' ]
    employer = item [ 'employer' ]
    startedAt = item [ 'startedAt' ]
    deadline = item [ 'deadline' ]

    print '<div>'

    print '<span style="width: 3em; margin-right: 5px; ">%s</span>' % jurisdiction
    print '<span style="width: 30em; margin-right: 5px; ">%s</span>' % community
    print '<span style="width: 30em; margin-right: 5px; ">%s</span>' % link
    print '<span style="width: 30em; margin-right: 5px; ">%s</span>' % employer
    print '<span style="width: 30em; margin-right: 5px; ">%s</span>' % deadline

    print '</div>'


print '<p/>Data collection started at', startedAt, 'GMT'