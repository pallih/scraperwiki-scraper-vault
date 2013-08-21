from scraperwiki.sqlite import save, select
from scraperwiki import swimport
from requests import session
from lxml.html import fromstring, tostring
import re
from time import time
keyify=swimport('keyify').keyify
randomsleep=swimport('randomsleep').randomsleep

URL="http://www.ncr.org.za/register_of_registrants/index.php"

#DEV=True
DEV=False

DATE=time()

RE={
  'leftpadding':re.compile(r'^ *')
, 'rightpadding':re.compile(r' *$')
}

def headquarters():
  cp1()
  #dc_and_cb1()

def cp1():
  p=Page('CP1')

  while p.lastpage()==False:
    tables=p.table().subtables()
    d = []
    for table in tables:
        row = table.parse()
        row['business_premises'] = table.business_premises()
        d.append(row)
        print row

    more_cleaning(d,p.pagenum)
    save([],d,'cp1')
    randomsleep()
    p=p.next25()

def dc_and_cb1():
  tables=tables.extend(Page('DC').table().subtables())+tables.extend(Page('CB1').table().subtables())
  d=[table.parse() for table in tables]
  more_cleaning(d)
  save([],d,'other')

def more_cleaning(d,pagenum):
  for row in d:
    row['date_scraped']=DATE
    if pagenum!=None:
      row['pagenum']=pagenum
      row['url']=URL+"?page=%d"%pagenum

class Subtable:
  def __str__(self,page):
    return tostring(self.x)

  def __init__(self,subtable_tree,registrant_type):
    self.x=subtable_tree
    self.registrant_type=registrant_type

  def parse(self,clean=True):
    record=self.rawparse()

    if clean:
      #Clean the keys if cleanliness is requested rather than rawness
      for key in record.keys():
        record[key]=self.clean_string(record[key])
    return record

  def business_premises(self):
    onclicks = self.x.xpath('descendant::span/@onclick')
    return 'http://www.ncr.org.za/register_of_registrants/' + onclicks[0][:-1].replace("location.href='", '') if len(onclicks) == 1 else None

  def rawparse(self):
    record={
      'registrant-type':self.registrant_type
    , 'registrant':self.registrant()
    , 'full-address':self.physical_address()
    , 'registration-number':self.registration_number()
    , 'phone':self.phone()
    , 'fax':self.fax()
    , 'town':self.town()
    }
    return record

  def physical_address(self):
    if self.registrant_type in ("DC","CP1"):
      return '\n'.join(self.x.xpath('descendant::td/span[text()="Physical Address :"]/following-sibling::span/text()'))

    elif self.registrant_type=="CB1":
      nodes=self.x.xpath('descendant::span[@class="bodybold" and text()="Physical Address :"]/following-sibling::span[position()=1]/text()')
      assert 1==len(nodes)
      return nodes[0]

  def registration_number(self):
    if self.registrant_type=="CP1":
      nodes=self.x.xpath('descendant::span[@class="idText1"]/descendant::span[@class="smallText"]/text()')
      assert 1==len(nodes)
      return nodes[0]
    else:
      return ''.join(self.x.xpath('descendant::span[@class="idText1"][position()=2]/text()'))

  def phone_and_fax_not_cb1(self):
    nodes=self.x.xpath('descendant::span[@class="bodybold" and text()="Phone :"]/following-sibling::span/text()')
    assert len(nodes)==4
    assert "Fax : "==nodes[1]
    return {
      "phone":nodes[0]
    , "fax":nodes[2]
    }

  def phone_and_fax_cb1(self):
    nodes=self.x.xpath('descendant::div[@align="right"]/span[@class="Text2"]/text()')
    assert len(nodes)==2
    return dict(zip(['phone','fax'],nodes))

  def phone_and_fax(self):
    if self.registrant_type=="CB1":
      return self.phone_and_fax_cb1()
    elif self.registrant_type in ("DC","CP1"):
      return self.phone_and_fax_not_cb1()

  def phone(self):
    return self.phone_and_fax()['phone']

  def fax(self):
    return self.phone_and_fax()['fax']

  def town(self):
    if self.registrant_type in ("DC","CP1"):
      nodes=self.x.xpath('descendant::span[@class="bodybold" and text()="Town : " or text()="Town :"]/../text()[position()=last()]')
    elif self.registrant_type=="CB1":
      nodes=self.x.xpath('descendant::span[@class="bodybold" and text()="Town :"]/following-sibling::span[position()=1]/text()')
    assert 1==len(nodes),map(tostring,nodes)
    return nodes[0]

  def registrant(self):
    raw=''.join(self.x.xpath('descendant::span[@class="style9"]/text()'))
    return raw

  @staticmethod
  def clean_string(string):
    lines=string.split('\n')
    cleanlines=[re.sub(RE['leftpadding'],'',re.sub(RE['rightpadding'],'',line)) for line in lines]
    for cleanline in cleanlines:
      if cleanline=="":
        cleanlines.remove(cleanline)
    return '\n'.join(cleanlines)

class Table:
  def __str__(self):
    return tostring(self.x)

  def __init__(self,table_tree,registrant_type):
    self.x=table_tree
    self.registrant_type=registrant_type

  def subtables(self):
    return [Subtable(st,self.registrant_type) for st in self.x.xpath('tr/td/table')]

class Page:
  def __init__(self,registrant_type,s=None,pagenum=None):
    self.registrant_type=registrant_type

    if s==None:
      self.s=session()
    else:
      self.s=s

    if pagenum==None:
      search_text="aad" if (DEV and registrant_type=="DC") else "*"
      self.h=self.s.post(URL,{"ns_BType": registrant_type, "ns_SearchText": search_text, "ns_Town": "All", "_submit_check_": 1, "ns_cancel": "registered"}).content
      if registrant_type=="CP1":
        self.pagenum=25
    else:
      self.h=self.s.get(URL+"?page=%d"%pagenum).content
      self.pagenum=pagenum
    self.x=fromstring(self.h)

  def lastpage(self):
    "True or False"
    nodes=self.x.xpath('//font[@color="#FF0000"][text()="No Results Returned."]')
    return len(nodes)>0

  def next25(self):
    "Only used for CP1"
    return Page(self.registrant_type,s=self.s,pagenum=self.pagenum+25)

  def search_total(self):
    nodes=self.x.xpath('//font[@color="#FF9900"]/text()')
    numbers=[]
    assert 2==len(nodes)
    for node in nodes:
      find=''.join(re.findall(r'[0-9]*',node))
      numbers.append(find)
    s=set(numbers)
    log('Search Total:')
    log(s)
    assert 1==len(s)
    return int(s.pop())

  def table(self):
    nodes=self.x.xpath("""//table[@style="color: black;

            text-decoration: none;



            background: #ffffff;

            padding: 5px;

            font-size: 12;"]""")
    assert len(nodes)==1
    return Table(nodes[0],self.registrant_type)

def cpTables():
  cp=CreditProviders()
  cp.paginate()
  print cp.tables



def log(thing):
  if DEV:
    print(thing)

class Test:
  """This test runner runs methods containing the word "download" or "local". If you 
  """
  def __init__(self,download=True):
    self.download=download
    self.onLoad()
    self.errors=[]
    self.run()
    self.report()

  def run(self):
    if self.download:
      self.dc=Page('DC')
      self.cb1=Page('CB1')
    for methodname in Test.__dict__:
      if "local" in methodname:
        self.run_test_method(methodname)
      elif "download" in methodname and self.download:
        self.run_test_method(methodname)

  def run_test_method(self,methodname):
    getattr(self,methodname)()

  def onLoad(self):
    self.crosscheck=Subtable(fromstring("""<table width="740" border="0" cellpadding="2" cellspacing="0">
            <tbody><tr>
                <td colspan="2"><span class="style9">
                         CrossCheck (Pty) Ltd (previously known as MLCB)                     </span><br>
                    <span class="smallTextb">LegalReg No: </span> <span class="smallText">
                        1997/015143/07                    </span><br>
                <br>                        </td>
                <td valign="top"><div align="right"><span class="idText1"> <a href="JavaScript:window.print();"><img src="images/printButton.jpg" width="12" height="12" border="0"></a><br>
                            <br>
                        NCR Reference No:</span> <span class="idText1">
                            NCRCB1                            <br>
                            <br>
                            <br>
                </span></div></td>
            </tr>
            <tr>
            <td colspan="2" valign="top"><span class="bodybold">Website :</span><br>
                    <span class="Text2">
                        http://www.crosscheckonline.co.za                    </span> <br><span class="bodybold">Website for credit report : </span> <span class="Text2">
                     <span class="Text2">
                        </span>
                <br>     
                     <span class="bodybold">Email Address : </span> <span class="Text2">
                     <span class="Text2">
                        </span>              </span></span></td>
                <td colspan="2" valign="top"><span class="bodybold">Physical Address :</span><br>
                    <span class="Text2">
                        Kent park, 332 Kent Avenue, Ferndale, Randburg, 2196                     </span> <br>  <br>
                            <span class="bodybold">Town :</span>
                            <span class="Text2"> Randburg                </span>
                <br>                        </td>
                <td colspan="2" valign="top"><div align="right"><br>
                        <span class="bodybold">Phone :</span> <span class="Text2">
                            0105 909 505                        </span><br>
                        <span class="bodybold">Fax : </span> <span class="Text2">
                            011 388 8582                           </span></div></td>
            </tr>
        <tr>
                        <td colspan="5"><div align="left"><img src="images/info.jpg" width="16" height="16" vspace="5" align="absmiddle"> <span class="style13" span="" onclick="location.href='business.php?id=3&amp;show=NCRCB1'"> View Business Premises</span> </div></td>
                        </tr>
            <tr>
                <td colspan="5"><div align="center"></div></td>
            </tr>
            <tr>
                <td colspan="5"></td>
            </tr>
                                        <tr>
                                <td colspan="8"><img src="images/line.gif" width="715" height="1" vspace="20"></td>
                            </tr>
                    </tbody></table>"""),'CB1')
    self.aadielah_moses=Subtable(fromstring("""<table width="740" border="0" cellpadding="2" cellspacing="0">
                            <tbody><tr>
                                <td colspan="2"><span class="style9"><br>
                                        Aadielah Moses                                </span> </td>
                                <td valign="top"><div align="right"><span class="idText1"> <a href="JavaScript:window.print();"><img src="images/printButton.jpg" width="12" height="12" border="0"></a><br>
                                            <br>
                                        NCR Reg No:</span> <span class="idText1">
                                            NCRDC1825                                            <br>
                                            <br>
                                            <br>
                                </span></div></td>
                            </tr>
                            <tr>
                                <td colspan="2" valign="top"><span class="bodybold">Physical Address :</span><br>
                                    <span class="Text2">
                                        Debtbrakes: 85 Goulburn Street, Goodwood                                    </span> <br>
                                    <span class="Text1">
                                        85 Goulburn Street, Goodwood, 7460                                    </span><br>
                                <br>                                    </td>
                                <td colspan="2" valign="top"><div align="right"><br>
                                        <span class="bodybold">Phone :</span> <span class="Text2">
                                            021 592 6766                                        </span><br>
                                        <span class="bodybold">Fax : </span> <span class="Text2">
                                            021 592 6766                                            <br>
                                            <span class="bodybold">Town :</span>
                                            Goodwood                                </span></div></td>
                            </tr>
                            <tr>
                                <td colspan="5"><div align="left"></div></td>
                            </tr>
                            <tr>
                                                                <td colspan="5"><div align="center"></div></td>
                                                            </tr>
                            <tr>
                                
                            </tr>
                            <tr>
                                <td colspan="5"></td>
                            </tr>
                                                        <tr>
                                <td colspan="8"><img src="images/line.gif" width="715" height="1" vspace="20"></td>
                            </tr>
                    </tbody></table>"""),'DC')

  def assertBool(self,question,error=""):
    if question==True:
      self.errors.append(False)
    else:
      self.errors.append(error)

  def assertDict(self,observed,expected):
    #print("Testing the following keys")
    #print(observed.keys())
    for key in expected.keys():
      if observed.has_key(key):
        message='%s was "%s" and not "%s".' % (key,observed[key],expected[key])
        self.assertBool(observed[key]==expected[key],message)
      else:
        message='The key "%s" was not observed.' % key
        self.assertBool(observed.has_key(key),message)

  def assertEqual(self,a,b):
    message=str(a)+"!="+str(b)
    self.assertBool(a==b,message)

  def report(self):
    print "Running %d tests" % len(self.errors)
    for i,error in zip(range(len(self.errors)),self.errors):
      testnum=i+1
      if error==False:
        print("Test %d passed." % testnum)
      else:
        print("Test %d failed: %s" % (testnum,error))

  def cb1_local_subtable_parsing_clean(self):
    observed=self.crosscheck.parse()
    expected={
      'registrant':"CrossCheck (Pty) Ltd (previously known as MLCB)"
    , 'full-address':'Kent park, 332 Kent Avenue, Ferndale, Randburg, 2196'
    , 'registration-number':'NCRCB1'
    , 'phone':'0105 909 505'
    , 'fax':'011 388 8582'
    , 'town':'Randburg'
    }
    self.assertDict(observed,expected)

  def dc_local_subtable_parsing_clean(self):
    observed=self.aadielah_moses.parse()
    expected={
      'registrant':'Aadielah Moses'
    , 'full-address':'Debtbrakes: 85 Goulburn Street, Goodwood\n85 Goulburn Street, Goodwood, 7460'
    , 'registration-number':'NCRDC1825'
    , 'phone':'021 592 6766'
    , 'fax':'021 592 6766'
    , 'town':'Goodwood'
    }
    self.assertDict(observed,expected)

  def local_subtable_contacts_raw(self):
    observed=self.aadielah_moses.parse(clean=False)
    expected={
      'registrant':"""
                                        Aadielah Moses                                """
    , 'full-address': """
                                        Debtbrakes: 85 Goulburn Street, Goodwood                                    

                                        85 Goulburn Street, Goodwood, 7460                                    """
    , "phone":"""
                                            021 592 6766                                        """
    , "fax":"""
                                            021 592 6766                                            """
    , "town":"""
                                            Goodwood                                """
    }
    self.assertDict(observed,expected)

  def dc_download_count_subtables(self):
    self.subtables=self.dc.table().subtables()
    #self.assertEqual(len(self.subtables),self.dc.search_total())

  def cb1_download_count_subtables(self):
    self.subtables=self.cb1.table().subtables()
    self.assertEqual(len(self.subtables),11)
    #self.assertEqual(len(self.subtables),self.dc.search_total())

  def dc_download_and_parse(self):
    aadielah_moses=self.dc.table().subtables()[0]
    observed=aadielah_moses.parse()
    expected={
      'registrant':'Aadielah Moses'
    , 'full-address':'Debtbrakes: 85 Goulburn Street, Goodwood\n85 Goulburn Street, Goodwood, 7460'
    , 'registration-number':'NCRDC1825'
    , 'phone':'021 592 6766'
    , 'fax':'021 592 6766'
    , 'town':'Goodwood'
    }
    self.assertDict(observed,expected)

def business_premises():
  s = session()
  s.get(URL)
  s.post(URL,{"ns_BType": "CP1", "ns_SearchText": "*", "ns_Town": "All", "_submit_check_": 1, "ns_cancel": "registered"})
  urls = [row['business_premises'] for row in select('business_premises from cp1 where date_scraped = (select max(date_scraped) from cp1)')]
  for url in urls:
    html = fromstring(s.get(url).content)
    premises = html.xpath('//table[@width="740" and @cellpadding="5"]')
    assert 1 == len(premises), tostring(html)
    trs = premises[0].cssselect('tr')
    datalists = [[td.text_content() for td in tr.cssselect('td')] for tr in trs]
    header = [key.replace(' ', '') for key in datalists.pop(0)]
    data = [dict(zip(header, row)) for row in datalists]
    for row in data:
        row.update({
            'date_scraped': DATE,
            'businessPremisesURL': url
        })
    save(['date_scraped', 'businessPremisesURL'], data, 'business_premises')
    randomsleep()

Test(download=False)
#headquarters()
business_premises()