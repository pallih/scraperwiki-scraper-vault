import pickle

# Blank Python

class myclass:
    def __init__(self,animal):
        self.bag=[animal]

    def ocelot(self):
        if cat in self.bag:
            self.bag={'cat':'ocelot'}

#a=[1,2,3]
a=myclass('cat')
b=pickle.dumps(a.__dict__)
c=myclass('dog')
c.__dict__=pickle.loads(b)

print a.bag
print c.bag

assert c==a

