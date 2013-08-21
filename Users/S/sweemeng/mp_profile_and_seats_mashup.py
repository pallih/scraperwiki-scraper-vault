import scraperwiki

# Blank Python
def combine_data():
    scraperwiki.sqlite.attach('malaysian_mp_profile','mp_profile')
    scraperwiki.sqlite.attach('mys_seats','seats')
    

def setup():
    scraperwiki.sqlite.attach('malaysian_mp_profile','mp_profile')
    scraperwiki.sqlite.attach('mys_seats','seats')
    existing = scraperwiki.sqlite.show_tables()
    if not existing:
        contituency_query = '''
            CREATE table Constituency as select cast(trim(Parlimen,'P') as INTEGER) as Parlimen,Kawasan from mp_profile.swdata;
        '''
        scraperwiki.sqlite.execute(contituency_query)
        mp_query = '''
            CREATE table MembersParlimen as Select Nama,'Alamat_Surat-menyurat',img,Parti,'E-Mail',No_Telefon,
                       cast(trim(Parlimen,'P') as INTEGER) as Parlimen,No_Fax,
                       Jawatan_dalam_Kabinet,Jawatan_dalam_Parlimen from mp_profile.swdata;
        '''
        scraperwiki.sqlite.execute(mp_query)

setup()

