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

echo '[receive]' >> remote/.git/config
echo 'denyCurrentBranch = ignore' >> remote/.git/config

# Ordinary local workflow
cd local
echo rm -rf / > fungame.sh
git add fungame.sh
git commit -m 'Fun game'
git push ../remote/.git master
cd -

# There would also be a post-commit hook to
# check that things don't break and to handle
# race conditions.

chainsaw
