import resource
import sys

#resource.setrlimit(resource.RLIMIT_CPU, (2, 3))
x = 1000000000
for i in range(1,1000000):
    x = x * i
    if not (i % 1000):
        used = resource.getrusage(resource.RUSAGE_SELF)
        print i, len(str(x)), resource.getrlimit(resource.RLIMIT_CPU), used[0], used[1]


