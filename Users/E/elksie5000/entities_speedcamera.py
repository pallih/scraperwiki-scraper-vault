import scraperwiki
import nltk
import json
import lxml.etree
from geopy import geocoders  

def geoCode(address):
    #base_url = http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.placefinder%20where%20text%3D%22sfo%22&diagnostics=true 
    #http://where.yahooapis.com/geocode?q=1600+Pennsylvania+Avenue,+Washington,+DC&appid=LKeT9Q4k
    url_part1 = "http://where.yahooapis.com/geocode?q="
    url_part2 = "&appid=LKeT9Q4k"
    address = address+", Staffordshire, United Kingdom"
    #address = address.replace(" ", "+")
    #address = address.replace (".", "")
    
    combined_url = url_part1+address+url_part2
    print address
    
    
    #print combined_url
    address_xml = lxml.etree.parse(combined_url)
    print +str(address_xml)
    #address_root = lxml.etree.fromstring(address_xml)
    longitude = address_xml.xpath("//longitude")
    latitude = address_xml.xpath("//latitude")
    quality = address_xml.xpath("//quality")
    return longitude[0].text, latitude[0].text, quality[0].text

def process_entities(sentence):  
    words = []
    #print sentence

    #now break sentences into tokens
    tokens = nltk.word_tokenize(sentence)
    #print tokens

    #A bit of POS tagging
    pos_tagged_tokens = [nltk.pos_tag(tokens)]

    #Chunk extraction time
    ne_chunks = nltk.batch_ne_chunk(pos_tagged_tokens)

    # Flatten the list since we're not using sentence structure
    # and sentences are guaranteed to be separated by a special
    # POS tuple such as ('.', '.')
    pos_tagged_tokens = [token for sent in pos_tagged_tokens for token in sent]

    #Entity extraction

    #Code from Mining data from the social web: https://github.com/ptwobrussell/Mining-the-Social-Web/blob/master/python_code/blogs_and_nlp__extract_entities.py
    post = {}
    all_entity_chunks = []
    previous_pos = None
    current_entity_chunk = []
    #print pos_tagged_tokens
    for (token, pos) in pos_tagged_tokens:

        if pos == previous_pos and pos.startswith('NN'):
            current_entity_chunk.append(token)
        elif pos.startswith('NN'):
            if current_entity_chunk != []:

                # Note that current_entity_chunk could be a duplicate when appended,
                # so frequency analysis again becomes a consideration

                all_entity_chunks.append((' '.join(current_entity_chunk), pos))
            current_entity_chunk = [token]

        previous_pos = pos

    # Store the chunks as an index for the document
    # and account for frequency while we're at it...

    post['entities'] = {}
    for c in all_entity_chunks:
        post['entities'][c] = post['entities'].get(c, 0) + 1

    # For example, we could display just the title-cased entities


    proper_nouns = []
    for (entity, pos) in post['entities']:
        if entity.istitle():
            proper_nouns.append(entity)
            #print '\t%s (%s)' % (entity, post['entities'][(entity, pos)])
            #print entity
            #[(entity, pos)]
    return proper_nouns



scraperwiki.sqlite.attach("pdftoxmltest")
data =  scraperwiki.sqlite.select("*  from pdftoxmltest.swdata")




print data
for el in data:
    entities_list =process_entities(el['Camera_Location'])
    print entities_list
    stuff = " ".join(entities_list)
    print stuff
    lat, longitude, quality = geoCode(stuff)
    row ={}
    row['lat'] = lat
    row['lng'] = longitude
    row['qual'] =quality
    row['cam_loc']=el['Camera_Location']
    row['cam_loc']=el['Camera_Location']
    row['date'] = el['Date']
    row['index'] = el['index']
    print lat, longitude, quality
    scraperwiki.sqlite.save(['index'], row)



import scraperwiki
import nltk
import json
import lxml.etree
from geopy import geocoders  

def geoCode(address):
    #base_url = http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20geo.placefinder%20where%20text%3D%22sfo%22&diagnostics=true 
    #http://where.yahooapis.com/geocode?q=1600+Pennsylvania+Avenue,+Washington,+DC&appid=LKeT9Q4k
    url_part1 = "http://where.yahooapis.com/geocode?q="
    url_part2 = "&appid=LKeT9Q4k"
    address = address+", Staffordshire, United Kingdom"
    #address = address.replace(" ", "+")
    #address = address.replace (".", "")
    
    combined_url = url_part1+address+url_part2
    print address
    
    
    #print combined_url
    address_xml = lxml.etree.parse(combined_url)
    print +str(address_xml)
    #address_root = lxml.etree.fromstring(address_xml)
    longitude = address_xml.xpath("//longitude")
    latitude = address_xml.xpath("//latitude")
    quality = address_xml.xpath("//quality")
    return longitude[0].text, latitude[0].text, quality[0].text

def process_entities(sentence):  
    words = []
    #print sentence

    #now break sentences into tokens
    tokens = nltk.word_tokenize(sentence)
    #print tokens

    #A bit of POS tagging
    pos_tagged_tokens = [nltk.pos_tag(tokens)]

    #Chunk extraction time
    ne_chunks = nltk.batch_ne_chunk(pos_tagged_tokens)

    # Flatten the list since we're not using sentence structure
    # and sentences are guaranteed to be separated by a special
    # POS tuple such as ('.', '.')
    pos_tagged_tokens = [token for sent in pos_tagged_tokens for token in sent]

    #Entity extraction

    #Code from Mining data from the social web: https://github.com/ptwobrussell/Mining-the-Social-Web/blob/master/python_code/blogs_and_nlp__extract_entities.py
    post = {}
    all_entity_chunks = []
    previous_pos = None
    current_entity_chunk = []
    #print pos_tagged_tokens
    for (token, pos) in pos_tagged_tokens:

        if pos == previous_pos and pos.startswith('NN'):
            current_entity_chunk.append(token)
        elif pos.startswith('NN'):
            if current_entity_chunk != []:

                # Note that current_entity_chunk could be a duplicate when appended,
                # so frequency analysis again becomes a consideration

                all_entity_chunks.append((' '.join(current_entity_chunk), pos))
            current_entity_chunk = [token]

        previous_pos = pos

    # Store the chunks as an index for the document
    # and account for frequency while we're at it...

    post['entities'] = {}
    for c in all_entity_chunks:
        post['entities'][c] = post['entities'].get(c, 0) + 1

    # For example, we could display just the title-cased entities


    proper_nouns = []
    for (entity, pos) in post['entities']:
        if entity.istitle():
            proper_nouns.append(entity)
            #print '\t%s (%s)' % (entity, post['entities'][(entity, pos)])
            #print entity
            #[(entity, pos)]
    return proper_nouns



scraperwiki.sqlite.attach("pdftoxmltest")
data =  scraperwiki.sqlite.select("*  from pdftoxmltest.swdata")




print data
for el in data:
    entities_list =process_entities(el['Camera_Location'])
    print entities_list
    stuff = " ".join(entities_list)
    print stuff
    lat, longitude, quality = geoCode(stuff)
    row ={}
    row['lat'] = lat
    row['lng'] = longitude
    row['qual'] =quality
    row['cam_loc']=el['Camera_Location']
    row['cam_loc']=el['Camera_Location']
    row['date'] = el['Date']
    row['index'] = el['index']
    print lat, longitude, quality
    scraperwiki.sqlite.save(['index'], row)



