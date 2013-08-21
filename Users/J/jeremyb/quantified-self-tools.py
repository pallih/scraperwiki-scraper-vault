import itertools, BeautifulSoup, requests

itertools.chain(*([table.find('h3').nextSibling.nextSibling for table
in BeautifulSoup.BeautifulSoup(requests.get('http://quantifiedself.com/guide/tools?sort=reviews&pg=%d'
% i).content).find('div',
{'class':'inner'}).find('div').findAll('table')] for i in range(1,52)))

lynx -dump -stdin -nolist -assume_local_charset=utf-8 <
quantifiedselftools.joined.txt > quantifiedselftools.joined.lynxed.txt

textin = tempfile.NamedTemporaryFile(mode='r', suffix='.html')
tmptext = textin.name
cmd = 'lynx -dump -stdin -nolist -assume_local_charset=utf-8 "%s" "%s"' % (pdffout.name, tmptext)
cmd = cmd + " >/dev/null 2>&1" # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)
