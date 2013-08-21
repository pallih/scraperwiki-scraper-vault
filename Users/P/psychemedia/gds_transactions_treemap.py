import gviz_api,scraperwiki,math

sourcescraper = 'gds_webservice_transactional_data'

page_template = """
<html>
  <head>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['treemap']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
     var json_data = new google.visualization.DataTable(%(json)s, 0.6);
     var treemap = new google.visualization.TreeMap(document.getElementById('visualization'));
     treemap.draw(json_data, {maxDepth:2,maxPostDepth:1});
    }
  </script>
  </head>
  <body>
    <h1>Quirky View over GDS Logged UKGov Transactional Services</h1>
    <p>First stab at a treemap way of navigating the Transactional Services data that GDS have just started delivering.</p>
    <p>Because the transaction numbers of some departments are orders of magnitude larger than other departments,
    I have used the log10 of the number of transactions rather than the actual transaction count in sizing the blocks.
    This apparently arbitrary decision will really upset the viz folk, so I'm calling it a "Quirky View" instead.
    The lowest level block size is a function of the log10 of the number of transactions; views further up the
    hierarchy have a block size that is the sum of the log10 number of transactions in the lowest block, and as such
    indicates not only (not even?!) the number of transactions, but also the variety of transactions carried out by
    each department. That is, the block size is related to, erm, ah, I know, <em>interestingness</em>, where <em>interesting</em>
    is a weird function of number and vareity of transactions... ;-)</p>
    <p>If you have any good ideas about how to cope with number ranges over several orders of magnitude in a treemap context,
    whilst still making the treemap navigable, please let me know;-)</p>
    <p>Via <a href="http://digital.cabinetoffice.gov.uk/2012/07/24/data-driven-delivery/">GDS: Data Driven Delivery</a>; <a href="http://transactionalservices.alphagov.co.uk/">Get the data</a></p>
    <p>Usage: click to zoom in, right click to zoom out (<a href="https://scraperwiki.com/views/gds_transactions_treemap/">code</a>; <a href="https://scraperwiki.com/scrapers/gds_webservice_transactional_data/">data</a>).</p>
    <hr/>
    <div id="visualization" style="width: 900px; height: 700px;" ></div>
  </body>
</html>
"""

scraperwiki.sqlite.attach( sourcescraper )

q = '* FROM "transactions"'
data = scraperwiki.sqlite.select(q)

#print data

description={"item":('string','item'),"parent":('string','parent'),"transactions":('number','transactions')}

def itemise(item,parent,transactions):
    try:
        if transactions!='' and transactions>0: transactions=math.log10(int(transactions))
        else: transactions=0
    except:
        #print transactions
        transactions=0
    item={'item':item,'parent':parent,'transactions':transactions}
    return item


ddata=[]
depts=[]
cdata=[]
deptchildren={}
ddata.append(itemise("GDS TransactionsLog",'',0))
for row in data:
    tx=row['Transactions per year']
    if row['Abbreviation'] not in depts:
        depts.append(row['Abbreviation'])
        ddata.append(itemise(depts[-1],"GDS TransactionsLog",0))
        deptchildren[row['Abbreviation']]=[]
    if row['Body'] not in deptchildren[row['Abbreviation']]:
        deptchildren[row['Abbreviation']].append(row['Body'])
        ddata.append(itemise(row['Body']+':',row['Abbreviation'],0))
    ddata.append(itemise(row['Transactional service']+' '+str(tx),row['Body']+':',tx))

ddata_table = gviz_api.DataTable(description)
ddata_table.LoadData(ddata)
json = ddata_table.ToJSon(columns_order=("item", "parent","transactions"))
#print ddata
#print json
print page_template % vars()