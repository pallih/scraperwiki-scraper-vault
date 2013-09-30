from mechanize import Browser
from lxml.html import fromstring
from scraperwiki.sqlite import save

class CoachScheduleBrowser(Browser):
  "Browse the coach schedule with mechanize."

  SELECTS=(
    {'singular':'originState','plural':'originStates'}
  , {'singular':'originCity','plural':'originCities'}
  , {'singular':'destinationState','plural':'destinationStates'}
  , {'singular':'destinationCity','plural':'destinationCities'}
  )

  def __init__(self,auto_open=True):
    Browser.__init__(self)
    if auto_open:
      r=self.open('http://coachusa.com/coachss-v2/index.asp?action=GetSetOriginState')
      self.__setxml(r)

  class ParseError(Exception):
    pass

  def __setxml(self,response):
    text=response.read()
    self.xml=fromstring(text)

  def _coachsubmit(self,formName,selectName,optionValue):
    "Submit a particular form value based on the form name and stuff."
    self.select_form(name=formName)
    self[selectName]=[optionValue]
    r=self.submit()
    self.__setxml(r)

  def _coachextract(self,selectName):
    "Extract options from the form."
    options=self.xml.xpath('//select[@name="%s"]/option' % selectName)
    table=[]
    for option in options[1:]: #Skip the first option because it's empty.
       text=option.xpath('text()')
       if len(text)!=1:
         #Check that there is indeed only one text node.
         raise self.ParseError
       row={
         "value":option.attrib['value']
       , "text":text[0]
       }
       table.append(row)
    return table

  def submit_originState(self,stateValue):
    self._coachsubmit('route1','originState',stateValue)
  def extract_originStates(self):
    return self._coachextract('originState')

  def submit_originCity(self,cityValue):
    self._coachsubmit('route2','originCity',cityValue)
  def extract_originCities(self):
    return self._coachextract('originCity')

  def submit_destinationState(self,stateValue):
    self._coachsubmit('route3','destinationState',stateValue)
  def extract_destinationStates(self):
    return self._coachextract('destinationState')

  def submit_destinationCity(self,cityValue):
    self._coachsubmit('route4','destinationCity',cityValue)
  def extract_destinationCities(self):
    return self._coachextract('destinationCity')

  def is_megabus(self):
    try:
      pagetitle=self.xml.xpath('//td[@class="subHdrTextCellNW"]/text()')[0]
    except:
      return False
    else:
      return pagetitle=='megabus.com'

  def descend(self,selectIndex=0):
    """Traverse the form fields in a depth-first fashion.
Sometimes, a form will provide no responses, but this isn't actually a problem
because the loop just does nothing in that case."""
    select=self.SELECTS[selectIndex]
    options=getattr(self,'extract_%s' % select['plural'])()
    save([],options,select['plural'])
    for option in options:
      getattr(self,'submit_%s' % select['singular'])(option['value'])
      if self.is_megabus():
        option['is_megabus']=True
        save([],option,select['plural'])
      elif selectIndex < len(self.SELECTS)-1:
        self.descend(selectIndex+1)
      #break #Avoid thrashing the server during development

def main():
  cb=CoachScheduleBrowser()
  cb.descend()

main()from mechanize import Browser
from lxml.html import fromstring
from scraperwiki.sqlite import save

class CoachScheduleBrowser(Browser):
  "Browse the coach schedule with mechanize."

  SELECTS=(
    {'singular':'originState','plural':'originStates'}
  , {'singular':'originCity','plural':'originCities'}
  , {'singular':'destinationState','plural':'destinationStates'}
  , {'singular':'destinationCity','plural':'destinationCities'}
  )

  def __init__(self,auto_open=True):
    Browser.__init__(self)
    if auto_open:
      r=self.open('http://coachusa.com/coachss-v2/index.asp?action=GetSetOriginState')
      self.__setxml(r)

  class ParseError(Exception):
    pass

  def __setxml(self,response):
    text=response.read()
    self.xml=fromstring(text)

  def _coachsubmit(self,formName,selectName,optionValue):
    "Submit a particular form value based on the form name and stuff."
    self.select_form(name=formName)
    self[selectName]=[optionValue]
    r=self.submit()
    self.__setxml(r)

  def _coachextract(self,selectName):
    "Extract options from the form."
    options=self.xml.xpath('//select[@name="%s"]/option' % selectName)
    table=[]
    for option in options[1:]: #Skip the first option because it's empty.
       text=option.xpath('text()')
       if len(text)!=1:
         #Check that there is indeed only one text node.
         raise self.ParseError
       row={
         "value":option.attrib['value']
       , "text":text[0]
       }
       table.append(row)
    return table

  def submit_originState(self,stateValue):
    self._coachsubmit('route1','originState',stateValue)
  def extract_originStates(self):
    return self._coachextract('originState')

  def submit_originCity(self,cityValue):
    self._coachsubmit('route2','originCity',cityValue)
  def extract_originCities(self):
    return self._coachextract('originCity')

  def submit_destinationState(self,stateValue):
    self._coachsubmit('route3','destinationState',stateValue)
  def extract_destinationStates(self):
    return self._coachextract('destinationState')

  def submit_destinationCity(self,cityValue):
    self._coachsubmit('route4','destinationCity',cityValue)
  def extract_destinationCities(self):
    return self._coachextract('destinationCity')

  def is_megabus(self):
    try:
      pagetitle=self.xml.xpath('//td[@class="subHdrTextCellNW"]/text()')[0]
    except:
      return False
    else:
      return pagetitle=='megabus.com'

  def descend(self,selectIndex=0):
    """Traverse the form fields in a depth-first fashion.
Sometimes, a form will provide no responses, but this isn't actually a problem
because the loop just does nothing in that case."""
    select=self.SELECTS[selectIndex]
    options=getattr(self,'extract_%s' % select['plural'])()
    save([],options,select['plural'])
    for option in options:
      getattr(self,'submit_%s' % select['singular'])(option['value'])
      if self.is_megabus():
        option['is_megabus']=True
        save([],option,select['plural'])
      elif selectIndex < len(self.SELECTS)-1:
        self.descend(selectIndex+1)
      #break #Avoid thrashing the server during development

def main():
  cb=CoachScheduleBrowser()
  cb.descend()

main()