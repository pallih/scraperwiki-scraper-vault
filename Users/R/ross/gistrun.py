# Hacky way of running gists

import os,cgi, sys
import json
import requests
import subprocess
import scraperwiki

scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')

compiled = {
    "C": ["gcc", "{filename}", "-o", "/tmp/{id}/a.out"],
    "C++": ["g++", "{filename}", "-o", "/tmp/{id}/a.out"],
}

langs = {
    "Python": ["python", "{filename}"],
    "Ruby": ["ruby", "{filename}"],
    "Perl": ["perl", "{filename}"],
    "Shell": ["bash", "{filename}"],
    "Tcl": ["tclsh", "{filename}"],
    "R": ["Rscript", "{filename}"],
    "C": ["/tmp/{id}/a.out"],
    "C++": ["/tmp/{id}/a.out"],
}

params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))


def save_file(name, url, idnum):
    """ Fetch the gist and save it to disk """
    r = requests.get(url, verify=False)    
    p = os.path.join('/tmp/', str(idnum))
    if not os.path.exists(p):
        os.mkdir(p)

    with open(os.path.join(p,name), "w+") as f:
        f.write(r.content)
    return os.path.join(p, name), r.content


if not 'id' in params:
    print "No id specified"
    sys.exit(0)

# Get info about the gist
r = requests.get('https://api.github.com/gists/%s' % params['id'], verify=False)
if r.status_code != 200:
    print "Failed to get GIST ({r})".format(r=r.status_code)
    sys.exit(0)

# Load the gist json
info = json.loads(r.content)
files = info['files']

# For each file 
for name,data in files.iteritems():
    url = data['raw_url']
    lang = data['language']

    if lang not in langs:
        if not lang:
            print "Sorry, unknown filetypes are not supported".format(l=lang)
        else:
            print "Sorry, {l} is not supported".format(l=lang)
        sys.exit(0)

    p,c  = save_file(name, url, params['id'])    

    # Check if it is a compiled language and compile it.    
    if lang in compiled:
        cmd = compiled[lang][:]
        for i in range(0, len(cmd)):
            cmd[i] = cmd[i].format(filename=p, id=params['id'])
        subprocess.call(cmd)

    # Do some replacement on the cmd to make sure we point at the file
    cmd = langs[lang][:]
    for i in range(0, len(cmd)):
        cmd[i] = cmd[i].format(filename=p, id=params['id'])

    print '-' * 30, "Code ({l})".format(l=lang)
    print "%s\r\n" % c
    print '-' * 30, "Output"

    # Run, or crash, or something.
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, bufsize=0, universal_newlines=True)
    line = p.stdout.readline()
    while line:
        print line
        line = p.stdout.readline()


# Hacky way of running gists

import os,cgi, sys
import json
import requests
import subprocess
import scraperwiki

scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')

compiled = {
    "C": ["gcc", "{filename}", "-o", "/tmp/{id}/a.out"],
    "C++": ["g++", "{filename}", "-o", "/tmp/{id}/a.out"],
}

langs = {
    "Python": ["python", "{filename}"],
    "Ruby": ["ruby", "{filename}"],
    "Perl": ["perl", "{filename}"],
    "Shell": ["bash", "{filename}"],
    "Tcl": ["tclsh", "{filename}"],
    "R": ["Rscript", "{filename}"],
    "C": ["/tmp/{id}/a.out"],
    "C++": ["/tmp/{id}/a.out"],
}

params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))


def save_file(name, url, idnum):
    """ Fetch the gist and save it to disk """
    r = requests.get(url, verify=False)    
    p = os.path.join('/tmp/', str(idnum))
    if not os.path.exists(p):
        os.mkdir(p)

    with open(os.path.join(p,name), "w+") as f:
        f.write(r.content)
    return os.path.join(p, name), r.content


if not 'id' in params:
    print "No id specified"
    sys.exit(0)

# Get info about the gist
r = requests.get('https://api.github.com/gists/%s' % params['id'], verify=False)
if r.status_code != 200:
    print "Failed to get GIST ({r})".format(r=r.status_code)
    sys.exit(0)

# Load the gist json
info = json.loads(r.content)
files = info['files']

# For each file 
for name,data in files.iteritems():
    url = data['raw_url']
    lang = data['language']

    if lang not in langs:
        if not lang:
            print "Sorry, unknown filetypes are not supported".format(l=lang)
        else:
            print "Sorry, {l} is not supported".format(l=lang)
        sys.exit(0)

    p,c  = save_file(name, url, params['id'])    

    # Check if it is a compiled language and compile it.    
    if lang in compiled:
        cmd = compiled[lang][:]
        for i in range(0, len(cmd)):
            cmd[i] = cmd[i].format(filename=p, id=params['id'])
        subprocess.call(cmd)

    # Do some replacement on the cmd to make sure we point at the file
    cmd = langs[lang][:]
    for i in range(0, len(cmd)):
        cmd[i] = cmd[i].format(filename=p, id=params['id'])

    print '-' * 30, "Code ({l})".format(l=lang)
    print "%s\r\n" % c
    print '-' * 30, "Output"

    # Run, or crash, or something.
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, bufsize=0, universal_newlines=True)
    line = p.stdout.readline()
    while line:
        print line
        line = p.stdout.readline()


# Hacky way of running gists

import os,cgi, sys
import json
import requests
import subprocess
import scraperwiki

scraperwiki.utils.httpresponseheader('Content-Type', 'text/plain')

compiled = {
    "C": ["gcc", "{filename}", "-o", "/tmp/{id}/a.out"],
    "C++": ["g++", "{filename}", "-o", "/tmp/{id}/a.out"],
}

langs = {
    "Python": ["python", "{filename}"],
    "Ruby": ["ruby", "{filename}"],
    "Perl": ["perl", "{filename}"],
    "Shell": ["bash", "{filename}"],
    "Tcl": ["tclsh", "{filename}"],
    "R": ["Rscript", "{filename}"],
    "C": ["/tmp/{id}/a.out"],
    "C++": ["/tmp/{id}/a.out"],
}

params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))


def save_file(name, url, idnum):
    """ Fetch the gist and save it to disk """
    r = requests.get(url, verify=False)    
    p = os.path.join('/tmp/', str(idnum))
    if not os.path.exists(p):
        os.mkdir(p)

    with open(os.path.join(p,name), "w+") as f:
        f.write(r.content)
    return os.path.join(p, name), r.content


if not 'id' in params:
    print "No id specified"
    sys.exit(0)

# Get info about the gist
r = requests.get('https://api.github.com/gists/%s' % params['id'], verify=False)
if r.status_code != 200:
    print "Failed to get GIST ({r})".format(r=r.status_code)
    sys.exit(0)

# Load the gist json
info = json.loads(r.content)
files = info['files']

# For each file 
for name,data in files.iteritems():
    url = data['raw_url']
    lang = data['language']

    if lang not in langs:
        if not lang:
            print "Sorry, unknown filetypes are not supported".format(l=lang)
        else:
            print "Sorry, {l} is not supported".format(l=lang)
        sys.exit(0)

    p,c  = save_file(name, url, params['id'])    

    # Check if it is a compiled language and compile it.    
    if lang in compiled:
        cmd = compiled[lang][:]
        for i in range(0, len(cmd)):
            cmd[i] = cmd[i].format(filename=p, id=params['id'])
        subprocess.call(cmd)

    # Do some replacement on the cmd to make sure we point at the file
    cmd = langs[lang][:]
    for i in range(0, len(cmd)):
        cmd[i] = cmd[i].format(filename=p, id=params['id'])

    print '-' * 30, "Code ({l})".format(l=lang)
    print "%s\r\n" % c
    print '-' * 30, "Output"

    # Run, or crash, or something.
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, bufsize=0, universal_newlines=True)
    line = p.stdout.readline()
    while line:
        print line
        line = p.stdout.readline()


