from time import time
from scraperwiki.sqlite import save
from scraperwiki import swimport
keyify=swimport('keyify').keyify

#dsp=swimport('dsp').dsp
from lxml.etree import fromstring
#import re
from urllib2 import urlopen

URL="http://www.saccol.org.za/saccos_in_saccol.php"


def clean_page(raw):
  raw=raw.split('<table width="98%" border="1" align="center" cellpadding="3" cellspacing="0">')[1]
  raw=raw.split('</table>')[0]
  raw=raw.replace('<col width="64" span="4"  />','')
  cleaned='<table>%s</table>' % raw
  return cleaned

def main():
  #Load page
  #x=dsp(URL,False)
  raw=urlopen(URL).read()
  cleaned=clean_page(raw)

  #Load table
  table=fromstring(cleaned)
  t=BizarreTable(table)

  #Get the header
  keys=t.get_header()
  print keys

  #Get the non-telephone columns
  cols=[
    t.get_other_col(1)
  , t.get_other_col(2)
  , {}
  , t.get_other_col(4)
  ]

  #Check that the rowspans are the same
  try:
    assert cols[0]['rowspans']==cols[1]['rowspans']==cols[3]['rowspans']
  except:
    for col in cols[0:2]+[cols[3]]:
      print col['rowspans']
    raise
  rowspans=map(int,cols[0]['rowspans'])

  #Get the telephone columns
  cols[2]=t.get_telephone_col(rowspans)

  #Restructure the columns
  cols_text=[col['text'] for col in cols]

  d_noregion=join_cols_with_header(keys,cols_text)
  d=add_region(d_noregion,t,rowspans)

  print d

def add_region(d,t,rowspans):
  "Go through the ordered list of dicts. Add the appropriate region for each."
  pos=t.get_region_positions()
  pos_diffs=[p[1]-p[0] for p in zip(pos[:-1],pos[1:])]
  #print pos_diff

  #Group the rowspans
  real_rows_per_region=[]
  for current_pos_diff in pos_diffs:
    s=0
    while s<current_pos_diff:
      s+=1
    real_rows_per_region.append(s)

  print real_rows_per_region

  rowstart=0
  while len(real_rows_per_region)>0:
    rowend=rowstart+real_rows_per_region.pop(0)
    for row in d[rowstart:rowend]:
      row['region']=rowstart
    print rowstart,rowend
    rowstart+=rowend

  return d

def join_cols_with_header(header,cols_text):
  "Join the header row to the columns matrix"

  #Check lengths
  nrow_set=set(map(len,cols_text))
  assert 1==len(nrow_set)
  nrow=list(nrow_set)[0]

  ncol=len(cols_text)

  m=[]
  for i_row in range(nrow):
    m.append([])
    for i_col in range(ncol):
      cell=cols_text[i_col][i_row]
      m[i_row].append(cell)

  return [dict(zip(header,row)) for row in m]

class BizarreTable:
  "A class for this bizarre table"

  def __init__(self,table):
    self.table=table
    self.region_positions=self.get_region_positions()

  @staticmethod
  def sum_rowspans(rowspans_list,rowspan_next):
    return rowspans_list+[rowspans_list[-1]+rowspan_next]

  def get_telephone_col(self,rowspans):
    "Combine those rows for the telephone column"
    positions=reduce(self.sum_rowspans,rowspans,[0])
    ranges=zip(positions[:-1],positions[1:])
    print ranges

    col=[]
    textnodes=self.table.xpath('tr[not(@colspan)]/td[not(@rowspan)]/text()')
    for row1position,row2position in ranges:
      cell='\n'.join(textnodes[row1position:row2position])
      col.append(cell)
    return {"text":col}

  def get_other_col(self,colnum):
    text=self.table.xpath('tr/td[@rowspan and position()="%d"]/text()' % colnum)
    rowspans=self.table.xpath('tr/td[@rowspan and position()="%d"][text()]/@rowspan' % colnum)
    assert len(text)==len(rowspans)
    return {"text":text,"rowspans":rowspans}

  def get_region_positions(self):
    return [tr.xpath('count(preceding-sibling::*)')+1 for tr in self.table.xpath('tr[td[@colspan="4"]]')]

  def get_header(self):
    "Get the header row from the table"
    #Retrieve
    raws=self.table.xpath('tr[td[@valign="middle"]]/td/strong/text()')

    #Clean
    return [keyify(raw.replace('/','_or_')) for raw in raws]

main()