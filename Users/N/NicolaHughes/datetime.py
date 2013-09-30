import datetime

class pet:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        
    def same_age_as(self, other):
        if self.birth_date == other.birth_date:
            print "%s and %s have the same birthday!" % (self.name, other.name)
        else:
            print "%s and %s don't have the same birthday!" % (self.name, other.name)
            
    delta = axolotl.birth_date - alphahamster.birth_date
        
axolotl = pet("Pinky", datetime.date(2010,6,6))
alphamalehamster = pet("Morbo", datetime.date(2009,11,16))
betamalehamster = pet("Cuddles", datetime.date(2009,11,16))
femalehamster = pet("Uncle Pecos", datetime.date(2009,11,16))
import datetime

class pet:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date
        
    def same_age_as(self, other):
        if self.birth_date == other.birth_date:
            print "%s and %s have the same birthday!" % (self.name, other.name)
        else:
            print "%s and %s don't have the same birthday!" % (self.name, other.name)
            
    delta = axolotl.birth_date - alphahamster.birth_date
        
axolotl = pet("Pinky", datetime.date(2010,6,6))
alphamalehamster = pet("Morbo", datetime.date(2009,11,16))
betamalehamster = pet("Cuddles", datetime.date(2009,11,16))
femalehamster = pet("Uncle Pecos", datetime.date(2009,11,16))
