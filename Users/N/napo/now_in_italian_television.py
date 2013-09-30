import scraperwiki 
import os
from datetime import datetime
from pytz import timezone
scraperdata = "italian_tv_schedules"
scraperwiki.sqlite.attach(scraperdata,"its")
now = datetime.now(timezone('Europe/Rome'))
day = now.strftime('%Y-%m-%d')
hour = now.strftime('%H')
minutes = now.strftime('%M')
sql ="begin,tv,what \
        from its.tvschedules where its.tvschedules.day ='%s' \
        and its.tvschedules.hour >= %i and its.tvschedules.hour <= %i \
        order by hour, minutes, tv" % (day,int(hour),(int(hour)+1))
data = scraperwiki.sqlite.select(sql) 
print '<h1>Italian television schedule - %s</h1>' % day
print '''
<style type="text/css">
#t_schedule {
    font-family: arial, geneva, helvetica;
}
table, th, td
{
border: 1px solid black;
}
table
{
border-collapse:collapse;
}
table,th, td
{
border: 1px solid black;
}
table
{
width:100%;
}
th
{
height:50px;
} 
table, td, th
{
border:1px solid green;
}
th
{
background-color:green;
color:white;
}
</style>
<div>
'''
print '<table id="t_schedule">'
print '<tbody>'
print '<tr><th>time</th><th>tv</th><th>program</th></tr>'
for d in data:
    print '<tr>'
    print '<td>%s</>' % d['begin']
    print '<td>%s</>' % d['tv']
    print '<td>%s</>' % d['what']
    print '</tr>'
print '''
    </tbody>
    </table>
</div>
'''

import scraperwiki 
import os
from datetime import datetime
from pytz import timezone
scraperdata = "italian_tv_schedules"
scraperwiki.sqlite.attach(scraperdata,"its")
now = datetime.now(timezone('Europe/Rome'))
day = now.strftime('%Y-%m-%d')
hour = now.strftime('%H')
minutes = now.strftime('%M')
sql ="begin,tv,what \
        from its.tvschedules where its.tvschedules.day ='%s' \
        and its.tvschedules.hour >= %i and its.tvschedules.hour <= %i \
        order by hour, minutes, tv" % (day,int(hour),(int(hour)+1))
data = scraperwiki.sqlite.select(sql) 
print '<h1>Italian television schedule - %s</h1>' % day
print '''
<style type="text/css">
#t_schedule {
    font-family: arial, geneva, helvetica;
}
table, th, td
{
border: 1px solid black;
}
table
{
border-collapse:collapse;
}
table,th, td
{
border: 1px solid black;
}
table
{
width:100%;
}
th
{
height:50px;
} 
table, td, th
{
border:1px solid green;
}
th
{
background-color:green;
color:white;
}
</style>
<div>
'''
print '<table id="t_schedule">'
print '<tbody>'
print '<tr><th>time</th><th>tv</th><th>program</th></tr>'
for d in data:
    print '<tr>'
    print '<td>%s</>' % d['begin']
    print '<td>%s</>' % d['tv']
    print '<td>%s</>' % d['what']
    print '</tr>'
print '''
    </tbody>
    </table>
</div>
'''

