import scraperwiki

# Blank Python


"""
Cross-validation script
"""

#---------------------------------
POSFILES = []
for j in range(10):
    POSFILES.append('data%02i' %j)
#### In Python >= 2.*, we could write
## POSFILES = ['data%02i' %i for i in range(10)]
#---------------------------------

NEG = 'filetemplate'

import os, sys

for file in POSFILES:
    partdata = []
    #---------------------------------
    for f in POSFILES:
        if f!= file:
            partdata.append(f)
    #### In Python >= 2.*, we could write
##     partdata = [f for f in POSFILES if f != file]
    #---------------------------------
    print 'Dataset:', partdata
    cmd = "echo \"read_all(aff, [%s], '%s'). set(verbosity,1). induce.\" \
          | yap -l ${HOME}/src/Aleph/aleph.pl > th-0%s.out 2>&1" %(','.join(partdata)\
                                                                   , NEG, sys.argv[1]) 
    os.system(cmd)import scraperwiki

# Blank Python


"""
Cross-validation script
"""

#---------------------------------
POSFILES = []
for j in range(10):
    POSFILES.append('data%02i' %j)
#### In Python >= 2.*, we could write
## POSFILES = ['data%02i' %i for i in range(10)]
#---------------------------------

NEG = 'filetemplate'

import os, sys

for file in POSFILES:
    partdata = []
    #---------------------------------
    for f in POSFILES:
        if f!= file:
            partdata.append(f)
    #### In Python >= 2.*, we could write
##     partdata = [f for f in POSFILES if f != file]
    #---------------------------------
    print 'Dataset:', partdata
    cmd = "echo \"read_all(aff, [%s], '%s'). set(verbosity,1). induce.\" \
          | yap -l ${HOME}/src/Aleph/aleph.pl > th-0%s.out 2>&1" %(','.join(partdata)\
                                                                   , NEG, sys.argv[1]) 
    os.system(cmd)