import scraperwiki

# Blank Python

data=[{'a':'aardvark','b':'bear'},
      {'a':'aardvark','b':'bear'},
      {'a':'aardvark','b':'bees'}]

scraperwiki.sqlite.save(unique_keys=['a','b'],data=data)
