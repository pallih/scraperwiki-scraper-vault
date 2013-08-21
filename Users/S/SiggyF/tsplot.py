import matplotlib.pyplot as plt
import matplotlib.dates
import cStringIO
import numpy as np
import pandas # Use this once it is updated to a newer version...
import scraperwiki
import datetime
import base64
import itertools
# Attach to time series database
sourcescraper = 'waterbase_timeseries'
scraperwiki.sqlite.attach(sourcescraper)
# Lookup data from a station
rs = scraperwiki.sqlite.execute("SELECT location_id, date, sea_surface_wind_wave_significant_height FROM waves WHERE  date > '2011-07-01' ORDER BY location_id")

fig, ax = plt.subplots(1,1)
for location, records in itertools.groupby(rs['data'], key=lambda x:x[0]):
    records = list(records)
    if not records:
        continue
    arr = np.asarray(records)
    nums = matplotlib.dates.date2num([datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S') for x in arr[:,1]])
    
    # Create a figure
    
    ax.plot(nums, arr[:,2].astype('double'), alpha=0.7, label=location)
leg = ax.legend(loc='best')
leg.set_alpha(1)
ax.set_xlabel('Time')
ax.set_ylabel('Wave height [cm]')

# Format the dates
weeks = matplotlib.dates.AutoDateLocator()  # every month
ax.xaxis.set_major_locator(weeks)
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))

# Save the generated figure to a file
stream = cStringIO.StringIO()
fig.savefig(stream,format='png')

# Some http stuff..
scraperwiki.utils.httpresponseheader("Content-Type", "image/png")
scraperwiki.dumpMessage({"content":base64.encodestring(stream.getvalue()), "message_type":"console", "encoding":"base64"})




