import scraperwiki,requests,string

# Blank Python
print "*"

omit="*#/\\-;,![]{}_()$@=~&¢%+<>\"?.\r"
trans=string.maketrans(omit, ' '*len(omit))

def words(line):
    close=line.translate(trans).split(' ')
    return filter (lambda a: a != '', close) # http://stackoverflow.com/questions/1157106/remove-all-occurences-of-a-value-from-a-python-list

url='http://wondermark.com/x/wondermark800.txt'
text=requests.get(url).content
# TO DO: find &auml;
wordlist={}
ngramlist={}
for line in text.split('\n'):
    parsed=words(line)
    if not parsed:
        continue
    
    # create 1grams
    for word in parsed:
        if word in wordlist:
            wordlist[word]=wordlist[word]+1
        else:
            wordlist[word]=1

    # create (1+)grams
    print "*"
    for pos in range(0,len(line):
        for l=range(2,len(line)-pos):
            phrase=' '.join(line[pos:pos+l]
            print "%s is a %dgram."% (phrase, l)
            exit()
        
        
print wordlist
data=[]
for i in wordlist:
    try:
        if i.translate(None,"abcdefghijklmnopqrstuvwxyz0123456789'") != "":
            scraperwiki.sqlite.save(unique_keys=['word'], data={'word':i}, table_name="weirdchar")
        data.append({'word':i,'count':wordlist[i]})
    except Exception, e:
        print e

print "---"

scraperwiki.sqlite.save(unique_keys=['word'],data=data, table_name='1gram')
    
    