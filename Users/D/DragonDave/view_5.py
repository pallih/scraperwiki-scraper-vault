# Blank Python

import cgi,os,urllib

query_string = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

client_id="359-acf1403320e75e3cbc7b90dfd6d36042ff764296"
client_secret="e90057fa6ef1a272dcb3c2a0fdaa3d65f61226cb"
redirect_uri="https://views.scraperwiki.com/run/view_5/"

auth_query={"response_type":"token",
            "client_id":client_id,
            "redirect_uri":redirect_uri,
            "scope":"identity",
            "state":"hello-world"}

auth_uri="https://api.glitch.com/oauth2/authorize?"+urllib.urlencode(auth_query)


# STAGE 2A: horrible hack to get hash data
print """<script>if (window.location.hash) {window.location='%s?'+window.location.hash.slice(1)}</script>"""%redirect_uri

# STAGE 1: get CODE
if not query_string:
    print """Click to authorise: <a href=%s>here</a>"""%(auth_uri)

#token_query={"grant_type":"authorization_code",
#             "code":query_string['code'],
#             "client_id":client_id,
#             "client_secret":client_secret,
#             "redirect_uri":redirect_uri}
#token_url="https://api.glitch.com/oauth2/token?"+urllib.urlencode(token_query)


# STAGE 2: store CODE
if 'access_token' in query_string:
    print """You're in!"""
    req_uri="https://api.glitch.com/simple/auth.check?oauth_token="+query_string['access_token']+"&simple=1&pretty=1"
    print urllib.urlopen(req_uri).read()
    import scraperwiki
    scraperwiki.sqlite.save(unique_keys, data, table_name="swdata", verbose=2)
    

print "<small>%s, %s</small>"%(str(query_string), str(bool(query_string)))
# Blank Python

import cgi,os,urllib

query_string = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))

client_id="359-acf1403320e75e3cbc7b90dfd6d36042ff764296"
client_secret="e90057fa6ef1a272dcb3c2a0fdaa3d65f61226cb"
redirect_uri="https://views.scraperwiki.com/run/view_5/"

auth_query={"response_type":"token",
            "client_id":client_id,
            "redirect_uri":redirect_uri,
            "scope":"identity",
            "state":"hello-world"}

auth_uri="https://api.glitch.com/oauth2/authorize?"+urllib.urlencode(auth_query)


# STAGE 2A: horrible hack to get hash data
print """<script>if (window.location.hash) {window.location='%s?'+window.location.hash.slice(1)}</script>"""%redirect_uri

# STAGE 1: get CODE
if not query_string:
    print """Click to authorise: <a href=%s>here</a>"""%(auth_uri)

#token_query={"grant_type":"authorization_code",
#             "code":query_string['code'],
#             "client_id":client_id,
#             "client_secret":client_secret,
#             "redirect_uri":redirect_uri}
#token_url="https://api.glitch.com/oauth2/token?"+urllib.urlencode(token_query)


# STAGE 2: store CODE
if 'access_token' in query_string:
    print """You're in!"""
    req_uri="https://api.glitch.com/simple/auth.check?oauth_token="+query_string['access_token']+"&simple=1&pretty=1"
    print urllib.urlopen(req_uri).read()
    import scraperwiki
    scraperwiki.sqlite.save(unique_keys, data, table_name="swdata", verbose=2)
    

print "<small>%s, %s</small>"%(str(query_string), str(bool(query_string)))
