import scraperwiki
import lxml.html

# load company list
scraperwiki.sqlite.attach("ca_corps_scraper")
company_list = scraperwiki.sqlite.select('''* from ca_corps_scraper.swdata order by CompanyNumber limit 10000''')

def normalize_string(string):
    import unicodedata
    return unicodedata.normalize('NFKD', unicode(string)).encode('ascii','ignore')

def normalize_dict(d):
    new_dict = {}

    for key, val in d.iteritems():
        if isinstance(val, dict):
            new_dict[key] = normalize_dict(val)
        elif isinstance(val, basestring):
            new_dict[key] = normalize_string(val).upper()
        elif isinstance(val, list):
            new_dict[key] = map(normalize_string, val)
        else:
            new_dict[key] = val

    return new_dict
    

def parse_registry(html):  
    root = lxml.html.fromstring(html)

    def find_value(attr_name, div_helper, div_root):
        if isinstance(div_helper, int):
            div  = list(div_root.cssselect("div"))[div_helper]
        else:
            div = list(div_root.cssselect(div_helper))[0]

        attr_text = div.text_content()
        if attr_name is not None:
            index = attr_text.find(attr_name)
            return attr_text[index + len(attr_name):].strip()
        else:
            return attr_text
    
    def extract_address(office_div):
        office_address = {}
        office_text = office_div.text_content().strip()
        street_address = office_div.text.strip()
        postal_code = [node for node in office_div][1].text

        office_text = office_text[len(street_address):]
        region, country = office_text.split(postal_code)

        city = region[:-5]
        province = region[-4:].strip()
    
        office_address["street_address"] = street_address
        office_address["postal_code"] = postal_code
        office_address["city"] = city
        office_address["provice"] = province
        office_address["country"] = country

        return office_address

    registry = {}

    for search_div in root.cssselect("div[class='search']"):

        # Corporation Number     
        registry["corporation_number"] = int(find_value("Corporation Number", 
                                                        "div[class='floatLeft width20']",
                                                        search_div))

        # Business Number (BN)
        registry["business_number"] = find_value("Business Number (BN)", 
                                                 "div[class='floatLeft width25']",
                                                 search_div)

        # Governing Legislation
        legislation = find_value("Governing Legislation", 
                                 "div[style='margin-left: 30em;']",
                                 search_div)

        governing_legislation, legislation_date = legislation.split("\n")
        registry["governing_legislation"] = governing_legislation
        registry["governing_legislation_date"] = legislation_date.strip()[2:]

        # Corporate Name
        registry["corporate_name"] = find_value("Corporate Name",
                                                "div[class='clearBoth marginTop12']",
                                                search_div)

        # Status
        registry["status"] = find_value("Status", 8, search_div)


        # Registered Office Address
        office_div = list(search_div.cssselect("div"))[9]
        office_dict = extract_address(office_div)

        for key, val in office_dict.iteritems():
            registry["office_%s" % key] = val 
 
        # Directors
        registry["directors_minimum"] = int(find_value("Minimum", 10, search_div))
        registry["directors_maximum"] = int(find_value("Maximum", 11, search_div))
        count = 1
        for director in list(search_div.cssselect("div"))[13].cssselect("li"):
            registry["directors_%d" % count] = director.text_content().strip().upper()
            count += 1

    return normalize_dict(registry)

for company in company_list:
    try:
        html = scraperwiki.scrape(company["RegistryUrl"])
        registry = parse_registry(html)
        scraperwiki.sqlite.save(unique_keys=['corporation_number'], data=registry)
    except:
        continue