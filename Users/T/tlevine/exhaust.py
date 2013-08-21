from urllib2 import urlopen

TEST_PAGE_LINK = 'https://www.list.cornell.edu:9443/u?id=26920648.1dfbfa0e6b3ac396a4fa6f6096ddc9dc&n=T&l=squidserve-l&o=43528639'
FORM_ACTION = 'https://www.list.cornell.edu:9443/subscribe/unsubscribe.tml'
QS_JUNK = '&u=&e=&c=&w=&a=&confirm_first=F&yes_unsubscribe.x=17&yes_unsubscribe.y=12'

REAL_URLS = [
    'https://www.list.cornell.edu:9443/u?id=26920632.f62375fc0b585fad42c268fea55e7075&n=T&l=squidserve-l&o=43786770',
    'https://www.list.cornell.edu:9443/u?id=26920783.d2eb6fe468dd9b94ae14b303ac2e2525&n=T&l=squidserve-l&o=43780432',
    'https://www.list.cornell.edu:9443/u?id=26920731.3f268590f84a92200d4a00918ba8c792&n=T&l=squidserve-l&o=43774571',
    'https://www.list.cornell.edu:9443/u?id=26920745.911b83fbaf3d9a2e01e1dda5dd0185eb&n=T&l=squidserve-l&o=42564135',
    'https://www.list.cornell.edu:9443/u?id=26920758.23cb393268568fcbefc45d8db9db13bf&n=T&l=squidserve-l&o=43773689',
    'https://www.list.cornell.edu:9443/u?id=26920622.dbcd3af9466cb5edc936d781cbc6904f&n=T&l=squidserve-l&o=42233038',
    'https://www.list.cornell.edu:9443/u?id=26920698.a5da748cd38a295198b7a2fe971ccc67&n=T&l=squidserve-l&o=42237033',
    'https://www.list.cornell.edu:9443/u?id=26920622.dbcd3af9466cb5edc936d781cbc6904f&n=T&l=squidserve-l&o=42215220',
    'https://www.list.cornell.edu:9443/u?id=26920627.8386fdf9414f83a1f7546431923c574d&n=T&l=squidserve-l&o=42214488',
    'https://www.list.cornell.edu:9443/u?id=26920743.bbb8015c1589c9dc15f5db9b73dfdbe9&n=T&l=squidserve-l&o=42050040',
    'https://www.list.cornell.edu:9443/u?id=26920625.bda6d77260f436e1b656d9a01fe0323c&n=T&l=squidserve-l&o=42050040',
    'https://www.list.cornell.edu:9443/u?id=26920635.47a822a0496d6b8f116f65146371ff56&n=T&l=squidserve-l&o=42050052',
    'https://www.list.cornell.edu:9443/u?id=26920771.37b4b3c60e1b4a128f4e3af5113521d7&n=T&l=squidserve-l&o=42050050',
    'https://www.list.cornell.edu:9443/u?id=26920800.c1a5b23d7ec9ea04f7bee4f0bbadae14&n=T&l=squidserve-l&o=42062063',
    'https://www.list.cornell.edu:9443/u?id=26920650.17ea5e508aad7811f5a11de39c6152ff&n=T&l=squidserve-l&o=42064053',
    'https://www.list.cornell.edu:9443/u?id=26920778.faec486d13fd06cb0051ec9b813bfc20&n=T&l=squidserve-l&o=42064053',
    'https://www.list.cornell.edu:9443/u?id=26976877.72eb3254992a034568e4b19e495f5306&n=T&l=squidserve-l&o=41976033',
    'https://www.list.cornell.edu:9443/u?id=26920791.a0ed05e0118ddb20bea716fb6712f1c3&n=T&l=squidserve-l&o=41981047',
    'https://www.list.cornell.edu:9443/u?id=26920770.e99c0517eaf99f39279647fa36909a86&n=T&l=squidserve-l&o=41882174',
    'https://www.list.cornell.edu:9443/u?id=26920789.82266448dc366dd5f27a0c4ef5f0f06f&n=T&l=squidserve-l&o=41647817',
    'https://www.list.cornell.edu:9443/u?id=26976836.c06df56d0712ab17b9b6f0989a1d611f&n=T&l=squidserve-l&o=41643144',
    'https://www.list.cornell.edu:9443/u?id=26920622.dbcd3af9466cb5edc936d781cbc6904f&n=T&l=squidserve-l&o=41640169',
    'https://www.list.cornell.edu:9443/u?id=26976828.55cc16659c98d436947649b763b07d68&n=T&l=squidserve-l&o=41223728',
    'https://www.list.cornell.edu:9443/u?id=26920723.93e74ee527e88319b7fe139a1171f5d4&n=T&l=squidserve-l&o=41219403',
    'https://www.list.cornell.edu:9443/u?id=26920755.21495b38c1174daa086b1c7cc994781f&n=T&l=squidserve-l&o=41213794',
    'https://www.list.cornell.edu:9443/u?id=26920773.5f2fe462305f95df2e29f6b13e286663&n=T&l=squidserve-l&o=41213334',
    'https://www.list.cornell.edu:9443/u?id=26976845.e5fb4a4f6a9b27d5122efb49c3f7ba1e&n=T&l=squidserve-l&o=41211874',
    'https://www.list.cornell.edu:9443/u?id=26920748.bf21bf2a68e8203bd9d9ce55b0110805&n=T&l=squidserve-l&o=41212013',
    'https://www.list.cornell.edu:9443/u?id=26920688.e99c5dc83ec37d216708e98df27e4a60&n=T&l=squidserve-l&o=41209272',
    'https://www.list.cornell.edu:9443/u?id=26920732.63a05ba1bb36b065889fda0b46989479&n=T&l=squidserve-l&o=40956052',
    'https://www.list.cornell.edu:9443/u?id=26976836.c06df56d0712ab17b9b6f0989a1d611f&n=T&l=squidserve-l&o=40959085',
    'https://www.list.cornell.edu:9443/u?id=26920648.1dfbfa0e6b3ac396a4fa6f6096ddc9dc&n=T&l=squidserve-l&o=40777043',
    'https://www.list.cornell.edu:9443/u?id=26920678.ff308378800a03d4ba5ffc23dbb2829e&n=T&l=squidserve-l&o=40646048',
    'https://www.list.cornell.edu:9443/u?id=26920800.c1a5b23d7ec9ea04f7bee4f0bbadae14&n=T&l=squidserve-l&o=40390091',
    'https://www.list.cornell.edu:9443/u?id=26920772.63c03cef60f9984b6c05efaf20b03c73&n=T&l=squidserve-l&o=40382303',
    'https://www.list.cornell.edu:9443/u?id=26920641.1d8e467fb4b09bbf93b3a4b9c9bdddfb&n=T&l=squidserve-l&o=40029202',
    'https://www.list.cornell.edu:9443/u?id=26920748.bf21bf2a68e8203bd9d9ce55b0110805&n=T&l=squidserve-l&o=39983042',
    'https://www.list.cornell.edu:9443/u?id=26920718.c080f2188a17b62fbce50ee911512c8a&n=T&l=squidserve-l&o=39835036',
    'https://www.list.cornell.edu:9443/u?id=26920786.d850129e3f40dc9df34d806c6d5f56d8&n=T&l=squidserve-l&o=39954039',
    'https://www.list.cornell.edu:9443/u?id=26920779.2de2100bace00d6395ae063a954df226&n=T&l=squidserve-l&o=39954039',
    'https://www.list.cornell.edu:9443/u?id=26976773.46d3c5d5eb8515126dcbc5b66e37dd48&n=T&l=squidserve-l&o=39550044',
    'https://www.list.cornell.edu:9443/u?id=26920786.d850129e3f40dc9df34d806c6d5f56d8&n=T&l=squidserve-l&o=39256064',
    'https://www.list.cornell.edu:9443/u?id=26920712.146b6417daefb0dba5dd3e1c3655ccb2&n=T&l=squidserve-l&o=39198652',
    'https://www.list.cornell.edu:9443/u?id=26920765.d23d798f9361aea0db2f656cb92ac5f8&n=T&l=squidserve-l&o=39196621',
    'https://www.list.cornell.edu:9443/u?id=26920683.ad7bd3e231b72420949588a16f2398c0&n=T&l=squidserve-l&o=39183547',
    'https://www.list.cornell.edu:9443/u?id=26920803.849a969e26893c448da562549dd73591&n=T&l=squidserve-l&o=39170485',
    'https://www.list.cornell.edu:9443/u?id=26920669.ec3491e894242c761593b692ded8f66e&n=T&l=squidserve-l&o=39170575',
    'https://www.list.cornell.edu:9443/u?id=13658880.450249e332d8497a7f0fba57a56816ff&n=T&l=squidserve-l&o=38979824',
    'https://www.list.cornell.edu:9443/u?id=13632832.2510ce874916252b4d9f08e06cacb1a5&n=T&l=squidserve-l&o=38969700',
    'https://www.list.cornell.edu:9443/u?id=24859056.0484f97539195fc3ff0e1f3fde39f0c3&n=T&l=squidserve-l&o=38943882',
    'https://www.list.cornell.edu:9443/u?id=13658790.352958cae339880f020e57a22a717144&n=T&l=squidserve-l&o=38308962',
    'https://www.list.cornell.edu:9443/u?id=24859194.c903d09a8bbec52c7d387c2569029f66&n=T&l=squidserve-l&o=38300866',
    'https://www.list.cornell.edu:9443/u?id=26920786.d850129e3f40dc9df34d806c6d5f56d8&n=T&l=squidserve-l&o=39534265',
    'https://www.list.cornell.edu:9443/u?id=24859150.8a137cd5fd469a97480aae169585ba94&n=T&l=squidserve-l&o=38203806',
    'https://www.list.cornell.edu:9443/u?id=13658869.3136d78c8b9747f7102521b81d5b375b&n=T&l=squidserve-l&o=38168394',
    'https://www.list.cornell.edu:9443/u?id=13658876.e6415e6d259dc718c10b9048e7f16a83&n=T&l=squidserve-l&o=38168699',
    'https://www.list.cornell.edu:9443/u?id=26920642.3e1302ac0bfe873a77421454ee4c576a&n=T&l=squidserve-l&o=39165216',
    'https://www.list.cornell.edu:9443/u?id=24859019.0c326130264c241bf12597e472acacc9&n=T&l=squidserve-l&o=37992572',
]

def main():
    #page_links = [TEST_PAGE_LINK]
    #page_links = []
    page_links = REAL_URLS
    for page_link in page_links:
        url = get_form_link(page_link)
        print url
        #pass
        #urlopen(url)

def get_form_link(page_link):
    "Convert the link from an email to a form submission."
    qs = page_link.split('?')[1]
    return FORM_ACTION + '?' + qs + QS_JUNK

print '"%s"' % '" OR "'.join(REAL_URLS)
#main()