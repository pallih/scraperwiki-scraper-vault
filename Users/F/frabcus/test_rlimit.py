import scraperwiki

import resource

print resource.getrlimit(resource.RLIMIT_CPU)

resource.setrlimit(resource.RLIMIT_CPU, (81, 82,))

print resource.getrlimit(resource.RLIMIT_CPU)

