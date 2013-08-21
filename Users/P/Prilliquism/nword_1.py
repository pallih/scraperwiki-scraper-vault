import scraperwiki
import string
scraperwiki.sqlite.attach('fed_speeches')
data = scraperwiki.sqlite.select(           
    '''* from fed_speeches.swdata 
    order by date desc limit 50'''
)
dic = {}
for item in data:
    dic[item["date"]]=item["text"]
corpus = ""
wordn=[set(),set()]
for text in dic.viewvalues():
    corpus+=text+' '
    myWords = text.split()
    for i,word in enumerate(myWords):
        for j in range(0,2):
            toAdd=word
            if i+j<len(myWords):
                for k in range(1,j+1):
                    toAdd+=' '+myWords[i+k]
            wordn[j].add(toAdd.strip(string.punctuation))

for i,wordSet in enumerate(wordn):
    invalids=set()
    for word in wordSet:
        if word.count(' ')<i or len(word)==0:
            invalids.add(word)
    for word in invalids:
        wordSet.remove(word);

print "Finished Finding all unique words and phrases"
for i in range(0,len(wordn)):
    print i
    occur=[]
    for word in wordn[i]:
        count = corpus.count(word)
        if count>0:
            occur.append({"word":word,"count":count})
    scraperwiki.sqlite.save(["word"],occur,"nword"+str(i+1))
