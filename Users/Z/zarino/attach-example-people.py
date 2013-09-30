import scraperwiki

def setup():
    people = [{ 'id': 1, 'first_name': 'Alice', 'last_name': 'Green' }, 
              { 'id': 2, 'first_name': 'Bob', 'last_name': 'Brown' }, 
              { 'id': 3, 'first_name': 'Carol', 'last_name': 'Black' }]
    scraperwiki.sqlite.save(['id'], people)

# setup()

scraperwiki.sqlite.attach('attach-example-pets')

print "all the owners:"
print scraperwiki.sqlite.select('* from swdata')

print "all the pets:"
print scraperwiki.sqlite.select('* from `attach-example-pets`.swdata')

print "all the owners and their pets (or None if they don't own any):"
print scraperwiki.sqlite.select('first_name, last_name, `attach-example-pets`.swdata.name, `attach-example-pets`.swdata.species from swdata left join `attach-example-pets`.swdata on swdata.id=`attach-example-pets`.swdata.owner')

print "all the pets and their owners (or None if they don't have owners):"
print scraperwiki.sqlite.select('`attach-example-pets`.swdata.name, `attach-example-pets`.swdata.species, first_name, last_name from `attach-example-pets`.swdata left join swdata on `attach-example-pets`.swdata.owner=swdata.id')import scraperwiki

def setup():
    people = [{ 'id': 1, 'first_name': 'Alice', 'last_name': 'Green' }, 
              { 'id': 2, 'first_name': 'Bob', 'last_name': 'Brown' }, 
              { 'id': 3, 'first_name': 'Carol', 'last_name': 'Black' }]
    scraperwiki.sqlite.save(['id'], people)

# setup()

scraperwiki.sqlite.attach('attach-example-pets')

print "all the owners:"
print scraperwiki.sqlite.select('* from swdata')

print "all the pets:"
print scraperwiki.sqlite.select('* from `attach-example-pets`.swdata')

print "all the owners and their pets (or None if they don't own any):"
print scraperwiki.sqlite.select('first_name, last_name, `attach-example-pets`.swdata.name, `attach-example-pets`.swdata.species from swdata left join `attach-example-pets`.swdata on swdata.id=`attach-example-pets`.swdata.owner')

print "all the pets and their owners (or None if they don't have owners):"
print scraperwiki.sqlite.select('`attach-example-pets`.swdata.name, `attach-example-pets`.swdata.species, first_name, last_name from `attach-example-pets`.swdata left join swdata on `attach-example-pets`.swdata.owner=swdata.id')