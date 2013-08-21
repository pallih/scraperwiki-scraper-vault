import scraperwiki
import lxml.html

pagename = 'http://scorecard.lcv.org/scorecard?year=2012'

##
## Although LCV indexes by year, all the votes live on each page, and are just hidden
## Hence it is sufficient to look at a single year to see all results
##

page = scraperwiki.scrape(pagename)
pageroot = lxml.html.fromstring(page)

### House ###
    
    
for row in pageroot.cssselect('''div#scorecard-votes-page-house-table-data > div.'tableRow dataItem' '''):
    house = 'House'
    for y in row.cssselect('span.voteYear'):
        voteYear = y.text

    for vN in row.cssselect('span.voteNumber'):
        voteNumber = vN.text

    for vT in row.cssselect('span.voteTitle a'):
        voteTitle = vT.text

    for vL in row.cssselect('span.voteTitle a'):
        voteLink = vL.attrib['href']

    for vI in row.cssselect('span.voteIssuesFULL'):
        voteIssues = vI.text

    votepagename = 'http://scorecard.lcv.org/' + voteLink
    votepage = scraperwiki.scrape(votepagename)
    votepageroot = lxml.html.fromstring(votepage)
    for p in votepageroot.cssselect('div#roll-call-vote-summary'):
        summary = p.text_content()

    for c in votepageroot.cssselect('div#roll-call-vote-pro-env-choice'):
        choice = c.text_content()
    for box in votepageroot.cssselect('div#roll-call-vote-stats-box'):
        for f in box.cssselect('span#roll-call-vote-number-for'):
            votesFor = f.text
        for a in box.cssselect('span#roll-call-vote-number-against'):
            votesAgainst = a.text
        for n in box.cssselect('span#roll-call-vote-number-notvoting'):
            votesNot = n.text
    #print(voteYear, house, voteNumber, voteTitle, voteLink, voteIssues, summary, choice, votesFor, votesAgainst, votesNot)
        
    data = {'Year': voteYear, 'House': house , 'Number': voteNumber, 'Title': voteTitle, 'Issues': voteIssues, 'Summary': summary, 'Choice': choice, 'VotesFor': votesFor, 'VotesAgainst': votesAgainst, 'NotVoting': votesNot}
    scraperwiki.sqlite.save(unique_keys = ['Summary'], data = data)



### SENATE ###
for row in pageroot.cssselect('''div#scorecard-votes-page-senate-table-data > div.'tableRow dataItem' '''):
    house = 'Senate'
    for y in row.cssselect('span.voteYear'):
        voteYear = y.text

    for vN in row.cssselect('span.voteNumber'):
        voteNumber = vN.text

    for vT in row.cssselect('span.voteTitle a'):
        voteTitle = vT.text

    for vL in row.cssselect('span.voteTitle a'):
        voteLink = vL.attrib['href']

    for vI in row.cssselect('span.voteIssuesFULL'):
        voteIssues = vI.text

    votepagename = 'http://scorecard.lcv.org/' + voteLink
    votepage = scraperwiki.scrape(votepagename)
    votepageroot = lxml.html.fromstring(votepage)
    for p in votepageroot.cssselect('div#roll-call-vote-summary'):
        summary = p.text_content()

    for c in votepageroot.cssselect('div#roll-call-vote-pro-env-choice'):
        choice = c.text_content()
    for box in votepageroot.cssselect('div#roll-call-vote-stats-box'):
        for f in box.cssselect('span#roll-call-vote-number-for'):
            votesFor = f.text
        for a in box.cssselect('span#roll-call-vote-number-against'):
            votesAgainst = a.text
        for n in box.cssselect('span#roll-call-vote-number-notvoting'):
            votesNot = n.text
    #print(voteYear, house, voteNumber, voteTitle, voteLink, voteIssues, summary, choice, votesFor, votesAgainst, votesNot)
        
    data = {'Year': voteYear, 'House': house , 'Number': voteNumber, 'Title': voteTitle, 'Issues': voteIssues, 'Summary': summary, 'Choice': choice, 'VotesFor': votesFor, 'VotesAgainst': votesAgainst, 'NotVoting': votesNot}
    scraperwiki.sqlite.save(unique_keys = ['Summary'], data = data)
