import scraperwiki
import re
import mechanize
import urllib
import time
from lxml.cssselect import CSSSelector
from lxml import etree
import lxml.html as lh

# Nested Posts
uid = 0
last_level = 0

def refresh_loop():
    print "Starting Run"
    global last_level
    global uid
    kind = 'P'
    arch = '0'
    post_url = "http://www.realoem.com/bmw/select.do"
    br = mechanize.Browser()
    #parameters = {'kind' : 'P',
    #              'arch' : 'C',
    #              'series' : 'E88',
    #              'body' : 'Cab',
    #              'model' : '118d',
    #              'zone'  : 'ECE',
    #              'prod' : '20101200',
    #              'motor' : 'N47',
    #              'steering' : 'R'}
    #parameters = {'kind' : 'P',
    #    'arch' : 'C',
    #    'series' : series.name,
    #    'body' : '',
    #    'model' : '116d',
    #    'zone' : 'ECE',
    #    'prod' : '20081100',
    #    'motor' : 'N47',
    #    'steering' : 'L'
    #}    
    br.open(post_url)
    #br.open(post_url,urllib.urlencode(parameters))
    print "last level is %d" % last_level
    #time.sleep(0.1)
    br.select_form(name="form1")

    series_list = br.find_control(name='series')
    for series in series_list.items:
        print "series:%s" % series.name
        # build post string for this one to get its BODY
        #POST
        parameters = {'kind' : 'P',
                      'arch' : 'C',
                      'series' : series.name,
                      'body' : ''
                     }
        br.open(post_url,urllib.urlencode(parameters))
        br.select_form(name="form1")
        body_list = br.find_control(name='body')
        for body in body_list.items:
            print body
            # build post string for this one to get its MODEL
            #POST
            parameters = {'kind' : 'P',
                          'arch' : 'C',
                          'series' : series.name,
                          'body' : body.name,
                          'model' : ''
                         }
            br.open(post_url,urllib.urlencode(parameters))
            br.select_form(name="form1")
            model_list = br.find_control(name='model')
            for model in model_list.items:
                print model.name
                # build post string for this one to get its ZONE
                #POST
                parameters = {'kind' : 'P',
                          'arch' : 'C',
                          'series' : series.name,
                          'body' : body.name,
                          'model' : model.name,
                          'zone'  : ''
                         }
                print parameters
                response = br.open(post_url,urllib.urlencode(parameters))
                doc=lh.parse(response)
                for elt in doc.iter('select'):
                    if elt.name == 'zone':
                        zone_list = elt.value_options
                        for zone in zone_list:
                            print zone
                            # build post string for this one to get its PROD
                            #POST
                            parameters = {'kind' : 'P',
                                          'arch' : 'C',
                                          'series' : series.name,
                                          'body' : body.name,
                                          'model' : model.name,
                                          'zone'  : zone,
                                          'prod' : ''
                                         }
                            br.open(post_url,urllib.urlencode(parameters))
                            response = br.open(post_url,urllib.urlencode(parameters))
                            doc=lh.parse(response)
                            for elt in doc.iter('select'):
                                if elt.name == 'prod':
                                    prod_list = elt.value_options
                                    for prod in prod_list:
                                        print prod
                                        # build post string for this one to get its MOTOR
                                        #POST
                                        parameters = {'kind' : 'P',
                                                      'arch' : 'C',
                                                      'series' : series.name,
                                                      'body' : body.name,
                                                      'model' : model.name,
                                                      'zone'  : zone,
                                                      'prod' : prod,
                                                      'motor' : ''
                                                     }
                                        br.open(post_url,urllib.urlencode(parameters))
                                        response = br.open(post_url,urllib.urlencode(parameters))
                                        doc=lh.parse(response)
                                        print 'fetching motor'
                                        for elt in doc.iter('select'):
                                            if elt.name == 'motor':
                                                motor_list = elt.value_options
                                                for motor in motor_list:
                                                    print motor
                                                    # build post string for this one to get its STEERING
                                                    #POST
                                                    parameters = {'kind' : 'P',
                                                                  'arch' : 'C',
                                                                  'series' : series.name,
                                                                  'body' : body.name,
                                                                  'model' : model.name,
                                                                  'zone'  : zone,
                                                                  'prod' : prod,
                                                                  'motor' : motor,
                                                                  'steering' : ''
                                                                 }
                                                    br.open(post_url,urllib.urlencode(parameters))
                                                    response = br.open(post_url,urllib.urlencode(parameters))
                                                    doc=lh.parse(response)
                                                    print 'fetching steering'
                                                    for elt in doc.iter('input'):
                                                        #if elt.attrib['disabled']:
                                                        #elt.disabled
                                                        if elt.name == "steering":
    
                                                            steering = elt.attrib['value']
                                                            print steering
                                                            #scraperwiki.sqlite.save(unique_keys=["id"], 
                                                            #    data={"id":uid, 
                                                            #          'kind' : 'P',
                                                            #          'arch' : 'C',
                                                            #          'series' : series.name,
                                                            #          'body' : body.name,
                                                            #          'model' : model.name,
                                                            #          'zone'  : zone,
                                                            #          'prod' : prod,
                                                            #          'motor' : motor,
                                                            #          'steering' : steering})
                                                            uid += 1
                                                                
    

refresh_loop()

import scraperwiki
import re
import mechanize
import urllib
import time
from lxml.cssselect import CSSSelector
from lxml import etree
import lxml.html as lh

# Nested Posts
uid = 0
last_level = 0

def refresh_loop():
    print "Starting Run"
    global last_level
    global uid
    kind = 'P'
    arch = '0'
    post_url = "http://www.realoem.com/bmw/select.do"
    br = mechanize.Browser()
    #parameters = {'kind' : 'P',
    #              'arch' : 'C',
    #              'series' : 'E88',
    #              'body' : 'Cab',
    #              'model' : '118d',
    #              'zone'  : 'ECE',
    #              'prod' : '20101200',
    #              'motor' : 'N47',
    #              'steering' : 'R'}
    #parameters = {'kind' : 'P',
    #    'arch' : 'C',
    #    'series' : series.name,
    #    'body' : '',
    #    'model' : '116d',
    #    'zone' : 'ECE',
    #    'prod' : '20081100',
    #    'motor' : 'N47',
    #    'steering' : 'L'
    #}    
    br.open(post_url)
    #br.open(post_url,urllib.urlencode(parameters))
    print "last level is %d" % last_level
    #time.sleep(0.1)
    br.select_form(name="form1")

    series_list = br.find_control(name='series')
    for series in series_list.items:
        print "series:%s" % series.name
        # build post string for this one to get its BODY
        #POST
        parameters = {'kind' : 'P',
                      'arch' : 'C',
                      'series' : series.name,
                      'body' : ''
                     }
        br.open(post_url,urllib.urlencode(parameters))
        br.select_form(name="form1")
        body_list = br.find_control(name='body')
        for body in body_list.items:
            print body
            # build post string for this one to get its MODEL
            #POST
            parameters = {'kind' : 'P',
                          'arch' : 'C',
                          'series' : series.name,
                          'body' : body.name,
                          'model' : ''
                         }
            br.open(post_url,urllib.urlencode(parameters))
            br.select_form(name="form1")
            model_list = br.find_control(name='model')
            for model in model_list.items:
                print model.name
                # build post string for this one to get its ZONE
                #POST
                parameters = {'kind' : 'P',
                          'arch' : 'C',
                          'series' : series.name,
                          'body' : body.name,
                          'model' : model.name,
                          'zone'  : ''
                         }
                print parameters
                response = br.open(post_url,urllib.urlencode(parameters))
                doc=lh.parse(response)
                for elt in doc.iter('select'):
                    if elt.name == 'zone':
                        zone_list = elt.value_options
                        for zone in zone_list:
                            print zone
                            # build post string for this one to get its PROD
                            #POST
                            parameters = {'kind' : 'P',
                                          'arch' : 'C',
                                          'series' : series.name,
                                          'body' : body.name,
                                          'model' : model.name,
                                          'zone'  : zone,
                                          'prod' : ''
                                         }
                            br.open(post_url,urllib.urlencode(parameters))
                            response = br.open(post_url,urllib.urlencode(parameters))
                            doc=lh.parse(response)
                            for elt in doc.iter('select'):
                                if elt.name == 'prod':
                                    prod_list = elt.value_options
                                    for prod in prod_list:
                                        print prod
                                        # build post string for this one to get its MOTOR
                                        #POST
                                        parameters = {'kind' : 'P',
                                                      'arch' : 'C',
                                                      'series' : series.name,
                                                      'body' : body.name,
                                                      'model' : model.name,
                                                      'zone'  : zone,
                                                      'prod' : prod,
                                                      'motor' : ''
                                                     }
                                        br.open(post_url,urllib.urlencode(parameters))
                                        response = br.open(post_url,urllib.urlencode(parameters))
                                        doc=lh.parse(response)
                                        print 'fetching motor'
                                        for elt in doc.iter('select'):
                                            if elt.name == 'motor':
                                                motor_list = elt.value_options
                                                for motor in motor_list:
                                                    print motor
                                                    # build post string for this one to get its STEERING
                                                    #POST
                                                    parameters = {'kind' : 'P',
                                                                  'arch' : 'C',
                                                                  'series' : series.name,
                                                                  'body' : body.name,
                                                                  'model' : model.name,
                                                                  'zone'  : zone,
                                                                  'prod' : prod,
                                                                  'motor' : motor,
                                                                  'steering' : ''
                                                                 }
                                                    br.open(post_url,urllib.urlencode(parameters))
                                                    response = br.open(post_url,urllib.urlencode(parameters))
                                                    doc=lh.parse(response)
                                                    print 'fetching steering'
                                                    for elt in doc.iter('input'):
                                                        #if elt.attrib['disabled']:
                                                        #elt.disabled
                                                        if elt.name == "steering":
    
                                                            steering = elt.attrib['value']
                                                            print steering
                                                            #scraperwiki.sqlite.save(unique_keys=["id"], 
                                                            #    data={"id":uid, 
                                                            #          'kind' : 'P',
                                                            #          'arch' : 'C',
                                                            #          'series' : series.name,
                                                            #          'body' : body.name,
                                                            #          'model' : model.name,
                                                            #          'zone'  : zone,
                                                            #          'prod' : prod,
                                                            #          'motor' : motor,
                                                            #          'steering' : steering})
                                                            uid += 1
                                                                
    

refresh_loop()

