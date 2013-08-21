import scraperwiki
import lxml.html
a=['http://www.bolivianexpress.org/blog/posts/recuperar-recuperar-el-litoral-y-el-ancho-mar',
'http://www.bolivianexpress.org/blog/posts/in-this-fair-city',
'http://www.bolivianexpress.org/blog/posts/borracho-estaba-e-hice-una-pelicula',
'http://www.bolivianexpress.org/blog/posts/busking-in-la-paz',
'http://www.bolivianexpress.org/blog/posts/oye-profes-leave-those-kids-alone',
'http://www.bolivianexpress.org/blog/posts/true-bolivianite-the-story-of-ametrine',
'http://www.bolivianexpress.org/blog/posts/networking-bolivia',
'http://www.bolivianexpress.org/blog/posts/drumming-for-hate-s-a',
'http://www.bolivianexpress.org/blog/posts/music-money-and-the-messiah-rocking-out-for-christ',
'http://www.bolivianexpress.org/blog/posts/vero-perez',
'http://www.bolivianexpress.org/blog/posts/the-maestro-departs',
'http://www.bolivianexpress.org/blog/posts/songs-of-freedom',
'http://www.bolivianexpress.org/blog/posts/one-dollar-at-a-time-microfinance-in-bolivia',
'http://www.bolivianexpress.org/blog/posts/a-woman-s-mission-to-change-mining-in-bolivia',
'http://www.bolivianexpress.org/blog/posts/bolivia-s-clandestine-abortion-industry',
'http://www.bolivianexpress.org/blog/posts/lessons-from-the-booth',
'http://www.bolivianexpress.org/blog/posts/the-homes-of-the-homeless',
'http://www.bolivianexpress.org/blog/posts/the-incan-milky-way',
'http://www.bolivianexpress.org/blog/posts/nighttime-on-high',
'http://www.bolivianexpress.org/blog/posts/the-living-skulls-of-the-dead',
'http://www.bolivianexpress.org/blog/posts/morir-en-la-paz',
'http://www.bolivianexpress.org/blog/posts/kandinsky'
]
b=0
smmry=str
while b !=1: 
    html = scraperwiki.scrape('http://access.alchemyapi.com/calls/url/URLGetRankedKeywords?apikey=751de2330c943b28183cc2f040aac2f517cf4414&url='+str(a[b]))
    root = lxml.html.fromstring(html)
    smmry=root
    scraperwiki.sqlite.save(unique_keys=['orden'],data={'orden':b,'smmry':smmry,'id':str(a[b])})
    b=b+1

