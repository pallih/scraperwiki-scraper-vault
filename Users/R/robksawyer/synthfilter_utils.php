<?php

$state = "Oregon"; //Must be Titlecase e.g, Alabama, Michigan. or use an array separated by commas Alabama, Washington
scraperwiki::save_var('state',$state);

//$states = explode(",",$state);
//print_r($states);

//$jsonManufacturerData = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=the_synth_list&query=select%20*%20from%20%60swdata%60");
$manufacturerScraper = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=the_synth_list&query=select%20*%20from%20%60swdata%60";
scraperwiki::save_var('manufacturer_scraper',$manufacturerScraper);

$manufacturers = array("ARP","Access Music","Adaptive Systems, Inc.","Advanced Tools for the Arts (ATA)","Akai","Alesis","Ampron","Analogue Systems","Applied Acoustics","Aries","Arturia","Atlantex","BOSS","Buchla","BitHeadz","Bomb Factory Studios","Casio","Chamberlin","Cheetah","Chimera Synthesis","Clavia","Con Brio","CRB Elettronica","Creamware","Crumar","Dave Smith Instruments","Davoli","Delta Music Research (DMR)","Digisound","Digital Keyboards","Doepfer","E-mu","E-mu Systems","EDP","EML","EMS","Electrix Pro","Electro Harmonix","Electronic Dream Plant (EDP)","Electronic Music Laboratories (EML)","Electronic Music Studios (EMS)","Elektron","Elka","Encore Electronics","Ensoniq","FBT Electronica","Firstman","Fairlight","Farfisa","Formanta","Future Retro","GDS","GForce Software","Generalmusic","Gleeman","Gray Laboratories","Hammond","Hartmann","Hohner","IK Multimedia","Image Line","Jen","Jen Electronics","JoMoX","Kawai","Kenton Electronics","KeyFax Hardware","Kinetic Sound","Koblo","Korg","Kurzweil","Linn Electronics","Logan Electronics","MAM","MOTU","MPC Electronics","MacBeth Studio Systems","Marion Systems","M-Audio","McLeyvier","Metasonix","Miscellaneous","Moog Music","Moog","Mutronics","MXR","Native Instruments","New England Digital","Novation","OSC","Oberheim","Octave","Optigan","PAiA","Performance Music Systems","Polyvox","Polyfusion","pollard International","PPG","Propellerheads","Prosoniq","Quasimidi","RCA","Red Sound Systems","Realistic (Radio Shack)","Rhodes","Rocky Mount Instruments","Roland","Sequential Circuits","Serge","Solton","Steiner-Parker","Stramp","Synclavier (New England Digital)","Synergy","Synton","Technos","Teisco","Thomas Organ","Univox","Waldorf","Wasatch Music Systems (WMS)","Whitehall","Wurlitzer","Yamaha");
$manufacturers = implode(",",$manufacturers);
scraperwiki::save_var('manufacturers',$manufacturers);


//Ignored words for each manufacturer
$iw_digital_keyboards = array('Bongo','bongos','Bongos','bongo','BONGO','BONGOS');
processIgnoredWords('iw_digital_keyboards',$iw_digital_keyboards);
$iw_adaptive_systems_inc = array();
processIgnoredWords('iw_adaptive_systems_inc',$iw_adaptive_systems_inc);
$iw_yamaha = array();
processIgnoredWords('iw_yamaha',$iw_yamaha);
$iw_wurlitzer = array();
processIgnoredWords('iw_wurlitzer',$iw_wurlitzer);
$iw_whitehall = array();
processIgnoredWords('iw_whitehall',$iw_whitehall);
$iw_wasatch_music_systems_wms = array();
processIgnoredWords('iw_wasatch_music_systems_wms',$iw_wasatch_music_systems_wms);
$iw_univox = array('leadsinger','karaoke','Karaoke','KARAOKE');
processIgnoredWords('iw_univox',$iw_univox);
$iw_thomas_organ = array();
processIgnoredWords('iw_thomas_organ',$iw_thomas_organ);
$iw_teisco = array();
processIgnoredWords('iw_teisco',$iw_teisco);
$iw_technos = array('Ludwig','LUDWIG','Zildjian','Viola','Heritage Sweet','Fender','Clarinet',
                    'Sabian','Crash Cymbal','CLARINET','Violin','FENDER','Celestion',
                    'Marshall','1x12 cab'
                    );
processIgnoredWords('iw_technos',$iw_technos);
$iw_synton = array();
processIgnoredWords('iw_synton',$iw_synton);
$iw_synergy = array('Bongo','bongos','Bongos','bongo','BONGO','BONGOS');
processIgnoredWords('iw_synergy',$iw_synergy);
$iw_synclavier_new_england_digital = array();
processIgnoredWords('iw_synclavier_new_england_digital',$iw_synclavier_new_england_digital);
$iw_stramp = array();
processIgnoredWords('iw_stramp',$iw_stramp);
$iw_steiner_parker = array();
processIgnoredWords('iw_steiner-parker',$iw_steiner_parker);
$iw_solton = array();
processIgnoredWords('iw_solton',$iw_solton);
$iw_serge = array();
processIgnoredWords('iw_serge',$iw_serge);
$iw_sequential_circuits = array('road runner', 'Road runner','14 inch','13 inch',
                    '14 Inch','13 Inch','epiphone','Epiphone','tom delonge','GIBRALTAR',
                    '14','Gibraltar','drums','rack tom','kick drum','Behringer','Pro Max',
                    'SKB 8','SKB-8','Tom case','Tom Case','tom case','TOM CASE','Hi Hat','hats','Remo',
                    'remo','heads','Heads'
                    );
processIgnoredWords('iw_sequential_circuits',$iw_sequential_circuits);
$iw_rocky_mount_instruments = array();
processIgnoredWords('iw_rocky_mount_instruments',$iw_rocky_mount_instruments);
$iw_realistic_radio_shack = array();
processIgnoredWords('iw_realistic_radio_shack',$iw_realistic_radio_shack);
$iw_rca = array();
processIgnoredWords('iw_rca',$iw_rca);
$iw_ppg = array();
processIgnoredWords('iw_ppg',$iw_ppg);
$iw_polyvox = array();
processIgnoredWords('iw_polyvox',$iw_polyvox);
$iw_polyfusion = array();
processIgnoredWords('iw_polyfusion',$iw_polyfusion);
$iw_pollard_international = array();
processIgnoredWords('iw_pollard_international',$iw_pollard_international);
$iw_performance_music_systems = array();
processIgnoredWords('iw_performance_music_systems',$iw_performance_music_systems);
$iw_optigan = array();
processIgnoredWords('iw_optigan',$iw_optigan);
$iw_mxr = array();
processIgnoredWords('iw_mxr',$iw_mxr);
$iw_mpc_electronics = array();
processIgnoredWords('iw_mpc_electronics',$iw_mpc_electronics);
$iw_moog = array('Guitiar','left handed','acoustic','Rogue Bass','rogue bass',
                    'Bass','bass','rogue acoustic','Rogue Acoustic','Acoustic Electric'
                    );
processIgnoredWords('iw_moog',$iw_moog);
$iw_miscellaneous = array();
processIgnoredWords('iw_miscellaneous',$iw_miscellaneous);
$iw_mcleyvier = array();
processIgnoredWords('iw_mcleyvier',$iw_mcleyvier);
$iw_kinetic_sound = array();
processIgnoredWords('iw_kinetic_sound',$iw_kinetic_sound);
$iw_jen = array();
processIgnoredWords('iw_jen',$iw_jen);
$iw_gray_laboratories = array();
processIgnoredWords('iw_gray_laboratories',$iw_gray_laboratories);
$iw_gds = array('Bongo','bongos','Bongos','bongo','BONGO','BONGOS');
processIgnoredWords('iw_gds',$iw_gds);
$iw_firstman = array();
processIgnoredWords('iw_firstman',$iw_firstman);
$iw_electronic_music_studios = array();
processIgnoredWords('iw_electronic_music_studios',$iw_electronic_music_studios);
$iw_electronic_music_laboratories = array();
processIgnoredWords('iw_electronic_music_laboratories',$iw_electronic_music_laboratories);
$iw_electronic_dream_plant = array();
processIgnoredWords('iw_electronic_dream_plant',$iw_electronic_dream_plant);
$iw_e_mu = array();
processIgnoredWords('iw_e-mu',$iw_e_mu);
$iw_digisound = array();
processIgnoredWords('iw_digisound',$iw_digisound);
$iw_delta_music_research = array();
processIgnoredWords('iw_delta_music_research',$iw_delta_music_research);
$iw_davoli = array();
processIgnoredWords('iw_davoli',$iw_davoli);
$iw_crb_elettronica = array();
processIgnoredWords('iw_crb_elettronica',$iw_crb_elettronica);
$iw_advanced_tools_for_the_arts = array();
processIgnoredWords('iw_advanced_tools_for_the_arts',$iw_advanced_tools_for_the_arts);
$iw_buchla = array('GETZEN','GETZAN','Getzen','getzen','trumpet','brass','Trumpet','TRUMPET', 'Shecter',
                    'SHECTER','shecter','Guitar','GUITAR','amplifier','Amplifier','PEAVEY'
                    );
processIgnoredWords('iw_buchla',$iw_buchla);
$iw_atlantex = array();
processIgnoredWords('iw_atlantex',$iw_atlantex);
$iw_ampron = array();
processIgnoredWords('iw_ampron',$iw_ampron);
$iw_roland = array('d2 drums','D2 Drums');
processIgnoredWords('iw_roland',$iw_roland);
$iw_rhodes = array();
processIgnoredWords('iw_rhodes',$iw_rhodes);
$iw_red_sound_systems = array();
processIgnoredWords('iw_red_sound_systems',$iw_red_sound_systems);
$iw_quasimidi = array();
processIgnoredWords('iw_quasimidi',$iw_quasimidi);
$iw_prosoniq = array();
processIgnoredWords('iw_prosoniq',$iw_prosoniq);
$iw_propellerheads = array();
processIgnoredWords('iw_propellerheads',$iw_propellerheads);
$iw_ppg = array();
processIgnoredWords('iw_ppg',$iw_ppg);
$iw_paia = array();
processIgnoredWords('iw_paia',$iw_paia);
$iw_octave = array('Danelectro','danelectro','Cool Cat','cool cat','Gig Bag','Martin','Felix The Cat','felix the cat','Black Cat','black cat','BLACK CAT',
                    'Bad Cat','bad cat','BAD CAT'
                    );
processIgnoredWords('iw_octave',$iw_octave);
$iw_oberheim = array('Epiphone','J200','Acoustic','Fishman Matrix','Metronome','metronome','UAD-1','uad-1','UAD1','uad1');
processIgnoredWords('iw_oberheim',$iw_oberheim);
$iw_osc = array('Schmidt');
processIgnoredWords('iw_osc',$iw_osc);
$iw_novation = array();
processIgnoredWords('iw_novation',$iw_novation);
$iw_new_england_digital = array();
processIgnoredWords('iw_new_england_digital',$iw_new_england_digital);
$iw_native_instruments = array('PA System','pa system','PA SYSTEM','Stereo Battery','stereo battery');
processIgnoredWords('iw_native_instruments',$iw_native_instruments);
$iw_mutronics = array();
processIgnoredWords('iw_mutronics',$iw_mutronics);
$iw_moog_music = array('Guitiar','left handed','acoustic','Rogue Bass','rogue bass',
                    'Bass','bass','rogue acoustic','Rogue Acoustic','Acoustic Electric');
processIgnoredWords('iw_moog_music',$iw_moog_music);
$iw_metasonix = array();
processIgnoredWords('iw_metasonix',$iw_metasonix);
$iw_marion_systems = array();
processIgnoredWords('iw_marion_systems',$iw_marion_systems);
$iw_macbeth_studio_systems = array('Avalon M5','Jensen','PDP M5');
processIgnoredWords('iw_macbeth_studio_systems',$iw_macbeth_studio_systems);
$iw_motu = array();
processIgnoredWords('iw_motu',$iw_motu);
$iw_mam = array();
processIgnoredWords('iw_mam',$iw_mam);
$iw_logan_electronics = array();
processIgnoredWords('iw_logan_electronics',$iw_logan_electronics);
$iw_linn_electronics = array();
processIgnoredWords('iw_linn_electronics',$iw_linn_electronics);
$iw_kurzweil = array();
processIgnoredWords('iw_kurzweil',$iw_kurzweil);
$iw_koblo = array();
processIgnoredWords('iw_koblo',$iw_koblo);
$iw_keyfax_hardware = array();
processIgnoredWords('iw_keyfax_hardware',$iw_keyfax_hardware);
$iw_kenton_electronics = array();
processIgnoredWords('iw_kenton_electronics',$iw_kenton_electronics);
$iw_kawai = array('Kanilea','kanilea','KANILEA');
processIgnoredWords('iw_kawai',$iw_kawai);
$iw_jomox = array();
processIgnoredWords('iw_jomox',$iw_jomox);
$iw_jen_electronics = array();
processIgnoredWords('iw_jen_electronics',$iw_jen_electronics);
$iw_image_line = array();
processIgnoredWords('iw_image_line',$iw_image_line);
$iw_ik_multimedia = array();
processIgnoredWords('iw_ik_multimedia',$iw_ik_multimedia);
$iw_hohner = array();
processIgnoredWords('iw_hohner',$iw_hohner);
$iw_hartmann = array();
processIgnoredWords('iw_hartmann',$iw_hartmann);
$iw_hammond = array();
processIgnoredWords('iw_hammond',$iw_hammond);
$iw_gleeman = array();
processIgnoredWords('iw_gleeman',$iw_gleeman);
$iw_generalmusic = array('CSX35','CSX 35','suhr s3','SUHR S3','Suhr S3','CSX');
processIgnoredWords('iw_generalmusic',$iw_generalmusic);
$iw_gforce_software = array();
processIgnoredWords('iw_gforce_software',$iw_gforce_software);
$iw_future_retro = array();
processIgnoredWords('iw_future_retro',$iw_future_retro);
$iw_formanta = array();
processIgnoredWords('iw_formanta',$iw_formanta);
$iw_farfisa = array();
processIgnoredWords('iw_farfisa',$iw_farfisa);
$iw_fairlight = array();
processIgnoredWords('iw_fairlight',$iw_fairlight);
$iw_fbt_electronica = array();
processIgnoredWords('iw_fbt_electronica',$iw_fbt_electronica);
$iw_ensoniq = array('accordian','accordion','Accordian','Accordion',
                    'ACCORDIAN','ACCORDION','boss','Boss','BOSS','Ibanez',
                    'ibanez','IBANEZ');
processIgnoredWords('iw_ensoniq',$iw_ensoniq);
$iw_encore_electronics = array();
processIgnoredWords('iw_encore_electronics',$iw_encore_electronics);
$iw_elka = array();
processIgnoredWords('iw_elka',$iw_elka);
$iw_elektron = array();
processIgnoredWords('iw_elektron',$iw_elektron);
$iw_electrix_pro = array();
processIgnoredWords('iw_electrix_pro',$iw_electrix_pro);
$iw_ems = array();
processIgnoredWords('iw_ems',$iw_ems);
$iw_eml = array();
processIgnoredWords('iw_eml',$iw_eml);
$iw_edp = array('Line Six','Line 6','LINE 6','Half stack','half stack','Half Stack','HALF STACK','AMPLIFIER',
                '75 watt','Dolly','dolly','Grand Piano','Spider III','Spider 3','spider III','spider 3','line 6','Line6',
                'Spider 111'
                );
processIgnoredWords('iw_edp',$iw_edp);
$iw_e_mu_systems = array('Hammond','B3 Organ','B3 organ', 'b3 organ', 'B3 Organ');
processIgnoredWords('iw_e-mu_systems',$iw_e_mu_systems);
$iw_doepfer = array();
processIgnoredWords('iw_doepfer',$iw_doepfer);
$iw_dave_smith_instruments = array();
processIgnoredWords('iw_dave_smith_instruments',$iw_dave_smith_instruments);
$iw_crumar = array('Flute','flute','FLUTE','woodwind','Indian','india','high spirit','High Spirit',
                    'Fender','fender','FENDER','Roland','ROLAND','roland','soundcraft','Soundcraft',
                    'Kimball','kimball','Tama','Jackson','Seymour Duncan','seymour','Boss Turbo','Boss',
                    'BOSS','Cable Organizer','SoundCraft','CBI Performer'
                    );
processIgnoredWords('iw_crumar',$iw_crumar);
$iw_creamware = array();
processIgnoredWords('iw_creamware',$iw_creamware);
$iw_con_brio = array();
processIgnoredWords('iw_con_brio',$iw_con_brio);
$iw_clavia = array();
processIgnoredWords('iw_clavia',$iw_clavia);
$iw_chimera_synthesis = array();
processIgnoredWords('iw_chimera_synthesis',$iw_chimera_synthesis);
$iw_cheetah = array();
processIgnoredWords('iw_cheetah',$iw_cheetah);
$iw_chamberlin = array();
processIgnoredWords('iw_chamberlin',$iw_chamberlin);
$iw_casio = array();
processIgnoredWords('iw_casio',$iw_casio);
$iw_bomb_factory_studios = array();
processIgnoredWords('iw_bomb_factory_studios',$iw_bomb_factory_studios);
$iw_bitheadz = array();
processIgnoredWords('iw_bitheadz',$iw_bitheadz);
$iw_boss = array();
processIgnoredWords('iw_boss',$iw_boss);
$iw_aries = array('Trumpet','horn','TRUMPET','trumpet','HORN','Horn','PEAVEY','peavey','Peavey','Digitech','digitech','MOSFET','Stand up bass',
                 'SENNHEISER','Sennheiser','sennheiser','300 Watt','Half Stack','300 watt','Nice Bass','Bass Guitar','Clarinet','clarinet','selmer',
                 'Selmer','Fender','fender','variax','Variax','Acoustic','acoustic','Magnus','vETTA','vetta','kustom 300','Kustom 300','AMPEX','Ampex',
                 'ampex','LINE 6','VETTA II','VESTAX','P.A. System','DJ American','Roland','CABINET','Yamaha','PA System','vestax','VCI 300','Digi 002',
                 'Lexicon 300','DigiTech\'s','DigiTech','Lexicon','lexicon','digitech','cd player','M. Audio','M-Audio','m-audio','Samick Piano','LINE6',
                 'PIONEER','YAMAHA','yamaha','335 Lawsuit','ESP LTD','American Audio','KRAMER','FRET','Vestax','FENDER','Turser300','Yamaha','Carvin',
                 'Pro Bass','YTP 300'
                 );
processIgnoredWords('iw_aries',$iw_aries);
$iw_applied_acoustics = array();
processIgnoredWords('iw_applied_acoustics',$iw_applied_acoustics);
$iw_analogue_systems = array();
processIgnoredWords('iw_analogue_systems',$iw_analogue_systems);
$iw_alesis = array('AMP','fender','Drum Kit','drum kit','DRUM KIT','Keller','Pearl','pearl','VSX-5','vsx 5','VSX 5','vsx-5',
                     'Keller Fusion','Fusion Drum','fusion drum','Drum Set','hihats','fusion kit','TAMA',
                     'Block Rocker','Jackson Fusion','jackson','Jackson','GK Fusion','gk fusion','Charvel fusion','charvel fusion',
                     'CHARVEL FUSION','ION Cassette','ION cassette','GZA 300','Turser300','Turser 300','Hand Drum','hand drum',
                     'P.A. System','Traktor S4','CORDOBA'
                    );
processIgnoredWords('iw_alesis',$iw_alesis);
$iw_akai = array('Stanton','stanton');
processIgnoredWords('iw_akai',$iw_akai);
$iw_arp = array('AMP','Gibson','gibson','GIBSON','epiphone','goth','Epiphone',
                 'EPIPHONE','Jackson','jackson','floyd','JACKSON','GIBSON',
                 'turntables','Turntables','TURNTABLES','Turn Tables','turn tables',
                 'B212','Bass Cab','bass cab','b212','Avatar cab', 'Avatar Cab',
                 'avatar cab','akai','Akai','AKAI','MPC 2500','mpc 2500','Delta Omni',
                 'sound card','EXPLORER CASE','Agile 2500','ATA Rack','Rack','RACK',
                 'ATA','ata','combo rack','Combo Rack','odyssey rack'
                );
processIgnoredWords('iw_arp',$iw_arp);
$iw_access_music = array();
processIgnoredWords('iw_access_music',$iw_access_music);
$iw_korg = array('Getzen','getzen','770 sg','770 SG','mandolin','MANDOLIN','Mandolin',
                'Big Muddy','big muddy','Pod X3','pod x3','Line 6 POD','Line 6');
processIgnoredWords('iw_korg',$iw_korg);
$iw_maudio = array();
processIgnoredWords('iw_maudio',$iw_maudio);
$iw_waldorf = array('Boss Micro','boss micro','boss','BOSS');
processIgnoredWords('iw_waldorf',$iw_waldorf);

//Templates
/*
//Inside of the scraper
$ignoreWords = explode(',',scraperwiki::get_var('iw_data'));
echo "Total ignored words: ".count($ignoreWords)."\n";

//In here
$iw_data = array();
processIgnoredWords('iw_data',$iw_data);
*/

///

//Handles processing specific ignored words related functions
function processIgnoredWords($name='',$iw_array=array()){
    $common_ignored = array('guitar','guitar amp','guitars','Guitar','Guitars',
                            'amp','Amp','pedal','bass cab','SPEAKERS','viola','violin','clarinet','Clarinet',
                            'capo','Capo','acoustic','Acoustic','Fender','Washburn','Danelectro','washburn',
                            'danelectro','fender','5 string','5 String','Epiphone','epiphone','flute','Flute',
                            'Tuba','tuba','trumpet','Trumpet','Trumbone','trumbone','harmonica','Harmonica',
                            'Drum Set','drum set','drum kit','Drum Kit','DRUM KIT','DRUM SET','hihats','hi hats',
                            '5 Piece','Djembe','djembe','conga','Conga','PEAVEY','Peavey','peavey','Ibanez','Schecter',
                            'strat','Strat','ibanez','schecter','Bajo quinto','Ludwig','LUDWIG','ludwig','Trombone','Greco',
                            'Laptop Battery','laptop battery','drum Kit','Drum kit','TAKE THIS PIANO','SPEAKER AND CAB',
                            'Rickenbacker','Bass Cabinet','Piano for sale','GUITAR','Wanted:','SOLD'
                            );
    if(empty($iw_array)){
        $iw_array = $common_ignored;
    }else{
        $iw_array = array_merge($iw_array,$common_ignored);
    }
    echo $name . " ignored words: ".count($iw_array)."\n";
    $iw_array = implode(',',$iw_array);
    scraperwiki::save_var($name,$iw_array);
}

?>