# scrapes terminology from an cpl.nl government data excel file
#
#

import xlrd
import scraperwiki
import re

LANG_EN=1
LANG_NL=0
VAL_COL=2

def make_id(label):
  id=label.lower()
  id=re.sub(' [ ]*','_',id)
  id=re.sub(' ','_',id)
  id=re.sub('^_','',id)
  id=re.sub('_$','',id)
  id=re.sub('[,\.$€()<>%\'\*]','',id)  
  return id

def make_label(label_en,label_nl):
  label={}
  label[LANG_EN]=label_en
  label[LANG_NL]=label_nl
  return label

def scrape_cpl_terminology(url):
  book = xlrd.open_workbook(file_contents=scraperwiki.scrape(url),formatting_info=True)
  sheet = book.sheet_by_index(0)
  label={}
  super_id=''
  for rownum in xrange(sheet.nrows):
    cell_value_en = sheet.cell(rownum, LANG_EN).value
    if cell_value_en!='':
      cell_value_nl = sheet.cell(rownum, LANG_NL).value
      concept_id=make_id(cell_value_en)
      label = make_label(cell_value_en,cell_value_nl)
      cell_data_first=sheet.cell(rownum, VAL_COL).value
    
      # get formating (xf, font)
      xf_index = sheet.cell_xf_index(rownum, 1)
      xf = book.xf_list[xf_index]
      xf_font_index = xf.font_index
      font = book.font_list[xf_font_index]
      isbold = font.bold
      indent_level = xf.alignment.hor_align

      # evaluate property flag
      is_property = 1 if (indent_level==3) else 0
      # evaluate super concept flag
      is_super = isbold
      # evaluate val flag  
      is_data = 1 if (cell_data_first!='') else 0  

      # generate data
      isstore=0
      isa_concept=''
      if is_super==1:
        super_id=concept_id
        isstore=1
      else:
        if is_property!=1:
          if is_data!=0:
            isa_concept=super_id
            isstore=1
      record={}
      record['id']=concept_id
      record['label-en']=label[LANG_EN]
      record['label-nl']=label[LANG_NL]
      record['is-a']=isa_concept
      if isstore==1:
        scraperwiki.datastore.save(['id'], record)


# scrape 24 excel files from Dutch Central Economic Plan 2010
#urls = ['http://www.cpb.nl/eng/data/cep2010/bijlage2.xls','http://www.cpb.nl/eng/data/cep2010/bijlage3.xls']
urls =['http://www.cpb.nl/eng/data/cep2010/bijlage1_1.xls','http://www.cpb.nl/eng/data/cep2010/bijlage1_2.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage1_3.xls','http://www.cpb.nl/eng/data/cep2010/bijlage2.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage3.xls','http://www.cpb.nl/eng/data/cep2010/bijlage4.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage5.xls','http://www.cpb.nl/eng/data/cep2010/bijlage6.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage7.xls','http://www.cpb.nl/eng/data/cep2010/bijlage8.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage9.xls','http://www.cpb.nl/eng/data/cep2010/bijlage10.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage11.xls','http://www.cpb.nl/eng/data/cep2010/bijlage12.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage13.xls','http://www.cpb.nl/eng/data/cep2010/bijlage_e1.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage_e2.xls','http://www.cpb.nl/eng/data/cep2010/bijlage_e3.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage_e4.xls','http://www.cpb.nl/eng/data/cep2010/bijlage_e5.xls',
'http://www.cpb.nl/eng/data/cep2010/bijlage_e6.xls','http://www.cpb.nl/eng/data/cep2010/bijlage_e7.xls']

for url in urls:
  print 'scrape '+url
  scrape_cpl_terminology(url)
