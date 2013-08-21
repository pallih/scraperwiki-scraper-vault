import scraperwiki
from itertools import chain

dguclient = scraperwiki.utils.swimport('dgu_client')


rsrcs = dguclient.get_resources_for_dataset('nhs-leeds-spend-over-25-000-november-2012')
assert len(rsrcs) == 1
print rsrcs[0]['url']

try:
    rsrcs = dguclient.get_resources_for_dataset('non-existent')
except dguclient.CkanError:
    pass


pkgs = dguclient.get_dataset_names_for_publisher('barnet-primary-care-trust')
assert len(pkgs) == 1, len(pkgs)

all_rsrcs = list(chain.from_iterable([dguclient.get_resources_for_dataset(pn) 
                                      for pn in dguclient.get_dataset_names_for_publisher('barnet-primary-care-trust')]))
print all_rsrcs