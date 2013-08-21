import scraperwiki

header_size = 10
col = [ 0, 55, 77, 99, 120 ]

scraperwiki.metadata.save('data_columns',
        ['quantity', 'value', 'uncertainty', 'unit'])

def parse_line(line):
    row = []
    for i in xrange(4):
        row.append(line[col[i]:col[i+1]].strip())
    if len(row[1]) == col[2] - col[1]:
        # oversized cells
        row[1] = line[col[1]  :col[2]+1].strip()
        row[2] = line[col[2]+1:col[3]+2].strip()
        row[3] = line[col[3]+2:        ].strip()
    return row

def clean_value(s):
    if s == '(exact)':
        return '0'
    s = s.replace('...', '')
    s = s.replace(' ', '')
    float(s) # ensure value is valid
    return s

text = scraperwiki.scrape('http://physics.nist.gov/cuu/Constants/Table/allascii.txt')
lines = text.split('\n')[header_size:-1]
for line in lines:
    row = parse_line(line)
    row[1] = clean_value(row[1])
    row[2] = clean_value(row[2])
    scraperwiki.datastore.save(['quantity'],
            {'quantity':row[0], 'value':row[1], 'uncertainty':row[2], 'unit':row[3]})

