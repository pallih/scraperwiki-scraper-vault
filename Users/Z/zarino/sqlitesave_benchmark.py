import scraperwiki
import datetime

loops = 500

def row_by_row_verbose():
    for i in range(0,loops):
        scraperwiki.sqlite.save(['id'], {'id': i, 'time': datetime.datetime.now()}, 'row_by_row_verbose')

def row_by_row_non_verbose():
    for i in range(0,loops):
        scraperwiki.sqlite.save(['id'], {'id': i, 'time': datetime.datetime.now()}, 'row_by_row_non_verbose', verbose=0)

def list_verbose():
    data = []
    for i in range(0,loops):
        data.append({'id': i, 'time': datetime.datetime.now()})
    scraperwiki.sqlite.save(['id'], data, 'list_verbose')

def list_non_verbose():
    data = []
    for i in range(0,loops):
        data.append({'id': i, 'time': datetime.datetime.now()})
    scraperwiki.sqlite.save(['id'], data, 'list_non_verbose', verbose=0)

start = datetime.datetime.now()
row_by_row_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('row_by_row_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'row_by_row_verbose: %s.%s' % (diff.seconds, diff.microseconds)

start = datetime.datetime.now()
row_by_row_non_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('row_by_row_non_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'row_by_row_non_verbose: %s.%s' % (diff.seconds, diff.microseconds)

start = datetime.datetime.now()
list_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('list_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'list_verbose: %s.%s' % (diff.seconds, diff.microseconds)

start = datetime.datetime.now()
list_non_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('list_non_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'list_non_verbose: %s.%s' % (diff.seconds, diff.microseconds)





import scraperwiki
import datetime

loops = 500

def row_by_row_verbose():
    for i in range(0,loops):
        scraperwiki.sqlite.save(['id'], {'id': i, 'time': datetime.datetime.now()}, 'row_by_row_verbose')

def row_by_row_non_verbose():
    for i in range(0,loops):
        scraperwiki.sqlite.save(['id'], {'id': i, 'time': datetime.datetime.now()}, 'row_by_row_non_verbose', verbose=0)

def list_verbose():
    data = []
    for i in range(0,loops):
        data.append({'id': i, 'time': datetime.datetime.now()})
    scraperwiki.sqlite.save(['id'], data, 'list_verbose')

def list_non_verbose():
    data = []
    for i in range(0,loops):
        data.append({'id': i, 'time': datetime.datetime.now()})
    scraperwiki.sqlite.save(['id'], data, 'list_non_verbose', verbose=0)

start = datetime.datetime.now()
row_by_row_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('row_by_row_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'row_by_row_verbose: %s.%s' % (diff.seconds, diff.microseconds)

start = datetime.datetime.now()
row_by_row_non_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('row_by_row_non_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'row_by_row_non_verbose: %s.%s' % (diff.seconds, diff.microseconds)

start = datetime.datetime.now()
list_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('list_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'list_verbose: %s.%s' % (diff.seconds, diff.microseconds)

start = datetime.datetime.now()
list_non_verbose()
stop = datetime.datetime.now()
diff = stop - start
scraperwiki.sqlite.save_var('list_non_verbose', '%s.%s' % (diff.seconds, diff.microseconds))
print 'list_non_verbose: %s.%s' % (diff.seconds, diff.microseconds)





