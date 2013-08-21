import scraperwiki
import os
import socket
import sys
import csv
import json
import oauth2
import optparse
import urllib
import urllib2
import time
import Queue
import threading
queue = Queue.Queue()
options_key = '6bcea566db4bdb3b84e5b704c085a2eb'
options_host = 'api2.yp.com'
options_format = 'json'
options_startid = 470035148
options_endid = 471000000

# Setup URL params from options
url_params = {}
url_params['format'] = options_format
url_params['key'] = options_key

def request(host, path, url_params, consumer_key):
    encoded_params = ''
    if url_params:
        encoded_params = urllib.urlencode(url_params)
        url = 'http://%s%s?%s' % (host, path, encoded_params)
    print url
    response = ''
    attempts = 0
    while attempts < 10:
        try:
            response = json.loads(urllib2.urlopen(url, timeout=10).read())
            attempts += 1
            break
        except urllib2.HTTPError, e:
            print 'The server didn\'t do the request'
            print 'Error code: ', str(e.code) + "  address: " + url
            time.sleep(4)
            attempts += 1
        except urllib2.URLError, e:
            print 'Failed to reach the server' 
            print 'Reason: ', str(e.reason) + "  address: " + url
            break
        except Exception, e:
            print 'Something bad happened in get PAGE.'
            print 'Address: ' + url
            time.sleep(4)
            attempts += 1
    return response


def fWriteToCSV(response):
    try:
        for businesses in response['listingsDetailsResult']['listingsDetails']['listingDetail']:
            
            row = []

            if 'adImage' in businesses:
                row.append(('adImage',str(businesses['adImage'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'adImageClick' in businesses:
                row.append(('adImageClick',str(businesses['adImageClick'].encode('utf-8'))))
            #else:
            #    row.append('')

            if 'additionalText' in businesses:
                #try:
                    row.append(('additionalText',str(businesses['additionalText']).encode('utf-8')))
                #except:
                #    row.append(str(businesses['additionalText'].encode('utf-8')))
            #else:
            #    row.append('')

            
            if 'audioURL' in businesses:
                row.append(('audioURL',str(businesses['audioURL'].encode('utf-8'))))
            #else:
            #    row.append('')
            
            if 'averageRating' in businesses:
                row.append(('averageRating',str(businesses['averageRating'])))
            #else:
            #    row.append('')
            
            if 'baseClickURL' in businesses:
                row.append(('baseClickURL',str(businesses['baseClickURL'].encode('utf-8'))))
            #else:
            #    row.append('')
            
            if 'businessName' in businesses:
                #try:
                    row.append(('businessName',str(businesses['businessName']).encode('utf-8')))
                #except:
                #    row.append(str(businesses['businessName'].encode('utf-8')))
            #else:
            #    row.append('')

            temp = []
            if 'categories' in businesses:
                if len(businesses['categories'])>0:
                    for category in businesses['categories']['category']:
                        temp.append(category.encode('utf-8'))
                    row.append(('categories','|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')

            if 'city' in businesses:
                #try:
                    row.append(('city',str(businesses['city']).encode('utf-8')))
                #except:
                #    row.append(str(businesses['city'].encode('utf-8')))
            #else:
            #    row.append('')

            if 'couponFlag' in businesses:
                row.append(('couponFlag',str(businesses['couponFlag'])))
            #else:
            #    row.append('')
                
            if 'couponURL' in businesses:
                row.append(('couponURL',str(businesses['couponURL'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'description1' in businesses:
                #try:
                    row.append(('description1',str(businesses['description1']).encode('utf-8')))
                #except:
                #    row.append(str(businesses['description1'].encode('utf-8')))
            #else:
            #    row.append('')
                
            if 'description2' in businesses:
                #try:
                    row.append(('description2',str(businesses['description2']).encode('utf-8')))
                #except:
                #    row.append(str(businesses['description2'].encode('utf-8')))
            #else:
            #    row.append('')

            if 'distance' in businesses:
                row.append(('distance',str(businesses['distance'])))
            #else:
            #    row.append('')
                
            if 'distribAdImage' in businesses:
                row.append(('distribAdImage',str(businesses['distribAdImage'].encode('utf-8'))))
            #else:
            #    row.append('')

            if 'distribAdImageClick' in businesses:
                row.append(('distribAdImageClick',str(businesses['distribAdImageClick'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'email' in businesses:
                row.append(('email', "'" + str(businesses['email'].encode('utf-8')) + "'"))
            #else:
            #    row.append('')

            if 'hasDisplayAddress' in businesses:
                row.append(('hasDisplayAddress',str(businesses['hasDisplayAddress'])))
            #else:
            #    row.append('')
                
            if 'hasPriorityShading' in businesses:
                row.append(('hasPriorityShading',str(businesses['hasPriorityShading'])))
            #else:
            #    row.append('')
                
            if 'isRedListing' in businesses:
                row.append(('isRedListing',str(businesses['isRedListing'])))
            #else:
            #    row.append('')

            if 'latitude' in businesses:
                row.append(('latitude',str(businesses['latitude'])))
            #else:
            #    row.append('')
                
            if 'listingId' in businesses:
                try:
                    row.append(('listingId',str(businesses['listingId']).encode('utf-8')))
                except:
                    row.append(('listingId', str(businesses['listingId'].encode('utf-8'))))
            #else:
            #    row.append('')
                            
            if 'longitude' in businesses:
                row.append(('longitude',str(businesses['longitude'])))
            #else:
            #    row.append('')
                
            if 'moreInfoURL' in businesses:
                row.append(('moreInfoURL',str(businesses['moreInfoURL'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'noAddressMessage' in businesses:
                try:
                    row.append(('noAddressMessage',str(businesses['noAddressMessage']).encode('utf-8')))
                except:
                    row.append(('noAddressMessage', str(businesses['noAddressMessage'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'omitAddress' in businesses:
                row.append(('omitAddress',str(businesses['omitAddress'])))
            #else:
            #    row.append('')
                
            if 'omitPhone' in businesses:
                row.append(('omitPhone',str(businesses['omitPhone'])))
            #else:
            #    row.append('')

            if 'openHours' in businesses:
                try:
                    row.append(('openHours',str(businesses['openHours']).encode('utf-8')))
                except:
                    row.append(('openHours', str(businesses['openHours'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'paymentMethods' in businesses:
                try:
                    row.append(('paymentMethods', str(businesses['paymentMethods']).encode('utf-8')))
                except:
                    row.append(('paymentMethods', str(businesses['paymentMethods'].encode('utf-8'))))
            #else:
            #    row.append('')

            if 'phone' in businesses:
                try:
                    row.append(('phone',"'" + str(businesses['phone'].encode('utf-8'))))
                except:
                    row.append(('phone', "'" + str(businesses['phone']).encode('utf-8')))
            #else:
            #    row.append('')
                
            if 'printAdImage' in businesses:
                row.append(('printAdImage',str(businesses['printAdImage'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'printAdImageClick' in businesses:
                row.append(('printAdImageClick',"'" + str(businesses['printAdImageClick'].encode('utf-8')) + "'"))
            #else:
            #    row.append('')
                
            if 'ratingCount' in businesses:
                row.append(('ratingCount',str(businesses['ratingCount'])))
            #else:
            #    row.append('')
                
            if 'ringToNumberDisplay' in businesses:
                try:
                    row.append(('ringToNumberDisplay',str(businesses['ringToNumberDisplay']).encode('utf-8')))
                except:
                    row.append(('ringToNumberDisplay', str(businesses['ringToNumberDisplay'].encode('utf-8'))))
            #else:
            #    row.append('')

            if 'searchResultType' in businesses:
                try:
                    row.append(('searchResultType',str(businesses['searchResultType']).encode('utf-8')))
                except:
                    row.append(('searchResultType', str(businesses['searchResultType'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'services' in businesses:
                try:
                    row.append(('services',str(businesses['services']).encode('utf-8').replace('<li>', '').replace('</li>', '').replace('<ul>', '').replace('</ul>', '').replace('\n', '|')))
                except:
                    row.append(('services', str(businesses['services'].encode('utf-8').replace('<li>', '').replace('</li>', '').replace('<ul>', '').replace('</ul>', '').replace('\n', '|'))))
            #else:
            #    row.append('')

            if 'slogan' in businesses:
                try:
                    row.append(('slogan',str(businesses['slogan']).encode('utf-8').replace('\n', '')))
                except:
                    row.append(('slogan',str(businesses['slogan'].encode('utf-8')).replace('\n', '')))
            #else:
            #    row.append('')

            if 'state' in businesses:
                row.append(('state',str(businesses['state'].encode('utf-8'))))
            #else:
            #    row.append('')

            if 'street' in businesses:
                try:
                    row.append(('street',str(businesses['street']).encode('utf-8')))
                except:
                    row.append(('street', businesses['street'].encode('utf-8', 'ignore')))
                
            #else:
            #    row.append('')

            if 'videoURL' in businesses:
                row.append(('videoURL',str(businesses['videoURL'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'viewPhone' in businesses:
                row.append(('viewPhone',str(businesses['viewPhone'].encode('utf-8'))))
            #else:
            #    row.append('')

            if 'websiteURL' in businesses:
                row.append(('websiteURL',str(businesses['websiteURL'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'websitedisplayURL' in businesses:
                try:
                    row.append(('websitedisplayURL', str(businesses['websitedisplayURL']).encode('utf-8')))
                except:
                    row.append(('websitedisplayURL',str(businesses['websitedisplayURL'].encode('utf-8'))))
            #else:
            #    row.append('')
                
            if 'zip' in businesses:
                row.append(('zip', str(businesses['zip'])))
            #else:
            #    row.append('')
            
                
            #Additional    
            temp = []
            if 'accreditations' in businesses:
                if len(businesses['accreditations'])>0:
                    for acr in businesses['accreditations']['accreditation']:
                        try:
                            temp.append(acr.encode('utf-8').replace('\n', ' '))
                        except:
                            temp.append(str(acr).replace('\n', ' '))
                        
                    row.append(('accreditations', '|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')

            temp = []
            if 'additionalTexts' in businesses:
                if len(businesses['additionalTexts'])>0:
                    for acr in businesses['additionalTexts']['additionalText']:
                        temp.append(acr.encode('utf-8').replace('\n', ' '))
                    row.append(('additionalTexts','|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')
                
            if 'afterHoursPhone' in businesses:
                try:
                    row.append(('afterHoursPhone',"'" + str(businesses['afterHoursPhone'].encode('utf-8'))))
                except:
                    row.append(('afterHoursPhone',"'" + str(businesses['afterHoursPhone']).encode('utf-8')))
            #else:
            #    row.append('')

            temp = []
            if 'akas' in businesses:
                if len(businesses['akas'])>0:
                    for acr in businesses['akas']['aka']:
                        temp.append(acr.encode('utf-8').replace('\n', ' '))
                    row.append(('akas','|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')

            temp = []
            if 'amenities' in businesses:
                if len(businesses['amenities'])>0:
                    for acr in businesses['amenities']['amenity']:
                        temp.append(acr.encode('utf-8').replace('\n', ' '))
                    row.append(('amenities', '|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')
                
            temp = []
            if 'associations' in businesses:
                if len(businesses['associations'])>0:
                    for acr in businesses['associations']['association']:
                        temp.append(acr.encode('utf-8').replace('\n', ' '))
                    row.append(('associations','|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')
                
            if 'certification' in businesses:
                try:
                    row.append(('certification', str(businesses['certification'].encode('utf-8'))))
                except:
                    row.append(('certification', str(businesses['certification']).encode('utf-8')))
            #else:
            #    row.append('')
                
            temp = []
            if 'coupons' in businesses:
                if len(businesses['coupons'])>0:
                    #for acr in businesses['coupons']['coupon']:
                    #    temp.append(acr.encode('utf-8'))
                    #row.append('|'.join(temp))
                    row.append(('coupons', 'YES'))
                #else:
                #    row.append('')
            #else:
            #    row.append('')
                
            if 'emergencyPhone' in businesses:
                row.append(('emergencyPhone', "'" + str(businesses['emergencyPhone'].encode('utf-8')) + "'"))
            #else:
            #    row.append('')
                
            temp = []
            if 'extraEmails' in businesses:
                if len(businesses['extraEmails'])>0:
                    for acr in businesses['extraEmails']['extraEmail']:
                        temp.append(acr.encode('utf-8'))
                    row.append(('extraEmails', '|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')

            if 'extraFax' in businesses:
                try:
                    row.append(('extraFax', "'" + str(businesses['extraFax'].encode('utf-8'))))
                except:
                    row.append(('extraFax', "'" + str(businesses['extraFax']).encode('utf-8')))
            #else:
            #    row.append('')

            if 'extraPhone' in businesses:
                try:
                    row.append(('extraPhone', "'" + str(businesses['extraPhone'].encode('utf-8'))))
                except:
                    row.append(('extraPhone', "'" + str(businesses['extraPhone']).encode('utf-8')))
            #else:
            #    row.append('')
                
            if 'extraTollFree' in businesses:
                try:
                    row.append(('extraTollFree', "'" + str(businesses['extraTollFree'].encode('utf-8'))))
                except:
                    row.append(('extraTollFree', "'" + str(businesses['extraTollFree']).encode('utf-8')))
            #else:
            #    row.append('')

                
            temp = []
            if 'extraWebsiteURLs' in businesses:
                if len(businesses['extraWebsiteURLs'])>0:
                    for extraWebsiteURL in businesses['extraWebsiteURLs']['extraWebsiteURL']:
                        temp.append(extraWebsiteURL.encode('utf-8'))
                    row.append(('extraWebsiteURLs', '|'.join(temp)))
                #else:
                #    row.append('')
            #else:
            #    row.append('')
                
            if 'generalInfo' in businesses:
                try:
                    row.append(('generalInfo', str(businesses['generalInfo'].encode('utf-8').replace('\n',' '))))
                except:
                    row.append(('generalInfo', str(businesses['generalInfo']).encode('utf-8').replace('\n',' ')))
            #else:
            #    row.append('')

            if 'inBusinessSince' in businesses:
                try:
                    row.append(('inBusinessSince', "'" + str(businesses['inBusinessSince'].encode('utf-8').replace('\n',' '))))
                except:
                    row.append(('inBusinessSince', "'" + str(businesses['inBusinessSince']).encode('utf-8').replace('\n',' ')))
            #else:
            #    row.append('')
                
            if 'languagesSpoken' in businesses:
                try:
                    row.append(('languagesSpoken', str(businesses['languagesSpoken'].encode('utf-8').replace('\n',' '))))
                except:
                    row.append(('languagesSpoken', str(businesses['languagesSpoken']).encode('utf-8').replace('\n',' ')))
            #else:
            #    row.append('')

            if 'mobilePhone' in businesses:
                try:
                    row.append(('mobilePhone', "'" + str(businesses['mobilePhone'].encode('utf-8'))))
                except:
                    row.append(('mobilePhone', "'" + str(businesses['mobilePhone']).encode('utf-8')))
            #else:
            #    row.append('')
                
            if 'neighborhoods' in businesses:
                try:
                    row.append(('neighborhoods', "'" + str(businesses['neighborhoods'].encode('utf-8'))))
                except:
                    row.append(('neighborhoods', "'" + str(businesses['neighborhoods']).encode('utf-8')))
            #else:
            #    row.append('')
                
            if 'claimedStatus' in businesses:
                try:
                    row.append(('claimedStatus', "'" + str(businesses['claimedStatus'].encode('utf-8'))))
                except:
                    row.append(('claimedStatus', "'" + str(businesses['claimedStatus']).encode('utf-8')))
                
            scraperwiki.sqlite.save(unique_keys=['listingId'], data=dict(row))
            
    except:
        
        pass

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            count = self.queue.get()
            url_params['listingid'] = count
            response = request(options_host, '/listings/v1/details', url_params, options_key)
            if response:
                fWriteToCSV(response)
            self.queue.task_done()

for i in range(0,100):
    t = ThreadUrl(queue)
    t.setDaemon(True)
    t.start()
count = int(options_startid)
while(count < int(options_endid)):
    queue.put(count)
    count+=1
queue.join()

