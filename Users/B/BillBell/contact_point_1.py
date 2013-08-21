import scraperwiki           
scraperwiki.sqlite.attach("contact_point")

data = scraperwiki.sqlite.select(           
    '''jobTitle, community, jurisdiction, link, startedAt, conditions, deadline from swdata order by jurisdiction, community'''
)

print '<div>Jobs from Contact Point - Dates are deadlines</div>'

for item in data :
    jobTitle = item [ 'jobTitle' ]
    community = item [ 'community' ]
    jurisdiction = item [ 'jurisdiction' ]
    link = item [ 'link' ]
    startedAt = item [ 'startedAt' ]
    conditions = item [ 'conditions' ]
    deadline = item [ 'deadline' ]

    jobTitlePart = '<a href="%s">%s</a>' % ( link, jobTitle )
    print '<div><span style="width: 3em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span></div>' % ( jurisdiction, community, jobTitlePart, conditions, deadline, )

print '<p/>Data collection started at', startedAt, 'GMT'