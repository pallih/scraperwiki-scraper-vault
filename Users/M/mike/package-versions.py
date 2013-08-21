import    subprocess
import    scraperwiki.datastore

dpkg = subprocess.Popen([ '/usr/bin/dpkg', '-l' ], stdout = subprocess.PIPE).communicate()[0]
for line in dpkg.splitlines() :
    if line.startswith('ii') :
        bits = [ b for b in line.split(' ') if b != '' ]
        scraperwiki.datastore.save (unique_keys = ['package'], data = { 'package' : bits[1], 'version' : bits[2] })
