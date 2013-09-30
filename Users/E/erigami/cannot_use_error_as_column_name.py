import scraperwiki as sw
import traceback as tb

try:
    sw.sqlite.save(unique_keys=[], table_name='wontWork',
            data={
                    'f1' : 'foo',
                    'error' : 'fail'
            }
    )
except sw.sqlite.SqliteError, e: 
    tb.print_exc()


sw.sqlite.save(unique_keys=[], table_name='willWork',
        data={
                'f1' : 'foo',
                'iserror' : 'fail'
        }
)import scraperwiki as sw
import traceback as tb

try:
    sw.sqlite.save(unique_keys=[], table_name='wontWork',
            data={
                    'f1' : 'foo',
                    'error' : 'fail'
            }
    )
except sw.sqlite.SqliteError, e: 
    tb.print_exc()


sw.sqlite.save(unique_keys=[], table_name='willWork',
        data={
                'f1' : 'foo',
                'iserror' : 'fail'
        }
)