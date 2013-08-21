# Liverpool middle-classness

# Tongue-in-cheek measure of middle-classness for specific postcodes around Liverpool.
# Based on school statistics from DfE, including pupil-to-teacher ratios, truancy levels and ICT spending



import scraperwiki



def scrape():
    scraperwiki.sqlite.attach('liverpool_schools_data', 's')
    
    rows = scraperwiki.sqlite.select('spine.urn, spine.POSTCODE, spine.lat, spine.long, absence.PERCUA, absence.PPERSABS15, absence.PPERSABS20, census.PNUMFSM, workforce.RATPUPTEA, spend.LEARNINGRESOURCES, spend.ICT from s.spine, s.absence, s.census, s.workforce, s.spend where spine.urn=absence.urn and spine.urn=census.urn and spine.urn=workforce.urn and spine.urn=spend.urn and census.PNUMFSM != "SUPP" and workforce.RATPUPTEA != 0')
    # note: inner join means we exclude schools for which any of those statistics are not available
    
    for i, row in enumerate(rows):
        rows[i]['LEARNINGRESOURCES'] = int(rows[i]['LEARNINGRESOURCES'])
        rows[i]['ICT'] = int(rows[i]['ICT'])
        rows[i]['PNUMFSM'] = float(rows[i]['PNUMFSM'])
    
    scraperwiki.sqlite.save(['URN'], rows)




def normalise():
    rows = scraperwiki.sqlite.select('* from swdata')
    stats = scraperwiki.sqlite.select('MIN(LEARNINGRESOURCES), MAX(LEARNINGRESOURCES), MIN(ICT), MAX(ICT), MIN(PPERSABS20), MAX(PPERSABS20), MIN(PPERSABS15), MAX(PPERSABS15), MIN(PNUMFSM), MAX(PNUMFSM), MIN(PERCUA), MAX(PERCUA), MIN(RATPUPTEA), MAX(RATPUPTEA) from swdata')
    
    normalised = []
    for row in rows:
        temp = {}
        temp['learningresources'] = ( float(row['LEARNINGRESOURCES']) - float(stats[0]['MIN(LEARNINGRESOURCES)']) ) / float(stats[0]['MAX(LEARNINGRESOURCES)'])
        temp['ict'] = ( float(row['ICT']) - float(stats[0]['MIN(ICT)']) ) / float(stats[0]['MAX(ICT)'])
        temp['pnumfsm'] = ( row['PNUMFSM'] - stats[0]['MIN(PNUMFSM)'] ) / stats[0]['MAX(PNUMFSM)']
        temp['percua'] = ( row['PERCUA'] - stats[0]['MIN(PERCUA)'] ) / stats[0]['MAX(PERCUA)']
        temp['ratpuptea'] = ( float(row['RATPUPTEA']) - float(stats[0]['MIN(RATPUPTEA)']) ) / float(stats[0]['MAX(RATPUPTEA)'])
        temp['total'] = temp['learningresources'] + temp['ict'] - temp['pnumfsm'] - temp['percua'] - temp['ratpuptea']
        temp['postcode'] = row['POSTCODE']
        temp['lat'] = row['lat']
        temp['long'] = row['long']
        print temp
        normalised.append(temp)

    scraperwiki.sqlite.save(['postcode'], normalised, 'normalised')




def standardise():
    rows = scraperwiki.sqlite.select('* from swdata')
    stats = scraperwiki.sqlite.select('avg(LEARNINGRESOURCES) as LEARNINGRESOURCES, avg(ICT) as ICT, avg(PNUMFSM) as PNUMFSM, avg(PERCUA) as PERCUA, avg(RATPUPTEA) as RATPUPTEA from swdata')[0]

    for row in rows:
        print row['POSTCODE']
        lea_diff = float(row['LEARNINGRESOURCES']) - float(stats['LEARNINGRESOURCES'])
        ict_diff = float(row['ICT']) - float(stats['ICT'])
        fsm_diff = float(row['PNUMFSM']) - float(stats['PNUMFSM'])
        abs_diff = float(row['PERCUA']) - float(stats['PERCUA'])
        rat_diff = float(row['RATPUPTEA']) - float(stats['RATPUPTEA'])
        lea_vari = lea_diff * lea_diff
        ict_vari = ict_diff * ict_diff
        fsm_vari = fsm_diff * fsm_diff
        abs_vari = abs_diff * abs_diff
        rat_vari = rat_diff * rat_diff
        total = lea_diff + ict_diff - fsm_diff - abs_diff - rat_diff
        print lea_vari, ict_vari, fsm_vari, abs_vari, rat_vari, lea_vari+ict_vari-fsm_vari-abs_vari-rat_vari


standardise()
