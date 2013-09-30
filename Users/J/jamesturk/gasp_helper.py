import scraperwiki
import hashlib
import json

def _hash(content):
    return hashlib.sha256(content.encode('utf8')).hexdigest()

class GaspHelper(object):
    """
        Helper class for Great American Scraper Project scrapers.
        Serves to normalize output and handle utility functions.
    """
    def __init__(self, sunlight_key, bioguide_id):
        self.sunlight_key = sunlight_key
        self.bioguide_id = bioguide_id

        self._updates = []

    # updates ###########

    def _add_update(self, update_type, title, date, content, **kwargs):
        update = {'update_type': update_type, 'title': title, 'date': date,
                  'content': content, 'content_hash': _hash(content),
                  'extra': json.dumps(kwargs)
                 }
        scraperwiki.sqlite.save(unique_keys=['title', 'date',
                                             'content_hash', 'update_type'],
                                data=update, table_name='updates')


    def add_issue(self, title, content, **kwargs):
        issue = {'title': title, 'content': content,
                 'content_hash': _hash(content),
                 'extra': json.dumps(kwargs)
                }
        scraperwiki.sqlite.save(unique_keys=['title', 'content_hash'],
                                data=issue, table_name='issues')


    def add_office(self, address, phone, fax=None,
                   **kwargs):
        office = {'address': address,'phone': phone, 'fax': fax or "",
                  'extra': json.dumps(kwargs)
                 }
        unique_keys = ('address', 'phone', 'fax')
        scraperwiki.sqlite.save(unique_keys=unique_keys, data=office,
                                table_name='offices')

    def add_biography(self, content, **kwargs):
        bio = {'content': content, 'content_hash': _hash(content),
               'extra': json.dumps(kwargs)
              }
        scraperwiki.sqlite.save(unique_keys=['content_hash'],
                                data=bio,
                                table_name='biography')

    def add_event(self, title, date, location, **kwargs):
        event = {'title': title, 'date': date, 'location': location,
                 'extra': json.dumps(kwargs)
                }
        scraperwiki.sqlite.save(unique_keys=['title', 'date', 'location'],
                                data=event, table_name='events')


    def add_social_media(self, service_name, url, **kwargs):
        sm = {'service': service_name, 'url': url, 'extra': json.dumps(kwargs)}
        scraperwiki.sqlite.save(unique_keys=['service', 'url'], data=sm,
                                table_name='social_media')


    # type helpers

    def add_press_release(self, title, date, content, **kwargs):
        self._add_update('press_release', title, date, content, **kwargs)

    def add_news_update(self, title, date, content, **kwargs):
        self._add_update('news_update', title, date, content, **kwargs)

    def add_blog_post(self, title, date, content, **kwargs):
        self._add_update('blog_post', title, date, content, **kwargs)

    def add_other_update(self, title, date, content, **kwargs):
        self._add_update('other', title, date, content, **kwargs)

    def add_facebook(self, url, **kwargs):
        self.add_social_media('facebook', url, **kwargs)

    def add_flickr(self, url, **kwargs):
        self.add_social_media('flickr', url, **kwargs)

    def add_twitter(self, url, **kwargs):
        self.add_social_media('twitter', url, **kwargs)

    def add_youtube(self, url, **kwargs):
        self.add_social_media('youtube', url, **kwargs)

    def finish(self):
        # send heartbeat
        print scraperwiki.scrape('http://services.sunlightlabs.com/gasp/heartbeat/?apikey=%s&bioguide_id=%s&scraper_id=%s' %
          (self.sunlight_key, self.bioguide_id,
           scraperwiki.datastore.m_scrapername))import scraperwiki
import hashlib
import json

def _hash(content):
    return hashlib.sha256(content.encode('utf8')).hexdigest()

class GaspHelper(object):
    """
        Helper class for Great American Scraper Project scrapers.
        Serves to normalize output and handle utility functions.
    """
    def __init__(self, sunlight_key, bioguide_id):
        self.sunlight_key = sunlight_key
        self.bioguide_id = bioguide_id

        self._updates = []

    # updates ###########

    def _add_update(self, update_type, title, date, content, **kwargs):
        update = {'update_type': update_type, 'title': title, 'date': date,
                  'content': content, 'content_hash': _hash(content),
                  'extra': json.dumps(kwargs)
                 }
        scraperwiki.sqlite.save(unique_keys=['title', 'date',
                                             'content_hash', 'update_type'],
                                data=update, table_name='updates')


    def add_issue(self, title, content, **kwargs):
        issue = {'title': title, 'content': content,
                 'content_hash': _hash(content),
                 'extra': json.dumps(kwargs)
                }
        scraperwiki.sqlite.save(unique_keys=['title', 'content_hash'],
                                data=issue, table_name='issues')


    def add_office(self, address, phone, fax=None,
                   **kwargs):
        office = {'address': address,'phone': phone, 'fax': fax or "",
                  'extra': json.dumps(kwargs)
                 }
        unique_keys = ('address', 'phone', 'fax')
        scraperwiki.sqlite.save(unique_keys=unique_keys, data=office,
                                table_name='offices')

    def add_biography(self, content, **kwargs):
        bio = {'content': content, 'content_hash': _hash(content),
               'extra': json.dumps(kwargs)
              }
        scraperwiki.sqlite.save(unique_keys=['content_hash'],
                                data=bio,
                                table_name='biography')

    def add_event(self, title, date, location, **kwargs):
        event = {'title': title, 'date': date, 'location': location,
                 'extra': json.dumps(kwargs)
                }
        scraperwiki.sqlite.save(unique_keys=['title', 'date', 'location'],
                                data=event, table_name='events')


    def add_social_media(self, service_name, url, **kwargs):
        sm = {'service': service_name, 'url': url, 'extra': json.dumps(kwargs)}
        scraperwiki.sqlite.save(unique_keys=['service', 'url'], data=sm,
                                table_name='social_media')


    # type helpers

    def add_press_release(self, title, date, content, **kwargs):
        self._add_update('press_release', title, date, content, **kwargs)

    def add_news_update(self, title, date, content, **kwargs):
        self._add_update('news_update', title, date, content, **kwargs)

    def add_blog_post(self, title, date, content, **kwargs):
        self._add_update('blog_post', title, date, content, **kwargs)

    def add_other_update(self, title, date, content, **kwargs):
        self._add_update('other', title, date, content, **kwargs)

    def add_facebook(self, url, **kwargs):
        self.add_social_media('facebook', url, **kwargs)

    def add_flickr(self, url, **kwargs):
        self.add_social_media('flickr', url, **kwargs)

    def add_twitter(self, url, **kwargs):
        self.add_social_media('twitter', url, **kwargs)

    def add_youtube(self, url, **kwargs):
        self.add_social_media('youtube', url, **kwargs)

    def finish(self):
        # send heartbeat
        print scraperwiki.scrape('http://services.sunlightlabs.com/gasp/heartbeat/?apikey=%s&bioguide_id=%s&scraper_id=%s' %
          (self.sunlight_key, self.bioguide_id,
           scraperwiki.datastore.m_scrapername))