import scraperwiki
import lxml.html
import datetime
channel_names = ["BBC 1", "BBC 2", "ITV1", "Channel 4", "Channel 5", "BBC Three"]
channel_numbers = [101, 102, 103, 104, 105, 115]
index = 0
scraperwiki.sqlite.execute("drop table if exists swdata")


for day in range(0,7):
     for chan in range(len(channel_numbers)):
        html = scraperwiki.scrape("http://live.tvgenius.net/accessibletv/listings.html?genre=01%%7c%%7cEntertainment&firstChannel=101&lastChannel=784&tvgFirstChannelNumber=%d&tvgLastChannelNumber=%d&tvgDayOffset=%d&tvgFlagFilter=%%25&chan=BBC1+London&tvgBroadcaster=BDSSkyCable&colour=one&size=one&tvgChannelGenre=01%%7c%%7cEntertainment#content" % (channel_numbers[chan], channel_numbers[chan], day))

        root = lxml.html.fromstring(html)
        shows = []
        times = []
        suffixes = []
        for title in root.cssselect("a.tvg_show span.tvg_show_title"):
            shows.append(title.text)

        for tm in root.cssselect('a.tvg_show span.tvg_show_start'):
            tm = tm.text
            if tm[-2:] == 'pm':
                noon_value = 12
            else:
                noon_value = 0
            hour = int(tm[:-5])
            if len(tm) == 6:
                minute = int(tm[2:4])
            else:
                minute = int(tm[3:5])
            real_time = datetime.time(hour, minute)
            times.append(real_time)
            suffix = tm[-2:]
            suffixes.append(suffix)

        current_date = datetime.date.today()
        offset_date = datetime.date(current_date.year, current_date.month, current_date.day + day)
            

        for x in range(len(shows)):
            index += 1
            scraperwiki.sqlite.save(unique_keys=["index"], data={"date": offset_date, "time":times[x], "channel":channel_names[chan], "show":shows[x], "index":index, "suffix":suffixes[x]})