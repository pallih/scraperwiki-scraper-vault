import scraperwiki
import re



urls = '(?: %s)' % '|'.join("""http telnet gopher file wais
ftp www""".split())
ltrs = r'\w'
gunk = r'/#~:.?+=&%@!\-'
punc = r'.:?\-'
any = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                     'gunk' : gunk,
                                     'punc' : punc }

url = r"""
    \b                            # start at word boundary
        %(urls)s    :?             # need resource and a colon
        [%(any)s]  +?             # followed by one or more
                                  #  of any valid character, but
                                  #  be conservative and take only
                                  #  what you need to....
    (?=                           # look-ahead non-consumptive assertion
            [%(punc)s]*           # either 0 or more punctuation
            (?:   [^%(any)s]      #  followed by a non-url char
                |                 #   or end of the string
                  $
            )
    )
    """ % {'urls' : urls,
           'any' : any,
           'punc' : punc }

url_re = re.compile(url, re.VERBOSE | re.MULTILINE)








strTest = ' Kevin Carroll Election statement: I’m not just another career politician chasing a job vacancy. I’m Luton born and bred, fiercely proud of my home town and county and determined that Bedfordshire should get the best policing in Britain. A devoted father, full-time carpenter, keen amateur sportsman and community activist, I understand the devastation that crime and antisocial behaviour can bring to individuals, families and communities. I am dedicated to fighting crime and extremism, building trust between police and local people and restoring harmony to a county that has been damaged by community tensions. I believe it’s time to stop being soft on criminals and troublemakers. I intend to make Bedfordshire a place where criminals truly fear the consequences of crime; a place where women, children, the elderly and vulnerable feel safe by day and by night. My policing priorities • Zero tolerance for extremist and terrorist activity in Bedfordshire • Zero tolerance for possession of knives and other weapons • Decisive measures to cut drug-dealing and drug-related offences • Putting victims’ rights before criminals’ • Zero tolerance for antisocial behaviour • Firm measures to protect children from dangerous drivers • An end to so-called ‘honour’ crimes • An end to politically correct policing. I pledge to fight crime fearlessly and to make the hard decisions needed to improve Bedfordshire policing in a time of budget cuts. If you want tough action on crime, extremism and antisocial behaviour; if you want more police officers on the beat in your neighbourhood; if you want less red tape and more catching criminals, vote Kevin Carroll on 15th November. Vote Kevin Carroll – the people’s candidate for Police and Crime Commissioner! Prepared by: Simon Bennett, 15 Mount Camel, Camelford, Cornwall, PL32 9UW. Contact Details: http://www.KevinCarroll.org '



#website = url_re.findall(strTest)
#print(website)
#if len(website) != 0:
#    websites = ""
#    for wbs in website:
#        websites = websites + wbs +"\n"   
#    candidate['website'] = websites



1+1
#print(_)

print(locals())






import scraperwiki
import re



urls = '(?: %s)' % '|'.join("""http telnet gopher file wais
ftp www""".split())
ltrs = r'\w'
gunk = r'/#~:.?+=&%@!\-'
punc = r'.:?\-'
any = "%(ltrs)s%(gunk)s%(punc)s" % { 'ltrs' : ltrs,
                                     'gunk' : gunk,
                                     'punc' : punc }

url = r"""
    \b                            # start at word boundary
        %(urls)s    :?             # need resource and a colon
        [%(any)s]  +?             # followed by one or more
                                  #  of any valid character, but
                                  #  be conservative and take only
                                  #  what you need to....
    (?=                           # look-ahead non-consumptive assertion
            [%(punc)s]*           # either 0 or more punctuation
            (?:   [^%(any)s]      #  followed by a non-url char
                |                 #   or end of the string
                  $
            )
    )
    """ % {'urls' : urls,
           'any' : any,
           'punc' : punc }

url_re = re.compile(url, re.VERBOSE | re.MULTILINE)








strTest = ' Kevin Carroll Election statement: I’m not just another career politician chasing a job vacancy. I’m Luton born and bred, fiercely proud of my home town and county and determined that Bedfordshire should get the best policing in Britain. A devoted father, full-time carpenter, keen amateur sportsman and community activist, I understand the devastation that crime and antisocial behaviour can bring to individuals, families and communities. I am dedicated to fighting crime and extremism, building trust between police and local people and restoring harmony to a county that has been damaged by community tensions. I believe it’s time to stop being soft on criminals and troublemakers. I intend to make Bedfordshire a place where criminals truly fear the consequences of crime; a place where women, children, the elderly and vulnerable feel safe by day and by night. My policing priorities • Zero tolerance for extremist and terrorist activity in Bedfordshire • Zero tolerance for possession of knives and other weapons • Decisive measures to cut drug-dealing and drug-related offences • Putting victims’ rights before criminals’ • Zero tolerance for antisocial behaviour • Firm measures to protect children from dangerous drivers • An end to so-called ‘honour’ crimes • An end to politically correct policing. I pledge to fight crime fearlessly and to make the hard decisions needed to improve Bedfordshire policing in a time of budget cuts. If you want tough action on crime, extremism and antisocial behaviour; if you want more police officers on the beat in your neighbourhood; if you want less red tape and more catching criminals, vote Kevin Carroll on 15th November. Vote Kevin Carroll – the people’s candidate for Police and Crime Commissioner! Prepared by: Simon Bennett, 15 Mount Camel, Camelford, Cornwall, PL32 9UW. Contact Details: http://www.KevinCarroll.org '



#website = url_re.findall(strTest)
#print(website)
#if len(website) != 0:
#    websites = ""
#    for wbs in website:
#        websites = websites + wbs +"\n"   
#    candidate['website'] = websites



1+1
#print(_)

print(locals())






