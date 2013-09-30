import scraperwiki
import tweetstream
# Blank Python


#words = ["Russia"]
#locations = ["55.522412,37.301331", "55.963038,37.938538"]

#try:
#    with tweetstream.FilterStream("casyfill", "Kochin13",track=words, locations=locations) as stream
#    for tweet in stream:
#        print tweet

locations = ["55.522412,37.301331", "55.963038,37.938538"]
with tweetstream.FilterStream("casyfill", "Kochin13", locations=locations) as stream:
    for tweet in stream:
        print tweetimport scraperwiki
import tweetstream
# Blank Python


#words = ["Russia"]
#locations = ["55.522412,37.301331", "55.963038,37.938538"]

#try:
#    with tweetstream.FilterStream("casyfill", "Kochin13",track=words, locations=locations) as stream
#    for tweet in stream:
#        print tweet

locations = ["55.522412,37.301331", "55.963038,37.938538"]
with tweetstream.FilterStream("casyfill", "Kochin13", locations=locations) as stream:
    for tweet in stream:
        print tweet