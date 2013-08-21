import dateutil.parser
import datetime

def isoparser(s):
    x=dateutil.parser.parser()._parse(s)
    print x

    day=[]
    for val,l in [x.year,4], [x.month,2], [x.day,2]:
        format="%0"+str(l)+"d"
        if val is not None:
            day.append(format % val)
        else:
            break
    daystr='-'.join(day)

    time=[]
    for val,l in [x.hour,2], [x.minute,2], [x.second,2]:
        format="%0"+str(l)+"d"
        if val is not None:
            time.append(format % val)
        else:
            break

    timestr=':'.join(time)
    if timestr and x.microsecond:
        timestr=timestr+'.'+str(x.microsecond)
    #if timestr and x.tzoffset:
    #    print "%+03d:%02d"%(x.tzoffset/3600)
    if daystr and timestr:
        return 'T'.join([daystr,timestr])
    else:
        return daystr or timestr
#("1912")
#print isoparser('2 1928, 02pm')

