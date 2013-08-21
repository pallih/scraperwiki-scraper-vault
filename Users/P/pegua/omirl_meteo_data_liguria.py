import scraperwiki
import dateutil.parser
import calendar     

#http://93.62.155.214/~omirl/raw/astext.php?orain=201201010000&orafin=201202010000&staz=CAVI&interval=5&%20para=tem


url = "http://93.62.155.214/~omirl/raw/astext.php";

staz = "CAVI";
interval = "30";
para = "tem";



for year in range(2012,2013):
    for month in range(1,5):
        for day in calendar.monthrange(year,month):
            orain = str(year) + str(month).rjust(2, '0') + str(day).rjust(2, '0') + "0000";
            orafin = str(year) + str(month).rjust(2, '0') + str(day).rjust(2, '0') + "2359";

            get_url = url + "?" + "orain=" + orain + "&orafin=" + orafin + "&staz=" + staz + "&interval=" + interval + "&para=" + para;

            data =  scraperwiki.scrape(get_url);

            lines = data.splitlines();

            for l in lines:
    
                words = l.split();
                if( len(words) > 2 ):
                    row = {};
                    date = dateutil.parser.parse(words[2] + " " + words[3]);
                    row["date_time"] = date;
                    row["station_code"] = words[4];
                    row["measure_type"] = words[5];
                    row["measure"] = float(words[6]);
                    scraperwiki.sqlite.save(unique_keys=["date_time","station_code","measure_type"],data=row);
