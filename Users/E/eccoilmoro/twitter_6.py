import scraperwiki
import oauth2 as oauth

# Blank Python

def oauth_req(url, key, secret, http_method="GET", post_body='',http_headers=None):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers
    )
    return content

print oauth_req('http://api.twitter.com/1/statuses/home_timeline.json','sldkfslkdjf','jjjkjkjkjkjkjk')
