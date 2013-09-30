import scraperwiki

# Blank Python

import mechanize
import bz2
#import lxml.html
#from datetime import datetime


def firstitem() : "xaaaa"
def lastitem() : "xachy"
import tarfile  
import string
from cStringIO import StringIO
import struct
from io import BytesIO



def readnodes (position,block, nodesindex) :    
    f = BytesIO(nodesindex)
    #f = open(mode="r:b", fileobj =myfileobj)
    pos=0
    try:
        byte = f.read(4)
        while byte != "":
            value = struct.unpack('i', byte)
            if (value[0]>0) :
                #print ("%d" % value[0]);
                #bucket_files_nodes (project int, position int, block int, bpos int, node int)
                cmd ="insert or replace into bucket_file_nodes values (1,?,?,?,?)" 
                #print (position,block,pos,value[0])
                scraperwiki.sqlite.execute(cmd,(position,block,pos,value[0]));
                pos=pos+4
        # Do stuff with byte.
            byte = f.read(4)
    finally:
        f.close()
        scraperwiki.sqlite.commit()

def process():
    # used clear data : scraperwiki.sqlite.execute("drop table bucket_file_nodes") 
    scraperwiki.sqlite.execute("create table if not exists bucket_file_nodes (project int, bucketposition int, block int, bpos int, node int)") 
    scraperwiki.sqlite.execute("create index if not exists node_id on bucket_file_nodes(node)")    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    scraperwiki.sqlite.attach("fosm_index", "src1")
    scraperwiki.sqlite.attach("fosm_index_1", "src2")
    data= scraperwiki.sqlite.select("* from src2.bucket_files")       
    for x in data :
        block = x["block"]
        position = x["position"]
        sql = "name from src1.buckets where project=1 and position=%d" % position
        named = scraperwiki.sqlite.select(sql)     
        name= named[0]["name"]
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
        print name
        print block
        uri=  "%s%s/%s_index.zip/pine02/index/%06d_i.tbz" % (baseuri,name,name, block)

    #http://archive.org/download/fosm-20120401130001-xaapj/xaapj_index.zip/pine02/index/199501_i.tbz

        print uri
        data = br.open(uri).read()
        #data = br.response().read()
        #print data
        #tar = bz2.decompress(data);
        #print tar
        myfileobj=StringIO(data)
        mytarfile = tarfile.open(mode="r:bz2", fileobj =myfileobj)
        for member in mytarfile.getnames():
        # Print contents of every file
            print member
            if member.endswith("node_ids.bin") :
                nodes=mytarfile.extractfile(member).read()
                readnodes(position,block,nodes)
            #print tar.extractfile(member).read()

#        darray = data.rsplit("\n")
        #print darray
        #for y in darray :
        #    if y.endswith("_i.tbz"):
                #cmd ="insert or replace into bucket_files values (1,?,?)" 
                #scraperwiki.sqlite.execute(cmd,(x["position"],y[:-6]))
        #scraperwiki.sqlite.commit()

def main():
    
    print "test"
    
    #print genletters (lastitem())

    process ()
    scraperwiki.sqlite.commit()

main()
 import scraperwiki

# Blank Python

import mechanize
import bz2
#import lxml.html
#from datetime import datetime


def firstitem() : "xaaaa"
def lastitem() : "xachy"
import tarfile  
import string
from cStringIO import StringIO
import struct
from io import BytesIO



def readnodes (position,block, nodesindex) :    
    f = BytesIO(nodesindex)
    #f = open(mode="r:b", fileobj =myfileobj)
    pos=0
    try:
        byte = f.read(4)
        while byte != "":
            value = struct.unpack('i', byte)
            if (value[0]>0) :
                #print ("%d" % value[0]);
                #bucket_files_nodes (project int, position int, block int, bpos int, node int)
                cmd ="insert or replace into bucket_file_nodes values (1,?,?,?,?)" 
                #print (position,block,pos,value[0])
                scraperwiki.sqlite.execute(cmd,(position,block,pos,value[0]));
                pos=pos+4
        # Do stuff with byte.
            byte = f.read(4)
    finally:
        f.close()
        scraperwiki.sqlite.commit()

def process():
    # used clear data : scraperwiki.sqlite.execute("drop table bucket_file_nodes") 
    scraperwiki.sqlite.execute("create table if not exists bucket_file_nodes (project int, bucketposition int, block int, bpos int, node int)") 
    scraperwiki.sqlite.execute("create index if not exists node_id on bucket_file_nodes(node)")    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    scraperwiki.sqlite.attach("fosm_index", "src1")
    scraperwiki.sqlite.attach("fosm_index_1", "src2")
    data= scraperwiki.sqlite.select("* from src2.bucket_files")       
    for x in data :
        block = x["block"]
        position = x["position"]
        sql = "name from src1.buckets where project=1 and position=%d" % position
        named = scraperwiki.sqlite.select(sql)     
        name= named[0]["name"]
        baseuri = "http://archive.org/download/fosm-20120401130001-" 
        print name
        print block
        uri=  "%s%s/%s_index.zip/pine02/index/%06d_i.tbz" % (baseuri,name,name, block)

    #http://archive.org/download/fosm-20120401130001-xaapj/xaapj_index.zip/pine02/index/199501_i.tbz

        print uri
        data = br.open(uri).read()
        #data = br.response().read()
        #print data
        #tar = bz2.decompress(data);
        #print tar
        myfileobj=StringIO(data)
        mytarfile = tarfile.open(mode="r:bz2", fileobj =myfileobj)
        for member in mytarfile.getnames():
        # Print contents of every file
            print member
            if member.endswith("node_ids.bin") :
                nodes=mytarfile.extractfile(member).read()
                readnodes(position,block,nodes)
            #print tar.extractfile(member).read()

#        darray = data.rsplit("\n")
        #print darray
        #for y in darray :
        #    if y.endswith("_i.tbz"):
                #cmd ="insert or replace into bucket_files values (1,?,?)" 
                #scraperwiki.sqlite.execute(cmd,(x["position"],y[:-6]))
        #scraperwiki.sqlite.commit()

def main():
    
    print "test"
    
    #print genletters (lastitem())

    process ()
    scraperwiki.sqlite.commit()

main()
 