import scraperwiki
from bs4 import BeautifulSoup
import urllib
import re

def make_soup(url):
    fh = urllib.urlopen(url)
    # read website
    html = fh.read()
    soup = BeautifulSoup(html)
    return soup


def get_english_language_names(soup):

    options = soup.select('option')
    print str(len(options)) + " languages"
    for o in options:
        entry = {}

        id = o.get('class')[0]
        entry['language_id'] = id
        english_name = o.get('data-alternative-spellings').split()[0]
        entry['english_language_name'] = english_name

        native_name = o.text
        entry['native_language_name'] = native_name

        scraperwiki.sqlite.save(unique_keys=['language_id'], data=entry, table_name="language_names_english_native")

def get_language_codes(soup):

    codes = {}
    options = soup.select('option')
    print str(len(options)) + " languages"

    for o in options:
        code = o.get('class')[0]
        english_name = o.get('data-alternative-spellings').split()[0]
        codes[code] = english_name

    return codes

def get_language_dictionary(codes):

    data = dict.fromkeys(codes, {})
    for code in data.keys():

        data[code] = {'language_id': code, 'language_in_English': codes[code]}
        
        
    #print data
    
    for code in codes.keys():
        # for unknown reasons, the language pilaga (plg) gives a unicode error and is therefore skipped 
        if code == 'plg':
            continue
        #try:
         #   scraperwiki.sqlite.execute('alter table language_names_all add column language_name_in_' + codes[code] +  ' char(50)')
        #except:
            # if column already exists
         #   pass

        # language of webpage
        code_web = code.replace('_', '-')

        url = 'http://www.jw.org/' + code_web
        fh = urllib.urlopen(url)
        html = fh.read()
        soup = BeautifulSoup(html)

        options = soup.select('option')
        if not options:
            print 'error loading language page' 
            continue

        for o in options:
            # every language name in that language 
            # example: data['de'] = {'code':'de', 'language_name_in_English': 'German', language_name_in_French': 'Allemand', ...}

            
            language_id = o.get('class')[0]

            name_in_webpage_language = o.get('data-alternative-spellings').split()[0]

            english_name_of_webpage_language = codes[code]

            

            #print "The language name for the code " + language_id + " in " + english_name_of_webpage_language + " is " + name_in_webpage_language
            entry = data[language_id]
            entry['language_name_in_' + english_name_of_webpage_language] = name_in_webpage_language
            
            #print data[language_id]

    print "Scraping finished, will now save data..."
    for entry in data.values():
        print entry['language_id']
        scraperwiki.sqlite.save(unique_keys=['language_id'], data=entry, table_name="language_names_part2")



## main ##

url = 'http://www.jw.org/en/'
soup = make_soup(url)
#get_english_language_names(soup)
#codes = get_language_codes(soup)

codes = {'gu': u'Gujarati', 'mfe': u'Mauritian', 'tkl': 'Tokelauan', 'ne': u'Nepali', 'ttj': 'Rutoro', 'ga': 'Irish', 'mfy': u'Mayo', 'lg': 'Luganda', 'jw_tln': 'Tlapanec', 'tn': 'Tswana', 'ln': 'Lingala', 'tw': 'Twi', 'tt': u'Tatar', 'zai': 'Zapotec', 'tr': u'Turkish', 'ts': 'Tsonga', 'lv': u'Latvian', 'ngu': u'Nahuatl', 'lt': u'Lithuanian', 'tsz': u'Tarascan', 'th': u'Thai', 'ada': 'Dangme', 'jw_mxo': 'Mixtec', 'tg': u'Tajiki', 'djk': 'Aukan', 'cuk': 'Guna', 'ta': u'Tamil', 'guc': 'Wayuunaiki', 'ceb': 'Cebuano', 'yo': u'Yoruba', 'de': 'German', 'ko': u'Korean', 'kck': 'Kalanga', 'da': 'Danish', 'mgr': 'Mambwe-Lungu', 'qu': 'Quechua', 'hil': 'Hiligaynon', 'jw_trh': 'Tarahumara', 'crs': 'Seychelles', 'gug': u'Guarani', 'jw_vru': u'Voru', 'gur': 'Frafra', 'kmr_cyrl': u'Kurdish', 'el': u'Greek', 'en': 'English', 'teo': 'Ateso', 'ee': 'Ewe', 'nus': 'Nuer', 'zu': 'Zulu', 'jw_qi': 'Quichua', 'rmn': 'Romany', 'es': u'Spanish', 'kk_cyrl': u'Kazakh', 'ru': u'Russian', 'rw': 'Kinyarwanda', 'az_cyrl': u'Azerbaijani', 'quy': 'Quechua', 'lub': 'Kiluba', 'lue': 'Luvale', 'tzo': 'Tzotzil', 'si': u'Sinhala', 'new': u'Newari', 'ro': u'Romanian', 'cnh': 'Chin', 'luo': 'Luo', 'qus': 'Quichua', 'bg': u'Bulgarian', 'kek': u'Kekchi', 'leh': 'Lenje', 'quz': 'Quechua', 'plg': u'Pilag\xe1', 'kiz': 'Kisi', 'zh_hant': u'Chinese', 'que': 'Quechua', 'jw_wch': 'Wichi', 'ja': u'Japanese', 'tdt': 'Tetum', 'ctu': 'Chol', 'om': 'Oromo', 'pt': u'Portuguese', 'ilo': 'Iloko', 'zh_hans': u'Chinese', 'ach': 'Acholi', 'srn': 'Sranantongo', 'quc': u'Quiche', 'srm': u'Saramaccan', 'kri': 'Krio', 'iso': 'Isoko', 'yua': 'Maya', 'os': u'Ossetian', 'xh': 'Xhosa', 'mr': u'Marathi', 'nso': 'Sepedi', 'kwn': 'Kwangali', 'sop': 'Kisonge', 'cy': 'Welsh', 'jw_rny': 'Rumanyo', 'cs': u'Czech', 'ty': 'Tahitian', 'ncx': u'Nahuatl', 'jw_mxg': u'Mixtec', 'wal': 'Wolaita', 'hy_latn': u'Armenian', 'koo': 'Lhukonzo', 'to': 'Tongan', 'sr_cyrl': u'Serbian', 'swc': 'Swahili', 'tl': 'Tagalog', 'toj': 'Tojolabal', 'yan': 'Mayangna', 'tob': 'Toba', 'niu': 'Niuean', 'war': 'Waray-Waray', 'pl': 'Polish', 'hz': 'Herero', 'mck': 'Mbunda', 'sid': 'Sidama', 'oto': u'Otomi', 'hr': 'Croatian', 'ti': u'Tigrinya', 'lgg': 'Lugbara', 'ht': u'Haitian', 'hu': 'Hungarian', 'zpa': 'Zapotec', 'huv': 'Huave', 'hi': u'Hindi', 'hus': u'Huastec', 'ha': 'Hausa', 'xmv': 'Tankarana', 'gaa': 'Ga', 'mg': 'Malagasy', 'sr_latn': 'Serbian', 'jw_tot': 'Totonac', 'kln': 'Kalenjin', 'mn': u'Mongolian', 'mk': u'Macedonian', 'cak': 'Cakchiquel', 'mt': 'Maltese', 'zpg': 'Zapotec', 'uk': u'Ukrainian', 'kj': 'Kwanyama', 'cab': 'Garifuna', 'nzi': 'Nzema', 'az_latn': u'Azerbaijani', 'sq': 'Albanian', 'mco': 'Mixe', 've': 'Venda', 'af': 'Afrikaans', 'vi': u'Vietnamese', 'is': u'Icelandic', 'am': u'Amharic', 'it': 'Italian', 'sv': 'Swedish', 'mya': u'Myanmar', 'rar': 'Rarotongan', 'rap': 'Rapa', 'et': 'Estonian', 'ay': 'Aymara', 'tzh': 'Tzeltal', 'st': 'Sesotho', 'id': 'Indonesian', 'ig': 'Igbo', 'pap': u'Papiamento', 'pis': 'Solomon', 'nl': 'Dutch', 'no': 'Norwegian', 'pa': u'Punjabi', 'nah': u'Nahuatl', 'hns': 'Sarnami', 'ng': 'Ndonga', 'efi': u'Efik', 'lam': 'Lamba', 'naq': 'Khoekhoegowab', 'nyn': 'Runyankore', 'arn': u'Mapudungun', 'pag': 'Pangasinan', 'miq': 'Miskito', 'nr': 'Ndebele', 'nya': 'Cinyanja', 'kqn': 'Kikaonde', 'kab': 'Kabyle', 'fr': u'French', 'mau': 'Mazatec', 'kam': 'Kikamba', 'hy_armn': u'Armenian', 'fi': 'Finnish', 'rnd': 'Uruund', 'mam': 'Mam', 'fo': u'Faeroese', 'bcl': 'Bicol', 'ka': u'Georgian', 'kg': u'Kongo', 'bci': u'Baoule', 'zne': 'Zande', 'jw_vz': 'Vezo', 'ss': 'Swati', 'jw_rdu': u'Kurdish', 'ki': u'Kikuyu', 'jw_ngb': u'Ngabere', 'sw': 'Swahili', 'ncj': u'Nahuatl', 'km': u'Cambodian', 'kl': 'Greenlandic', 'sk': u'Slovak', 'lhu': u'Lahu', 'so': 'Somali', 'sn': 'Shona', 'sm': 'Samoan', 'sl': u'Slovenian', 'ky': u'Kirghiz', 'sg': 'Sango', 'tiv': 'Tiv'}

get_language_dictionary(codes)

