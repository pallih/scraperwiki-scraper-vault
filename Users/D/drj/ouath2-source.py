import scraperwiki
import oauth2
import os

print oauth2
directory = os.path.dirname(oauth2.__file__)
print "directory for oauth2 is", directory

for dir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.py'):
            print os.path.join(dir, file)