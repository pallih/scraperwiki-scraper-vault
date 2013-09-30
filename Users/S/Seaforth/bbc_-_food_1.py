import scraperwiki
import StringIO
import re
import lxml.html

phones_by_manufacturer = "http://www.mazumamobile.com/sell_mobile_phones.php"


scraperwiki.sqlite.execute("DROP TABLE 'MazumaManufacturers'");
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS 'MazumaManufacturers' ('Manufacturer' text, 'Link' text)");
scraperwiki.sqlite.execute("DROP TABLE 'MazumaData'");
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS 'MazumaData' ('Model' text, 'Price' text)");



man_tree = lxml.html.parse(phones_by_manufacturer)
    

data = [ {"Manufacturer":manufacturer.rsplit("/")[-1] , "href":manufacturer}  for manufacturer in man_tree.xpath("//div[@id='tiledManufacturers']/div/a/@href") ]           
print(data)    
scraperwiki.sqlite.save(["Manufacturer"], data, "MazumaManufacturers")

    



#for manufacturer in man_tree.xpath("//div[@id='tiledManufacturers']/div/a"):
#    print(manufacturer.xpath("./@href")[0])

 #   data = [ {"hrefs":manufacturer[0]}  for manufacturer in man_tree.xpath("//div[@id='tiledManufacturers']/div/a/@href") ]           
  #  scraperwiki.sqlite.save(["a"], data)

    #candidate_image = candidate_box.xpath("./a/img/@src")[0]    






if False:
    for police_area in police_areas:
        slug = police_area.replace(" ", "-").lower()
        area_url = area_page % slug
        print(area_url)
        tree = lxml.html.parse(area_url)
        for candidate_box in tree.xpath("//div[@class='related-candidate']"):
            try:
                candidate_image = candidate_box.xpath("./a/img/@src")[0]
            except IndexError:
                candidate_image = None

            candidate_name = candidate_box.xpath("./h4")[0].text_content().strip()
            
            try:
                candidate_url = candidate_box.xpath("./a/@href")[0]
            except:
                candidate_url = "unknown/%s" % candidate_name
    
            candidate_party = candidate_box.xpath("./p")[0].text_content().strip()
            try:
                candidate_url = candidate_box.xpath("./a/@href")[0]
            except:
                candidate_url = "unknown/%s" % candidate_name
    
            print "%s (%s)" % (candidate_name, candidate_party)
    
            data = {'candidate_url': candidate_url,
                'candidate_image_small': candidate_image,
                'candidate_name': candidate_name,
                'candidate_party': candidate_party,
                'police_area': slug}
    
            candidates.append(data)

    print (len(candidates))
    scraperwiki.sqlite.save(["candidate_url"], candidates, "pcc_candidates")

    for candidate in candidates:
        print candidate['candidate_name']
        print "-" + candidate['candidate_url'][0:7] + "-"
        print ('unknown' in candidate['candidate_url'][0:7])
        if  (candidate['candidate_url'][0:7] == 'unknown'):
            continue
    
        if 'candidate_content' not in candidate:
            try:
                tree = lxml.html.parse(candidate['candidate_url'])
                content = lxml.html.tostring(tree.xpath("//div[@class='col12']")[0])
                candidate['candidate_content'] = content
            except:
                continue
        else:
            tree = lxml.html.parse(StringIO.StringIO(candidate['candidate_content']))
    
        if 'candidate_image_big' not in candidate:
            candidate_image_big = tree.xpath('//img[@class="attachment-candidate"]/@src')[0]
            candidate['candidate_image_big'] = candidate_image_big
    
    
        if candidate['candidate_content'] is not None:
            candidate['candidate_content_text'] = lxml.html.fromstring(candidate['candidate_content']).text_content()
        else:
            candidate['candidate_content'] = ""
            candidate['candidate_content_text'] = ""
    
        print(candidate['candidate_content'])
        print(candidate['candidate_content_text'])
        facebook = re.findall("www\.facebook\.com/([^ ]+)", candidate['candidate_content_text'])
    
        if len(facebook) != 0:
            candidate['facebook'] = "https://www.facebook.com/" + facebook[0]
    
        website = url_re.findall(candidate['candidate_content_text'])
        if len(website) != 0:
            websites = ""
            for wbs in website:
                websites = websites.join(wbs.join("\n"))
            candidate['website'] = websites
        
        try:
            candidate_en_email = tree.xpath("//a[@id='__cf_email__']/@class")[0]
        except:
            candidate_en_email = ""
    
        if candidate_en_email != "":
            a = candidate_en_email 
            s=''
            r = int(a[0:2],16)
            for j in xrange(2, len(a), 2):
                c = a[j:j+2]
                cstr = str(unichr(int(c,16)^r))
                s = s + cstr    
            candidate_email = s
        else:
            candidate_email = "" 
    
    
        candidate['email'] = candidate_email
    
    
        scraperwiki.sqlite.save(["candidate_url"], candidate, "pcc_candidates")
    
