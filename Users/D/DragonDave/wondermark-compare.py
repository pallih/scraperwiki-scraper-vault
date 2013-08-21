import scraperwiki
      
magic = 105232.0
print "*"
scraperwiki.sqlite.attach("wondermark")
scraperwiki.sqlite.attach("bnc_frequency_list")
data = scraperwiki.sqlite.select(           
    '''* from `1gram` where count>3'''
)

for item in data:
    bnc = scraperwiki.sqlite.select("sum(ratio) from swdata where word=\"%s\""%item['word'])
    if bnc[0]['sum(ratio)']==None:
        output={'word':item['word'],'ratio':-1}
        #print "The word '%s' is not in the corpus, but appears %d times in Wondermark."%(item['word'], item['count'])
    else:
        r=(item['count']/magic)/bnc[0]['sum(ratio)']
        output={'word':item['word'],'ratio':r}
        #print "The word '%s' is %.2f times as common in Wondermark"%(item['word'], r)
    scraperwiki.sqlite.save(unique_keys=["word"], data=output, table_name='compare')
    
