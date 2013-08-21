import scraperwiki

from pandas import *
import numpy as np
randn = np.random.randn

# "Essential basic functionality"
# http://pandas.sourceforge.net/basics.html

index = DateRange('1/1/2000', periods=8)
s = Series(randn(5), index=['a', 'b', 'c', 'd', 'e'])
df = DataFrame(randn(8, 3), index=index,
            columns=['A', 'B', 'C'])
wp = Panel(randn(2, 5, 4), items=['Item1', 'Item2'],
               major_axis=DateRange('1/1/2000', periods=5),
               minor_axis=['A', 'B', 'C', 'D'])

print df[:2]
print df
