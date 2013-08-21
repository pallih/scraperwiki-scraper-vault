import scraperwiki
import urllib2
import BeautifulSoup
import re


def shakespeare_play(url):
    html = scraperwiki.scrape(url)
    print html
    
    soup = BeautifulSoup.BeautifulSoup(html)
    vocab = {}
    char = ''
    
    for a in soup.findAll('a'):
        b = str(a)
        if b[9]=="s":
            char = a.find('b').string
            if char not in vocab: 
                vocab[char] =''
        elif char != '':
            vocab[char] = vocab[char]+a.string+" "
            #print vocab
                    
    for char in vocab:
        #print char
        vocaball = vocab[char].split()

        vocabulary = []
        for word in vocaball:
            cleanword = word.strip('.,;:?!-[]')
            listword = cleanword.split('--')
            vocabulary.extend(listword)
            totalvocab = len(set(vocabulary))
        #print set(vocabulary)
        #print totalvocab 
    scraperwiki.sqlite.save(unique_keys=["Name", "Play url"], data={"Name":char, "Play url":url, "Total Vocabulary":totalvocab})
    
shakespeare_play("http://shakespeare.mit.edu/tempest/full.html")
shakespeare_play("http://shakespeare.mit.edu/romeo_juliet/full.html")
shakespeare_play("http://shakespeare.mit.edu/allswell/full.html")
shakespeare_play("http://shakespeare.mit.edu/asyoulikeit/full.html")
shakespeare_play("http://shakespeare.mit.edu/comedy_errors/full.html")
shakespeare_play("http://shakespeare.mit.edu/cymbeline/full.html")
shakespeare_play("http://shakespeare.mit.edu/lll/full.html")
shakespeare_play("http://shakespeare.mit.edu/measure/full.html")
shakespeare_play("http://shakespeare.mit.edu/merry_wives/full.html")
shakespeare_play("http://shakespeare.mit.edu/merchant/full.html")
shakespeare_play("http://shakespeare.mit.edu/midsummer/full.html")
shakespeare_play("http://shakespeare.mit.edu/much_ado/full.html")
shakespeare_play("http://shakespeare.mit.edu/pericles/full.html")
shakespeare_play("http://shakespeare.mit.edu/taming_shrew/full.html")
shakespeare_play("http://shakespeare.mit.edu/troilus_cressida/full.html")
shakespeare_play("http://shakespeare.mit.edu/twelfth_night/full.html")
shakespeare_play("http://shakespeare.mit.edu/two_gentlemen/full.html")
shakespeare_play("http://shakespeare.mit.edu/winters_tale/full.html")
shakespeare_play("http://shakespeare.mit.edu/1henryiv/full.html")
shakespeare_play("http://shakespeare.mit.edu/2henryiv/full.html")
shakespeare_play("http://shakespeare.mit.edu/henryv/full.html")
shakespeare_play("http://shakespeare.mit.edu/1henryvi/full.html")
shakespeare_play("http://shakespeare.mit.edu/2henryvi/full.html") 
shakespeare_play("http://shakespeare.mit.edu/3henryvi/full.html")
shakespeare_play("http://shakespeare.mit.edu/henryviii/full.html")
shakespeare_play("http://shakespeare.mit.edu/john/full.html")
shakespeare_play("http://shakespeare.mit.edu/richardii/full.html")
shakespeare_play("http://shakespeare.mit.edu/richardiii/full.html")
shakespeare_play("http://shakespeare.mit.edu/cleopatra/full.html")
shakespeare_play("http://shakespeare.mit.edu/coriolanus/full.html")
shakespeare_play("http://shakespeare.mit.edu/hamlet/full.html")
shakespeare_play("http://shakespeare.mit.edu/julius_caesar/full.html")
shakespeare_play("http://shakespeare.mit.edu/lear/full.html")
shakespeare_play("http://shakespeare.mit.edu/macbeth/full.html")
shakespeare_play("http://shakespeare.mit.edu/othello/full.html")
shakespeare_play("http://shakespeare.mit.edu/timon/full.html")
shakespeare_play("http://shakespeare.mit.edu/titus/full.html")

