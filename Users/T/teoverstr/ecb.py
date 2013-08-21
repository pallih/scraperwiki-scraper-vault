# scrapes questions and trichet's answers from ecb press conference transcript

import urllib2
import re
import numpy
import scraperwiki
import operator
from nltk import pos_tag, word_tokenize

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("drop table if exists `totData`")

matchStr= '/press/pressconf/2011/html/is'
baseUrl = 'http://www.ecb.int/press/pressconf'
suffix  = '.en.html'

curYear = 2011

curUrl  = baseUrl + '/' + str(curYear) + '/html/index.en.html'

print(curUrl)

response = urllib2.urlopen(curUrl)
html = response.read()

urls = re.findall(r'href=[\'"]?([^\'" >]+)', html) 
pConf = []

for url in urls:
    if matchStr in url:
        if 'en' in url:
            pConf.append('http://www.ecb.int/' + url)

Q = []
A = []

i = 0

punctuation = re.compile(r'[.?!,":;]')
brackets    = re.compile(r'<.*>')


for url in pConf:
    q_curPC = []
    a_curPC = []
    response = urllib2.urlopen(url)
    html     = response.read()
    trichet  = re.findall(r'>Trichet:.*?>Q', html, re.DOTALL)
    endAns   = re.findall(r'>Trichet:.*?<address', html, re.DOTALL)
    question = re.findall(r'>Question.*?<strong>Trichet:', html, re.DOTALL)
    Q.extend(question)
    A.extend(trichet)
    A.extend(endAns)
    if len(trichet) != 0:
        for trichets in trichet:
            q_word_tags = pos_tag(word_tokenize(Q[i]))
            q_word_list = re.split('\s+', Q[i])
            q_freq_dict = {}
            for word in q_word_list:
                word = punctuation.sub("", word)
                word = brackets.sub("", word)
                try:         
                    q_freq_dict[word] += 1    
                except:         
                    q_freq_dict[word] = 1
            a_word_tags = pos_tag(word_tokenize(A[i]))
            a_word_list = re.split('\s+', A[i])
            a_freq_dict = {}
            for word in a_word_list:
                word = punctuation.sub("", word)
                word = brackets.sub("", word)
                try:         
                    a_freq_dict[word] += 1    
                except:         
                    a_freq_dict[word] = 1

            #print(q_freq_dict)
            scraperwiki.sqlite.save(unique_keys=["question"], data={"question":Q[i], "answer":A[i], "q_word_count": q_freq_dict, "a_word_count": a_freq_dict, "q_word_tags":q_word_tags, "a_word_tags":a_word_tags})
            i += 1

        q_curPC.extend(q_word_list)
        q_tot_dict = {}
        for word in q_curPC:
            word = punctuation.sub("", word)
            word = brackets.sub("", word)
            try:         
                    q_tot_dict[word] += 1    
            except:         
                    q_tot_dict[word] = 1

        a_curPC.extend(a_word_list)
        a_tot_dict = {}
        for word in a_curPC:
            word = punctuation.sub("", word)
            word = brackets.sub("", word)
            try:         
                    a_tot_dict[word] += 1    
            except:         
                    a_tot_dict[word] = 1
    
        q_tot_dict = sorted(q_tot_dict.iteritems(), key=operator.itemgetter(1))
        a_tot_dict = sorted(a_tot_dict.iteritems(), key=operator.itemgetter(1))

        scraperwiki.sqlite.save(unique_keys=["q_tot_dict"], data={"q_tot_dict":q_tot_dict,"a_tot_dict":a_tot_dict}, table_name = "totData")
        print(q_tot_dict)
        print(a_tot_dict)




        
    






