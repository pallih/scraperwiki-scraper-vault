"""Dumbly look for all routes within New York state"""
from urllib2 import urlopen, build_opener,HTTPCookieProcessor
from lxml.html import fromstring
from scraperwiki.sqlite import save,get_var,save_var,show_tables,select
from httplib import BadStatusLine

def main():
  if not 'cities_done' in show_tables():
    cities_done=[]
  else:
    cities_done=select('* from cities_done')

  for fromcity in CITIES_NY:
    for tocity in CITIES_NY:
      if fromcity==tocity:
        print 'Skipping within-%s route' % fromcity
      elif {"from":fromcity,"to":tocity} in cities_done:
        print 'Already scraped %s to %s' % (fromcity,tocity)
      else:
        grab(fromcity,"NY",tocity,"NY")
        save([],{"from":fromcity,"to":tocity},'cities_done')

def url(from_city,from_state,to_city,to_state):
  return 'http://www.coachusa.com/ss.details.asp?action=Lookup&c1=%s&s1=%s&c2=%s&s2=%s' % (from_city.replace(' ','+'),from_state,to_city,to_state)

CITIES_NY=(
  "Albany",
  "Alfred",
  "Alfred+Station",
  "Alleghany",
  "Almond",
  "Angola",
  "Arcade",
  "Athol+Springs",
  "Bardonia",
  "Bath",
  "Bear+Mountain",
  "Belmont",
  "Belvediere",
  "Binghamton",
  "Black+Creek",
  "Blauvelt",
  "Bloomingburg",
  "Bradford+Junction",
  "Buffalo",
  "Buffalo+Airport",
  "Burnside",
  "Cassadaga",
  "Central+Nyack",
  "Central+Valley",
  "Chaffee",
  "Cheektowaga",
  "Chester",
  "Circleville",
  "Clinton",
  "Cobleskill",
  "Coldenham",
  "Congers",
  "Corning",
  "Cornwall",
  "Croton+Falls",
  "Delevan",
  "Deposit",
  "Dunkirk",
  "East+Aurora",
  "East+Randolph",
  "Eighteen+Mile",
  "Ellenville",
  "Elmira",
  "Evans+Center",
  "Falconer",
  "Fallsburg",
  "Farnham",
  "Ferndale",
  "Fishkill",
  "Fort+Montgomery",
  "Franklinville",
  "Fredonia",
  "Gerry",
  "Goshen",
  "Grandview",
  "Greene",
  "Hamilton",
  "Hancock",
  "Harriman",
  "Harris",
  "Haverstraw",
  "Hempstead",
  "High+View",
  "Highland",
  "Highland+Falls",
  "Highland+Mills",
  "Hillcrest",
  "Hinsdale",
  "Holland",
  "Hornell",
  "Hyde+Park",
  "Irving+Junction",
  "Ischua",
  "Islip",
  "Ithaca",
  "Jamestown",
  "Jerusalem",
  "Kennedy",
  "Kerhonkson",
  "Kiamesha",
  "Lackawanna",
  "Lake+Ronkonkoma",
  "Lakeview+Junction",
  "Laona",
  "Liberty",
  "Lime+Lake",
  "Little+Valley",
  "Livingston+Manor",
  "Loch+Sheldrake",
  "Machias",
  "Mahopac",
  "Maplehurst",
  "Maybrook",
  "Melville",
  "Merriwold",
  "Middletown",
  "Mineola",
  "Monroe",
  "Montgomery",
  "Monticello",
  "Morrisville",
  "Mount+Ivy",
  "Mountaindale",
  "Mountainville",
  "Nanuet",
  "Napanoch",
  "New+City",
  "New+Hampton",
  "New+Windsor",
  "New+York",
  "Newark+Liberty+Airport",
  "Newburgh",
  "Norwich",
  "Nyack",
  "Olean",
  "Oneonta",
  "Orangeburg",
  "Owego",
  "Oxford",
  "Palisades",
  "Parksville",
  "Patchogue",
  "Pearl+River",
  "Phillipsport",
  "Piermont",
  "Pomona",
  "Port+Jervis",
  "Poughkeepsie",
  "Queens+Village",
  "Randolph",
  "Rhinebeck",
  "Rochester",
  "Rock+Hill",
  "Rockland+Lake",
  "Rockland+Plaza+Station",
  "Roscoe",
  "Saint+Bonaventure",
  "Salamanca",
  "Schenectady",
  "Shaleton",
  "Sherburne",
  "Sheridan",
  "Silver+Creek",
  "Sinclairville",
  "Sloatsburg",
  "South+Fallsburg",
  "South+Spring+Valley",
  "South+Wales",
  "Southfields",
  "Sparkill",
  "Spring+Glen",
  "Spring+Valley",
  "Staatsburg",
  "Stony+Point",
  "Suffern",
  "Summitville",
  "Syracuse",
  "Tallman",
  "Tappan",
  "Tarrytown",
  "Tompkins+Cove",
  "Tuxedo",
  "Upper+Nyack",
  "Utica",
  "Vails+Gate",
  "Valhalla",
  "Valley+Cottage",
  "Vandalia",
  "Walden",
  "Wanakah",
  "Wappingers+Falls",
  "Washingtonville",
  "Waverly",
  "Wawarsing",
  "West+Haverstraw",
  "West+Nyack",
  "West+Point",
  "White+Plains",
  "Whitney+Point",
  "Woodbourne",
  "Woodbury+Common",
  "Woodlawn",
  "Woodridge",
  "Wurtsboro",
  "Yorkshire",
)


def get_columns(table):
  """Get the schedule table columns from the xml"""
  rawcolumns=table.xpath('tr[position()=2]/td')  
  columns=[rawcolumn.xpath('descendant::img/@title') for rawcolumn in rawcolumns]

  nonstop=['days','arrow','route']
  for i in range(len(columns)):
    if columns[i]==[]:
      columns[i]=[nonstop.pop(0)]

  #print columns
  return [col[0] for col in columns]

def grab(from_city,from_state,to_city,to_state):
  theurl=url(from_city,from_state,to_city,to_state)
  opener = build_opener(HTTPCookieProcessor())

  try:
    o=opener.open(theurl)
  except BadStatusLine:
    return None

  xml=fromstring(o.read())
  if not route_exists(xml):
    return None

  try:
    table=xml.xpath('//table[tr[@class="tableHilightHeader"]]')[0]
  except:
    save([],{
      "from_city":from_city
    , "from_stat":from_state
    , "to_city":to_city
    , "to_state":to_state
    },'errors')
    return None

  #cities=table.xpath('tr[position()=1]/td')
  schedules=table.xpath('tr[position()>2]')
  columns=get_columns(table)

  #Get the id
  odId=get_var('origin_destination_id')
  sId=get_var('schedule_id')
  if None==odId:
    odId=1
  if None==sId:
    sId=1

  #Initialize for the loop
  d=[]
  on_fromstops=True

  for schedule in schedules:
    times=schedule.xpath('td/child::node()[position()=1]')
    #times.pop()
    #times.append(schedule.xpath('td/text()')[-1])
    print zip(times,columns)
    #assert False
    for value,column in zip(times,columns):
      if "days"==column:
        row={"key":"days"}
      elif "arrow"==column:
        on_fromstops=False
        continue
      elif "Route/Trip"==column:
        row={"key":"route_code"}

      elif on_fromstops:
        row={
          "key":"fromstop"
        , "stop":column
        }
      elif not on_fromstops:
        row={
          "key":"tostop"
        , "stop":column
        }
      #End if statement
      row.update({
        "value":value
      , "sId":sId
      , "odId":odId
      })
      d.append(row)
    #End for loop
    sId+=1
  #End for loop

  #Save origin-destination information
  save(['id'],{
    "id":odId
  , "from_city":from_city
  , "from_stat":from_state
  , "to_city":to_city
  , "to_state":to_state
  },'origin_destinations')

  #Save schedule information
  save([],d,'schedules')

  odId+=1
  save_var('origin_destination_id',odId)
  save_var('schedule_id',sId)

def route_exists(xml):
  """Given the xml, check whether there are any schedules on the page"""
  img=xml.xpath('//img[@src="/apps/SSAdmin/views/images/btn_plan.gif"]')
  return 0==len(img)

#grab("White+Plains","NY","Ithaca","NY")
#main()

#from scraperwiki.sqlite import execute
#for t in show_tables():
#  execute('alter table %s rename to %s_backup' % (t,t))
#  if not '_backup' not in t:
#    execute('drop table %s' % t )"""Dumbly look for all routes within New York state"""
from urllib2 import urlopen, build_opener,HTTPCookieProcessor
from lxml.html import fromstring
from scraperwiki.sqlite import save,get_var,save_var,show_tables,select
from httplib import BadStatusLine

def main():
  if not 'cities_done' in show_tables():
    cities_done=[]
  else:
    cities_done=select('* from cities_done')

  for fromcity in CITIES_NY:
    for tocity in CITIES_NY:
      if fromcity==tocity:
        print 'Skipping within-%s route' % fromcity
      elif {"from":fromcity,"to":tocity} in cities_done:
        print 'Already scraped %s to %s' % (fromcity,tocity)
      else:
        grab(fromcity,"NY",tocity,"NY")
        save([],{"from":fromcity,"to":tocity},'cities_done')

def url(from_city,from_state,to_city,to_state):
  return 'http://www.coachusa.com/ss.details.asp?action=Lookup&c1=%s&s1=%s&c2=%s&s2=%s' % (from_city.replace(' ','+'),from_state,to_city,to_state)

CITIES_NY=(
  "Albany",
  "Alfred",
  "Alfred+Station",
  "Alleghany",
  "Almond",
  "Angola",
  "Arcade",
  "Athol+Springs",
  "Bardonia",
  "Bath",
  "Bear+Mountain",
  "Belmont",
  "Belvediere",
  "Binghamton",
  "Black+Creek",
  "Blauvelt",
  "Bloomingburg",
  "Bradford+Junction",
  "Buffalo",
  "Buffalo+Airport",
  "Burnside",
  "Cassadaga",
  "Central+Nyack",
  "Central+Valley",
  "Chaffee",
  "Cheektowaga",
  "Chester",
  "Circleville",
  "Clinton",
  "Cobleskill",
  "Coldenham",
  "Congers",
  "Corning",
  "Cornwall",
  "Croton+Falls",
  "Delevan",
  "Deposit",
  "Dunkirk",
  "East+Aurora",
  "East+Randolph",
  "Eighteen+Mile",
  "Ellenville",
  "Elmira",
  "Evans+Center",
  "Falconer",
  "Fallsburg",
  "Farnham",
  "Ferndale",
  "Fishkill",
  "Fort+Montgomery",
  "Franklinville",
  "Fredonia",
  "Gerry",
  "Goshen",
  "Grandview",
  "Greene",
  "Hamilton",
  "Hancock",
  "Harriman",
  "Harris",
  "Haverstraw",
  "Hempstead",
  "High+View",
  "Highland",
  "Highland+Falls",
  "Highland+Mills",
  "Hillcrest",
  "Hinsdale",
  "Holland",
  "Hornell",
  "Hyde+Park",
  "Irving+Junction",
  "Ischua",
  "Islip",
  "Ithaca",
  "Jamestown",
  "Jerusalem",
  "Kennedy",
  "Kerhonkson",
  "Kiamesha",
  "Lackawanna",
  "Lake+Ronkonkoma",
  "Lakeview+Junction",
  "Laona",
  "Liberty",
  "Lime+Lake",
  "Little+Valley",
  "Livingston+Manor",
  "Loch+Sheldrake",
  "Machias",
  "Mahopac",
  "Maplehurst",
  "Maybrook",
  "Melville",
  "Merriwold",
  "Middletown",
  "Mineola",
  "Monroe",
  "Montgomery",
  "Monticello",
  "Morrisville",
  "Mount+Ivy",
  "Mountaindale",
  "Mountainville",
  "Nanuet",
  "Napanoch",
  "New+City",
  "New+Hampton",
  "New+Windsor",
  "New+York",
  "Newark+Liberty+Airport",
  "Newburgh",
  "Norwich",
  "Nyack",
  "Olean",
  "Oneonta",
  "Orangeburg",
  "Owego",
  "Oxford",
  "Palisades",
  "Parksville",
  "Patchogue",
  "Pearl+River",
  "Phillipsport",
  "Piermont",
  "Pomona",
  "Port+Jervis",
  "Poughkeepsie",
  "Queens+Village",
  "Randolph",
  "Rhinebeck",
  "Rochester",
  "Rock+Hill",
  "Rockland+Lake",
  "Rockland+Plaza+Station",
  "Roscoe",
  "Saint+Bonaventure",
  "Salamanca",
  "Schenectady",
  "Shaleton",
  "Sherburne",
  "Sheridan",
  "Silver+Creek",
  "Sinclairville",
  "Sloatsburg",
  "South+Fallsburg",
  "South+Spring+Valley",
  "South+Wales",
  "Southfields",
  "Sparkill",
  "Spring+Glen",
  "Spring+Valley",
  "Staatsburg",
  "Stony+Point",
  "Suffern",
  "Summitville",
  "Syracuse",
  "Tallman",
  "Tappan",
  "Tarrytown",
  "Tompkins+Cove",
  "Tuxedo",
  "Upper+Nyack",
  "Utica",
  "Vails+Gate",
  "Valhalla",
  "Valley+Cottage",
  "Vandalia",
  "Walden",
  "Wanakah",
  "Wappingers+Falls",
  "Washingtonville",
  "Waverly",
  "Wawarsing",
  "West+Haverstraw",
  "West+Nyack",
  "West+Point",
  "White+Plains",
  "Whitney+Point",
  "Woodbourne",
  "Woodbury+Common",
  "Woodlawn",
  "Woodridge",
  "Wurtsboro",
  "Yorkshire",
)


def get_columns(table):
  """Get the schedule table columns from the xml"""
  rawcolumns=table.xpath('tr[position()=2]/td')  
  columns=[rawcolumn.xpath('descendant::img/@title') for rawcolumn in rawcolumns]

  nonstop=['days','arrow','route']
  for i in range(len(columns)):
    if columns[i]==[]:
      columns[i]=[nonstop.pop(0)]

  #print columns
  return [col[0] for col in columns]

def grab(from_city,from_state,to_city,to_state):
  theurl=url(from_city,from_state,to_city,to_state)
  opener = build_opener(HTTPCookieProcessor())

  try:
    o=opener.open(theurl)
  except BadStatusLine:
    return None

  xml=fromstring(o.read())
  if not route_exists(xml):
    return None

  try:
    table=xml.xpath('//table[tr[@class="tableHilightHeader"]]')[0]
  except:
    save([],{
      "from_city":from_city
    , "from_stat":from_state
    , "to_city":to_city
    , "to_state":to_state
    },'errors')
    return None

  #cities=table.xpath('tr[position()=1]/td')
  schedules=table.xpath('tr[position()>2]')
  columns=get_columns(table)

  #Get the id
  odId=get_var('origin_destination_id')
  sId=get_var('schedule_id')
  if None==odId:
    odId=1
  if None==sId:
    sId=1

  #Initialize for the loop
  d=[]
  on_fromstops=True

  for schedule in schedules:
    times=schedule.xpath('td/child::node()[position()=1]')
    #times.pop()
    #times.append(schedule.xpath('td/text()')[-1])
    print zip(times,columns)
    #assert False
    for value,column in zip(times,columns):
      if "days"==column:
        row={"key":"days"}
      elif "arrow"==column:
        on_fromstops=False
        continue
      elif "Route/Trip"==column:
        row={"key":"route_code"}

      elif on_fromstops:
        row={
          "key":"fromstop"
        , "stop":column
        }
      elif not on_fromstops:
        row={
          "key":"tostop"
        , "stop":column
        }
      #End if statement
      row.update({
        "value":value
      , "sId":sId
      , "odId":odId
      })
      d.append(row)
    #End for loop
    sId+=1
  #End for loop

  #Save origin-destination information
  save(['id'],{
    "id":odId
  , "from_city":from_city
  , "from_stat":from_state
  , "to_city":to_city
  , "to_state":to_state
  },'origin_destinations')

  #Save schedule information
  save([],d,'schedules')

  odId+=1
  save_var('origin_destination_id',odId)
  save_var('schedule_id',sId)

def route_exists(xml):
  """Given the xml, check whether there are any schedules on the page"""
  img=xml.xpath('//img[@src="/apps/SSAdmin/views/images/btn_plan.gif"]')
  return 0==len(img)

#grab("White+Plains","NY","Ithaca","NY")
#main()

#from scraperwiki.sqlite import execute
#for t in show_tables():
#  execute('alter table %s rename to %s_backup' % (t,t))
#  if not '_backup' not in t:
#    execute('drop table %s' % t )