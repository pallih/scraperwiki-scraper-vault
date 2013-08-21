import scraperwiki
import re
from collections import Counter

COUNCILLOR_LIST =["Rob Ford","Paul Ainslie","Maria Augimeri","Ana Bail","Michelle Berardinetti","Shelley Carroll","Raymond Cho","Josh Colle","Gary Crawford","Vincent Crisanti","Janet Davis","Glenn De Baeremaeker","Mike Del Grande","Frank Di Giorgio","Sarah Doucette","John Filion","Paula Fletcher","Doug Ford","Mary Fragedakis","Mark Grimes","Doug Holyday","Norman Kelly","Mike Layton","Chin Lee","Gloria Lindsay Luby","Giorgio Mammoliti","Josh Matlow","Pam McConnell","Mary-Margaret McMahon","Joe Mihevc","Peter Milczyn","Denzil Minnan-Wong","Ron Moeser","Frances Nunziata","Cesar Palacio","John Parker","James Pasternak","Gord Perks","Anthony Perruzza","Jaye Robinson","David Shiner","Karen Stintz","Michael Thompson","Adam Vaughan","Kristyn Wong-Tam"]

scraperwiki.sqlite.attach("lobbywatch_1") 

issueList = scraperwiki.sqlite.select("subjectMatter from lobbywatch_1.lobbying order by subjectMatter asc")

mainCounter = Counter()

# get all issues
for issue in issueList:
    stringList = re.split(';',issue['subjectMatter'])
    mainCounter.update(stringList)
        #print atom

csvString = "Name,Total Lobbied,"

#print headers for CSV
for letter, count in mainCounter.most_common(10):
    csvString = csvString + letter.replace(","," / ") + ","
print csvString

for councillor in COUNCILLOR_LIST:
  
    csvString2 = ""
    theTotalLobbied = scraperwiki.sqlite.select("count(councillor) as totalCount from lobbywatch_1.lobbying where councillor = '"+councillor+"'")
    csvString2 = csvString2 + councillor + "," + str(theTotalLobbied[0]['totalCount']) + ","

    # now get 10 most common for each councillor
    for letter, count in mainCounter.most_common(10):
        #print letter, count) 
 
        matterList = scraperwiki.sqlite.select("councillor, count(subjectMatter) as numberOfTimesLobbiedOnTopic from lobbywatch_1.lobbying where councillor like '%" + councillor + "%' and subjectMatter like '%" + letter + "%' group by councillor order by numberOfTimesLobbiedOnTopic desc")
     
        csvString2 = csvString2 + str(matterList[0]['numberOfTimesLobbiedOnTopic']) + "," 
    
    # row per councillor for CSV
    print csvString2 
