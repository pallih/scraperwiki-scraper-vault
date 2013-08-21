
# Blank Python

import scraperwiki
wikipedia_utils = scraperwiki.swimport("wikipedia_utils")

lcavepages = wikipedia_utils.GetWikipediaCategoryRecurse("Caves_of_the_United_Kingdom")
scraperwiki.sqlite.save(["title"], lcavepages, "cavepages")
