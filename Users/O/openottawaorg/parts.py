import scraperwiki
import re
import mechanize
import urllib
import time

# Nested Posts

last_level = 0

post_url = "http://www.realoem.com/bmw/select.do"
browser = mechanize.Browser()
parameters = {'kind' : 'P',
              'arch' : 'C',
              'series' : 'E81',
              'body' : 'HC',
              'model' : '116d',
              'zone' : 'ECE',
              'prod' : '20081100',
              'motor' : 'N47',
              'steering' : 'L',
             }
print "posting for zone:"
browser.open(post_url)


def refresh_loop(br):
    global last_level
    kind = 'P'
    arch = '0'
    print "Starting Run"
    print "last level is %d" % last_level
    time.sleep(0.1)
    for form in br.forms():
        print form
    br.select_form(name="form1")

    series_list = br.find_control(name='series')
    for series in series_list.items:
        print "series:%s" % series.name
        # build post string for this one to get it's body's
        try:
            body_list = br.find_control(name='body')
            for body in body_list.items:
                print "body: %s" % body.name
                # build post string for this one to get it's model
                try:
                    model_list = br.find_control(name='model')
                    for model in model_list.items:
                        print "model: %s" % model.name
                        ################ ZONES ##########################
                        # @TODO - for some reason, its never finding the zones control, even when it should.
                        # build post string for this one to get it's zone
                        try:
                            zone_list = br.find_control(name='zone')
                            for zone in zone_list.items:
                                print "zone: %s" % zone.name
                        except:
                            # didn't find a zone for this series. repost.
                            print "couldn't find a zone"
                            print "last level was %d" % last_level
                            # check if last level was this level
                            if last_level != 3:
                                #repost
                                browser = mechanize.Browser()
                                parameters = {'kind': kind,
                                              'arch' : arch,
                                              'series' : series.name,
                                              'body' : body.name,
                                              'model' : model.name
                                             }
                                print "posting to get a ZONE"
                                print parameters
                                data = urllib.urlencode(parameters)
                                browser.open(post_url,data)
                                last_level = 3                # note the last level we were at
                                refresh_loop(browser)
                        ################
                except:
                    # didn't find a body for this series. repost.
                    # check if last level was this level
                    print "last level was %d" % last_level
                    if last_level != 2:
                        #repost
                        browser = mechanize.Browser()
                        parameters = {'kind': kind,
                                      'arch' : arch,
                                      'series' : series.name,
                                      'body' : body.name
                                     }
                        print "posting to get a MODEL"
                        print parameters
                        data = urllib.urlencode(parameters)
                        browser.open(post_url,data)
                        last_level = 2                # note the last level we were at
                        refresh_loop(browser)
        except:
            # didn't find a body for this series. repost.
            # check if last level was this level
            print "last level was %d" % last_level
            if last_level != 1:
                #repost
                browser = mechanize.Browser()
                parameters = {'kind': kind,
                              'arch' : arch,
                              'series' : series.name
                             }
                print "posting to get a BODY"
                print parameters
                data = urllib.urlencode(parameters)
                browser.open(post_url,data)
                last_level = 1                # note the last level we were at
                refresh_loop(browser)
                

        
    

refresh_loop(browser)

