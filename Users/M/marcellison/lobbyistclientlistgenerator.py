import scraperwiki
import re
from collections import Counter

scraperwiki.sqlite.attach("lobbywatch_1") 

clientList = scraperwiki.sqlite.select("client, count(client) from lobbywatch_1.lobbying group by client")

theString = ""

for theClient in clientList:
    theString = theString + "<option value='" + theClient['client'] + "'>" + theClient['client'] + "</option>" + "\n"

print theString

import scraperwiki
import re
from collections import Counter

scraperwiki.sqlite.attach("lobbywatch_1") 

clientList = scraperwiki.sqlite.select("client, count(client) from lobbywatch_1.lobbying group by client")

theString = ""

for theClient in clientList:
    theString = theString + "<option value='" + theClient['client'] + "'>" + theClient['client'] + "</option>" + "\n"

print theString

import scraperwiki
import re
from collections import Counter

scraperwiki.sqlite.attach("lobbywatch_1") 

clientList = scraperwiki.sqlite.select("client, count(client) from lobbywatch_1.lobbying group by client")

theString = ""

for theClient in clientList:
    theString = theString + "<option value='" + theClient['client'] + "'>" + theClient['client'] + "</option>" + "\n"

print theString

