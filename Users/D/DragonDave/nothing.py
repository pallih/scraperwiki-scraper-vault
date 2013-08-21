class Nothing:
    def __init__(self, desc='NOTHING'):
        self.desc=desc

    def __str__(self):
        return ''

    def __repr__(self):
        return 'Nothing(%s)'%self.desc

    def __call__(self, *args, **kwargs):
        a=repr(args)[1:-1]
        k=', '.join([''.join( (k,'=', repr(kwargs[k]))) for k in kwargs])
        s= ', '.join ((a,k))
        return Nothing(s)

    def __getitem__(self, name):
        print 'FAILED: getitem %s on "%s"'%(name, self.desc)
        return Nothing(self.desc+'[%s]'%repr(name))

    def __getattr__(self, name):
        print 'FAILED: getattr %s on "%s"'%(name, self.desc)
        return Nothing(self.desc+'.%s'%name)

x=Nothing()
print repr(x.cat('dog', 'cat', fish=2, ocelot=5))
print repr(x['3'].iii[3])