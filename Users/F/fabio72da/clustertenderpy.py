import scraperwiki, random, math
import numpy as np
import scipy as sp
from scipy import spatial
from scipy import cluster


scraperwiki.sqlite.attach("geotenderpy", 'geotenders')
tenders=scraperwiki.sqlite.select("distinct * from geotenders.swdata limit 100")


#idtenders=[ t['id'] for t in tenders]
geotenders=[ [float(t['lat']),0.,0.,0.,float(t['lon']),0.,0.,0.] for t in tenders]

print geotenders
print "len %d" % len(geotenders)

#idarray = np.array(idtenders)
geoarray = np.array(geotenders)

print "geoarray:"
print geoarray 

"""
dists=spatial.distance.pdist(geoarray,'euclidean')

print dists

dists_square=spatial.distance.squareform(dists)

hcluster=cluster.hierarchy.linkage(dists_square,method='single', metric='euclidean')

print "hcluster:"
print hcluster

hcluster_ord=cluster.hierarchy.leaves_list(hcluster)
geoarray_ord=geoarray[hcluster_ord,:]

idarray_ord=idarray[hcluster_ord,:]

print idarray_ord
print geoarray_ord
"""

##############################################


#x=np.array([[0,1,4],[0,0,3],[0,0,0]])

#x=np.array([[2.5,2,0.5,1],[2.5,0,1,1],[7,1,0.5,1],[8,0,1,1],[8.5,0,0.5,0.5],[4.5,0,1,1]])

#x=np.array([[0,0,1,1],[0,0,3,3]])

#print x
#print "x size: "+str(x.size)+" | shape: " + str(x.shape)

def DiffFuzzy(a,b):
    gm=float(2*(a[0]-b[0])-(a[1]-b[1]))
    gp=float(2*(a[0]-b[0])+(a[1]-b[1]))
    return math.sqrt(0.25 * (pow(gm,2)+pow(gp,2)+pow(gm-(a[2]-b[2]),2) + pow(gp+(a[3]-b[3]),2) ))

x=geoarray

distMatrix=np.zeros((x.shape[0],x.shape[0]))


for i in range(x.shape[0]):
    for j in range(x.shape[0]):
        distMatrix[i,j]=DiffFuzzy(x[i,:4],x[j,:4])+DiffFuzzy(x[i,4:],x[j,4:])

print "distMatrix"
print distMatrix


#methods=['single','complete','average','ward']
methods=['single']

for method in methods:
    print "metodo: %s" % method
    linkageMatrix=cluster.hierarchy.linkage(distMatrix,method=method)
    print "linkageMatrix"
    print linkageMatrix
    inconsistencyMatrix=cluster.hierarchy.inconsistent(linkageMatrix,2) #linkageMatrix.shape[0]
    print "inconsistencyMatrix"
    print inconsistencyMatrix

#inconsistencyMatrix[:,3]+=0.0000001
print "corrected inconsistencyMatrix"
print inconsistencyMatrix

#scraperwiki.sqlite.save(["linkageMatrix"], [{"linkageMatrix":linkageMatrix}])




flat_cluster=cluster.hierarchy.fcluster(linkageMatrix, 1.0, criterion='inconsistent', depth=10, R=inconsistencyMatrix)


print "flat_cluster: "+str(len(flat_cluster))+" - n. clusters: "+str(flat_cluster.max())
print flat_cluster

print geoarray.shape
print flat_cluster.shape

#_ = np.append(flat_cluster, geoarray , 1)
_ = np.hstack([flat_cluster[np.newaxis].T, geoarray])


print "::::"
print _

all=[]
#calcolo centroide dei cluster
for i in range(1,flat_cluster.max()+1):
    all.append(  {'id': 'cluster'+str(i-1),'lat': float(_[_[:,0] == i].sum(axis=0)[1]), 'lon': float(_[_[:,0] == i].sum(axis=0)[5])} )
for i,t in enumerate(tenders):
    #i+=1
    #items_dict['item'+str(i)] = (float(t['lat']),float(t['lon']))
    all.append( {'id': 'item'+str(i),'lat': float(t['lat']), 'lon': float(t['lon'])} )


print all

scraperwiki.sqlite.save(['id'], all)

#centroids   np.where(for i in range(flat_cluster.max())

#cluster_tree=cluster.hierarchy.to_tree(linkageMatrix)
#dendrogram=cluster.hierarchy.dendrogram(linkageMatrix)
#scraperwiki.sqlite.save(['ivl','icoord'], dendrogram)import scraperwiki, random, math
import numpy as np
import scipy as sp
from scipy import spatial
from scipy import cluster


scraperwiki.sqlite.attach("geotenderpy", 'geotenders')
tenders=scraperwiki.sqlite.select("distinct * from geotenders.swdata limit 100")


#idtenders=[ t['id'] for t in tenders]
geotenders=[ [float(t['lat']),0.,0.,0.,float(t['lon']),0.,0.,0.] for t in tenders]

print geotenders
print "len %d" % len(geotenders)

#idarray = np.array(idtenders)
geoarray = np.array(geotenders)

print "geoarray:"
print geoarray 

"""
dists=spatial.distance.pdist(geoarray,'euclidean')

print dists

dists_square=spatial.distance.squareform(dists)

hcluster=cluster.hierarchy.linkage(dists_square,method='single', metric='euclidean')

print "hcluster:"
print hcluster

hcluster_ord=cluster.hierarchy.leaves_list(hcluster)
geoarray_ord=geoarray[hcluster_ord,:]

idarray_ord=idarray[hcluster_ord,:]

print idarray_ord
print geoarray_ord
"""

##############################################


#x=np.array([[0,1,4],[0,0,3],[0,0,0]])

#x=np.array([[2.5,2,0.5,1],[2.5,0,1,1],[7,1,0.5,1],[8,0,1,1],[8.5,0,0.5,0.5],[4.5,0,1,1]])

#x=np.array([[0,0,1,1],[0,0,3,3]])

#print x
#print "x size: "+str(x.size)+" | shape: " + str(x.shape)

def DiffFuzzy(a,b):
    gm=float(2*(a[0]-b[0])-(a[1]-b[1]))
    gp=float(2*(a[0]-b[0])+(a[1]-b[1]))
    return math.sqrt(0.25 * (pow(gm,2)+pow(gp,2)+pow(gm-(a[2]-b[2]),2) + pow(gp+(a[3]-b[3]),2) ))

x=geoarray

distMatrix=np.zeros((x.shape[0],x.shape[0]))


for i in range(x.shape[0]):
    for j in range(x.shape[0]):
        distMatrix[i,j]=DiffFuzzy(x[i,:4],x[j,:4])+DiffFuzzy(x[i,4:],x[j,4:])

print "distMatrix"
print distMatrix


#methods=['single','complete','average','ward']
methods=['single']

for method in methods:
    print "metodo: %s" % method
    linkageMatrix=cluster.hierarchy.linkage(distMatrix,method=method)
    print "linkageMatrix"
    print linkageMatrix
    inconsistencyMatrix=cluster.hierarchy.inconsistent(linkageMatrix,2) #linkageMatrix.shape[0]
    print "inconsistencyMatrix"
    print inconsistencyMatrix

#inconsistencyMatrix[:,3]+=0.0000001
print "corrected inconsistencyMatrix"
print inconsistencyMatrix

#scraperwiki.sqlite.save(["linkageMatrix"], [{"linkageMatrix":linkageMatrix}])




flat_cluster=cluster.hierarchy.fcluster(linkageMatrix, 1.0, criterion='inconsistent', depth=10, R=inconsistencyMatrix)


print "flat_cluster: "+str(len(flat_cluster))+" - n. clusters: "+str(flat_cluster.max())
print flat_cluster

print geoarray.shape
print flat_cluster.shape

#_ = np.append(flat_cluster, geoarray , 1)
_ = np.hstack([flat_cluster[np.newaxis].T, geoarray])


print "::::"
print _

all=[]
#calcolo centroide dei cluster
for i in range(1,flat_cluster.max()+1):
    all.append(  {'id': 'cluster'+str(i-1),'lat': float(_[_[:,0] == i].sum(axis=0)[1]), 'lon': float(_[_[:,0] == i].sum(axis=0)[5])} )
for i,t in enumerate(tenders):
    #i+=1
    #items_dict['item'+str(i)] = (float(t['lat']),float(t['lon']))
    all.append( {'id': 'item'+str(i),'lat': float(t['lat']), 'lon': float(t['lon'])} )


print all

scraperwiki.sqlite.save(['id'], all)

#centroids   np.where(for i in range(flat_cluster.max())

#cluster_tree=cluster.hierarchy.to_tree(linkageMatrix)
#dendrogram=cluster.hierarchy.dendrogram(linkageMatrix)
#scraperwiki.sqlite.save(['ivl','icoord'], dendrogram)