import scraperwiki

class Column:
    def __init__(self, name, title, data_type, format='', scale=1):
        self.name = name
        self.title = title
        self.data_type = data_type
        self.scale = scale
        self.format = format
        self.align = ''
        self.data = []
        if self.data_type == int or self.data_type == float:
            self.align = 'align="right"'

    def add(self, cell):
        self.data.append(self.data_type(cell))

    def __len__(self):
        return len(self.data)

class Table:
    def __init__(self, title):
        self.title = title
        self.columns = {}
        self.data = []
        self.rows = 0

    def add_column(self, column):
        self.columns[column.title] = column

    def add_rows(self, rows):
        for row in rows:
            for column_key in self.columns:
                column = self.columns[column_key]
                column.add(row[column.name])
            self.rows += 1
               
    def sort(self, column_title, reverse_order=False):
        rank = lambda l: sorted(range(len(l)), key=l.__getitem__, reverse=reverse_order)
        rank_order = rank(self.columns[column_title].data)
        for column in self.columns.values():
            column.data = [column.data[i] for i in rank_order]

    def __str__(self):
        table = '<table>'
        table += '<h1>{}</h1>'.format(self.title)
        table += '<tr>'
        for col in self.columns.values():
            table += '<th align="left">{}</th>'.format(col.title)
        table += '</tr>'
        for row in range(self.rows):
            table += '<tr>'
            for column in self.columns.values():
                table += '<td {align}>{cell}</td>'.format(align=column.align, cell=format(column.data_type(column.data[row])*column.scale, column.format))
            table += '</tr>'
        table += '</table>'
        return table

sourcescraper = 'index_universe_etf_data'

scraperwiki.sqlite.attach(sourcescraper)

recent_date = max(d['DataAsOf'] for d in scraperwiki.sqlite.select('DataAsOf FROM etf_data'))
aum_dicts = scraperwiki.sqlite.select('''
IssuingCompany, SUM(AssetsUnderManagement), SUM(AssetsUnderManagement*ExpRatio)
FROM etf_data
WHERE DataAsOf = ?
GROUP BY IssuingCompany''', recent_date)
table = Table('Assets Under Management by Issuer')
table.add_column(Column('IssuingCompany', 'Issuer', str))
table.add_column(Column('SUM(AssetsUnderManagement)', 'AUM', int, format=',d'))
table.add_column(Column('SUM(AssetsUnderManagement*ExpRatio)', 'Revenue', float, format=',.0f', scale=.01))
table.add_rows(aum_dicts)
table.sort('AUM', True)

print table
