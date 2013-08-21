import scraperwiki
import re
import lxml.html

police_areas = [x.strip() for x in """Avon Somerset
    Bedfordshire
    Cambridgeshire
    Cheshire
    Cleveland
    Cumbria
    Derbyshire
    Devon Cornwall
    Dorset
    Durham
    Dyfed Powys
    Essex
    Gloucestershire
    Greater Manchester
    Gwent
    Hampshire
    Hertfordshire 
    Humberside 
    Kent 
    Lancashire 
    Leicestershire 
    Lincolnshire 
    Merseyside 
    Norfolk 
    Northamptonshire 
    Northumbria 
    North Wales 
    North Yorkshire 
    Nottinghamshire 
    South Wales 
    South Yorkshire 
    Staffordshire 
    Suffolk 
    Surrey 
    Sussex 
    Thames Valley 
    Warwickshire 
    West Mercia 
    West Midlands 
    West Yorkshire
    Wiltshire""".split("\n")]

print len(police_areas)

area_page = "http://www.choosemypcc.org.uk/candidates/area/%s"

candidates = scraperwiki.sqlite.select("* from pcc_candidates")

if False:
  for police_area in police_areas:
    slug = police_area.replace(" ", "-").lower()

    print slug
    area_url = area_page % slug
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

      print "%s (%s)" % (candidate_name, candidate_party)

      data = {'candidate_url': candidate_url,
            'candidate_image_small': candidate_image,
            'candidate_name': candidate_name,
            'candidate_party': candidate_party,
            'police_area': slug}

      candidates.append(data)

  scraperwiki.sqlite.save(["candidate_url"], candidates, "pcc_candidates")

for candidate in candidates:
  print candidate['candidate_name']

  if 'candidate_content' not in candidate:
    try:
      tree = lxml.html.parse(candidate['candidate_url'])
    except:
      continue

    candidate_image_big = tree.xpath('//img[@class="attachment-candidate"]/@src')[0]
    candidate['candidate_image_big'] = candidate_image_big

    content = lxml.html.tostring(tree.xpath("//div[@class='col12']")[0])
    candidate['candidate_content'] = content
 
  if candidate['candidate_content'] is not None:
    candidate['candidate_content_text'] = lxml.html.fromstring(candidate['candidate_content']).text_content()

    facebook = re.findall("www\.facebook\.com/([^ ]+)", candidate['candidate_content_text'])

    if len(facebook) != 0:
      candidate['facebook'] = "https://www.facebook.com/" + facebook[0]

    scraperwiki.sqlite.save(["candidate_url"], candidate, "pcc_candidates")


