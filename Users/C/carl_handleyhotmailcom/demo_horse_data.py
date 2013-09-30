import scraperwiki

import urllib

import csv

import threading
from threading import Thread



class myURLOpener(urllib.FancyURLopener):
    
    def setpasswd(self, user, passwd):
        self.__user = user
        self.__passwd = passwd
    
    def prompt_user_passwd(self, host, realm):
        return self.__user, self.__passwd




urlopener = myURLOpener()
###urlopener.setpasswd("enter_username", "enter_password") ###uncomment this line to use a username and password

#horse = []

#def splitter(url):
#    if __name__ == '__main__':
#        Thread(target = idgen1(url)).start()
#        Thread(target = idgen2(url)).start()


def idgen1(url):
    counter = 137134
    while counter <= 150000:
        s = url
        s = s + str(counter)
        fp = urlopener.open(s)
        get_target(fp.read(10000),counter)
        counter += 1

#def idgen2(url):
#    counter = 1001 
#        s = url
#        s = s + str(counter)
#        fp = urlopener.open(s)
#        get_target(fp.read(10000),counter)
#        counter += 1

def get_target(page,horseid):
    test = page.find('There is no additional information available for this horse') 
    if (test == -1):
        
        start_point = page.find('<h1>')
        if start_point == -1:
            return None
        start = start_point
        end = page.find('<', start + 1)
        name = page[start + 6 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('(', start_point)
        end = page.find(')', start + 1)
        birth = page[start + 1 :end]
        
        birthlist = birth.split()
        if len(birthlist) == 3:
            birth = birthlist[0]
            colour = birthlist[1]
            sex = birthlist[2]
        if len(birthlist) == 2:
            birth = birthlist[0]
            colour = birthlist[1]
            sex = ' '
        if len(birthlist) == 1:
            birth = birthlist[0]
            colour = ' '
            sex = ' '

    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('stallion.sd?horse_id=', start_point)
        end = page.find('&amp', start + 1)
        stallionid = page[start +21 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('</a>', start + 1)
        stallionname= page[start + 1 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('dam_home.sd?horse_id=', start_point)
        end = page.find('"', start + 21)
        damid = page[start +21 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        damname = page[start + 1 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('stallion.sd?horse_id=', start_point)
        end = page.find('&amp', start + 1)
        sireid = page[start +21 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        sirename = page[start + 1 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('trainer_home.sd?trainer_id=', start_point)
        end = page.find('"', start + 1)
        trainerid = page[start +27 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        trainername = page[start + 1:end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('owner_home.sd?owner_id=', start_point)
        end = page.find('"', start + 1)
        ownerid = page[start + 23 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        ownername = page[start + 1:end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('<b>', start_point)
        end = page.find('<', start + 3)
        breeder = page[start + 3 :end]
        
        horsedata = dict(horse_id = horseid,horse_name = name, stallion_id = stallionid,stallion_name = stallionname,dam_id = damid,dam_name = damname,sire_id = sireid,sire_name = sirename,trainer_id = trainerid,trainer_name = trainername,owner_id = ownerid,owner_name = ownername,breeder_name = breeder,birth_data = birth, colour_data = colour, sex_data = sex)
    
        #print horsedata
        scraperwiki.sqlite.save(unique_keys = ["horse_id","horse_name","stallion_id","stallion_name","dam_id","dam_name", "sire_id", "sire_name", "trainer_id", "trainer_name", "owner_id","owner_name", "breeder_name", "birth_data", "colour_data","sex_data"], data = horsedata)
    
    
#splitter("http://www.racingpost.com/horses/horse_home.sd?horse_id=")

idgen1("http://www.racingpost.com/horses/horse_home.sd?horse_id=")
import scraperwiki

import urllib

import csv

import threading
from threading import Thread



class myURLOpener(urllib.FancyURLopener):
    
    def setpasswd(self, user, passwd):
        self.__user = user
        self.__passwd = passwd
    
    def prompt_user_passwd(self, host, realm):
        return self.__user, self.__passwd




urlopener = myURLOpener()
###urlopener.setpasswd("enter_username", "enter_password") ###uncomment this line to use a username and password

#horse = []

#def splitter(url):
#    if __name__ == '__main__':
#        Thread(target = idgen1(url)).start()
#        Thread(target = idgen2(url)).start()


def idgen1(url):
    counter = 137134
    while counter <= 150000:
        s = url
        s = s + str(counter)
        fp = urlopener.open(s)
        get_target(fp.read(10000),counter)
        counter += 1

#def idgen2(url):
#    counter = 1001 
#        s = url
#        s = s + str(counter)
#        fp = urlopener.open(s)
#        get_target(fp.read(10000),counter)
#        counter += 1

def get_target(page,horseid):
    test = page.find('There is no additional information available for this horse') 
    if (test == -1):
        
        start_point = page.find('<h1>')
        if start_point == -1:
            return None
        start = start_point
        end = page.find('<', start + 1)
        name = page[start + 6 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('(', start_point)
        end = page.find(')', start + 1)
        birth = page[start + 1 :end]
        
        birthlist = birth.split()
        if len(birthlist) == 3:
            birth = birthlist[0]
            colour = birthlist[1]
            sex = birthlist[2]
        if len(birthlist) == 2:
            birth = birthlist[0]
            colour = birthlist[1]
            sex = ' '
        if len(birthlist) == 1:
            birth = birthlist[0]
            colour = ' '
            sex = ' '

    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('stallion.sd?horse_id=', start_point)
        end = page.find('&amp', start + 1)
        stallionid = page[start +21 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('</a>', start + 1)
        stallionname= page[start + 1 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('dam_home.sd?horse_id=', start_point)
        end = page.find('"', start + 21)
        damid = page[start +21 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        damname = page[start + 1 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('stallion.sd?horse_id=', start_point)
        end = page.find('&amp', start + 1)
        sireid = page[start +21 :end]
    
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        sirename = page[start + 1 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('trainer_home.sd?trainer_id=', start_point)
        end = page.find('"', start + 1)
        trainerid = page[start +27 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        trainername = page[start + 1:end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('owner_home.sd?owner_id=', start_point)
        end = page.find('"', start + 1)
        ownerid = page[start + 23 :end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('>', start_point)
        end = page.find('<', start + 1)
        ownername = page[start + 1:end]
        
        start_point = end
        if start_point == -1:
            return None
        start = page.find('<b>', start_point)
        end = page.find('<', start + 3)
        breeder = page[start + 3 :end]
        
        horsedata = dict(horse_id = horseid,horse_name = name, stallion_id = stallionid,stallion_name = stallionname,dam_id = damid,dam_name = damname,sire_id = sireid,sire_name = sirename,trainer_id = trainerid,trainer_name = trainername,owner_id = ownerid,owner_name = ownername,breeder_name = breeder,birth_data = birth, colour_data = colour, sex_data = sex)
    
        #print horsedata
        scraperwiki.sqlite.save(unique_keys = ["horse_id","horse_name","stallion_id","stallion_name","dam_id","dam_name", "sire_id", "sire_name", "trainer_id", "trainer_name", "owner_id","owner_name", "breeder_name", "birth_data", "colour_data","sex_data"], data = horsedata)
    
    
#splitter("http://www.racingpost.com/horses/horse_home.sd?horse_id=")

idgen1("http://www.racingpost.com/horses/horse_home.sd?horse_id=")
