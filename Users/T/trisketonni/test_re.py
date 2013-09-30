import scraperwiki
import re

rt = "RT @xabier ola k ase"
rt2 = '"@xabier ola k ase"'

reply = "@xabier ola k ase"
reply2 = ". @xabier ola k ase"

PATTERN_RT = '(^RT |^\")@(\w+)'
pattern_reply = '^@|\. ?@(\w+)'


match = re.compile(PATTERN_RT)

match_rt = match.search(rt)
match_rt2 = match.search(rt2)
print match_rt.groups()
print match_rt2.groups()
#print match.split(rt2)


match = re.compile(pattern_reply)

match_rt = match.search(reply)
match_rt2 = match.search(reply2)
print match_rt.groups()
print match_rt2.groups()

tuit = 'Vogue México ‏@VogueMexico\
    Video: @PaulMcCartney, @jessicaalba y Mario Testino comentan sobre @StellaMcCartney FW13 #PFW http://www.vogue.mx/videos/stella-mc-cartney-fall-winter-13-paris-fashion-week/519 … pic.twitter.com/X7IhPZhZHN'

print tuit

print re.findall(r'@(\w+)', tuit)import scraperwiki
import re

rt = "RT @xabier ola k ase"
rt2 = '"@xabier ola k ase"'

reply = "@xabier ola k ase"
reply2 = ". @xabier ola k ase"

PATTERN_RT = '(^RT |^\")@(\w+)'
pattern_reply = '^@|\. ?@(\w+)'


match = re.compile(PATTERN_RT)

match_rt = match.search(rt)
match_rt2 = match.search(rt2)
print match_rt.groups()
print match_rt2.groups()
#print match.split(rt2)


match = re.compile(pattern_reply)

match_rt = match.search(reply)
match_rt2 = match.search(reply2)
print match_rt.groups()
print match_rt2.groups()

tuit = 'Vogue México ‏@VogueMexico\
    Video: @PaulMcCartney, @jessicaalba y Mario Testino comentan sobre @StellaMcCartney FW13 #PFW http://www.vogue.mx/videos/stella-mc-cartney-fall-winter-13-paris-fashion-week/519 … pic.twitter.com/X7IhPZhZHN'

print tuit

print re.findall(r'@(\w+)', tuit)