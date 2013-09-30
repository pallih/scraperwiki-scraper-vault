
import requests
import urllib
import urllib2
import urlparse
import time
import simplejson
import oauth2 as oauth
from urlparse import parse_qs
 
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
 
consumer_key = 'yq5jieRTQW8C4QlqIyDOQ'
consumer_secret = 'afwQzJKDVT9mMormevKNLWejapvWNErki5NES1sc'
token = '117092139-kO9lhepdeZqc3ZJYt6pP9NBzRZgaUN3JuwJ4I98x'
token_secret = 'Wi0R13e0vvIlZe5SFH7brDaF0a9o4h14AhnLozHECdY'

class OAuthApi():    
    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        if token and token_secret:
            token = oauth.Token(token, token_secret)
        else:
             token = None
        self._Consumer = oauth.Consumer(consumer_key, consumer_secret)
        self._signature_method = oauth.SignatureMethod_HMAC_SHA1()
        self._access_token = token

    def _GetOpener(self):
        opener = urllib2.build_opener()
        return opener

    def _FetchUrl(self,url,http_method=None,parameters=None):
        
        # Build the extra parameters dict
        extra_params = {}
        if parameters:
            extra_params.update(parameters)
        
        req = self._makeOAuthRequest(url, params=extra_params,http_method=http_method)
        
        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()

        if http_method == "POST":
            encoded_post_data = req.to_postdata()
            url = req.get_normalized_http_url()
        else:
            url = req.to_url()
            encoded_post_data = ""
            
        if encoded_post_data:
            url_data = opener.open(url, encoded_post_data).read()
        else:
            url_data = opener.open(url).read()
            opener.close()
    
        # Always return the latest version
        return url_data
    
    def _makeOAuthRequest(self, url, token=None,params=None, http_method="GET"):
               
        oauth_base_params = {
                            'oauth_version': "1.0",
                            'oauth_nonce': oauth.generate_nonce(),
                            'oauth_timestamp': int(time.time())
                            }
        
        if params:
            params.update(oauth_base_params)
        else:
            params = oauth_base_params
        
        if not token:
            token = self._access_token
        request = oauth.Request(method=http_method,url=url,parameters=params)
        request.sign_request(self._signature_method, self._Consumer, token)
        return request

    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        return "%s?oauth_token=%s" % (url, token['oauth_token'])

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        resp, content = oauth.Client(self._Consumer).request(url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        return dict(urlparse.parse_qsl(content))
    
    def getAccessToken(self, token, verifier, url=ACCESS_TOKEN_URL):
        token = oauth.Token(token['oauth_token'], token['oauth_token_secret'])
        token.set_verifier(verifier)
        client = oauth.Client(self._Consumer, token)
        
        resp, content = client.request(url, "POST")
        return dict(urlparse.parse_qsl(content))
    
    def FollowUser(self, user_id, options = {}):
        options['user_id'] = user_id
        self.ApiCall("friendships/create", "POST", options)

    def GetFriends(self, options={}):
        return self.ApiCall("statuses/followers", "GET", options)
    
    def GetFriendsTimeline(self, options = {}):
        return self.ApiCall("statuses/friends_timeline", "GET", options)
    
    def GetHomeTimeline(self, options={}):
        return self.ApiCall("statuses/home_timeline", "GET", options)    
    
    def GetUserTimeline(self, options={}):
        return self.ApiCall("statuses/user_timeline", "GET", options)    
    
    def GetPublicTimeline(self):
        return self.ApiCall("statuses/public_timeline", "GET", {})     
    
    def UpdateStatus(self, status, options = {}):
        options['status'] = status
        self.ApiCall("statuses/update", "POST", options)    
    
    def ApiCall(self, call, type="GET", parameters={}):
        json = self._FetchUrl("https://api.twitter.com/1/" + call + ".json", type, parameters)
        return simplejson.loads(json)


json = OAuthApi(consumer_key, consumer_secret, token, token_secret)
json2 = json._FetchUrl('','GET','')
soup = simplejson.loads(json)
for result in soup['results']:
    data = {}
    data['id'] = result['id']
    data['text'] = result['text']
    data['from_user'] = result['from_user']
    # save records to the datastore
    scraperwiki.datastore.save(["id"], data)



import requests
import urllib
import urllib2
import urlparse
import time
import simplejson
import oauth2 as oauth
from urlparse import parse_qs
 
REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZATION_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
 
consumer_key = 'yq5jieRTQW8C4QlqIyDOQ'
consumer_secret = 'afwQzJKDVT9mMormevKNLWejapvWNErki5NES1sc'
token = '117092139-kO9lhepdeZqc3ZJYt6pP9NBzRZgaUN3JuwJ4I98x'
token_secret = 'Wi0R13e0vvIlZe5SFH7brDaF0a9o4h14AhnLozHECdY'

class OAuthApi():    
    def __init__(self, consumer_key, consumer_secret, token, token_secret):
        if token and token_secret:
            token = oauth.Token(token, token_secret)
        else:
             token = None
        self._Consumer = oauth.Consumer(consumer_key, consumer_secret)
        self._signature_method = oauth.SignatureMethod_HMAC_SHA1()
        self._access_token = token

    def _GetOpener(self):
        opener = urllib2.build_opener()
        return opener

    def _FetchUrl(self,url,http_method=None,parameters=None):
        
        # Build the extra parameters dict
        extra_params = {}
        if parameters:
            extra_params.update(parameters)
        
        req = self._makeOAuthRequest(url, params=extra_params,http_method=http_method)
        
        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()

        if http_method == "POST":
            encoded_post_data = req.to_postdata()
            url = req.get_normalized_http_url()
        else:
            url = req.to_url()
            encoded_post_data = ""
            
        if encoded_post_data:
            url_data = opener.open(url, encoded_post_data).read()
        else:
            url_data = opener.open(url).read()
            opener.close()
    
        # Always return the latest version
        return url_data
    
    def _makeOAuthRequest(self, url, token=None,params=None, http_method="GET"):
               
        oauth_base_params = {
                            'oauth_version': "1.0",
                            'oauth_nonce': oauth.generate_nonce(),
                            'oauth_timestamp': int(time.time())
                            }
        
        if params:
            params.update(oauth_base_params)
        else:
            params = oauth_base_params
        
        if not token:
            token = self._access_token
        request = oauth.Request(method=http_method,url=url,parameters=params)
        request.sign_request(self._signature_method, self._Consumer, token)
        return request

    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        return "%s?oauth_token=%s" % (url, token['oauth_token'])

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        resp, content = oauth.Client(self._Consumer).request(url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        return dict(urlparse.parse_qsl(content))
    
    def getAccessToken(self, token, verifier, url=ACCESS_TOKEN_URL):
        token = oauth.Token(token['oauth_token'], token['oauth_token_secret'])
        token.set_verifier(verifier)
        client = oauth.Client(self._Consumer, token)
        
        resp, content = client.request(url, "POST")
        return dict(urlparse.parse_qsl(content))
    
    def FollowUser(self, user_id, options = {}):
        options['user_id'] = user_id
        self.ApiCall("friendships/create", "POST", options)

    def GetFriends(self, options={}):
        return self.ApiCall("statuses/followers", "GET", options)
    
    def GetFriendsTimeline(self, options = {}):
        return self.ApiCall("statuses/friends_timeline", "GET", options)
    
    def GetHomeTimeline(self, options={}):
        return self.ApiCall("statuses/home_timeline", "GET", options)    
    
    def GetUserTimeline(self, options={}):
        return self.ApiCall("statuses/user_timeline", "GET", options)    
    
    def GetPublicTimeline(self):
        return self.ApiCall("statuses/public_timeline", "GET", {})     
    
    def UpdateStatus(self, status, options = {}):
        options['status'] = status
        self.ApiCall("statuses/update", "POST", options)    
    
    def ApiCall(self, call, type="GET", parameters={}):
        json = self._FetchUrl("https://api.twitter.com/1/" + call + ".json", type, parameters)
        return simplejson.loads(json)


json = OAuthApi(consumer_key, consumer_secret, token, token_secret)
json2 = json._FetchUrl('','GET','')
soup = simplejson.loads(json)
for result in soup['results']:
    data = {}
    data['id'] = result['id']
    data['text'] = result['text']
    data['from_user'] = result['from_user']
    # save records to the datastore
    scraperwiki.datastore.save(["id"], data)


