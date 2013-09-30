# David Jones, Climate Code Foundation, 2011-09-13
# Study of how mean is computed.

# Facts I have discovered.
# Because there are days when we have min but not max, or vice versa, the monthly
#   mean is not the average of the monthly min and max.  WMO Station 71739 (EC 6078285)
#   1996-08 should provide a good example of this; this station is in GHCN-M but sadly
#   that year is not in GHCN.  Would be good to find an example in GHCN.
# CAE5040764_ 1992 06 - Daily estimates (flagged E) will result in monthly value
#   flagged as E; which is sad because there may be one or two estimated days.
# CAE4013480_ 2007 11 - Missing Daily data results in monthy value
#   being flagged as E. (a cursory inspection suggests that flag I is used
#   when the number of days is perilously low)
# CAE5022125_ 1999 08 - Monthly mean is computed from the daily means after they
#   have been rounded to 1 decimal place.

import scraperwiki

sourcescraper = 'canada-temperature-data'

scraperwiki.sqlite.attach(sourcescraper, 't')

data = scraperwiki.sqlite.execute("""select
a.id,a.year,m.`Station Name`,a.M01,a.M02,a.M03,a.M04,a.M05,a.M06,a.M07,a.M08,a.M09,a.M10,a.M11,a.M12,b.M01,b.M02,b.M03,b.M04,b.M05,b.M06,b.M07,b.M08,b.M09,b.M10,b.M11,b.M12,c.M01,c.M02,c.M03,c.M04,c.M05,c.M06,c.M07,c.M08,c.M09,c.M10,c.M11,c.M12 from t.swdata as a join t.swdata as b join t.swdata as c join t.meta as m
join (select id,n from (select id,count(*) as n from (select id,year from swdata where element='tmeanM') group by id) where n >= 30) as s
where s.id = a.id and m.id = a.id and m.`WMO Identifier` != '' and a.id == b.id and b.id == c.id and a.year == b.year and b.year == c.year and a.element == 'tminM' and b.element == 'tmaxM' and c.element == 'tmeanM'
""")

print "selected"
print data

for row in data['data']:
    i = data['keys'].index('a.M01')
    id,year,name = row[:3]
    t = row[i:]
    tmin = t[0:12]
    tmax = t[12:24]
    tmean = t[24:36]
    for idx,tn,tx,tm in [(i,a,b,c) for i,(a,b,c) in enumerate(zip(tmin,tmax,tmean)) if None not in (a,b,c)]:
        mean = (float(tn)+float(tx))*0.5
        d = float(tm)-mean
        if d > 0.1001:
            print id,year,"%02d"%(idx+1),name,tn,tx,tm,mean,d
# David Jones, Climate Code Foundation, 2011-09-13
# Study of how mean is computed.

# Facts I have discovered.
# Because there are days when we have min but not max, or vice versa, the monthly
#   mean is not the average of the monthly min and max.  WMO Station 71739 (EC 6078285)
#   1996-08 should provide a good example of this; this station is in GHCN-M but sadly
#   that year is not in GHCN.  Would be good to find an example in GHCN.
# CAE5040764_ 1992 06 - Daily estimates (flagged E) will result in monthly value
#   flagged as E; which is sad because there may be one or two estimated days.
# CAE4013480_ 2007 11 - Missing Daily data results in monthy value
#   being flagged as E. (a cursory inspection suggests that flag I is used
#   when the number of days is perilously low)
# CAE5022125_ 1999 08 - Monthly mean is computed from the daily means after they
#   have been rounded to 1 decimal place.

import scraperwiki

sourcescraper = 'canada-temperature-data'

scraperwiki.sqlite.attach(sourcescraper, 't')

data = scraperwiki.sqlite.execute("""select
a.id,a.year,m.`Station Name`,a.M01,a.M02,a.M03,a.M04,a.M05,a.M06,a.M07,a.M08,a.M09,a.M10,a.M11,a.M12,b.M01,b.M02,b.M03,b.M04,b.M05,b.M06,b.M07,b.M08,b.M09,b.M10,b.M11,b.M12,c.M01,c.M02,c.M03,c.M04,c.M05,c.M06,c.M07,c.M08,c.M09,c.M10,c.M11,c.M12 from t.swdata as a join t.swdata as b join t.swdata as c join t.meta as m
join (select id,n from (select id,count(*) as n from (select id,year from swdata where element='tmeanM') group by id) where n >= 30) as s
where s.id = a.id and m.id = a.id and m.`WMO Identifier` != '' and a.id == b.id and b.id == c.id and a.year == b.year and b.year == c.year and a.element == 'tminM' and b.element == 'tmaxM' and c.element == 'tmeanM'
""")

print "selected"
print data

for row in data['data']:
    i = data['keys'].index('a.M01')
    id,year,name = row[:3]
    t = row[i:]
    tmin = t[0:12]
    tmax = t[12:24]
    tmean = t[24:36]
    for idx,tn,tx,tm in [(i,a,b,c) for i,(a,b,c) in enumerate(zip(tmin,tmax,tmean)) if None not in (a,b,c)]:
        mean = (float(tn)+float(tx))*0.5
        d = float(tm)-mean
        if d > 0.1001:
            print id,year,"%02d"%(idx+1),name,tn,tx,tm,mean,d
