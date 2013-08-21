import scraperwiki
from string import join
from datetime import datetime

scraperwiki.sqlite.attach("contact_point_2")
scraperwiki.sqlite.attach("eluta")
scraperwiki.sqlite.attach("indeed")
scraperwiki.sqlite.attach("job_bank")


data = scraperwiki.sqlite.execute ( 'select * from contact_point_2.swdata union all select * from eluta.swdata union all select * from indeed.swdata union all select * from job_bank.swdata order by jurisdiction, community, jobTitle' )

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
<div style="font-size: 180%; ">
Jobs for Employment Counsellors and related
</div>
<div style="font-size: 150%; ">
Gleaned from Charity Village, Contact Point, eluta, Indeed and Job Bank. Mouse over colour patches for information. Other sources may be added as time permits.
<br/>
Refer to my <a href="http://unsymptomatictoo.blogspot.com">blog</a> for up-to-date information. You may bookmark this URL if your wish.
<br/>
<div style="font-size: 120%; ">Counts by Source</div>
<div style="font-size: 80%; ">
<div class="JBcount">Job Bank count: <span></span></div>
<div class="CPcount">Contact Point count: <span></span></div>
<div class="CVcount">Charity Village count: <span></span></div>
<div class="INcount">Indeed count: <span></span></div>
<div class="ELcount">Eluta count: <span></span></div>
<div class="othercount">others: <span></span></div>
</div>
<p/>
<b>Counts of one or less (except in the 'others' category) can mean a fault in my software.</b> However, for the time being, the zero count 
associated with Contact Point is a consequence of a change to that site that this software cannot accommodate yet. 
If you notice a problem or fault of any kind elsewhere though please report it as a comment at this 
<a href="http://unsymptomatictoo.blogspot.com/2011/08/job-listings-for-career-developers-new.html">blog link</a>.
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
JBcount = 0
CVcount = 0
INcount = 0
ELcount = 0
CPcount = 0
othercount = 0
for record in records :
    result = { }
    for item, key in zip ( record, keys ) :
        result [ key ] = item
    if result [ 'link' ] == '-' or len ( result [ 'link' ] ) < 3 : continue
    one = ( one + 1 ) % 2
    if one :
        result [ 'choice' ] = 'one'
    else :
        result [ 'choice' ] = 'two'
    result [ 'sourceColour' ] = sourceColour [ result [ 'source' ] ]
    result [ 'rightPortion' ] = join ( [ result [ item ] for item in [ 'link', 'employer', 'salary', 'conditions',  ] if result [ item ] ], ', ' )
    if result [ 'deadline' ] :
        result [ 'rightPortion' ] += ', Deadline ' + result [ 'deadline' ]
    if result [ 'dateposted' ] :
        post_date = datetime . strptime ( result [ 'dateposted' ],'%Y-%m-%d' )
        result [ 'rightPortion' ] += post_date . strftime ( ', Posted %%A %s %%B %%Y' % int ( post_date . strftime ( '%d' ) ) )
    result [ 'sourceFullName' ] = sourceFullNames [ result [ 'source' ] ]
    if result [ 'source' ] == 'JB' :
        JBcount += 1
    elif result [ 'source' ] == 'CP' :
        CPcount += 1
    elif result [ 'source' ] == 'CV' :
        CVcount += 1
    elif result [ 'source' ] == 'IN' :
        INcount += 1
    elif result [ 'source' ] == 'EL' :
        ELcount += 1
    else :
        othercount += 1
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

$("div.JBcount>span").text('%(JBcount)s');
$("div.CVcount>span").text('%(CVcount)s');
$("div.INcount>span").text('%(INcount)s');
$("div.ELcount>span").text('%(ELcount)s');
$("div.CPcount>span").text('%(CPcount)s');
$("div.othercount>span").text('%(othercount)s');


</script>
</html>
''' % locals ( )
