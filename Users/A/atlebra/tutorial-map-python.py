import scraperwiki
import pygooglechart


# New feature: you can put google charts onto a map:
# a new form of mash-up to experiment with
# (Any examples of similar mashups out there?)

# Known issues:
#    It would be better to assign the visualization (eg width of the chart) on already scraped data
#    The map looks good on only on one zoom level.  
#    See also http://thematicmapping.org/

def VariablePie(chartwidth, percent):
    chart = pygooglechart.PieChart2D(chartwidth, chartwidth, colours=["ff0000", "0000ff"])
    chart.add_data([percent, 100-percent])
    chart.fill_solid(pygooglechart.Chart.BACKGROUND, 'FFFFFF00')  # transparent background
    chartimg = chart.get_url()
    chart = { "chartimg":chartimg, 'Size': [chartwidth,chartwidth], 'Pixel': [-chartwidth/2,-chartwidth/2] }
    return chart


fakedata = [ ("place1", 338020, 711800, 60, 77), ("place2", 337901, 714550, 50, 89), 
             ("place3", 338979, 714749, 30, 29), ("place4", 339265, 715265, 40, 30), 
           ]


for place, easting, northing, chartwidth, percent in fakedata:
    latlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    chart = VariablePie(chartwidth, percent)
    data = { "place":place, "chart":chart }
    scraperwiki.datastore.save(unique_keys=["place"], data=data, latlng=latlng)
    
    pinurl = "http://chart.apis.google.com/chart?chst=d_map_xpin_letter&chld=pin_sright|Q|00FFFF|000000"
    pindata = { "place":place+"Q", "chart":pinurl }
    pinlatlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    scraperwiki.datastore.save(unique_keys=["place"], data=data, latlng=latlng)
    
    
    import scraperwiki
import pygooglechart


# New feature: you can put google charts onto a map:
# a new form of mash-up to experiment with
# (Any examples of similar mashups out there?)

# Known issues:
#    It would be better to assign the visualization (eg width of the chart) on already scraped data
#    The map looks good on only on one zoom level.  
#    See also http://thematicmapping.org/

def VariablePie(chartwidth, percent):
    chart = pygooglechart.PieChart2D(chartwidth, chartwidth, colours=["ff0000", "0000ff"])
    chart.add_data([percent, 100-percent])
    chart.fill_solid(pygooglechart.Chart.BACKGROUND, 'FFFFFF00')  # transparent background
    chartimg = chart.get_url()
    chart = { "chartimg":chartimg, 'Size': [chartwidth,chartwidth], 'Pixel': [-chartwidth/2,-chartwidth/2] }
    return chart


fakedata = [ ("place1", 338020, 711800, 60, 77), ("place2", 337901, 714550, 50, 89), 
             ("place3", 338979, 714749, 30, 29), ("place4", 339265, 715265, 40, 30), 
           ]


for place, easting, northing, chartwidth, percent in fakedata:
    latlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    chart = VariablePie(chartwidth, percent)
    data = { "place":place, "chart":chart }
    scraperwiki.datastore.save(unique_keys=["place"], data=data, latlng=latlng)
    
    pinurl = "http://chart.apis.google.com/chart?chst=d_map_xpin_letter&chld=pin_sright|Q|00FFFF|000000"
    pindata = { "place":place+"Q", "chart":pinurl }
    pinlatlng = scraperwiki.geo.os_easting_northing_to_latlng(easting, northing)
    scraperwiki.datastore.save(unique_keys=["place"], data=data, latlng=latlng)
    
    
    