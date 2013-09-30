import scraperwiki
import lxml.html
import lxml

html = scraperwiki.scrape("http://themallcineplex.com/")
html2 = scraperwiki.scrape("http://www.mvisioncinemas.com/?c=showtime")
html3 = scraperwiki.scrape("http://www.qlapcineplex.com/?c=showtime")
        
root = lxml.html.fromstring(html)
root2 = lxml.html.fromstring(html2)
root3 = lxml.html.fromstring(html3)

count = 0

## Below contains the data that is needed
## Each object within tables object is a movie entry
mallTable = root.xpath('//center/div/table')

## Below is for Empire Cinema
empireTable = root2.xpath('//table[@width="100%" and @cellspacing="5" and @cellpadding="5"]')

## Below is for Seri Qlap Cinema
qlapTable = root3.xpath('//table[@width="726" and @cellspacing="0" and @cellpadding="0" and @border="0"]')


## Next we need to seperate the information into particular sections:
## Movie Title
## Movie Image
## Movie Schedule Date
## Movie Schedule Timtable (for each date)

## Below is for counter
j = 0

## Below is for the date for each coloum, iterate the last one
##print mallTable[0][1][1][0][0][0].text_content()
##print len(mallTable[0][1][1][0][0])



## Get all the dates of all columns

date1 = ' '.join(mallTable[0][1][1][0][0][0].text_content().split())
date2 = ' '.join(mallTable[0][1][1][0][0][1].text_content().split())
date3 = ' '.join(mallTable[0][1][1][0][0][2].text_content().split())
date4 = ' '.join(mallTable[0][1][1][0][0][3].text_content().split())
date5 = ' '.join(mallTable[0][1][1][0][0][4].text_content().split())
date6 = ' '.join(mallTable[0][1][1][0][0][5].text_content().split())
date7 = ' '.join(mallTable[0][1][1][0][0][6].text_content().split())


for i in mallTable:
    movieTitle = i.xpath('//span[@class="showtitle2"]')
    moviePoster = i.xpath('//img[@border="1"]')

    timetable1 = ' '.join(i[1][1][0][1][0].text_content().split())
    timetable2 = ' '.join(i[1][1][0][1][1].text_content().split())
    timetable3 = ' '.join(i[1][1][0][1][2].text_content().split())
    timetable4 = ' '.join(i[1][1][0][1][3].text_content().split())
    timetable5 = ' '.join(i[1][1][0][1][4].text_content().split())
    timetable6 = ' '.join(i[1][1][0][1][5].text_content().split())
    timetable7 = ' '.join(i[1][1][0][1][6].text_content().split())


    data = {
        'table_id' : j,
        'cinema_id' : 'mall',
        'movie_title' : movieTitle[j].text_content(),
        'movie_poster' : moviePoster[j].get('src'),
        'movie_show_day_1' : date1,
        'movie_show_day_2' : date2,
        'movie_show_day_3' : date3,
        'movie_show_day_4' : date4,
        'movie_show_day_5' : date5,
        'movie_show_day_6' : date6,
        'movie_show_day_7' : date7,
        'movie_show_time_1' : timetable1,
        'movie_show_time_2' : timetable2,
        'movie_show_time_3' : timetable3,
        'movie_show_time_4' : timetable4,
        'movie_show_time_5' : timetable5,
        'movie_show_time_6' : timetable6,
        'movie_show_time_7' : timetable7,

    }
    j += 1
    ##save data
    scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

##for i in mallTable:
##    timetable1 = i[1][1][0][1][j].text_content()
##    print timetable1
##    j += 1

## Now start looping to Empire table

## Before that, we need to have a new counter and j now becomes table_id value
k = 0

Date = root2.xpath('//font[@face="arial" and @size="2" and @color="#ffffff"]')
currentDate = Date[0][0].text_content()

for i2 in empireTable :
##    print i2[0][0][1][0][0][0][1].text_content()
    movieTitle = i2.xpath('//span[@class="orangetxt"]')
    #print movieTitle[k].text_content()

    movieTimeTable = i2.xpath('//span[@class="whitetxt"]/b')
    #print movieTimeTable[k].text_content()
    
    ## For the empire table, we can only get for MOVIE TITLE & MOVIE TIMETABLE
    ## for today only!

    data = {
        'table_id' : j,
        'cinema_id' : 'empire',
        'movie_title' : movieTitle[k].text_content(),
        'movie_poster' : 'null',
        'movie_show_day_1' : currentDate,
        'movie_show_day_2' : 'null',
        'movie_show_day_3' : 'null',
        'movie_show_day_4' : 'null',
        'movie_show_day_5' : 'null',
        'movie_show_day_6' : 'null',
        'movie_show_day_7' : 'null',
        'movie_show_time_1' : movieTimeTable[k].text_content(),
        'movie_show_time_2' : 'null',
        'movie_show_time_3' : 'null',
        'movie_show_time_4' : 'null',
        'movie_show_time_5' : 'null',
        'movie_show_time_6' : 'null',
        'movie_show_time_7' : 'null',

    }
    j+=1
    k+=1
    ##save data
    scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

## Now start looping to Seri Qlap table

## As before j now becomes table_id value, a new counter is needed
p = 0

## Get the date, this is the same that was done to empire cinema
Date = root3.xpath('//font[@face="arial" and @size="3" and @color="#006600"]')
currentDate = Date[0][0].text_content()

## Sometimes Seri Qlap Cinema website don't have movie timetable at RANDOM days
## So now we need to check that, below is checks for that.
foundNoSchedule = qlapTable[0][0][0].text_content()

if foundNoSchedule.find('No Schedule') > -1:

    print 'DEBUG: ' + foundNoSchedule[0:33] + ' ' + foundNoSchedule[33:] + ' at Seri Qlap Cinema'
    data = {
        'table_id' : j,
        'cinema_id' : 'qlap',
        'movie_title' : 'NO SCHEDULE FOUND',
        'movie_poster' : 'null',
        'movie_show_day_1' : currentDate,
        'movie_show_day_2' : 'null',
        'movie_show_day_3' : 'null',
        'movie_show_day_4' : 'null',
        'movie_show_day_5' : 'null',
        'movie_show_day_6' : 'null',
        'movie_show_day_7' : 'null',
        'movie_show_time_1' : 'null',
        'movie_show_time_2' : 'null',
        'movie_show_time_3' : 'null',
        'movie_show_time_4' : 'null',
        'movie_show_time_5' : 'null',
        'movie_show_time_6' : 'null',
        'movie_show_time_7' : 'null',

    }
    ##save data
    scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

else:

    for i3 in qlapTable:
    ##    print i3[0][0][1][0][0][0][1].text_content()
        movieTitle = i3.xpath('//span[@class="movietitle"]')
        ##print movieTitle[p].text_content()

        movieTimeTable = i3.xpath('//td[@class="moviedetails"]/b')
        ##print movieTimeTable[p][0].text_content()

        ## For the Seri Qlap table, we can only get for MOVIE TITLE & MOVIE TIMETABLE
        ## for today only!
    
        data = {
            'table_id' : j,
            'cinema_id' : 'qlap',
            'movie_title' : movieTitle[p].text_content(),
            'movie_poster' : 'null',
            'movie_show_day_1' : currentDate,
            'movie_show_day_2' : 'null',
            'movie_show_day_3' : 'null',
            'movie_show_day_4' : 'null',
            'movie_show_day_5' : 'null',
            'movie_show_day_6' : 'null',
            'movie_show_day_7' : 'null',
            'movie_show_time_1' : movieTimeTable[p].text_content(),
            'movie_show_time_2' : 'null',
            'movie_show_time_3' : 'null',
            'movie_show_time_4' : 'null',
            'movie_show_time_5' : 'null',
            'movie_show_time_6' : 'null',
            'movie_show_time_7' : 'null',
    
        }


        j+=1
        p+=1
        ##save data
        scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

print 'DEBUG: Reached end of program'import scraperwiki
import lxml.html
import lxml

html = scraperwiki.scrape("http://themallcineplex.com/")
html2 = scraperwiki.scrape("http://www.mvisioncinemas.com/?c=showtime")
html3 = scraperwiki.scrape("http://www.qlapcineplex.com/?c=showtime")
        
root = lxml.html.fromstring(html)
root2 = lxml.html.fromstring(html2)
root3 = lxml.html.fromstring(html3)

count = 0

## Below contains the data that is needed
## Each object within tables object is a movie entry
mallTable = root.xpath('//center/div/table')

## Below is for Empire Cinema
empireTable = root2.xpath('//table[@width="100%" and @cellspacing="5" and @cellpadding="5"]')

## Below is for Seri Qlap Cinema
qlapTable = root3.xpath('//table[@width="726" and @cellspacing="0" and @cellpadding="0" and @border="0"]')


## Next we need to seperate the information into particular sections:
## Movie Title
## Movie Image
## Movie Schedule Date
## Movie Schedule Timtable (for each date)

## Below is for counter
j = 0

## Below is for the date for each coloum, iterate the last one
##print mallTable[0][1][1][0][0][0].text_content()
##print len(mallTable[0][1][1][0][0])



## Get all the dates of all columns

date1 = ' '.join(mallTable[0][1][1][0][0][0].text_content().split())
date2 = ' '.join(mallTable[0][1][1][0][0][1].text_content().split())
date3 = ' '.join(mallTable[0][1][1][0][0][2].text_content().split())
date4 = ' '.join(mallTable[0][1][1][0][0][3].text_content().split())
date5 = ' '.join(mallTable[0][1][1][0][0][4].text_content().split())
date6 = ' '.join(mallTable[0][1][1][0][0][5].text_content().split())
date7 = ' '.join(mallTable[0][1][1][0][0][6].text_content().split())


for i in mallTable:
    movieTitle = i.xpath('//span[@class="showtitle2"]')
    moviePoster = i.xpath('//img[@border="1"]')

    timetable1 = ' '.join(i[1][1][0][1][0].text_content().split())
    timetable2 = ' '.join(i[1][1][0][1][1].text_content().split())
    timetable3 = ' '.join(i[1][1][0][1][2].text_content().split())
    timetable4 = ' '.join(i[1][1][0][1][3].text_content().split())
    timetable5 = ' '.join(i[1][1][0][1][4].text_content().split())
    timetable6 = ' '.join(i[1][1][0][1][5].text_content().split())
    timetable7 = ' '.join(i[1][1][0][1][6].text_content().split())


    data = {
        'table_id' : j,
        'cinema_id' : 'mall',
        'movie_title' : movieTitle[j].text_content(),
        'movie_poster' : moviePoster[j].get('src'),
        'movie_show_day_1' : date1,
        'movie_show_day_2' : date2,
        'movie_show_day_3' : date3,
        'movie_show_day_4' : date4,
        'movie_show_day_5' : date5,
        'movie_show_day_6' : date6,
        'movie_show_day_7' : date7,
        'movie_show_time_1' : timetable1,
        'movie_show_time_2' : timetable2,
        'movie_show_time_3' : timetable3,
        'movie_show_time_4' : timetable4,
        'movie_show_time_5' : timetable5,
        'movie_show_time_6' : timetable6,
        'movie_show_time_7' : timetable7,

    }
    j += 1
    ##save data
    scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

##for i in mallTable:
##    timetable1 = i[1][1][0][1][j].text_content()
##    print timetable1
##    j += 1

## Now start looping to Empire table

## Before that, we need to have a new counter and j now becomes table_id value
k = 0

Date = root2.xpath('//font[@face="arial" and @size="2" and @color="#ffffff"]')
currentDate = Date[0][0].text_content()

for i2 in empireTable :
##    print i2[0][0][1][0][0][0][1].text_content()
    movieTitle = i2.xpath('//span[@class="orangetxt"]')
    #print movieTitle[k].text_content()

    movieTimeTable = i2.xpath('//span[@class="whitetxt"]/b')
    #print movieTimeTable[k].text_content()
    
    ## For the empire table, we can only get for MOVIE TITLE & MOVIE TIMETABLE
    ## for today only!

    data = {
        'table_id' : j,
        'cinema_id' : 'empire',
        'movie_title' : movieTitle[k].text_content(),
        'movie_poster' : 'null',
        'movie_show_day_1' : currentDate,
        'movie_show_day_2' : 'null',
        'movie_show_day_3' : 'null',
        'movie_show_day_4' : 'null',
        'movie_show_day_5' : 'null',
        'movie_show_day_6' : 'null',
        'movie_show_day_7' : 'null',
        'movie_show_time_1' : movieTimeTable[k].text_content(),
        'movie_show_time_2' : 'null',
        'movie_show_time_3' : 'null',
        'movie_show_time_4' : 'null',
        'movie_show_time_5' : 'null',
        'movie_show_time_6' : 'null',
        'movie_show_time_7' : 'null',

    }
    j+=1
    k+=1
    ##save data
    scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

## Now start looping to Seri Qlap table

## As before j now becomes table_id value, a new counter is needed
p = 0

## Get the date, this is the same that was done to empire cinema
Date = root3.xpath('//font[@face="arial" and @size="3" and @color="#006600"]')
currentDate = Date[0][0].text_content()

## Sometimes Seri Qlap Cinema website don't have movie timetable at RANDOM days
## So now we need to check that, below is checks for that.
foundNoSchedule = qlapTable[0][0][0].text_content()

if foundNoSchedule.find('No Schedule') > -1:

    print 'DEBUG: ' + foundNoSchedule[0:33] + ' ' + foundNoSchedule[33:] + ' at Seri Qlap Cinema'
    data = {
        'table_id' : j,
        'cinema_id' : 'qlap',
        'movie_title' : 'NO SCHEDULE FOUND',
        'movie_poster' : 'null',
        'movie_show_day_1' : currentDate,
        'movie_show_day_2' : 'null',
        'movie_show_day_3' : 'null',
        'movie_show_day_4' : 'null',
        'movie_show_day_5' : 'null',
        'movie_show_day_6' : 'null',
        'movie_show_day_7' : 'null',
        'movie_show_time_1' : 'null',
        'movie_show_time_2' : 'null',
        'movie_show_time_3' : 'null',
        'movie_show_time_4' : 'null',
        'movie_show_time_5' : 'null',
        'movie_show_time_6' : 'null',
        'movie_show_time_7' : 'null',

    }
    ##save data
    scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

else:

    for i3 in qlapTable:
    ##    print i3[0][0][1][0][0][0][1].text_content()
        movieTitle = i3.xpath('//span[@class="movietitle"]')
        ##print movieTitle[p].text_content()

        movieTimeTable = i3.xpath('//td[@class="moviedetails"]/b')
        ##print movieTimeTable[p][0].text_content()

        ## For the Seri Qlap table, we can only get for MOVIE TITLE & MOVIE TIMETABLE
        ## for today only!
    
        data = {
            'table_id' : j,
            'cinema_id' : 'qlap',
            'movie_title' : movieTitle[p].text_content(),
            'movie_poster' : 'null',
            'movie_show_day_1' : currentDate,
            'movie_show_day_2' : 'null',
            'movie_show_day_3' : 'null',
            'movie_show_day_4' : 'null',
            'movie_show_day_5' : 'null',
            'movie_show_day_6' : 'null',
            'movie_show_day_7' : 'null',
            'movie_show_time_1' : movieTimeTable[p].text_content(),
            'movie_show_time_2' : 'null',
            'movie_show_time_3' : 'null',
            'movie_show_time_4' : 'null',
            'movie_show_time_5' : 'null',
            'movie_show_time_6' : 'null',
            'movie_show_time_7' : 'null',
    
        }


        j+=1
        p+=1
        ##save data
        scraperwiki.sqlite.save(unique_keys=['table_id'], data=data)

print 'DEBUG: Reached end of program'