from scraperwiki.sqlite import save,select
from copy import copy

DATA={u'City': None, u'Latitude': u'-32.476662', u'id': u'1', u'Longitute': u'24.062041', u'Status': u'A', u'SuburdId': 1, u'TownName': u'ABERDEEN', u'Address1': u'', u'Address2': u'', u'EntityType': None, 'provinceId': '1', u'EntityCentreNumber': u'5541', u'ProvinceId': 1, u'RegionName': u'', u'Province': None, u'EntityTypeOptionId': 11, u'OperatingHoursWeekend': u'8:30 AM \u2013 11AM', u'EntityName': u'ABERDEEN', u'EntitySwiftCode': u'SBZAZAJJ', 'cityId': '1', u'IBTNumber': u'16', u'EntityTypeId': 2, u'OperatingHoursWeekDay': u'9 AM \u2013 3:30PM', 'provinceName': 'Eastern Cape', 'date_scraped': 1328932864.404724, u'DateAdded': u'/Date(1298325600000+0200)/', u'EntityTypeOption': None, 'cityName': 'ABERDEEN', u'AddedBy': 1, u'CityId': 1, u'SuburdSuburb': None, u'EntityDescription': u'', u'Guid': u'370a8d57-399e-4df3-a9f3-2cb550467924', u'Id': 6679, u'StreetName': u'6 PORTER STREET'}

del(DATA['id'])
save([], DATA)

for key in DATA.keys():
    if DATA[key] == None:
        del(DATA[key])
save([], DATA)from scraperwiki.sqlite import save,select
from copy import copy

DATA={u'City': None, u'Latitude': u'-32.476662', u'id': u'1', u'Longitute': u'24.062041', u'Status': u'A', u'SuburdId': 1, u'TownName': u'ABERDEEN', u'Address1': u'', u'Address2': u'', u'EntityType': None, 'provinceId': '1', u'EntityCentreNumber': u'5541', u'ProvinceId': 1, u'RegionName': u'', u'Province': None, u'EntityTypeOptionId': 11, u'OperatingHoursWeekend': u'8:30 AM \u2013 11AM', u'EntityName': u'ABERDEEN', u'EntitySwiftCode': u'SBZAZAJJ', 'cityId': '1', u'IBTNumber': u'16', u'EntityTypeId': 2, u'OperatingHoursWeekDay': u'9 AM \u2013 3:30PM', 'provinceName': 'Eastern Cape', 'date_scraped': 1328932864.404724, u'DateAdded': u'/Date(1298325600000+0200)/', u'EntityTypeOption': None, 'cityName': 'ABERDEEN', u'AddedBy': 1, u'CityId': 1, u'SuburdSuburb': None, u'EntityDescription': u'', u'Guid': u'370a8d57-399e-4df3-a9f3-2cb550467924', u'Id': 6679, u'StreetName': u'6 PORTER STREET'}

del(DATA['id'])
save([], DATA)

for key in DATA.keys():
    if DATA[key] == None:
        del(DATA[key])
save([], DATA)