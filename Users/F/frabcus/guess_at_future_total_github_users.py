import datetime

# A(t+1) = A(t) * [ 1 + r(t) ]
#
# where
#
# A(t)   = Number of users in the current month (This must come from a month after June 2009.)
# A(t+1) = Number of users in the next month
# r(t)   = 14.67% - 0.15% * (Current number of months since December 2007)

# Github user growth by Thomas:
# https://github.com/tlevine/github-user-growth

def r(t):
    return (14.67 - 0.15 * t) / 100.0

# starting months
t = 4.0 * 12.0 + 4.0
a = 1553647.0 # real figure, April 2012
d = datetime.date(2012, 04, 01)

for l in range(0, 60):
    a = a * ( 1.0 + r(t) )
    t = t + 1

    # add more than one calendar month, then round down to 1st of month
    d = d + datetime.timedelta(32)
    d = datetime.date(d.year, d.month, 1)

    print d, ":", a, "users"
