'''
I figure out how different types are saved to the database.
'''
import datetime
from scraperwiki.sqlite import save, save_var, execute, commit

execute('drop table if exists swdata')
execute('drop table if exists swvariables')
execute('drop table if exists complex')
commit()

for t in {dict, list, set, str, unicode, bool, int, float, long}:
    save_var(str(t), t())
    save([], {str(t).replace("'","").replace(' ', '').replace('<type', '').replace('>', ''): t()})

save([], {
    u'list': [u'thing'],
    u'dict': {u'key': u'value'},
    u'set': {u'thing'},
}, 'complex')'''
I figure out how different types are saved to the database.
'''
import datetime
from scraperwiki.sqlite import save, save_var, execute, commit

execute('drop table if exists swdata')
execute('drop table if exists swvariables')
execute('drop table if exists complex')
commit()

for t in {dict, list, set, str, unicode, bool, int, float, long}:
    save_var(str(t), t())
    save([], {str(t).replace("'","").replace(' ', '').replace('<type', '').replace('>', ''): t()})

save([], {
    u'list': [u'thing'],
    u'dict': {u'key': u'value'},
    u'set': {u'thing'},
}, 'complex')