import requests
import csv  
import scraperwiki

def latcon(deg):
    split = deg.split('\xb0')
    sec = float(split[1].replace(',','.'))
    dsec = sec/60
    dd = int(split[0]) + dsec
    return dd

def lngcon(deg):
    split = deg.split('\xb0')
    sec = float(split[1].replace(',','.'))
    dsec = sec/60
    dd = int(split[0]) + dsec
    return -dd

url = 'https://dl.dropbox.com/u/2192482/sofn.csv'
url2='https://dl.dropbox.com/u/2192482/sofn2.csv'

data = requests.get(url2,verify=False).text
data = data.encode('iso-8859-1')

print data
         
reader = csv.reader(data.splitlines())
headerline = reader.next()

#reader = csv.DictReader(data.splitlines(),delimiter=',')


batch = []
for row in reader:
    record = {}   
    record['safn'] =  row[0].decode('iso-8859-1')
    record['Heimilisfang'] =  row[1].decode('iso-8859-1')
    record['Postnumer'] =  row[2].decode('iso-8859-1')
    record['Simi 1'] =  row[3].decode('iso-8859-1')
    record['Simi 2'] =  row[4].decode('iso-8859-1')
    record['Netfang'] =  row[5].decode('iso-8859-1')
    record['Heimasida'] =  row[6].decode('iso-8859-1')
    record['Landshluti'] =  row[7].decode('iso-8859-1')
    record['GPS Hnit N'] =  row[8].decode('iso-8859-1')
    record['GPS hnit W'] =  row[9].decode('iso-8859-1')
    record['Texti'] =  row[10].decode('iso-8859-1')
    record['Myndaheiti 1'] =  row[11].decode('iso-8859-1')
    record['Myndaheiti 2'] =  row[12].decode('iso-8859-1')
    record['myndaheiti 3'] =  row[13].decode('iso-8859-1')
    record['myndaheiti 4'] =  row[14].decode('iso-8859-1')
    record['myndaheiti 5'] =  row[15].decode('iso-8859-1')
    record['myndaheiti 6'] =  row[16].decode('iso-8859-1')
    record['annar texti'] =  row[17].decode('iso-8859-1')
    try:
        record['lat'] = latcon(record['GPS Hnit N'].encode('iso-8859-1'))
        record['lng'] = lngcon(record['GPS hnit W'].encode('iso-8859-1'))
    except:
        pass
    batch.append(record)
    #row['id'] = counter
    #print repr(row['GPS Hnit N'])
    #try:
    #    row['lat'] = latcon(row['GPS Hnit N'])
    #    row['lng'] = lngcon(row['GPS hnit W'])
    #except:
    #    pass
scraperwiki.sqlite.save(unique_keys=['safn'], data=batch)
    #counter = counter +1



import requests
import csv  
import scraperwiki

def latcon(deg):
    split = deg.split('\xb0')
    sec = float(split[1].replace(',','.'))
    dsec = sec/60
    dd = int(split[0]) + dsec
    return dd

def lngcon(deg):
    split = deg.split('\xb0')
    sec = float(split[1].replace(',','.'))
    dsec = sec/60
    dd = int(split[0]) + dsec
    return -dd

url = 'https://dl.dropbox.com/u/2192482/sofn.csv'
url2='https://dl.dropbox.com/u/2192482/sofn2.csv'

data = requests.get(url2,verify=False).text
data = data.encode('iso-8859-1')

print data
         
reader = csv.reader(data.splitlines())
headerline = reader.next()

#reader = csv.DictReader(data.splitlines(),delimiter=',')


batch = []
for row in reader:
    record = {}   
    record['safn'] =  row[0].decode('iso-8859-1')
    record['Heimilisfang'] =  row[1].decode('iso-8859-1')
    record['Postnumer'] =  row[2].decode('iso-8859-1')
    record['Simi 1'] =  row[3].decode('iso-8859-1')
    record['Simi 2'] =  row[4].decode('iso-8859-1')
    record['Netfang'] =  row[5].decode('iso-8859-1')
    record['Heimasida'] =  row[6].decode('iso-8859-1')
    record['Landshluti'] =  row[7].decode('iso-8859-1')
    record['GPS Hnit N'] =  row[8].decode('iso-8859-1')
    record['GPS hnit W'] =  row[9].decode('iso-8859-1')
    record['Texti'] =  row[10].decode('iso-8859-1')
    record['Myndaheiti 1'] =  row[11].decode('iso-8859-1')
    record['Myndaheiti 2'] =  row[12].decode('iso-8859-1')
    record['myndaheiti 3'] =  row[13].decode('iso-8859-1')
    record['myndaheiti 4'] =  row[14].decode('iso-8859-1')
    record['myndaheiti 5'] =  row[15].decode('iso-8859-1')
    record['myndaheiti 6'] =  row[16].decode('iso-8859-1')
    record['annar texti'] =  row[17].decode('iso-8859-1')
    try:
        record['lat'] = latcon(record['GPS Hnit N'].encode('iso-8859-1'))
        record['lng'] = lngcon(record['GPS hnit W'].encode('iso-8859-1'))
    except:
        pass
    batch.append(record)
    #row['id'] = counter
    #print repr(row['GPS Hnit N'])
    #try:
    #    row['lat'] = latcon(row['GPS Hnit N'])
    #    row['lng'] = lngcon(row['GPS hnit W'])
    #except:
    #    pass
scraperwiki.sqlite.save(unique_keys=['safn'], data=batch)
    #counter = counter +1



