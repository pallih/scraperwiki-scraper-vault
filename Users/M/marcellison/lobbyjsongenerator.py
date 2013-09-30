import scraperwiki
import json

#COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

COUNCILLOR_DICT = {}
CLIENT_DICT = {}

MAIN_JSON_STRING = "{\"maxArtistSongs\":100,\"links\":["

MAIN_JSON_STRING2 = "],\"maxGenreSongs\":671,\"maxGenrePlays\":9000,\"maxArtistPlays\":500,\"nodes\":["

scraperwiki.sqlite.attach("lobbywatch_1") 

councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by councillor order by councillor asc")


#councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying  group by councillor order by numberOfTimesLobbied desc")

#print councillorList

clientList = scraperwiki.sqlite.select("client, count(client) as numberOfRelationships, councillor from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by client order by client asc")

for result in councillorList:
#    print result["client"]
    COUNCILLOR_DICT[result["councillor"]] = result["numberOfTimesLobbied"]
    #print len(CLIENT_DICT)
    councillorNode = "{\"count\":" + str(result["numberOfTimesLobbied"]) + ",\"name\":\"" + str(result["councillor"]) + "\",\"type\":\"a\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + councillorNode

for result in clientList:
    CLIENT_DICT[result["client"]] = result["numberOfRelationships"]
    #print len(CLIENT_DICT)
    clientNode = "{\"count\":" + str(result["numberOfRelationships"]) + ",\"name\":\"" + str(result["client"]).lstrip() + "\",\"type\":\"g\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + clientNode

#now generate nodes for councillor and clients
#print MAIN_JSON_STRING2

relationships = scraperwiki.sqlite.select("distinct councillor,client from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') order by councillor asc")

for relation in relationships:
    
    #print str(relation)
    #print str(COUNCILLOR_DICT.keys().index(relation["councillor"]))
    print str(relation["client"]) + " " + str(CLIENT_DICT.keys().index(relation["client"]))
    
    clientIndex = CLIENT_DICT.keys().index(relation["client"])
    link = "{\"source\":" + str(COUNCILLOR_DICT.keys().index(relation["councillor"])) + ",\"target\":" + str(clientIndex + 5) + "},"
    MAIN_JSON_STRING = MAIN_JSON_STRING + link


#print str(CLIENT_DICT)
print MAIN_JSON_STRING + MAIN_JSON_STRING2 + "]}"
import scraperwiki
import json

#COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

COUNCILLOR_DICT = {}
CLIENT_DICT = {}

MAIN_JSON_STRING = "{\"maxArtistSongs\":100,\"links\":["

MAIN_JSON_STRING2 = "],\"maxGenreSongs\":671,\"maxGenrePlays\":9000,\"maxArtistPlays\":500,\"nodes\":["

scraperwiki.sqlite.attach("lobbywatch_1") 

councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by councillor order by councillor asc")


#councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying  group by councillor order by numberOfTimesLobbied desc")

#print councillorList

clientList = scraperwiki.sqlite.select("client, count(client) as numberOfRelationships, councillor from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by client order by client asc")

for result in councillorList:
#    print result["client"]
    COUNCILLOR_DICT[result["councillor"]] = result["numberOfTimesLobbied"]
    #print len(CLIENT_DICT)
    councillorNode = "{\"count\":" + str(result["numberOfTimesLobbied"]) + ",\"name\":\"" + str(result["councillor"]) + "\",\"type\":\"a\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + councillorNode

for result in clientList:
    CLIENT_DICT[result["client"]] = result["numberOfRelationships"]
    #print len(CLIENT_DICT)
    clientNode = "{\"count\":" + str(result["numberOfRelationships"]) + ",\"name\":\"" + str(result["client"]).lstrip() + "\",\"type\":\"g\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + clientNode

#now generate nodes for councillor and clients
#print MAIN_JSON_STRING2

relationships = scraperwiki.sqlite.select("distinct councillor,client from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') order by councillor asc")

for relation in relationships:
    
    #print str(relation)
    #print str(COUNCILLOR_DICT.keys().index(relation["councillor"]))
    print str(relation["client"]) + " " + str(CLIENT_DICT.keys().index(relation["client"]))
    
    clientIndex = CLIENT_DICT.keys().index(relation["client"])
    link = "{\"source\":" + str(COUNCILLOR_DICT.keys().index(relation["councillor"])) + ",\"target\":" + str(clientIndex + 5) + "},"
    MAIN_JSON_STRING = MAIN_JSON_STRING + link


#print str(CLIENT_DICT)
print MAIN_JSON_STRING + MAIN_JSON_STRING2 + "]}"
import scraperwiki
import json

#COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

COUNCILLOR_DICT = {}
CLIENT_DICT = {}

MAIN_JSON_STRING = "{\"maxArtistSongs\":100,\"links\":["

MAIN_JSON_STRING2 = "],\"maxGenreSongs\":671,\"maxGenrePlays\":9000,\"maxArtistPlays\":500,\"nodes\":["

scraperwiki.sqlite.attach("lobbywatch_1") 

councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by councillor order by councillor asc")


#councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying  group by councillor order by numberOfTimesLobbied desc")

#print councillorList

clientList = scraperwiki.sqlite.select("client, count(client) as numberOfRelationships, councillor from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by client order by client asc")

for result in councillorList:
#    print result["client"]
    COUNCILLOR_DICT[result["councillor"]] = result["numberOfTimesLobbied"]
    #print len(CLIENT_DICT)
    councillorNode = "{\"count\":" + str(result["numberOfTimesLobbied"]) + ",\"name\":\"" + str(result["councillor"]) + "\",\"type\":\"a\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + councillorNode

for result in clientList:
    CLIENT_DICT[result["client"]] = result["numberOfRelationships"]
    #print len(CLIENT_DICT)
    clientNode = "{\"count\":" + str(result["numberOfRelationships"]) + ",\"name\":\"" + str(result["client"]).lstrip() + "\",\"type\":\"g\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + clientNode

#now generate nodes for councillor and clients
#print MAIN_JSON_STRING2

relationships = scraperwiki.sqlite.select("distinct councillor,client from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') order by councillor asc")

for relation in relationships:
    
    #print str(relation)
    #print str(COUNCILLOR_DICT.keys().index(relation["councillor"]))
    print str(relation["client"]) + " " + str(CLIENT_DICT.keys().index(relation["client"]))
    
    clientIndex = CLIENT_DICT.keys().index(relation["client"])
    link = "{\"source\":" + str(COUNCILLOR_DICT.keys().index(relation["councillor"])) + ",\"target\":" + str(clientIndex + 5) + "},"
    MAIN_JSON_STRING = MAIN_JSON_STRING + link


#print str(CLIENT_DICT)
print MAIN_JSON_STRING + MAIN_JSON_STRING2 + "]}"
import scraperwiki
import json

#COUNCILLOR_LIST =["Rob+Ford","Paul+Ainslie","Maria+Augimeri","Ana+Bail","Michelle+Berardinetti","Shelley+Carroll","Raymond+Cho","Josh+Colle","Gary+Crawford","Vincent+Crisanti","Janet+Davis","Glenn+De+Baeremaeker","Mike+Del+Grande","Frank+Di+Giorgio","Sarah+Doucette","John+Filion","Paula+Fletcher","Doug+Ford","Mary+Fragedakis","Mark+Grimes","Doug+Holyday","Norman+Kelly","Mike+Layton","Chin+Lee","Gloria+Lindsay+Luby","Giorgio+Mammoliti","Josh+Matlow","Pam+McConnell","Mary-Margaret+McMahon","Joe+Mihevc","Peter+Milczyn","Denzil+Minnan-Wong","Ron+Moeser","Frances+Nunziata","Cesar+Palacio","John+Parker","James+Pasternak","Gord+Perks","Anthony+Perruzza","Jaye+Robinson","David+Shiner","Karen+Stintz","Michael+Thompson","Adam+Vaughan","Kristyn+Wong-Tam"]

COUNCILLOR_DICT = {}
CLIENT_DICT = {}

MAIN_JSON_STRING = "{\"maxArtistSongs\":100,\"links\":["

MAIN_JSON_STRING2 = "],\"maxGenreSongs\":671,\"maxGenrePlays\":9000,\"maxArtistPlays\":500,\"nodes\":["

scraperwiki.sqlite.attach("lobbywatch_1") 

councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by councillor order by councillor asc")


#councillorList = scraperwiki.sqlite.select("councillor, count(councillor) as numberOfTimesLobbied from lobbywatch_1.lobbying  group by councillor order by numberOfTimesLobbied desc")

#print councillorList

clientList = scraperwiki.sqlite.select("client, count(client) as numberOfRelationships, councillor from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') group by client order by client asc")

for result in councillorList:
#    print result["client"]
    COUNCILLOR_DICT[result["councillor"]] = result["numberOfTimesLobbied"]
    #print len(CLIENT_DICT)
    councillorNode = "{\"count\":" + str(result["numberOfTimesLobbied"]) + ",\"name\":\"" + str(result["councillor"]) + "\",\"type\":\"a\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + councillorNode

for result in clientList:
    CLIENT_DICT[result["client"]] = result["numberOfRelationships"]
    #print len(CLIENT_DICT)
    clientNode = "{\"count\":" + str(result["numberOfRelationships"]) + ",\"name\":\"" + str(result["client"]).lstrip() + "\",\"type\":\"g\"},"
    MAIN_JSON_STRING2 = MAIN_JSON_STRING2 + clientNode

#now generate nodes for councillor and clients
#print MAIN_JSON_STRING2

relationships = scraperwiki.sqlite.select("distinct councillor,client from lobbywatch_1.lobbying where councillor in ('Peter Milczyn','Adam Vaughan','Karen Stintz','John Parker','Denzil Minnan-Wong') order by councillor asc")

for relation in relationships:
    
    #print str(relation)
    #print str(COUNCILLOR_DICT.keys().index(relation["councillor"]))
    print str(relation["client"]) + " " + str(CLIENT_DICT.keys().index(relation["client"]))
    
    clientIndex = CLIENT_DICT.keys().index(relation["client"])
    link = "{\"source\":" + str(COUNCILLOR_DICT.keys().index(relation["councillor"])) + ",\"target\":" + str(clientIndex + 5) + "},"
    MAIN_JSON_STRING = MAIN_JSON_STRING + link


#print str(CLIENT_DICT)
print MAIN_JSON_STRING + MAIN_JSON_STRING2 + "]}"
