import random

class RussianDwarfHamster:
    def __init__(self, name, weight = 300):
        self.name = name
        self.weight = weight
        
    def run(self):
        print "%s says: 'Eeek! Morbo is chasing me again'" % self.name
        self.weight = self.weight - 2
        if self.weight <= 0:
            raise Exception("Hamster %s has died :`(" % self.name)
        
    def eat(self):
        print "%s says: 'Cheese! Yummy my favourite!'" % self.name
        self.weight = self.weight + 5
        
    def evil(self):
        print "%s says: 'All hamsters are vermin in the eyes of Morbo!'" % self.name

cuddles = RussianDwarfHamster("Cuddles")
morbo = RussianDwarfHamster("Morbo")

days_living = 0


while True:
    try:
        for x in range( random.randrange(10) ):
            cuddles.run()
            print "%s now weighs %d grammes" % (cuddles.name, cuddles.weight)
    except Exception,e:
        print e
        print "%s lived for %d days" % (cuddles.name, days_living)
        break
    days_living = days_living + 1    
    cuddles.eat() 
    morbo.evil()
    print "%s now weighs %d grammes" % (cuddles.name, cuddles.weight)


