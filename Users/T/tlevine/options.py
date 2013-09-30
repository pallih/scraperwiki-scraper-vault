from lxml.html import fromstring

def options(parentnode,ignore_first=False,ignore_value=None,ignore_text=None,textname="text",valuename="value"):
  """
  Provide a list of option nodes. Receive parent of values and text()s.
  The node list can be an lxml nodes or a text representation.
  In either case, all child option tags will be used.

  You may specify that the first node, the node with a particular value or the node with a particular text be ignored.
  """
  if type(parentnode)==str:
    parentnode=fromstring(parentnode)

  if ignore_first!=None:
    nodes=parentnode.xpath('option[position()>1]')
  elif ignore_value!=None:
    nodes=parentnode.xpath('option[@value!="%s"]'%ignore_value)
  elif ignore_text!=None:
    nodes=parentnode.xpath('option[text()!="%s"]'%ignore_text)
  else:
    nodes=parentnode.xpath('option')

  return [{textname:node.text,valuename:node.xpath('attribute::value')[0]} for node in nodes]

def test():
  observed1=options(fromstring("""<option value="1">Macaroni</option><option value="2">Cheese</option>"""),textname="text",valuename="text")
  expected1=[{"text":"Macaroni","value":"1"},{"text":"Cheese","value":"2"}]
  assert observed1==expected1

#test()from lxml.html import fromstring

def options(parentnode,ignore_first=False,ignore_value=None,ignore_text=None,textname="text",valuename="value"):
  """
  Provide a list of option nodes. Receive parent of values and text()s.
  The node list can be an lxml nodes or a text representation.
  In either case, all child option tags will be used.

  You may specify that the first node, the node with a particular value or the node with a particular text be ignored.
  """
  if type(parentnode)==str:
    parentnode=fromstring(parentnode)

  if ignore_first!=None:
    nodes=parentnode.xpath('option[position()>1]')
  elif ignore_value!=None:
    nodes=parentnode.xpath('option[@value!="%s"]'%ignore_value)
  elif ignore_text!=None:
    nodes=parentnode.xpath('option[text()!="%s"]'%ignore_text)
  else:
    nodes=parentnode.xpath('option')

  return [{textname:node.text,valuename:node.xpath('attribute::value')[0]} for node in nodes]

def test():
  observed1=options(fromstring("""<option value="1">Macaroni</option><option value="2">Cheese</option>"""),textname="text",valuename="text")
  expected1=[{"text":"Macaroni","value":"1"},{"text":"Cheese","value":"2"}]
  assert observed1==expected1

#test()