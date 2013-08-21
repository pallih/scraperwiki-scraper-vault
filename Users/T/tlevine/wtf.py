from scraperwiki.sqlite import save,select
from copy import copy
from itertools import combinations
DATA={u'City': None, u'Latitude': u'-32.476662', u'id': u'1', u'Longitute': u'24.062041', u'Status': u'A', u'SuburdId': 1, u'TownName': u'ABERDEEN', u'Address1': u'', u'Address2': u'', u'EntityType': None, 'provinceId': '1', u'EntityCentreNumber': u'5541', u'ProvinceId': 1, u'RegionName': u'', u'Province': None, u'EntityTypeOptionId': 11, u'OperatingHoursWeekend': u'8:30 AM \u2013 11AM', u'EntityName': u'ABERDEEN', u'EntitySwiftCode': u'SBZAZAJJ', 'cityId': '1', u'IBTNumber': u'16', u'EntityTypeId': 2, u'OperatingHoursWeekDay': u'9 AM \u2013 3:30PM', 'provinceName': 'Eastern Cape', 'date_scraped': 1328932864.404724, u'DateAdded': u'/Date(1298325600000+0200)/', u'EntityTypeOption': None, 'cityName': 'ABERDEEN', u'AddedBy': 1, u'CityId': 1, u'SuburdSuburb': None, u'EntityDescription': u'', u'Guid': u'370a8d57-399e-4df3-a9f3-2cb550467924', u'Id': 6679, u'StreetName': u'6 PORTER STREET'}

def str_and_save(data):
  strdata={}
  for key in data.keys():
    strdata[str(key)]=data[key]
  print strdata
  save([],strdata,'str-data')

def subsets():
  allkeys=set(DATA.keys())
  print("The full row has %d keys." % len(keys))

  ns=range(len(allkeys)+1)
  ns.reverse()

  for n in ns:
    for combination in combinations(allkeys,n):
      save_except(DATA,combination)

  #Compare
  compare_keys()

def save_except(data_orig,keys):
  data=copy(data_orig)

  data["count-removed"]=len(keys)
  data["removed-keys"]=''
  for key in keys:
    data["removed-keys"]+=key+','
    del(data[key])
  data["removed-keys"]=data["removed-keys"][0:-1] #Remove trailing comma
  save([], data, 'wtf')

def compare_keys():
  allkeys=set(DATA.keys())
  columns=set(select("* from `wtf` limit 1")[0].keys())
  difference=allkeys.difference(columns)

  difference_nonnull=set()
  for key in difference:
    if DATA.has_key(key) and DATA[key]!=None:
      difference_nonnull=difference_nonnull.union([key])


  print("Here is the original set of keys.")
  print(allkeys)
  print("Here is resulting column list.)")
  print(columns)
  print("These keys were the original set of keys but not in the resulting table list")
  print(difference)
  print("These keys were the not null in original set of keys and were not in the resulting table list")
  print(difference_nonnull)

def save_except_nones(DATA):
  data=copy(DATA)
  for key in data.keys():
    if data[key]==None:
      del(data[key])
  save([],data,'nones-removed')

#Basic saves
save([], DATA, 'plain')
save([u'id'], DATA)
save(['id'], DATA)

#Adjusting the data before saving
#save_except_nones(DATA)
#str_and_save(DATA)

#Craziness
#subsets()
#compare_keys()

for key in DATA:
    if DATA[key] == None:
        del(DATA[key])
save([], DATA)