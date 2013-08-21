from scraperwiki import swimport
from time import time
swv=swimport('swversion')

def main():
  #Load
  xml=swimport('dsp').dsp('http://www.vbsmutualbank.co.za/ContactUs/ContactUs.htm')

  #Parse
  branches=xml.xpath('//table[@width="556"]/tr[position()>1 and position()<last()]')
  branches_text=[branch.xpath('td[position()=last()]')[0].text_content() for branch in branches]
  d=[parse_branch_text(t) for t in branches_text]

def parse_branch_text(branch_text):
  branchinfo=''
  for line in branch_text.split('\n'):
    branchinfo+=line+'\n'
    if "Tel" in line:
      break
  print branchinfo
  return branchinfo


#  swsave([],d)


#Versioning
swv.swversion()

#Test


main()