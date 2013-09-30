import scraperwiki
import xlrd
import string

def checkpoint_set (newstate, newpoint):
    global state, point
    state = newstate
    point = newpoint
    scraperwiki.sqlite.save_var ('state', state, verbose=0)
    scraperwiki.sqlite.save_var ('point', point, verbose=0)
def checkpoint_get ():
    global state, point
    state = scraperwiki.sqlite.get_var ('state', 'ks2', verbose=0)
    point = scraperwiki.sqlite.get_var ('point', 0, verbose=0)

lea_national = 971 #NB not an official code
lea_maintained = 970 #Presuming that RECTYPE 7, i.e. maintained schools, corresponds to code 970 "National", and 5 ("all") is unused

ks_list = ['ks2', 'ks4', 'ks5', 'abs', 'cfr', 'swf', 'census']

checkpoint_get ()
print 'Checkpoint %s %d' % (state, point)

if (state == 'Postproc'):
    pass
else:
    for ks in ks_list:
        if ks_list.index(ks) >= ks_list.index(state): #checkpointing
            print 'Downloading '+ks
            url = 'http://www.education.gov.uk/schools/performance/download/xls/england_'+ks+'.xls'
            data = scraperwiki.scrape (url)
            
            print 'Opening '+ks
            book = xlrd.open_workbook (file_contents=data)
            sheet = book.sheet_by_index (0)
            headers = sheet.row_values (1)
            texts = set(['LAESTAB', 'SCHNAME', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'TOWN', 'PCODE', 'TELNUM', 'SCHNAME_AC', 'OPEN_AC', 'NFTYPE', 'RELDENOM', 'AGERANGE', 'ADMPOL', 'FEEDER', 'GENDER1618', 'EXAMCONF', 'LONDON', 'MEDIAN', 'FSMBAND'])
        
            print 'Processing '+str(sheet.nrows)+' schools'
            
            for r in range (2,sheet.nrows):
                if r >= point: #checkpointing
                    if r % 500 == 0:
                        print '  Row '+str(r)
    
                    out = dict(zip(headers,sheet.row_values(r)))
                
                    for k in headers:
                        if k == 'URN' or k == 'LEA':
                            try:
                                out[k] = int(out[k])
                            except ValueError:
                                del out[k] #This occurs for "LEA" level entries, which don't have a URN
                        elif not (k in texts):
                            try:
                                out[k] = float(out[k])
                            except ValueError:
                                try:
                                    out[k] = int(out[k])
                                except ValueError:
                                    del out[k]
                        else:
                            out[k] = str(out[k])

                    if not('RECTYPE' in out): #abs, spend, swf, spine, ofsted, census
                        if 'URN' in out:
                            out['RECTYPE'] = 1
                        else:
                            out['RECTYPE'] = 4

                    if 'LAESTAB' in out: #census
                        out['LEA'] = int(out['LAESTAB'][:3])
                        out['ESTAB'] = int(out['LAESTAB'][3:])
                        del out['LAESTAB']

                    for k in ['LA', 'LANUMBER']: #all non-ks*
                        if k in out:
                            out['LEA'] = int(out[k])
                            del out[k]

                    #RECTYPE
                    # 1 = school
                    # 2 = special school
                    # 3 = 6th form centre
                    # 4 = LA
                    # 5 = National (all)
                    # 7 = National (maintained)
                    #Except bloody KS2:
                    # 3 = LA
                    # 4 = National (all)
                    # 5 = National (maintained)
                    if out['RECTYPE'] <= 2 or (out['RECTYPE'] == 3 and ks != 'ks2'):
                        if 'URN' in out:
                            scraperwiki.sqlite.save (unique_keys=['URN'], data=out, table_name=ks+'_school', verbose=0)
                    elif ks == 'ks2':
                        if out['RECTYPE'] == 4:
                            out['LEA'] = lea_national
                        elif out['RECTYPE'] == 5:
                            out['LEA'] = lea_maintained
                        if 'LEA' in out:
                            scraperwiki.sqlite.save (unique_keys=['LEA'], data=out, table_name=ks+'_la', verbose=0)
                    else:
                        if out['RECTYPE'] == 5:
                            out['LEA'] = lea_national
                        elif out['RECTYPE'] == 7:
                            out['LEA'] = lea_maintained
                        if 'LEA' in out:
                            scraperwiki.sqlite.save (unique_keys=['LEA'], data=out, table_name=ks+'_la', verbose=0)
                
                    checkpoint_set (ks, r)
            next_ks = ks_list.index(ks) + 1
            if (next_ks < len(ks_list)):
                checkpoint_set (ks_list[next_ks], 0)
            else:
                checkpoint_set ('Postproc', 0)

if state == 'Postproc':
    pass #FIXME: LA calculations for all non-KS* tables

import scraperwiki
import xlrd
import string

def checkpoint_set (newstate, newpoint):
    global state, point
    state = newstate
    point = newpoint
    scraperwiki.sqlite.save_var ('state', state, verbose=0)
    scraperwiki.sqlite.save_var ('point', point, verbose=0)
def checkpoint_get ():
    global state, point
    state = scraperwiki.sqlite.get_var ('state', 'ks2', verbose=0)
    point = scraperwiki.sqlite.get_var ('point', 0, verbose=0)

lea_national = 971 #NB not an official code
lea_maintained = 970 #Presuming that RECTYPE 7, i.e. maintained schools, corresponds to code 970 "National", and 5 ("all") is unused

ks_list = ['ks2', 'ks4', 'ks5', 'abs', 'cfr', 'swf', 'census']

checkpoint_get ()
print 'Checkpoint %s %d' % (state, point)

if (state == 'Postproc'):
    pass
else:
    for ks in ks_list:
        if ks_list.index(ks) >= ks_list.index(state): #checkpointing
            print 'Downloading '+ks
            url = 'http://www.education.gov.uk/schools/performance/download/xls/england_'+ks+'.xls'
            data = scraperwiki.scrape (url)
            
            print 'Opening '+ks
            book = xlrd.open_workbook (file_contents=data)
            sheet = book.sheet_by_index (0)
            headers = sheet.row_values (1)
            texts = set(['LAESTAB', 'SCHNAME', 'ADDRESS1', 'ADDRESS2', 'ADDRESS3', 'TOWN', 'PCODE', 'TELNUM', 'SCHNAME_AC', 'OPEN_AC', 'NFTYPE', 'RELDENOM', 'AGERANGE', 'ADMPOL', 'FEEDER', 'GENDER1618', 'EXAMCONF', 'LONDON', 'MEDIAN', 'FSMBAND'])
        
            print 'Processing '+str(sheet.nrows)+' schools'
            
            for r in range (2,sheet.nrows):
                if r >= point: #checkpointing
                    if r % 500 == 0:
                        print '  Row '+str(r)
    
                    out = dict(zip(headers,sheet.row_values(r)))
                
                    for k in headers:
                        if k == 'URN' or k == 'LEA':
                            try:
                                out[k] = int(out[k])
                            except ValueError:
                                del out[k] #This occurs for "LEA" level entries, which don't have a URN
                        elif not (k in texts):
                            try:
                                out[k] = float(out[k])
                            except ValueError:
                                try:
                                    out[k] = int(out[k])
                                except ValueError:
                                    del out[k]
                        else:
                            out[k] = str(out[k])

                    if not('RECTYPE' in out): #abs, spend, swf, spine, ofsted, census
                        if 'URN' in out:
                            out['RECTYPE'] = 1
                        else:
                            out['RECTYPE'] = 4

                    if 'LAESTAB' in out: #census
                        out['LEA'] = int(out['LAESTAB'][:3])
                        out['ESTAB'] = int(out['LAESTAB'][3:])
                        del out['LAESTAB']

                    for k in ['LA', 'LANUMBER']: #all non-ks*
                        if k in out:
                            out['LEA'] = int(out[k])
                            del out[k]

                    #RECTYPE
                    # 1 = school
                    # 2 = special school
                    # 3 = 6th form centre
                    # 4 = LA
                    # 5 = National (all)
                    # 7 = National (maintained)
                    #Except bloody KS2:
                    # 3 = LA
                    # 4 = National (all)
                    # 5 = National (maintained)
                    if out['RECTYPE'] <= 2 or (out['RECTYPE'] == 3 and ks != 'ks2'):
                        if 'URN' in out:
                            scraperwiki.sqlite.save (unique_keys=['URN'], data=out, table_name=ks+'_school', verbose=0)
                    elif ks == 'ks2':
                        if out['RECTYPE'] == 4:
                            out['LEA'] = lea_national
                        elif out['RECTYPE'] == 5:
                            out['LEA'] = lea_maintained
                        if 'LEA' in out:
                            scraperwiki.sqlite.save (unique_keys=['LEA'], data=out, table_name=ks+'_la', verbose=0)
                    else:
                        if out['RECTYPE'] == 5:
                            out['LEA'] = lea_national
                        elif out['RECTYPE'] == 7:
                            out['LEA'] = lea_maintained
                        if 'LEA' in out:
                            scraperwiki.sqlite.save (unique_keys=['LEA'], data=out, table_name=ks+'_la', verbose=0)
                
                    checkpoint_set (ks, r)
            next_ks = ks_list.index(ks) + 1
            if (next_ks < len(ks_list)):
                checkpoint_set (ks_list[next_ks], 0)
            else:
                checkpoint_set ('Postproc', 0)

if state == 'Postproc':
    pass #FIXME: LA calculations for all non-KS* tables

