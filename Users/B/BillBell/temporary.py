import scraperwiki
from string import join

scraperwiki.sqlite.attach("charity_village")
scraperwiki.sqlite.attach("contact_point")
scraperwiki.sqlite.attach("eluta")
scraperwiki.sqlite.attach("indeed")
scraperwiki.sqlite.attach("job_bank")


data = scraperwiki.sqlite.execute ( 'select * from charity_village.swdata union all select * from contact_point.swdata union all select * from eluta.swdata union all select * from indeed.swdata union all select * from job_bank.swdata order by jurisdiction, community, jobTitle' )

keys = data [ 'keys' ]
records = data [ 'data' ]

print '''\
<html>
<title>
Career Developer Jobs
</title>
<style type="text/css">
* { font: Helvetica; margin: 0; }
.job { width: 100%; padding: 5px; overflow: auto; border-top: thin solid black; border-left: thin solid black; border-right: thin solid black; }
.one { background : lightgray; }
.two { background: white; }
.leftPortion { width: 15%;  float: left; }
.source { width: 1em; background : yellow; float: left;  }
.community { text-align:right; }
.jurisdiction { float: left; width: 4em; text-align: center; }
.rightPortion { width: 78%; margin-left: 21%; }
</style>
<script type="text/javascript" src="https://www.google.com/jsapi?key=nPkihvVQFHKS2/DEjVwaA4azPxjf75PI"></script>
<script>
google.load("jquery", "1.6.2");
</script>
<body>
<div style="font-size: 150%; ">
Job vacancies gleaned from Charity Village, Contact Point, eluta, Indeed and Job Bank. Mouse over colour patches for information. Other sources may be added as time permits.
<br/>
Refer to my <a href="http://unsymptomatictoo.blogspot.com">blog</a> for up-to-date information. You may bookmark this URL if your wish.
<br/>
If you notice a problem or fault of any kind please report it as a comment at this 
<a href="http://unsymptomatictoo.blogspot.com/2011/08/job-listings-for-career-developers-new.html">blog link</a>.
<p/>
Dates are deadlines, where they are available from the primary sources.
<p/>

</div>
'''

oneRecordTemplate = '''\
<div class="job %(choice)s">
    <div class="leftPortion">
        <div class="source" style="background : %(sourceColour)s;" source='%(sourceFullName)s' startedAt='%(startedAt)s'>&nbsp;</div>
        <div class="community">%(community)s</div>
    </div>
    <div class="jurisdiction">%(jurisdiction)s</div>
    <div class="rightPortion">
        %(rightPortion)s
    </div>
</div>'''

sourceColour = {
    'JB': '#000000',
    'CP': '#A50063',
    'CV': '#31007B',
    'IN': '#00A5C6',
    'EL': '#52B552',
    }

sourceFullNames = {
    'JB': 'Job Bank',
    'CP': 'Contact Point',
    'CV': 'Charity Village',
    'IN': 'indeed.ca',
    'EL': 'eluta.ca',
    }

one = 0
for record in records :
    result = { }
    one = ( one + 1 ) % 2
    if one :
        result [ 'choice' ] = 'one'
    else :
        result [ 'choice' ] = 'two'
    for item, key in zip ( record, keys ) :
        result [ key ] = item
    result [ 'sourceColour' ] = sourceColour [ result [ 'source' ] ]
    result [ 'rightPortion' ] = join ( [ result [ item ] for item in [ 'link', 'employer', 'salary', 'conditions', 'deadline', ] if result [ item ] ], ', ' )
    result [ 'sourceFullName' ] = sourceFullNames [ result [ 'source' ] ]
    print ( oneRecordTemplate % result ) . replace ( ', ,', ', ' )


print '''\
</body>
<script>
$("div.source").mouseover(function() {
    $(this).text('Recovered sometime after ' + $(this).attr('startedAt') + 'GMT from ' + $(this).attr('source') );
    $(this).css('color','yellow');
     $(this).width ( '300px' );
})

$("div.source").mouseout(function() {
    $(this).html('&nbsp;');
    $(this).css('color','black');
     $(this).width ( '1em' );
})

</script>
</html>
'''
