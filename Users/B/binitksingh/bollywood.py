import scraperwiki
import urllib2
import lxml.etree
import sys
import re

def wiki12():
    print 'wiki12'
    loop=0
    scraperwiki.sqlite.execute("create table wiki11 (id_ int,  month string, day string, title string, genere string, director string, cast string, CBFC_rating string)")



    id_count = 0
    table_count=0

    rev = page.find(".//rev")
    content = rev.text
    #print content
    month_table_list=content.split('class="wikitable"')
    del month_table_list[0]



    for table in month_table_list:

        table_row_list= table.split('|-')
        table_count= table_count+1
        row_count=0
        for row in table_row_list:
            print 'table no:',table_count
            db_list = []
            row_count= row_count+1
            print 'row no:',row_count


################################   replacing all  unwanted characters from row      #######################################

            row = row.replace('\n','')
            row = row.replace("'","")
            row = row.replace("<br>","")
            row = row.replace("<br/>","")
            row = row.replace("<br />","")
            row = row.replace("#","")
            row = row.replace("[[","")
            row = row.replace("]]","")
            row = row.replace('"','')
            row = row.replace('!','')
            row = row.replace('&','')
            row = row.replace(':','')
            row = row.replace("style=text-align:center;","")
            row = row.replace('style=text-aligncenter;','')
            row = row.replace('background','')
            row = row.replace('textcolor','')
            row = row.replace(']',')')
            row = row.replace('[','(')
            row = row.replace('<big>','')


            print row



    ################################   Defining regular expression to match row       #######################################




            reg=r'(\|\s+rowspan=(\d+)[\w\s;]+\|\s+(\w+))?(\|(\srowspan=(\d+))?[\w\s;]+\|\s(\d+))?\|\s?([,\?\.%\w\s\(\)]+\|)?([,\-\w\s\?!%\.]+)\s?\|\|\s([\-\w\s]+\|)?([\-\w\s]+)(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?\s?\|\|\s?([,\(\)\.\w\-\s]+)?\|?([,\(\)\.\w\-\s]+)\s?\|\|([\-\w\s,\|\(\)\.]+)(<[\.\w=\s/]+>({?{?[,\+\?\w\s\|=\./\-\(\)]+}?}?</ref>)?)?(<[\.\w=\s/]+>({{[,\+\?\w\s\|=\./\-\(\)]+}}</ref>)?)?(?:\s?\s?\|\|\s?([\w/]+))?'




            match=re.search(reg,row)
            if match:
                print 'yes'
                loop=1
                
            
            ################################   logic to calculate month_value      #######################################
            
                if match.group(1) and match.group(4):

                    month_count = match.group(2)
                    month_value = match.group(3)

                id_count = id_count+1
                db_list.append(id_count)                                                     ### incrementing id_count and appending it into list db_list

                  
                if month_count:
                    db_list.append(month_value)                                              ### appending month_value into list db_list
                    month_count = int(month_count)-1
                else:
                    db_list.append(0)



################################   logic to calculate day_value      ####################################### 

                if match.group(1) and not(match.group(4)):

                    if match.group(2) and match.group(3):

                        day_count = match.group(2)
                        day_value = match.group(3)

                    elif match.group(3):

                        day_count=1
                        day_value= match.group(3)

                elif match.group(4):

                    if match.group(5) and match.group(7):

                        day_count=match.group(6)
                        day_value=match.group(7)

                    elif match.group(7):

                        day_count=1
                        day_value=match.group(7)
            
            
                if day_count:

                    db_list.append(day_value)                                                 ### appending day_value into list db_list
                    day_count = int(day_count) - 1

                else:
                    db_list.append(0)

                #db_list.append(match.group(8))                                                ### appending title_href into list db_list



                db_list.append(match.group(9))                                                ### appending title into list db_list

################################   logic to append genere in list      #######################################


                genere_list=[]
                if match.group(11):
                     genere_list.append(str(match.group(11)))
                if match.group(14):
                     genere_list.append(str(match.group(14)))
                if match.group(17):
                     genere_list.append(str(match.group(17)))
            
                genere_str = '/'.join(genere_list)
                print genere_str
                db_list.append(genere_str)                                                     ### appending genere into list db_list


################################   logic to append director in list      #######################################
            
            
                director_list=[]
                if match.group(18):
                    director_list.append(str(match.group(18)))
                if match.group(19):
                    director_list.append(str(match.group(19)))
            
                director_str = ','.join(director_list)
                db_list.append(director_str)

################################   logic to append actor in list          #######################################


                db_list.append(str(match.group(20)))                                           ### appending cast into list db_list


################################   logic to append CBFC Rating in list     #######################################
                if match.group(25):

                    db_list.append(str(match.group(25)))
                else:
                    db_list.append(str('not given'))                                           ### appending CBFC into list db_list



################################   inserting values of list db_list into table       #######################################
        
                try:

                    scraperwiki.sqlite.execute("insert into wiki11 values (?,?,?,?,?,?,?,?)", db_list)
                    scraperwiki.sqlite.commit()
                except Exception,e:
                    print e
                    continue            
            else:
                print 'no'
                if loop:
                    if month_value=='JUN':
                        month_value='JUL'
                        month_count=10
            
                if table_count>1 and row_count>2:
                    if day_count==0:
                        day_value= int(day_value) + 7
                        if int(day_value)>31:
                                day_value= int(day_value) - 31
                        elif int(day_value)>30:
                                day_value= int(day_value) - 30
                            
                    
                        day_count=5 




#########################             end of function wiki 12                                             ############################################ 






def wiki10():
    print 'wiki10'
    loop=0
    scraperwiki.sqlite.execute("create table wiki8 (id_ int,  month string, day string, title string, genere string, director string, cast string, CBFC_rating string)")



    id_count = 0
    table_count=0

    rev = page.find(".//rev")
    content = rev.text
    #print content
    month_table_list=content.split('class="wikitable"')
    del month_table_list[0]



    for table in month_table_list:

        table_row_list= table.split('|-')
        table_count= table_count+1
        row_count=0
        for row in table_row_list:
            print 'table no:',table_count
            db_list = []
            row_count= row_count+1
            print 'row no:',row_count


################################   replacing all  unwanted characters from row      #######################################

            row = row.replace('\n','')
            row = row.replace("'","")
            row = row.replace("<br>","")
            row = row.replace("</br>","")
            row = row.replace("<br/>","")
            row = row.replace("<br />","")
            row = row.replace("#","")
            row = row.replace("[[","")
            row = row.replace("]]","")
            row = row.replace('"','')
            row = row.replace('!','')
            row = row.replace('&','')
            row = row.replace(':','')
            row = row.replace("style=text-align:center;","")
            row = row.replace('style=text-aligncenter;','')
            row = row.replace('background','')
            row = row.replace('textcolor','')
            row = row.replace(']',')')
            row = row.replace('[','(')
            row = row.replace('<big>','')


            print row



################################   Defining regular expression to match row       #######################################



            reg=r'(\|\s+rowspan=(\d+)[\w\s;=]+\|\s+(\w+))?\s?(\|(\srowspan=(\d+))?[\w\s;=]+\|\s(\d+))?\s?\|\|?\s*([,\?\.%\w\s\(\);]+\|)?([,\-\w\s\?!%\.]+)\s?\|\|\s?([;,\(\)\.\w\-\s]+)?\|?([,\(\)\.\w\-\s]+)\s?\|\|([\-\w\s,\|\(\)\.]+)\|\|(?:\s([\-\w\s]+\|)?([\-\w\s]+)(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?\s?)?(<[\.\w=\s/]+>({?{?[,\+\?\w\s\|=\./\-\(\)]+}?}?</ref>)?)?(<[\.\w=\s/]+>({{[,\+\?\w\s\|=\./\-\(\)]+}}</ref>)?)?(?:\s?\s?\|\|\s?([\w/]+))?'




            match=re.search(reg,row)
            if match:
                print 'yes'
                loop=1
                
                

        ################################   logic to calculate month_value      #######################################
            
                if match.group(1) and match.group(4):

                    month_count = match.group(2)
                    month_value = match.group(3)

                id_count = id_count+1
                db_list.append(id_count)                                                     ### incrementing id_count and appending it into list db_list

                  
                if month_count:
                    db_list.append(month_value)                                              ### appending month_value into list db_list
                    month_count = int(month_count)-1
                else:
                    db_list.append(0)



################################   logic to calculate day_value      #######################################

                if match.group(1) and not(match.group(4)):

                    if match.group(2) and match.group(3):

                        day_count = match.group(2)
                        day_value = match.group(3)

                    elif match.group(3):

                        day_count=1
                        day_value= match.group(3)

                elif match.group(4):

                    if match.group(5) and match.group(7):

                        day_count=match.group(6)
                        day_value=match.group(7)

                    elif match.group(7):

                        day_count=1
                        day_value=match.group(7)
            
            
                if day_count:

                    db_list.append(day_value)                                                 ### appending day_value into list db_list
                    day_count = int(day_count) - 1

                else:
                    db_list.append(0)

                #db_list.append(match.group(8))                                                ### appending title_href into list db_list



                db_list.append(match.group(9))                                                ### appending title into list db_list

################################   logic to append genere in list      #######################################


                genere_list=[]
                if match.group(14):
                     genere_list.append(str(match.group(14)))
                if match.group(17):
                     genere_list.append(str(match.group(17)))
                if match.group(20):
                     genere_list.append(str(match.group(20)))
            
                genere_str = '/'.join(genere_list)
                print genere_str
                db_list.append(genere_str)                                                     ### appending genere into list db_list


################################   logic to append director in list      #######################################
            
            
                director_list=[]
                if match.group(10):
                    director_list.append(str(match.group(10)))
                if match.group(11):
                    director_list.append(str(match.group(11)))
            
                director_str = ','.join(director_list)
                db_list.append(director_str)

################################   logic to append actor in list          #######################################


                db_list.append(str(match.group(12)))                                           ### appending cast into list db_list


################################   logic to append CBFC Rating in list     #######################################


                db_list.append(str('not given'))                                           ### appending CBFC into list db_list



################################   inserting values of list db_list into table       #######################################
        
                try:

                    scraperwiki.sqlite.execute("insert into wiki8 values (?,?,?,?,?,?,?,?)", db_list)
                    scraperwiki.sqlite.commit()
                except Exception,e:
                    print e
                    continue            
            else:
                print 'no'
                if loop:
                    if month_value=='JUN':
                        month_value='JUL'
                        month_count=10
            
                if table_count>1 and row_count>2:
                    if day_count==0:
                        day_value= int(day_value) + 7
                        if int(day_value)>31:
                                day_value= int(day_value) - 31
                        elif int(day_value)>30:
                                day_value= int(day_value) - 30
                            
                    
                        day_count=5



#########################             end of function wiki 10                                             ############################################






def wiki7():
    print'wiki 7'
    loop=0
    scraperwiki.sqlite.execute("create table wiki4 (id_ int,  month string, day string, title string, genere string, director string, cast string, CBFC_rating string)")



    id_count = 0
    table_count=0

    rev = page.find(".//rev")
    content = rev.text
    #print content
    month_table_list=content.split('class="wikitable"')
    del month_table_list[0]



    for table in month_table_list:

        table_row_list= table.split('|-')
        table_count= table_count+1
        row_count=0
        for row in table_row_list:
            print 'table no:',table_count
            db_list = []
            row_count= row_count+1
            print 'row no:',row_count


################################   replacing all  unwanted characters from row      #######################################

            row = row.replace('\n','')
            row = row.replace("'","")
            row = row.replace("<br>","")
            row = row.replace("</br>","")
            row = row.replace("<br/>","")
            row = row.replace("<br />","")
            row = row.replace("#","")
            row = row.replace("[[","")
            row = row.replace("]]","")
            row = row.replace('"','')
            row = row.replace('!','')
            row = row.replace('&','')
            row = row.replace(':','')
            row = row.replace("style=text-align:center;","")
            row = row.replace('style=text-aligncenter;','')
            row = row.replace('background','')
            row = row.replace('textcolor','')
            row = row.replace(']',')')
            row = row.replace('[','(')
            row = row.replace('<big>','')


            print row



################################   Defining regular expression to match row       #######################################



            reg=r'(?:(\|\s+rowspan=(\d+)[\w\s;=]+\|\s+(\w+))?\s?(\|(\srowspan=(\d+))?[\w\s;=]+\|\s(\d+))?\s?)?\|\|?\s*([,\?\.%\w\s\(\);]+\|)?([,\-\w\s\?!%\.]+)\s?\|\|\s?([;,\(\)\.\w\-\s]+)?\|?([,\(\)\.\w\-\s]+)\s?\|\|([\-\w\s,\|\(\)\.]+?)\|\|(?:\s([\-\w\s]+\|)?([\-\w\s]+)(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?\s?)?(<[\.\w=\s/]+>({?{?[,\+\?\w\s\|=\./\-\(\)]+}?}?</ref>)?)?(<[\.\w=\s/]+>({{[,\+\?\w\s\|=\./\-\(\)]+}}</ref>)?)?(?:\s?\s?\|\|\s?([\w/]+))?'




            match=re.search(reg,row)
            if match:
                print 'yes'
                loop=1
                


        ################################   logic to calculate month_value      #######################################
           

                if match.group(1) and match.group(4):

                    month_count = match.group(2)
                    month_value = match.group(3)
                else:
                    month_count=0
            
                id_count = id_count+1
                db_list.append(id_count)                                                     ### incrementing id_count and appending it into list db_list
            
                  
                if month_count:
                    db_list.append(month_value)                                              ### appending month_value into list db_list
                    month_count = int(month_count)-1
                else:
                    db_list.append(0)



################################   logic to calculate day_value      #######################################

                if match.group(1) and not(match.group(4)):

                    if match.group(2) and match.group(3):

                        day_count = match.group(2)
                        day_value = match.group(3)

                    elif match.group(3):

                        day_count=1
                        day_value= match.group(3)
                    else:
                        day_count=0

                elif match.group(4):

                    if match.group(5) and match.group(7):

                        day_count=match.group(6)
                        day_value=match.group(7)

                    elif match.group(7):

                        day_count=1
                        day_value=match.group(7)
                    else:
                        day_count=0
                else:
                    day_count=0
            
                if day_count:

                    db_list.append(day_value)                                                 ### appending day_value into list db_list
                    day_count = int(day_count) - 1

                else:
                    db_list.append(0)

                #db_list.append(match.group(8))                                                ### appending title_href into list db_list



                db_list.append(match.group(9))                                                ### appending title into list db_list

################################   logic to append genere in list      #######################################


                genere_list=[]
                if match.group(14):
                     genere_list.append(str(match.group(14)))
                if match.group(17):
                     genere_list.append(str(match.group(17)))
                if match.group(20):
                     genere_list.append(str(match.group(20)))
            
                genere_str = '/'.join(genere_list)
                print genere_str
                db_list.append(genere_str)                                                     ### appending genere into list db_list


################################   logic to append director in list      #######################################
            
            
                director_list=[]
                if match.group(10):
                    director_list.append(str(match.group(10)))
                if match.group(11):
                    director_list.append(str(match.group(11)))
            
                director_str = ','.join(director_list)
                db_list.append(director_str)

################################   logic to append actor in list          #######################################


                db_list.append(str(match.group(12)))                                           ### appending cast into list db_list


################################   logic to append CBFC Rating in list     #######################################


                db_list.append(str('not given'))                                           ### appending CBFC into list db_list



################################   inserting values of list db_list into table       #######################################
        
                try:

                    scraperwiki.sqlite.execute("insert into wiki4 values (?,?,?,?,?,?,?,?)", db_list)
                    scraperwiki.sqlite.commit()
                except Exception,e:
                    print e
                    continue  
                  
            else:
                print 'no'
                


#########################             end of function wiki 07                                             ############################################










print 'hello u r in main block'

f= urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&redirects=yes&titles=List_of_Bollywood_films_of_2005&rvprop=timestamp|user|comment|content")

print 'file opened'
doc = lxml.etree.parse(f)

root = doc.getroot()
data =lxml.etree.tostring(root)

page = root.find(".//page")
title = page.get("title")
print title

functions = {'List of Bollywood films of 2012': wiki12,
             'List of Bollywood films of 2011': wiki12,
             'List of Bollywood films of 2010': wiki10,
             'List of Bollywood films of 2009': wiki10,
             'List of Bollywood films of 2008': wiki10,
             'List of Bollywood films of 2007': wiki7,
             'others':wiki7}


if title not in functions.keys():
    title='others'

func =functions[title]
func()


import scraperwiki
import urllib2
import lxml.etree
import sys
import re

def wiki12():
    print 'wiki12'
    loop=0
    scraperwiki.sqlite.execute("create table wiki11 (id_ int,  month string, day string, title string, genere string, director string, cast string, CBFC_rating string)")



    id_count = 0
    table_count=0

    rev = page.find(".//rev")
    content = rev.text
    #print content
    month_table_list=content.split('class="wikitable"')
    del month_table_list[0]



    for table in month_table_list:

        table_row_list= table.split('|-')
        table_count= table_count+1
        row_count=0
        for row in table_row_list:
            print 'table no:',table_count
            db_list = []
            row_count= row_count+1
            print 'row no:',row_count


################################   replacing all  unwanted characters from row      #######################################

            row = row.replace('\n','')
            row = row.replace("'","")
            row = row.replace("<br>","")
            row = row.replace("<br/>","")
            row = row.replace("<br />","")
            row = row.replace("#","")
            row = row.replace("[[","")
            row = row.replace("]]","")
            row = row.replace('"','')
            row = row.replace('!','')
            row = row.replace('&','')
            row = row.replace(':','')
            row = row.replace("style=text-align:center;","")
            row = row.replace('style=text-aligncenter;','')
            row = row.replace('background','')
            row = row.replace('textcolor','')
            row = row.replace(']',')')
            row = row.replace('[','(')
            row = row.replace('<big>','')


            print row



    ################################   Defining regular expression to match row       #######################################




            reg=r'(\|\s+rowspan=(\d+)[\w\s;]+\|\s+(\w+))?(\|(\srowspan=(\d+))?[\w\s;]+\|\s(\d+))?\|\s?([,\?\.%\w\s\(\)]+\|)?([,\-\w\s\?!%\.]+)\s?\|\|\s([\-\w\s]+\|)?([\-\w\s]+)(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?\s?\|\|\s?([,\(\)\.\w\-\s]+)?\|?([,\(\)\.\w\-\s]+)\s?\|\|([\-\w\s,\|\(\)\.]+)(<[\.\w=\s/]+>({?{?[,\+\?\w\s\|=\./\-\(\)]+}?}?</ref>)?)?(<[\.\w=\s/]+>({{[,\+\?\w\s\|=\./\-\(\)]+}}</ref>)?)?(?:\s?\s?\|\|\s?([\w/]+))?'




            match=re.search(reg,row)
            if match:
                print 'yes'
                loop=1
                
            
            ################################   logic to calculate month_value      #######################################
            
                if match.group(1) and match.group(4):

                    month_count = match.group(2)
                    month_value = match.group(3)

                id_count = id_count+1
                db_list.append(id_count)                                                     ### incrementing id_count and appending it into list db_list

                  
                if month_count:
                    db_list.append(month_value)                                              ### appending month_value into list db_list
                    month_count = int(month_count)-1
                else:
                    db_list.append(0)



################################   logic to calculate day_value      ####################################### 

                if match.group(1) and not(match.group(4)):

                    if match.group(2) and match.group(3):

                        day_count = match.group(2)
                        day_value = match.group(3)

                    elif match.group(3):

                        day_count=1
                        day_value= match.group(3)

                elif match.group(4):

                    if match.group(5) and match.group(7):

                        day_count=match.group(6)
                        day_value=match.group(7)

                    elif match.group(7):

                        day_count=1
                        day_value=match.group(7)
            
            
                if day_count:

                    db_list.append(day_value)                                                 ### appending day_value into list db_list
                    day_count = int(day_count) - 1

                else:
                    db_list.append(0)

                #db_list.append(match.group(8))                                                ### appending title_href into list db_list



                db_list.append(match.group(9))                                                ### appending title into list db_list

################################   logic to append genere in list      #######################################


                genere_list=[]
                if match.group(11):
                     genere_list.append(str(match.group(11)))
                if match.group(14):
                     genere_list.append(str(match.group(14)))
                if match.group(17):
                     genere_list.append(str(match.group(17)))
            
                genere_str = '/'.join(genere_list)
                print genere_str
                db_list.append(genere_str)                                                     ### appending genere into list db_list


################################   logic to append director in list      #######################################
            
            
                director_list=[]
                if match.group(18):
                    director_list.append(str(match.group(18)))
                if match.group(19):
                    director_list.append(str(match.group(19)))
            
                director_str = ','.join(director_list)
                db_list.append(director_str)

################################   logic to append actor in list          #######################################


                db_list.append(str(match.group(20)))                                           ### appending cast into list db_list


################################   logic to append CBFC Rating in list     #######################################
                if match.group(25):

                    db_list.append(str(match.group(25)))
                else:
                    db_list.append(str('not given'))                                           ### appending CBFC into list db_list



################################   inserting values of list db_list into table       #######################################
        
                try:

                    scraperwiki.sqlite.execute("insert into wiki11 values (?,?,?,?,?,?,?,?)", db_list)
                    scraperwiki.sqlite.commit()
                except Exception,e:
                    print e
                    continue            
            else:
                print 'no'
                if loop:
                    if month_value=='JUN':
                        month_value='JUL'
                        month_count=10
            
                if table_count>1 and row_count>2:
                    if day_count==0:
                        day_value= int(day_value) + 7
                        if int(day_value)>31:
                                day_value= int(day_value) - 31
                        elif int(day_value)>30:
                                day_value= int(day_value) - 30
                            
                    
                        day_count=5 




#########################             end of function wiki 12                                             ############################################ 






def wiki10():
    print 'wiki10'
    loop=0
    scraperwiki.sqlite.execute("create table wiki8 (id_ int,  month string, day string, title string, genere string, director string, cast string, CBFC_rating string)")



    id_count = 0
    table_count=0

    rev = page.find(".//rev")
    content = rev.text
    #print content
    month_table_list=content.split('class="wikitable"')
    del month_table_list[0]



    for table in month_table_list:

        table_row_list= table.split('|-')
        table_count= table_count+1
        row_count=0
        for row in table_row_list:
            print 'table no:',table_count
            db_list = []
            row_count= row_count+1
            print 'row no:',row_count


################################   replacing all  unwanted characters from row      #######################################

            row = row.replace('\n','')
            row = row.replace("'","")
            row = row.replace("<br>","")
            row = row.replace("</br>","")
            row = row.replace("<br/>","")
            row = row.replace("<br />","")
            row = row.replace("#","")
            row = row.replace("[[","")
            row = row.replace("]]","")
            row = row.replace('"','')
            row = row.replace('!','')
            row = row.replace('&','')
            row = row.replace(':','')
            row = row.replace("style=text-align:center;","")
            row = row.replace('style=text-aligncenter;','')
            row = row.replace('background','')
            row = row.replace('textcolor','')
            row = row.replace(']',')')
            row = row.replace('[','(')
            row = row.replace('<big>','')


            print row



################################   Defining regular expression to match row       #######################################



            reg=r'(\|\s+rowspan=(\d+)[\w\s;=]+\|\s+(\w+))?\s?(\|(\srowspan=(\d+))?[\w\s;=]+\|\s(\d+))?\s?\|\|?\s*([,\?\.%\w\s\(\);]+\|)?([,\-\w\s\?!%\.]+)\s?\|\|\s?([;,\(\)\.\w\-\s]+)?\|?([,\(\)\.\w\-\s]+)\s?\|\|([\-\w\s,\|\(\)\.]+)\|\|(?:\s([\-\w\s]+\|)?([\-\w\s]+)(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?\s?)?(<[\.\w=\s/]+>({?{?[,\+\?\w\s\|=\./\-\(\)]+}?}?</ref>)?)?(<[\.\w=\s/]+>({{[,\+\?\w\s\|=\./\-\(\)]+}}</ref>)?)?(?:\s?\s?\|\|\s?([\w/]+))?'




            match=re.search(reg,row)
            if match:
                print 'yes'
                loop=1
                
                

        ################################   logic to calculate month_value      #######################################
            
                if match.group(1) and match.group(4):

                    month_count = match.group(2)
                    month_value = match.group(3)

                id_count = id_count+1
                db_list.append(id_count)                                                     ### incrementing id_count and appending it into list db_list

                  
                if month_count:
                    db_list.append(month_value)                                              ### appending month_value into list db_list
                    month_count = int(month_count)-1
                else:
                    db_list.append(0)



################################   logic to calculate day_value      #######################################

                if match.group(1) and not(match.group(4)):

                    if match.group(2) and match.group(3):

                        day_count = match.group(2)
                        day_value = match.group(3)

                    elif match.group(3):

                        day_count=1
                        day_value= match.group(3)

                elif match.group(4):

                    if match.group(5) and match.group(7):

                        day_count=match.group(6)
                        day_value=match.group(7)

                    elif match.group(7):

                        day_count=1
                        day_value=match.group(7)
            
            
                if day_count:

                    db_list.append(day_value)                                                 ### appending day_value into list db_list
                    day_count = int(day_count) - 1

                else:
                    db_list.append(0)

                #db_list.append(match.group(8))                                                ### appending title_href into list db_list



                db_list.append(match.group(9))                                                ### appending title into list db_list

################################   logic to append genere in list      #######################################


                genere_list=[]
                if match.group(14):
                     genere_list.append(str(match.group(14)))
                if match.group(17):
                     genere_list.append(str(match.group(17)))
                if match.group(20):
                     genere_list.append(str(match.group(20)))
            
                genere_str = '/'.join(genere_list)
                print genere_str
                db_list.append(genere_str)                                                     ### appending genere into list db_list


################################   logic to append director in list      #######################################
            
            
                director_list=[]
                if match.group(10):
                    director_list.append(str(match.group(10)))
                if match.group(11):
                    director_list.append(str(match.group(11)))
            
                director_str = ','.join(director_list)
                db_list.append(director_str)

################################   logic to append actor in list          #######################################


                db_list.append(str(match.group(12)))                                           ### appending cast into list db_list


################################   logic to append CBFC Rating in list     #######################################


                db_list.append(str('not given'))                                           ### appending CBFC into list db_list



################################   inserting values of list db_list into table       #######################################
        
                try:

                    scraperwiki.sqlite.execute("insert into wiki8 values (?,?,?,?,?,?,?,?)", db_list)
                    scraperwiki.sqlite.commit()
                except Exception,e:
                    print e
                    continue            
            else:
                print 'no'
                if loop:
                    if month_value=='JUN':
                        month_value='JUL'
                        month_count=10
            
                if table_count>1 and row_count>2:
                    if day_count==0:
                        day_value= int(day_value) + 7
                        if int(day_value)>31:
                                day_value= int(day_value) - 31
                        elif int(day_value)>30:
                                day_value= int(day_value) - 30
                            
                    
                        day_count=5



#########################             end of function wiki 10                                             ############################################






def wiki7():
    print'wiki 7'
    loop=0
    scraperwiki.sqlite.execute("create table wiki4 (id_ int,  month string, day string, title string, genere string, director string, cast string, CBFC_rating string)")



    id_count = 0
    table_count=0

    rev = page.find(".//rev")
    content = rev.text
    #print content
    month_table_list=content.split('class="wikitable"')
    del month_table_list[0]



    for table in month_table_list:

        table_row_list= table.split('|-')
        table_count= table_count+1
        row_count=0
        for row in table_row_list:
            print 'table no:',table_count
            db_list = []
            row_count= row_count+1
            print 'row no:',row_count


################################   replacing all  unwanted characters from row      #######################################

            row = row.replace('\n','')
            row = row.replace("'","")
            row = row.replace("<br>","")
            row = row.replace("</br>","")
            row = row.replace("<br/>","")
            row = row.replace("<br />","")
            row = row.replace("#","")
            row = row.replace("[[","")
            row = row.replace("]]","")
            row = row.replace('"','')
            row = row.replace('!','')
            row = row.replace('&','')
            row = row.replace(':','')
            row = row.replace("style=text-align:center;","")
            row = row.replace('style=text-aligncenter;','')
            row = row.replace('background','')
            row = row.replace('textcolor','')
            row = row.replace(']',')')
            row = row.replace('[','(')
            row = row.replace('<big>','')


            print row



################################   Defining regular expression to match row       #######################################



            reg=r'(?:(\|\s+rowspan=(\d+)[\w\s;=]+\|\s+(\w+))?\s?(\|(\srowspan=(\d+))?[\w\s;=]+\|\s(\d+))?\s?)?\|\|?\s*([,\?\.%\w\s\(\);]+\|)?([,\-\w\s\?!%\.]+)\s?\|\|\s?([;,\(\)\.\w\-\s]+)?\|?([,\(\)\.\w\-\s]+)\s?\|\|([\-\w\s,\|\(\)\.]+?)\|\|(?:\s([\-\w\s]+\|)?([\-\w\s]+)(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?(/?,?([\-\w\s\(\)]+\|)?([\-\w\s]+))?\s?)?(<[\.\w=\s/]+>({?{?[,\+\?\w\s\|=\./\-\(\)]+}?}?</ref>)?)?(<[\.\w=\s/]+>({{[,\+\?\w\s\|=\./\-\(\)]+}}</ref>)?)?(?:\s?\s?\|\|\s?([\w/]+))?'




            match=re.search(reg,row)
            if match:
                print 'yes'
                loop=1
                


        ################################   logic to calculate month_value      #######################################
           

                if match.group(1) and match.group(4):

                    month_count = match.group(2)
                    month_value = match.group(3)
                else:
                    month_count=0
            
                id_count = id_count+1
                db_list.append(id_count)                                                     ### incrementing id_count and appending it into list db_list
            
                  
                if month_count:
                    db_list.append(month_value)                                              ### appending month_value into list db_list
                    month_count = int(month_count)-1
                else:
                    db_list.append(0)



################################   logic to calculate day_value      #######################################

                if match.group(1) and not(match.group(4)):

                    if match.group(2) and match.group(3):

                        day_count = match.group(2)
                        day_value = match.group(3)

                    elif match.group(3):

                        day_count=1
                        day_value= match.group(3)
                    else:
                        day_count=0

                elif match.group(4):

                    if match.group(5) and match.group(7):

                        day_count=match.group(6)
                        day_value=match.group(7)

                    elif match.group(7):

                        day_count=1
                        day_value=match.group(7)
                    else:
                        day_count=0
                else:
                    day_count=0
            
                if day_count:

                    db_list.append(day_value)                                                 ### appending day_value into list db_list
                    day_count = int(day_count) - 1

                else:
                    db_list.append(0)

                #db_list.append(match.group(8))                                                ### appending title_href into list db_list



                db_list.append(match.group(9))                                                ### appending title into list db_list

################################   logic to append genere in list      #######################################


                genere_list=[]
                if match.group(14):
                     genere_list.append(str(match.group(14)))
                if match.group(17):
                     genere_list.append(str(match.group(17)))
                if match.group(20):
                     genere_list.append(str(match.group(20)))
            
                genere_str = '/'.join(genere_list)
                print genere_str
                db_list.append(genere_str)                                                     ### appending genere into list db_list


################################   logic to append director in list      #######################################
            
            
                director_list=[]
                if match.group(10):
                    director_list.append(str(match.group(10)))
                if match.group(11):
                    director_list.append(str(match.group(11)))
            
                director_str = ','.join(director_list)
                db_list.append(director_str)

################################   logic to append actor in list          #######################################


                db_list.append(str(match.group(12)))                                           ### appending cast into list db_list


################################   logic to append CBFC Rating in list     #######################################


                db_list.append(str('not given'))                                           ### appending CBFC into list db_list



################################   inserting values of list db_list into table       #######################################
        
                try:

                    scraperwiki.sqlite.execute("insert into wiki4 values (?,?,?,?,?,?,?,?)", db_list)
                    scraperwiki.sqlite.commit()
                except Exception,e:
                    print e
                    continue  
                  
            else:
                print 'no'
                


#########################             end of function wiki 07                                             ############################################










print 'hello u r in main block'

f= urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&redirects=yes&titles=List_of_Bollywood_films_of_2005&rvprop=timestamp|user|comment|content")

print 'file opened'
doc = lxml.etree.parse(f)

root = doc.getroot()
data =lxml.etree.tostring(root)

page = root.find(".//page")
title = page.get("title")
print title

functions = {'List of Bollywood films of 2012': wiki12,
             'List of Bollywood films of 2011': wiki12,
             'List of Bollywood films of 2010': wiki10,
             'List of Bollywood films of 2009': wiki10,
             'List of Bollywood films of 2008': wiki10,
             'List of Bollywood films of 2007': wiki7,
             'others':wiki7}


if title not in functions.keys():
    title='others'

func =functions[title]
func()


