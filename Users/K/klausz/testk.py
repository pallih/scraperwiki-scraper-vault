# Take the table and put additional code

import scraperwiki
import urllib
import lxml.etree 
import re
import locale
from datetime import date



locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # use German locale; name might vary with platform >>>
encoding = locale.nl_langinfo(locale.CODESET) #encode: how data comes in, decode: how data gets out
print 'Encoding: ', encoding # tells what codeset is used, dont remove, from time to time necessary to activate code

# Spain Islas Canarias
pdfurl = "http://www.dgfc.sgpg.meh.es/sitios/DGFC/es-ES/Beneficiarios%20Fondos%20Feder%20y%20Fondos%20de%20Cohesin/IC34.pdf"




# First SQL Transformation:
# select
# a.PrId
# , a.sequencenumber
# , (select b.sequencenumber from pdf_data_unstructured b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1) as ByDn
# from pdf_data_unstructured a
# where a.RecNo > 0
# and length(page) = 1
# and ((ByDn > a.sequencenumber) or (ByDn is null))
# order by page , recno

# changed
# select PrId, sequencenumber , case  when (ByDn is null) then ((sequencenumber / 1000) *1000 ) + 999 else ByDn end ByDn from (select distinct a.PrId , (a.sequencenumber -1) as sequencenumber , ((select b.sequencenumber from PDF_DATA_UNSTRUCTURED b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1)-1)  as ByDn from PDF_DATA_UNSTRUCTURED a where a.RecNo > 0 and ((ByDn > a.sequencenumber) or (ByDn is null)))

#scraperwiki.sqlite.attach('pdf_reader_template');

#results = scraperwiki.sqlite.select('a.PrId , (a.sequencenumber -1) as sequencenumber , ((select b.sequencenumber from PDF_DATA_UNSTRUCTURED b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1)-1)  as ByDn from PDF_DATA_UNSTRUCTURED a where a.RecNo > 0 and ((ByDn > a.sequencenumber) or (ByDn is null))' )

results = scraperwiki.sqlite.select(' PrId, sequencenumber , case  when (ByDn is null) then ((sequencenumber / 1000) *1000 ) + 999 else ByDn end ByDn from (select distinct a.PrId , (a.sequencenumber -1) as sequencenumber , ((select b.sequencenumber from PDF_DATA_UNSTRUCTURED b where a.recno = b.recno-1 and b.page = a.page and a.recno >= 1)-1)  as ByDn from PDF_DATA_UNSTRUCTURED a where a.RecNo > 0 and ((ByDn > a.sequencenumber) or (ByDn is null)))')

scraperwiki.sqlite.save([], results, table_name="TransformTestTable")

