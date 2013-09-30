import scraperwiki,md5

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    key=qsenv["KEY"]
    if 'cloudscapeID' in qsenv: cloudscapeID=qsenv['cloudscapeID']
    else: cloudscapeID='2451'
    if 'userID' in qsenv: userID=qsenv['userID']
    else: userID='108'
    if 'filterNdegree' in qsenv: filterNdegree=int(qsenv['filterNdegree'])
    else: filterNdegree=''
    if 'viewtype' in qsenv: viewtype=qsenv['viewtype']
    else: viewtype='cloudscapeinnerfollowers'
    if 'format' in qsenv: format=qsenv['format']
    else: format='json'
except:
    exit(-1)


#http://cloudworks.ac.uk/api/clouds/{cloud_id}.{format}?api_key={api_key}


import urllib2,json, networkx as nx
from networkx.readwrite import json_graph

#id=cloudscapeID #need logic


def ascii(s): return "".join(i for i in s.encode('utf-8') if ord(i)<128)

def graphRoot(DG,title,root=1):
    DG.add_node(root,name=ascii(title))
    return DG,root

def gNodeAdd(DG,root,node,name):
    node=node+1
    #print str(root),'..',str(node)
    DG.add_node(node,name=ascii(name))
    DG.add_edge(root,node)
    return DG,node


def getXYZentities(id,main,typ):
    urlstub="http://cloudworks.ac.uk/api/"
    bigstub=urlstub+main+"/"+str(id)
    urlsuffix=".json?api_key="+str(key)

    if typ!='':url=bigstub+"/"+typ+urlsuffix
    else:url=bigstub+urlsuffix
    #print url
    return json.load(urllib2.urlopen(url))

def getXYZ(id,main,typ,att,field):
    results=getXYZentities(id,main,typ)
    #print results
    f=[]
    if results[att]!=None: 
        for r in results[att]:
            f.append(r[field])
    return f

def getUserFollowers(id):
    urlstub="http://cloudworks.ac.uk/api/"
    urluserstub=urlstub+"users/"+str(id)
    urlsuffix=".json?api_key="+str(key)

    ctyp="/followers"
    url=urluserstub+ctyp+urlsuffix
    results=json.load(urllib2.urlopen(url))
    #print results
    f=[]
    for r in results['items']: f.append(r['user_id'])
    return f

def getCloudCloudscapes(id):
    return getXYZ(id,'clouds','cloudscapes','items','cloudscape_id')


#--

urlstub="http://cloudworks.ac.uk/api/"
urlsuffix=".json?api_key="+str(key)

DG=nx.DiGraph()

#viewtype='usercloudcloudscapefollower'
if viewtype=='cloudscapecloudtags':
    entities=getXYZentities(cloudscapeID,'cloudscapes','clouds')
    #example of tags associated with cllouds in this cloudscape
    taghash={}
    for c in entities['items']:
        currcid=c['cloud_id']
        DG.add_node(currcid,name=ascii(c['title']).strip(),group='cloud')
        cloud=getXYZentities(currcid,'clouds','')
        if cloud['tags']!=None:
            for tag in cloud['tags']:
                if tag['name'] not in taghash:
                    taghash[tag['name']]=md5.new(tag['api_url']).hexdigest()
                    DG.add_node(taghash[tag['name']],name=ascii(tag['name']).strip(),group='tag')
                DG.add_edge(currcid,taghash[tag['name']])

elif viewtype=='usercloudcloudscapefollower':
    entities=getXYZentities(userID,'users','clouds')
    cloudscapes={}
    users=[]
    for c in entities['items']:
        currcid=c['cloud_id']
        #get cloudscapes for cloud
        cloudscapesforcloud=getXYZentities(currcid,'clouds','cloudscapes')
        #if cloudscapesforcloud==None: cloudscapesforcloud=[]
        for cloudscape in cloudscapesforcloud['items']:
            if cloudscape['cloudscape_id'] not in cloudscapes:
                cloudscapes[cloudscape['cloudscape_id']]=cloudscape['title']
        for c in cloudscapes: DG.add_node(c,name=ascii(cloudscapes[c]).strip(),group='cloud')
        #get followers for cloudscapes
        for cloudscape in cloudscapes:
            entities=getXYZentities(cloudscape,'cloudscapes','followers')
            for follower in entities['items']:
                if follower['user_id'] not in users:
                    users.append(follower['user_id'])
                    DG.add_node(follower['user_id'],name=ascii(follower['name']).strip(),group='user')
                DG.add_edge(cloudscape,follower['user_id'])
elif viewtype=='cloudscapecloudcloudscape':
    entities=getXYZentities(cloudscapeID,'cloudscapes','clouds')

    cloudscapelist=[]
    #example of other cloudscapes clouds in this cloud are in
    for c in entities['items']:
        currcid=c['cloud_id']
        DG.add_node(currcid,name=ascii(c['title']).strip(),group='cloud')
        cloudscapes=getXYZentities(currcid,'clouds','cloudscapes')
        for cloudscape in cloudscapes['items']:
            if cloudscape['cloudscape_id'] not in cloudscapelist:
                cloudscapelist.append(cloudscape['cloudscape_id'])
                DG.add_node(cloudscape['cloudscape_id'],name=ascii(cloudscape['title']).strip(),group='cloudscape')
            DG.add_edge(currcid,cloudscape['cloudscape_id'])                

else: #viewtype=='cloudscapeinnerfollowers':
    urlcloudscapestub=urlstub+"cloudscapes/"+str(cloudscapeID)
    ctyp="/followers"
    url=urlcloudscapestub+ctyp+urlsuffix
    #print url
    entities=json.load(urllib2.urlopen(url))

    #print entities
    #--

    followerIDs=[]

    #example inner followers graph
    for c in entities['items']:
        curruid=c['user_id']
        DG.add_node(curruid,name=ascii(c['name']).strip())
        #if curruid not in followerIDs: DG.add_node(curruid,name='')
        followerIDs.append(curruid)
    #print entities['items']
    for c in entities['items']:
        curruid=c['user_id']
        followers=getUserFollowers(curruid)
        for followerid in followers:
            if followerid in followerIDs:
                DG.add_edge(curruid,followerid)

if filterNdegree!='':DG.remove_nodes_from((n for n,d in DG.degree_iter() if d<=filterNdegree))

if format=='gexf':
    import networkx.readwrite.gexf as gf
    writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
    writer.add_graph(DG)
    scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
    from xml.etree.cElementTree import tostring
    print tostring(writer.xml)
else: #format=='json'
    jdata = json_graph.node_link_data(DG)
    scraperwiki.utils.httpresponseheader("Content-Type", "text/json")
    print json_graph.dumps(jdata)
#For some reason, templated view giving a string error? Line length?!
#print page_template % vars()import scraperwiki,md5

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    key=qsenv["KEY"]
    if 'cloudscapeID' in qsenv: cloudscapeID=qsenv['cloudscapeID']
    else: cloudscapeID='2451'
    if 'userID' in qsenv: userID=qsenv['userID']
    else: userID='108'
    if 'filterNdegree' in qsenv: filterNdegree=int(qsenv['filterNdegree'])
    else: filterNdegree=''
    if 'viewtype' in qsenv: viewtype=qsenv['viewtype']
    else: viewtype='cloudscapeinnerfollowers'
    if 'format' in qsenv: format=qsenv['format']
    else: format='json'
except:
    exit(-1)


#http://cloudworks.ac.uk/api/clouds/{cloud_id}.{format}?api_key={api_key}


import urllib2,json, networkx as nx
from networkx.readwrite import json_graph

#id=cloudscapeID #need logic


def ascii(s): return "".join(i for i in s.encode('utf-8') if ord(i)<128)

def graphRoot(DG,title,root=1):
    DG.add_node(root,name=ascii(title))
    return DG,root

def gNodeAdd(DG,root,node,name):
    node=node+1
    #print str(root),'..',str(node)
    DG.add_node(node,name=ascii(name))
    DG.add_edge(root,node)
    return DG,node


def getXYZentities(id,main,typ):
    urlstub="http://cloudworks.ac.uk/api/"
    bigstub=urlstub+main+"/"+str(id)
    urlsuffix=".json?api_key="+str(key)

    if typ!='':url=bigstub+"/"+typ+urlsuffix
    else:url=bigstub+urlsuffix
    #print url
    return json.load(urllib2.urlopen(url))

def getXYZ(id,main,typ,att,field):
    results=getXYZentities(id,main,typ)
    #print results
    f=[]
    if results[att]!=None: 
        for r in results[att]:
            f.append(r[field])
    return f

def getUserFollowers(id):
    urlstub="http://cloudworks.ac.uk/api/"
    urluserstub=urlstub+"users/"+str(id)
    urlsuffix=".json?api_key="+str(key)

    ctyp="/followers"
    url=urluserstub+ctyp+urlsuffix
    results=json.load(urllib2.urlopen(url))
    #print results
    f=[]
    for r in results['items']: f.append(r['user_id'])
    return f

def getCloudCloudscapes(id):
    return getXYZ(id,'clouds','cloudscapes','items','cloudscape_id')


#--

urlstub="http://cloudworks.ac.uk/api/"
urlsuffix=".json?api_key="+str(key)

DG=nx.DiGraph()

#viewtype='usercloudcloudscapefollower'
if viewtype=='cloudscapecloudtags':
    entities=getXYZentities(cloudscapeID,'cloudscapes','clouds')
    #example of tags associated with cllouds in this cloudscape
    taghash={}
    for c in entities['items']:
        currcid=c['cloud_id']
        DG.add_node(currcid,name=ascii(c['title']).strip(),group='cloud')
        cloud=getXYZentities(currcid,'clouds','')
        if cloud['tags']!=None:
            for tag in cloud['tags']:
                if tag['name'] not in taghash:
                    taghash[tag['name']]=md5.new(tag['api_url']).hexdigest()
                    DG.add_node(taghash[tag['name']],name=ascii(tag['name']).strip(),group='tag')
                DG.add_edge(currcid,taghash[tag['name']])

elif viewtype=='usercloudcloudscapefollower':
    entities=getXYZentities(userID,'users','clouds')
    cloudscapes={}
    users=[]
    for c in entities['items']:
        currcid=c['cloud_id']
        #get cloudscapes for cloud
        cloudscapesforcloud=getXYZentities(currcid,'clouds','cloudscapes')
        #if cloudscapesforcloud==None: cloudscapesforcloud=[]
        for cloudscape in cloudscapesforcloud['items']:
            if cloudscape['cloudscape_id'] not in cloudscapes:
                cloudscapes[cloudscape['cloudscape_id']]=cloudscape['title']
        for c in cloudscapes: DG.add_node(c,name=ascii(cloudscapes[c]).strip(),group='cloud')
        #get followers for cloudscapes
        for cloudscape in cloudscapes:
            entities=getXYZentities(cloudscape,'cloudscapes','followers')
            for follower in entities['items']:
                if follower['user_id'] not in users:
                    users.append(follower['user_id'])
                    DG.add_node(follower['user_id'],name=ascii(follower['name']).strip(),group='user')
                DG.add_edge(cloudscape,follower['user_id'])
elif viewtype=='cloudscapecloudcloudscape':
    entities=getXYZentities(cloudscapeID,'cloudscapes','clouds')

    cloudscapelist=[]
    #example of other cloudscapes clouds in this cloud are in
    for c in entities['items']:
        currcid=c['cloud_id']
        DG.add_node(currcid,name=ascii(c['title']).strip(),group='cloud')
        cloudscapes=getXYZentities(currcid,'clouds','cloudscapes')
        for cloudscape in cloudscapes['items']:
            if cloudscape['cloudscape_id'] not in cloudscapelist:
                cloudscapelist.append(cloudscape['cloudscape_id'])
                DG.add_node(cloudscape['cloudscape_id'],name=ascii(cloudscape['title']).strip(),group='cloudscape')
            DG.add_edge(currcid,cloudscape['cloudscape_id'])                

else: #viewtype=='cloudscapeinnerfollowers':
    urlcloudscapestub=urlstub+"cloudscapes/"+str(cloudscapeID)
    ctyp="/followers"
    url=urlcloudscapestub+ctyp+urlsuffix
    #print url
    entities=json.load(urllib2.urlopen(url))

    #print entities
    #--

    followerIDs=[]

    #example inner followers graph
    for c in entities['items']:
        curruid=c['user_id']
        DG.add_node(curruid,name=ascii(c['name']).strip())
        #if curruid not in followerIDs: DG.add_node(curruid,name='')
        followerIDs.append(curruid)
    #print entities['items']
    for c in entities['items']:
        curruid=c['user_id']
        followers=getUserFollowers(curruid)
        for followerid in followers:
            if followerid in followerIDs:
                DG.add_edge(curruid,followerid)

if filterNdegree!='':DG.remove_nodes_from((n for n,d in DG.degree_iter() if d<=filterNdegree))

if format=='gexf':
    import networkx.readwrite.gexf as gf
    writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
    writer.add_graph(DG)
    scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
    from xml.etree.cElementTree import tostring
    print tostring(writer.xml)
else: #format=='json'
    jdata = json_graph.node_link_data(DG)
    scraperwiki.utils.httpresponseheader("Content-Type", "text/json")
    print json_graph.dumps(jdata)
#For some reason, templated view giving a string error? Line length?!
#print page_template % vars()