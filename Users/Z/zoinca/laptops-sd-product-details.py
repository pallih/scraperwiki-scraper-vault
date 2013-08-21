import scraperwiki

# Blank Python

import re
import urllib2

#url = "http://www.flipkart.com/samsung-np300e5z-s08in-laptop-2-gen-ci5-4gb-750gb-1gb/p/itmd8dhnybfbngtu?pid=COMD8DHN7KUCHY33&ref=75e3ea45-0bfa-417d-a7b3-a4e7ad95924d"
#url="http://www.flipkart.com/dell-inspiron-5050-laptop-2nd-gen-ci3-4gb-500gb-win7-hb/p/itmd9pf6f7rhvjhe?pid=COMD9PEWRZA4H2VZ&ref=12dde97b-50e4-4e90-8065-a9fd1e819bc2"
#url = "http://www.flipkart.com/sony-vaio-sve15113en-laptop-2nd-gen-ci3-2gb-320gb-win7-hb/p/itmdatb5fzya689a?pid=COMDATB57ER5ZRBH&ref=12dde97b-50e4-4e90-8065-a9fd1e819bc2"

scraperwiki.sqlite.attach('laptops-sd-products-urls',"urls")
urls = scraperwiki.sqlite.select('* from urls.swdata')
count = 1
for url in urls:
 graphics = "0"
 battery = '4'
 hd=""
 listurl = url.values()
 pagelink = listurl[0]
 print pagelink
 open = urllib2.urlopen(pagelink)
 lines = str(open.read())
 open4image = urllib2.urlopen(pagelink)
 lines4image = open4image.readlines()

 match_title = re.search(r'(<h1>)(\w+)([+.,\\\'\(\)\"\w\d\s&-/]+)(</h1>)',lines)
 if match_title:
  brand = match_title.group(2)
  title = match_title.group(2)+match_title.group(3)
  print count
  count = count + 1
 
 match_price = re.search(r'(selling-price-id">)(\d+)(</span>)',lines)
 if match_price:
  print match_price.group(2)
  price = match_price.group(2)

 match_offer = re.search(r'(prodbuy-discount"><span>)(\d+%)(</span>)',lines)
 if match_offer:
  print match_offer.group(2)
  offer = match_offer.group(2)

 match_shipping = re.search(r'(<span>)(Free)(</span>)',lines)
 if match_shipping:
  print match_shipping.group(2)
  shipping = match_shipping.group(2)

 match_delivery = re.search(r'(shippingSpace.{5,100}<strong>)([\d]+)',lines)
 if match_delivery:
  print 'delivery : '+match_delivery.group(2)
  delivery = match_delivery.group(2)

 match_processor = re.search(r'(>Processor.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_processor: 
  print match_processor.group(2)
  processor = match_processor.group(2)
 
 match_variant = re.search(r'(>Variant.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_variant:
  print 'variant : '+match_variant.group(2)
  variant = match_variant.group(2)

 match_specs_procbrand = re.search(r'(>Brand.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_specs_procbrand:
  print 'proc brand : '+match_specs_procbrand.group(2)
  procbrand = match_specs_procbrand.group(2)

 match_specs_clockspeed = re.search(r'(>Clock Speed.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_specs_clockspeed:
  print 'proc clockspeed : '+match_specs_clockspeed.group(2)
  clockspeed = match_specs_clockspeed.group(2)
  match_clockspeed = re.findall('[.\d]+',clockspeed)
  for match in match_clockspeed:
   clockspeed = match

 match_expmemory = re.search(r'(>Expandable Memory.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_expmemory:
  print 'Expandable Memory : '+match_expmemory.group(2)
  expmem = match_expmemory.group(2)

 match_ram = re.search(r'(>System Memory.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_ram:
  print 'ram : '+match_ram.group(2)
  ram = match_ram.group(2)
  match_ram = re.search(r'\d+',ram)
  if match_ram:
   ram = match_ram.group()
 
 match_hd = re.search(r'(>HDD Capacity.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_hd:
  print 'hd : '+match_hd.group(2)
  hd = match_hd.group(2)
  match_hd = re.search(r'\d+',hd)
  if match_hd:
   hd = match_hd.group()

 match_hd = re.search(r'(>Hard Disk Capacity.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_hd:
  print 'hd : '+match_hd.group(2)
  hd = match_hd.group(2)
  match_hd = re.search(r'\d+',hd)
  if match_hd:
   hd = match_hd.group()
 

 match_os = re.search(r'(>Operating System.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_os:
  print 'os : '+match_os.group(2)
  os = match_os.group(2)

 match_screensize = re.search(r'(>Screen Size.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_screensize:
  print 'screensize : '+match_screensize.group(2)
  screensize = match_screensize.group(2)
  match_display = re.findall('[.\d]+',screensize)
  for match in match_display:
   screensize = match
   print 'screen size '+screensize

 match_graphics = re.search(r'(>Dedicated Graphics Memory Capacity.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_graphics:
  print 'graphics : '+match_graphics.group(2)
  graphics = match_graphics.group(2)
  match_gb_graphics = re.search(r'\d.\d+',graphics)
  if match_gb_graphics:
   graphics = match_gb_graphics.group()
   print "gb graphics : "+graphics
 
 match_battery = re.search(r'(>Batter Backup.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_battery:
  print 'battery : '+match_battery.group(2)
  battery = match_battery.group(2)
 
 clockspeed = ""
 match_clockspeed = re.search(r'(>Clock Speed.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_clockspeed:
  print 'clockspeed : '+match_clockspeed.group(2)
  clockspeed = match_clockspeed.group(2)
 
 match_clockspeed = re.search(r'(>Speed.{5,50}\W+<td>)(.{5,100})(</td>)',lines)
 if match_clockspeed:
  print 'clockspeed : '+match_clockspeed.group(2)
  clockspeed = match_clockspeed.group(2)

 match_clockspeed = re.findall('[.\d]+',clockspeed)
 for match in match_clockspeed:
  clockspeed = match

 match_clockspeed = re.search(r'(>Processor.{5,50}\W+<td>)(.{5,150})(GHz)(.{0,50}</td>)',lines)
 if match_clockspeed:
  print 'clockspeed : '+match_clockspeed.group(2)
  clockspeed = match_clockspeed.group(2)

 match_clockspeed = re.search(r'(>Bus Speed.{5,50}\W+<td>)(.{5,100})(GHz)(</td>)',lines)
 if match_clockspeed:
  print 'clockspeed : '+match_clockspeed.group(2)
  clockspeed = match_clockspeed.group(2)

 match_clockspeed = re.search(r'(>Microprocessor.{5,50}\W+<td>)(.{5,150})(GHz)(.{0,50}</td>)',lines)
 if match_clockspeed:
  print 'clockspeed : '+match_clockspeed.group(2)
  clockspeed = match_clockspeed.group(2)

 match_clockspeed = re.search(r'(>CPU.{5,50}\W+<td>)(.{5,150})(\d+.\d+)(G)(.{0,50}</td>)',lines)
 if match_clockspeed:
  print 'clockspeed : '+match_clockspeed.group(3)
  clockspeed = match_clockspeed.group(3)

 match_image = re.search(r'(http://i1.sdlcdn.com/)(img[-/\w\d]+..{3,4})',lines)
 if match_image:
  image_url = match_image.group()
  image_url = image_url.replace('"',"")
  image_url = image_url.replace("'","")
  image_path = match_image.group(2)
  image_path = image_path.replace("'","")
  image_path = image_path.replace('"',"")
  image_path = "images/sd/"+image_path
 

 scraperwiki.sqlite.save(['url'],data = { 'url':pagelink,'brand':brand,'title':title,'price':price,'stock':'In','delivery':delivery,'shipping':shipping,'offer':offer,'processor':processor,'variant':variant,'procband':procbrand,'clockspeed':clockspeed,'ram':ram,'expram':expmem,'graphics':graphics,'hd':hd,'os':os,'screensize':screensize,'battery':battery,'image_url':image_url,'image_path':image_path})

print 'total count :'+str(count)
