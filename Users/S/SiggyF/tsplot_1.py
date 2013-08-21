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
rs = scraperwiki.sqlite.execute("SELECT location_id, sea_surface_wind_wave_significant_height, sea_surface_wind_wave_period, sea_surface_wind_wave_from_direction FROM waves WHERE  date > '2010-01-01' ORDER BY location_id")

perlocation = dict((key, list(val)) for key, val in itertools.groupby(rs['data'], lambda x:x[0]))
n= len(perlocation)
fig, axes = plt.subplots(n,1, figsize=(5,4*n), sharex=True, sharey=True)
for ax, (location, records) in zip(axes,perlocation.items()):
    if not records:
        continue
    arr = np.asarray(records)
    
    # Create a figure   
    sc = ax.scatter(
            arr[:,2].astype('double') + np.random.random(arr.shape[0]) - 0.005, #jitter
            arr[:,1].astype('double'),
            c=arr[:,3].astype('double'), 
            alpha=0.05, edgecolor='none', label=location,
            cmap='hsv'
        )
    ax.set_xlabel('Wave period [s]')
    ax.set_ylabel('Wave height [cm]')
    ax.set_title(location)
    cb = plt.colorbar(sc, ax=ax)
    cb.set_alpha(1)
    cb.draw_all()
    
fig.subplots_adjust(hspace=0)
plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)


# Save the generated figure to a file
stream = cStringIO.StringIO()
fig.savefig(stream,format='png', dpi=300)

# Some http stuff..
scraperwiki.utils.httpresponseheader("Content-Type", "image/png")
scraperwiki.dumpMessage({"content":base64.encodestring(stream.getvalue()), "message_type":"console", "encoding":"base64"})




