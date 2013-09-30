import scraperwiki           
scraperwiki.sqlite.attach("job_bank")
data = scraperwiki.sqlite.select(           
    '''employer, jobTitle, salary, community, jurisdiction, link, startedAt from swdata order by jurisdiction, community'''
)

print '<div>Jobs from jobbank.gc.ca where NOC is 4213</div>'

for item in data :
    jobTitle = item [ 'jobTitle' ]
    employer = item [ 'employer' ]
    salary = item [ 'salary' ]
    community = item [ 'community' ]
    jurisdiction = item [ 'jurisdiction' ]
    link = item [ 'link' ]
    startedAt = item [ 'startedAt' ]

    print '<div><span style="width: 3em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span>%s</div>' % ( jurisdiction, community, link, employer, salary,  )

print '<p/>Data collection started at', startedAt, 'GMT'import scraperwiki           
scraperwiki.sqlite.attach("job_bank")
data = scraperwiki.sqlite.select(           
    '''employer, jobTitle, salary, community, jurisdiction, link, startedAt from swdata order by jurisdiction, community'''
)

print '<div>Jobs from jobbank.gc.ca where NOC is 4213</div>'

for item in data :
    jobTitle = item [ 'jobTitle' ]
    employer = item [ 'employer' ]
    salary = item [ 'salary' ]
    community = item [ 'community' ]
    jurisdiction = item [ 'jurisdiction' ]
    link = item [ 'link' ]
    startedAt = item [ 'startedAt' ]

    print '<div><span style="width: 3em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span><span style="width: 30em; margin-right: 5px; ">%s</span>%s</div>' % ( jurisdiction, community, link, employer, salary,  )

print '<p/>Data collection started at', startedAt, 'GMT'