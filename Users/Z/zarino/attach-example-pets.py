import scraperwiki

def setup():
    pets = [{ 'owner': 1, 'name': 'Rover', 'species': 'dog' }, 
            { 'owner': 2, 'name': 'Tiddles', 'species': 'cat' },
            { 'owner': 2, 'name': 'Polly', 'species': 'parrot' }, 
            { 'owner': 4, 'name': 'Cyril', 'species': 'snake' }]
    scraperwiki.sqlite.save(['name'], pets)

# setup()

scraperwiki.sqlite.attach('attach-example-people')

print "all the owners:"
print scraperwiki.sqlite.select('* from `attach-example-people`.swdata')

print "all the pets:"
print scraperwiki.sqlite.select('* from swdata')

print "all the owners and their pets (or None if they don't own any):"
print scraperwiki.sqlite.select('`attach-example-people`.swdata.first_name, `attach-example-people`.swdata.last_name, name, species from swdata left join `attach-example-people`.swdata on `attach-example-people`.swdata.id=owner')

print "all the pets and their owners (or None if they don't have owners):"
print scraperwiki.sqlite.select('name, species, `attach-example-people`.swdata.first_name, `attach-example-people`.swdata.last_name from swdata left join `attach-example-people`.swdata on `attach-example-people`.swdata.id=swdata.owner')