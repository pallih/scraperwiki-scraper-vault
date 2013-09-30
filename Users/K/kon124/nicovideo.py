import scraperwiki
import lxml.html
from time import time
from urllib2 import URLError

u"""
extract video-metadata from nicovideo api.
form of data is
# video_id :        sm****
# title
# thumbnail_url
# first_retrieve
# length
# movie_type
# size_high
# size_low
# view_counter
# comment_num
# mylist_counter
# last_res_body
# watch_url
# thumb_type
# embeddable
# no_live_play
# tags :            list of tags
# category :        *if exists
# user_id

# view_verocity:    (viewCounterNew - viewCounterOld)/time
# comment_verocity: (commentNumNew - commentNumOld)/time
# mylist_verocity:  (mylistCounterNew - mylistCounterOld)/time
# accessed:         time accessed (utc second)

"""

URL = 'http://ext.nicovideo.jp/api/getthumbinfo/sm'

def get_nicodata(num):
    u"""
    num: video_id

    get video data and return it as a dict.
    """

    data = {}
    try:
        data_string = scraperwiki.scrape(URL+str(num))
    except URLError:
        time.sleep(10)
        get_nicodata(num)
        return
    data['accessed'] = int(time())
    
    e = lxml.html.fromstring(data_string)
    e.find('.//nicovideo_thumb_response')
    if e.attrib.get('status') != 'ok':
        return None
    tags = []
    for t in e.iter():
        if t.text is None:
            continue
        if t.tag == 'tag':
            tags.append(t.text)
            if t.attrib.get('category') is not None:
                data['category'] = t.text
        else:
            data[t.tag] = t.text
    data['tag'] = tags

    return data

max_num = 9502
flag = False
if flag:
    # for movies that has already been crawled
    data = scraperwiki.sqlite.execute('select video_id,view_counter,mylist_counter,comment_num,accessed from swdata')[u'data']
    u"""
    0 # video_id
    1 # view_counter    -> vc
    2 # mylist_counter  -> mc
    3 # comment_num     -> cn
    4 # accessed
    """
    nums = [int(v[0][2:]) for v in data]
    
    for index,vnum in enumerate(nums):
        new_data = get_nicodata(vnum)
        if data is None:
            scraperwiki.sqlite.execute('delete from swdata where video_id==%s' % data[index][0])
            continue
        
        vc_diff = int(new_data['view_counter']) - int(data[index][1])
        mc_diff = int(new_data['mylist_counter']) - int(data[index][2])
        cn_diff = int(new_data['comment_num']) - int(data[index][3])
    
        time_diff = int(new_data['accessed']) - int(data[index][4])
        hours = time_diff / 3600
    
        new_data['view_verocity'] = float(vc_diff / hours)
        new_data['comment_verocity'] = float(mc_diff / hours)
        new_data['mylist_verocity'] = float(mc_diff / hours)
    
        scraperwiki.sqlite.save(unique_keys=['video_id'],data=new_data)
    
    max_num = nums[-1]
count = 0 # if errors happen 100 times continuously, exit program

# for movies that has not been crawled
for i in xrange(max_num+1,max_num+20000000):
    data = get_nicodata(i)
    if data is None:
        count += 1
        if count > 100:
            print 'stopped at %d' % i
            exit()
        continue
    count = 0
    scraperwiki.sqlite.save(unique_keys=["video_id"], data=data)           
#"""import scraperwiki
import lxml.html
from time import time
from urllib2 import URLError

u"""
extract video-metadata from nicovideo api.
form of data is
# video_id :        sm****
# title
# thumbnail_url
# first_retrieve
# length
# movie_type
# size_high
# size_low
# view_counter
# comment_num
# mylist_counter
# last_res_body
# watch_url
# thumb_type
# embeddable
# no_live_play
# tags :            list of tags
# category :        *if exists
# user_id

# view_verocity:    (viewCounterNew - viewCounterOld)/time
# comment_verocity: (commentNumNew - commentNumOld)/time
# mylist_verocity:  (mylistCounterNew - mylistCounterOld)/time
# accessed:         time accessed (utc second)

"""

URL = 'http://ext.nicovideo.jp/api/getthumbinfo/sm'

def get_nicodata(num):
    u"""
    num: video_id

    get video data and return it as a dict.
    """

    data = {}
    try:
        data_string = scraperwiki.scrape(URL+str(num))
    except URLError:
        time.sleep(10)
        get_nicodata(num)
        return
    data['accessed'] = int(time())
    
    e = lxml.html.fromstring(data_string)
    e.find('.//nicovideo_thumb_response')
    if e.attrib.get('status') != 'ok':
        return None
    tags = []
    for t in e.iter():
        if t.text is None:
            continue
        if t.tag == 'tag':
            tags.append(t.text)
            if t.attrib.get('category') is not None:
                data['category'] = t.text
        else:
            data[t.tag] = t.text
    data['tag'] = tags

    return data

max_num = 9502
flag = False
if flag:
    # for movies that has already been crawled
    data = scraperwiki.sqlite.execute('select video_id,view_counter,mylist_counter,comment_num,accessed from swdata')[u'data']
    u"""
    0 # video_id
    1 # view_counter    -> vc
    2 # mylist_counter  -> mc
    3 # comment_num     -> cn
    4 # accessed
    """
    nums = [int(v[0][2:]) for v in data]
    
    for index,vnum in enumerate(nums):
        new_data = get_nicodata(vnum)
        if data is None:
            scraperwiki.sqlite.execute('delete from swdata where video_id==%s' % data[index][0])
            continue
        
        vc_diff = int(new_data['view_counter']) - int(data[index][1])
        mc_diff = int(new_data['mylist_counter']) - int(data[index][2])
        cn_diff = int(new_data['comment_num']) - int(data[index][3])
    
        time_diff = int(new_data['accessed']) - int(data[index][4])
        hours = time_diff / 3600
    
        new_data['view_verocity'] = float(vc_diff / hours)
        new_data['comment_verocity'] = float(mc_diff / hours)
        new_data['mylist_verocity'] = float(mc_diff / hours)
    
        scraperwiki.sqlite.save(unique_keys=['video_id'],data=new_data)
    
    max_num = nums[-1]
count = 0 # if errors happen 100 times continuously, exit program

# for movies that has not been crawled
for i in xrange(max_num+1,max_num+20000000):
    data = get_nicodata(i)
    if data is None:
        count += 1
        if count > 100:
            print 'stopped at %d' % i
            exit()
        continue
    count = 0
    scraperwiki.sqlite.save(unique_keys=["video_id"], data=data)           
#"""