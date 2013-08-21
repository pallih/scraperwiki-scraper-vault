# Datastore error
 
import scraperwiki

record = { "fish" : "pike", "beast" : "horse" }


scraperwiki.sqlite.save(["fish"], record)
record["beast"] = "llama"
scraperwiki.sqlite.save(["fish"], record)   # There should be no horses in the datastore after this is called
    
