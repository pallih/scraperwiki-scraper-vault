import time, scraperwiki, hashlib, json
        

class ScraperHelper(object):
    """Helper class for Great American Scraper Project scrapers. Serves to normalize output and handle utility functions."""
    def __init__(self, sunlight_api_key, bioguide_id):
        super(ScraperHelper, self).__init__()
        
        self.sunlight_api_key = sunlight_api_key
        self.bioguide_id = bioguide_id
        self.time = time.time()
        
        self.content = {
            'biography': {},            
            'updates': {
                'press releases': [],
                'news updates': [],
                'in the news': [],
                'blog posts': [],    
                'other': []            
            },
            'social media': [],
            'issues': [],
            'offices': [],
            'events': [],
        }
            
        
    def _prepare_update(self, title, date, content, **kwargs):
        update = { 'title': title, 'date': date, 'content': content, 'meta': {} }
        for (k,v) in kwargs.items():
            update['meta'][k] = v
        return update
        
    def add_press_release(self, title, date, content, **kwargs):                
        self.content['updates']['press releases'].append(self._prepare_update(title, date, content, **kwargs))
        
    def add_news_update(self, title, date, content, **kwargs):        
        self.content['updates']['news updates'].append(self._prepare_update(title, date, content, **kwargs))
        
    def add_blog_post(self, title, date, content, **kwargs):
        self.content['updates']['blog posts'].append(self._prepare_update(title, date, content, **kwargs))        
        
    def add_in_the_news_item(self, title, date, content, **kwargs):
        self.content['updates']['in the news'].append(self._prepare_update(title, date, content, **kwargs))
        
    def add_other_update_type(self, update_type, title, date, content, **kwargs):  
        update = self._prepare_update(title, date, content, **kwargs)
        update['type'] = update_type        
        self.content['updates']['other'].append(update)

    def add_issue(self, title, content, **kwargs):
        issue = { 'title': title, 'content': content, 'meta': {} }
        for (k,v) in kwargs.items():
            issue['meta'][k] = v
        self.content['issues'].append(issue)
        
    def add_office(self, address, city, state, zipcode, phone, fax, **kwargs):
        office = { 'address': address, 'city': city, 'state': state, 'zipcode': zipcode, 'phone': phone, 'fax': fax, 'meta': {} }
        for (k,v) in kwargs.items():
            office['meta'][k] = v
        self.content['offices'].append(office)

    def add_biography(self, content, **kwargs):
        self.content['biography']['content'] = content
        self.content['biography']['meta'] = {}
        for (k,v) in kwargs.items():
            self.content['biography']['meta'][k] = v
        
    def add_event(self, title, date, location, **kwargs):
        event = { 'title': title, 'date': date, 'location': location, 'meta': {} }
        for (k,v) in kwargs.items():
            event['meta'][k] = v
        self.content['events'].append(event)
    
    def _set_social_media(self, service_name, url, **kwargs):
        sm = { 'service': service_name, 'url': url, 'meta': {} }
        for (k,v) in kwargs.items():
            sm['meta'][k] = v
        self.content['social media'].append(sm)
    
    def add_facebook(self, url, **kwargs):
        self._set_social_media('facebook', url, **kwargs)
        
    def add_flickr(self, url, **kwargs):
        self._set_social_media('flickr', url, **kwargs)
        
    def add_twitter(self, url, **kwargs):
        self._set_social_media('twitter', url, **kwargs)
        
    def add_youtube(self, url, **kwargs):
        self._set_social_media('youtube', url, **kwargs)
        
    def add_other_social_media(self, social_media_service_name, url, **kwargs):
        self._set_social_media(social_media_service_name, url, **kwargs)
    
    def finish(self):
        # tag self (not using actual tags) as a GASP scraper
        scraperwiki.sqlite.save_var('gasp_scraper', 1)
        scraperwiki.sqlite.save_var('gasp_bioguide', self.bioguide_id)
                
        # store biography
        if self.content['biography'].has_key('content'):
            self.content['biography']['content_hash'] = hashlib.sha256(self.content['biography']['content']).hexdigest()
            self.content['biography']['meta'] = json.dumps(self.content['biography']['meta'])
            scraperwiki.sqlite.save(unique_keys=['content_hash'], data=self.content['biography'], table_name='biography')                       
        
        
        # store social media        
        for social_media_account in self.content['social media']:
            social_media_account['meta'] = json.dumps(social_media_account['meta'])
            scraperwiki.sqlite.save(unique_keys=['service', 'url'], data=social_media_account, table_name='social_media')                       
        
        # store events
        for event in self.content['events']:
            event['meta'] = json.dumps(event['meta'])
            unique_keys = event.keys()
            unique_keys.remove('meta')
            scraperwiki.sqlite.save(unique_keys=unique_keys, data=event, table_name='events')           
        
        # store offices
        for office in self.content['offices']:
            office['meta'] = json.dumps(office['meta'])
            unique_keys = office.keys()
            unique_keys.remove('meta')
            scraperwiki.sqlite.save(unique_keys=unique_keys, data=office, table_name='offices') # consider every office attribute unique?     
        
        # store issues
        for issue in self.content['issues']:
            issue['content_hash'] = hashlib.sha256(issue['content']).hexdigest()
            issue['meta'] = json.dumps(issue['meta'])
            scraperwiki.sqlite.save(unique_keys=['title', 'content_hash'], data=issue, table_name='issues')
        
        # store updates
        for update_type in self.content['updates']:
            for update in self.content['updates'][update_type]:
                update['content_hash'] = hashlib.sha256(update['content']).hexdigest()
                update['meta'] = json.dumps(update['meta'])
                scraperwiki.sqlite.save(unique_keys=['title', 'date', 'content_hash'], data=update, table_name='updates_%s' % update_type.replace(' ', '_'))
        
        # send heartbeat
        scraperwiki.scrape('http://services.sunlightlabs.com/gasp/heartbeat?apikey=%s&scraper_id=%s&bioguide_id=%s' % (self.sunlight_api_key, scraperwiki.datastore.m_scrapername, self.bioguide_id))
    

print scraperwiki.datastore.m_scrapername  

#sh = ScraperHelper(sunlight_api_key='abcdefg', bioguide_id='boehner')
#sh.add_press_release('Boehner Announces New Plan', 'January 1, 2012', 'Sample copy.')
#sh.finish()
        import time, scraperwiki, hashlib, json
        

class ScraperHelper(object):
    """Helper class for Great American Scraper Project scrapers. Serves to normalize output and handle utility functions."""
    def __init__(self, sunlight_api_key, bioguide_id):
        super(ScraperHelper, self).__init__()
        
        self.sunlight_api_key = sunlight_api_key
        self.bioguide_id = bioguide_id
        self.time = time.time()
        
        self.content = {
            'biography': {},            
            'updates': {
                'press releases': [],
                'news updates': [],
                'in the news': [],
                'blog posts': [],    
                'other': []            
            },
            'social media': [],
            'issues': [],
            'offices': [],
            'events': [],
        }
            
        
    def _prepare_update(self, title, date, content, **kwargs):
        update = { 'title': title, 'date': date, 'content': content, 'meta': {} }
        for (k,v) in kwargs.items():
            update['meta'][k] = v
        return update
        
    def add_press_release(self, title, date, content, **kwargs):                
        self.content['updates']['press releases'].append(self._prepare_update(title, date, content, **kwargs))
        
    def add_news_update(self, title, date, content, **kwargs):        
        self.content['updates']['news updates'].append(self._prepare_update(title, date, content, **kwargs))
        
    def add_blog_post(self, title, date, content, **kwargs):
        self.content['updates']['blog posts'].append(self._prepare_update(title, date, content, **kwargs))        
        
    def add_in_the_news_item(self, title, date, content, **kwargs):
        self.content['updates']['in the news'].append(self._prepare_update(title, date, content, **kwargs))
        
    def add_other_update_type(self, update_type, title, date, content, **kwargs):  
        update = self._prepare_update(title, date, content, **kwargs)
        update['type'] = update_type        
        self.content['updates']['other'].append(update)

    def add_issue(self, title, content, **kwargs):
        issue = { 'title': title, 'content': content, 'meta': {} }
        for (k,v) in kwargs.items():
            issue['meta'][k] = v
        self.content['issues'].append(issue)
        
    def add_office(self, address, city, state, zipcode, phone, fax, **kwargs):
        office = { 'address': address, 'city': city, 'state': state, 'zipcode': zipcode, 'phone': phone, 'fax': fax, 'meta': {} }
        for (k,v) in kwargs.items():
            office['meta'][k] = v
        self.content['offices'].append(office)

    def add_biography(self, content, **kwargs):
        self.content['biography']['content'] = content
        self.content['biography']['meta'] = {}
        for (k,v) in kwargs.items():
            self.content['biography']['meta'][k] = v
        
    def add_event(self, title, date, location, **kwargs):
        event = { 'title': title, 'date': date, 'location': location, 'meta': {} }
        for (k,v) in kwargs.items():
            event['meta'][k] = v
        self.content['events'].append(event)
    
    def _set_social_media(self, service_name, url, **kwargs):
        sm = { 'service': service_name, 'url': url, 'meta': {} }
        for (k,v) in kwargs.items():
            sm['meta'][k] = v
        self.content['social media'].append(sm)
    
    def add_facebook(self, url, **kwargs):
        self._set_social_media('facebook', url, **kwargs)
        
    def add_flickr(self, url, **kwargs):
        self._set_social_media('flickr', url, **kwargs)
        
    def add_twitter(self, url, **kwargs):
        self._set_social_media('twitter', url, **kwargs)
        
    def add_youtube(self, url, **kwargs):
        self._set_social_media('youtube', url, **kwargs)
        
    def add_other_social_media(self, social_media_service_name, url, **kwargs):
        self._set_social_media(social_media_service_name, url, **kwargs)
    
    def finish(self):
        # tag self (not using actual tags) as a GASP scraper
        scraperwiki.sqlite.save_var('gasp_scraper', 1)
        scraperwiki.sqlite.save_var('gasp_bioguide', self.bioguide_id)
                
        # store biography
        if self.content['biography'].has_key('content'):
            self.content['biography']['content_hash'] = hashlib.sha256(self.content['biography']['content']).hexdigest()
            self.content['biography']['meta'] = json.dumps(self.content['biography']['meta'])
            scraperwiki.sqlite.save(unique_keys=['content_hash'], data=self.content['biography'], table_name='biography')                       
        
        
        # store social media        
        for social_media_account in self.content['social media']:
            social_media_account['meta'] = json.dumps(social_media_account['meta'])
            scraperwiki.sqlite.save(unique_keys=['service', 'url'], data=social_media_account, table_name='social_media')                       
        
        # store events
        for event in self.content['events']:
            event['meta'] = json.dumps(event['meta'])
            unique_keys = event.keys()
            unique_keys.remove('meta')
            scraperwiki.sqlite.save(unique_keys=unique_keys, data=event, table_name='events')           
        
        # store offices
        for office in self.content['offices']:
            office['meta'] = json.dumps(office['meta'])
            unique_keys = office.keys()
            unique_keys.remove('meta')
            scraperwiki.sqlite.save(unique_keys=unique_keys, data=office, table_name='offices') # consider every office attribute unique?     
        
        # store issues
        for issue in self.content['issues']:
            issue['content_hash'] = hashlib.sha256(issue['content']).hexdigest()
            issue['meta'] = json.dumps(issue['meta'])
            scraperwiki.sqlite.save(unique_keys=['title', 'content_hash'], data=issue, table_name='issues')
        
        # store updates
        for update_type in self.content['updates']:
            for update in self.content['updates'][update_type]:
                update['content_hash'] = hashlib.sha256(update['content']).hexdigest()
                update['meta'] = json.dumps(update['meta'])
                scraperwiki.sqlite.save(unique_keys=['title', 'date', 'content_hash'], data=update, table_name='updates_%s' % update_type.replace(' ', '_'))
        
        # send heartbeat
        scraperwiki.scrape('http://services.sunlightlabs.com/gasp/heartbeat?apikey=%s&scraper_id=%s&bioguide_id=%s' % (self.sunlight_api_key, scraperwiki.datastore.m_scrapername, self.bioguide_id))
    

print scraperwiki.datastore.m_scrapername  

#sh = ScraperHelper(sunlight_api_key='abcdefg', bioguide_id='boehner')
#sh.add_press_release('Boehner Announces New Plan', 'January 1, 2012', 'Sample copy.')
#sh.finish()
        