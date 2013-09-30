#puts 'Content-Type: text/plain'
#puts
require 'scraperwiki'
ScraperWiki::httpresponseheader('Content-Type', 'text/plain')

puts <<chainsaw
#!/bin/bash
for d in local remote; do
  mkdir $d
  cd $d
  git init
  cd -
done

# This hack on the remote makese the master not checked out.
# This could be done less disgustingly.
echo '[receive]\n\tdenyCurrentBranch = ignore'

# Ordinary local workflow
cd local
echo rm -rf / > fungame.sh
git add fungame.sh
git commit -m 'Fun game'
git push ../remote/.git master
cd -

# This part would be a post-receive hook, also done less hack-ed-ly.
cd remote
git checkout master
git symbolic-ref HEAD refs/heads/___
chainsaw
#puts 'Content-Type: text/plain'
#puts
require 'scraperwiki'
ScraperWiki::httpresponseheader('Content-Type', 'text/plain')

puts <<chainsaw
#!/bin/bash
for d in local remote; do
  mkdir $d
  cd $d
  git init
  cd -
done

# This hack on the remote makese the master not checked out.
# This could be done less disgustingly.
echo '[receive]\n\tdenyCurrentBranch = ignore'

# Ordinary local workflow
cd local
echo rm -rf / > fungame.sh
git add fungame.sh
git commit -m 'Fun game'
git push ../remote/.git master
cd -

# This part would be a post-receive hook, also done less hack-ed-ly.
cd remote
git checkout master
git symbolic-ref HEAD refs/heads/___
chainsaw
