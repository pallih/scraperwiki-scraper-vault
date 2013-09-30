<?php

require 'scraperwiki/simple_html_dom.php';  

$zones = array(
    array( 'Zone' => 'JHR02', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Kota Tinggi, Mersing, Johor Bahru' ),
    array( 'Zone' => 'JHR04', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Batu Pahat, Muar, Segamat, Gemas' ),
    array( 'Zone' => 'JHR03', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Kluang dan Pontian' ),
    array( 'Zone' => 'JHR01', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Pulau Aur dan Pemanggil' ),

    array( 'Zone' => 'KDH06', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Puncak Gunung Jerai' ),
    array( 'Zone' => 'KDH01', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Kota Setar, Kubang Pasu, Pokok Sena' ),
    array( 'Zone' => 'KDH05', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Langkawi' ),
    array( 'Zone' => 'KDH02', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Pendang, Kuala Muda, Yan' ),
    array( 'Zone' => 'KDH03', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Padang Terap, Sik, Baling' ),
    array( 'Zone' => 'KDH04', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Kulim, Bandar Baharu' ),

    array( 'Zone' => 'KTN03', 'Negeri' => 'KELANTAN' , 'Lokasi' => 'Jeli, Gua Musang (Mukim Galas, Bertam)' ),
    array( 'Zone' => 'KTN01', 'Negeri' => 'KELANTAN' , 'Lokasi' => 'K.Bharu,Bachok,Pasir Puteh,Tumpat,Pasir Mas,Tnh. Merah,Machang,Kuala Krai,Mukim Chiku' ),

    array( 'Zone' => 'MLK01', 'Negeri' => 'MELAKA' , 'Lokasi' => 'Bandar Melaka, Alor Gajah, Jasin, Masjid Tanah, Merlimau, Nyalas' ),

    array( 'Zone' => 'NGS02', 'Negeri' => 'NEGERI SEMBILAN' , 'Lokasi' => 'Port Dickson, Seremban, Kuala Pilah, Jelebu, Rembau' ),
    array( 'Zone' => 'NGS01', 'Negeri' => 'NEGERI SEMBILAN' , 'Lokasi' => 'Jempol, Tampin' ),

    array( 'Zone' => 'PHG05', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Genting Sempah, Janda Baik, Bukit Tinggi' ),
    array( 'Zone' => 'PHG04', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Bentong, Raub, Kuala Lipis' ),
    array( 'Zone' => 'PHG03', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Maran, Chenor, Temerloh, Bera, Jerantut' ),
    array( 'Zone' => 'PHG06', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Bukit Fraser, Genting Higlands, Cameron Higlands' ),
    array( 'Zone' => 'PHG02', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Kuantan, Pekan, Rompin, Muadzam Shah' ),
    array( 'Zone' => 'PHG01', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Pulau Tioman' ),

    array( 'Zone' => 'PRK07', 'Negeri' => 'PERAK' , 'Lokasi' => 'Bukit Larut' ),
    array( 'Zone' => 'PRK02', 'Negeri' => 'PERAK' , 'Lokasi' => 'Ipoh, Batu Gajah, Kampar, Sg. Siput dan Kuala Kangsar' ),
    array( 'Zone' => 'PRK01', 'Negeri' => 'PERAK' , 'Lokasi' => 'Tapah,Slim River dan Tanjung Malim' ),
    array( 'Zone' => 'PRK03', 'Negeri' => 'PERAK' , 'Lokasi' => 'Pengkalan Hulu, Grik dan Lenggong ' ),
    array( 'Zone' => 'PRK04', 'Negeri' => 'PERAK' , 'Lokasi' => 'Temengor dan Belum' ),
    array( 'Zone' => 'PRK05', 'Negeri' => 'PERAK' , 'Lokasi' => 'Teluk Intan, Bagan Datoh, Kg.Gajah,Sri Iskandar, Beruas,Parit,Lumut,Setiawan dan Pulau Pangkor' ),
    array( 'Zone' => 'PRK06', 'Negeri' => 'PERAK' , 'Lokasi' => 'Selama, Taiping, Bagan Serai dan Parit Buntar' ),

    array( 'Zone' => 'PLS01', 'Negeri' => 'PERLIS' , 'Lokasi' => 'Kangar, Padang Besar, Arau' ),
    array( 'Zone' => 'PNG01', 'Negeri' => 'PULAU PINANG' , 'Lokasi' => 'Seluruh Negeri Pulau Pinang' ),

    array( 'Zone' => 'SBH09', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 9 - Sipitang, Membakut, Beaufort, Kuala Penyu, Weston, Tenom, Long Pa Sia' ),
    array( 'Zone' => 'SBH08', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 8 - Pensiangan, Keningau, Tambunan, Nabawan' ),
    array( 'Zone' => 'SBH07', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 7 - Papar, Ranau, Kota Belud, Tuaran, Penampang, Kota Kinabalu' ),
    array( 'Zone' => 'SBH06', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 6 - Gunung Kinabalu' ),
    array( 'Zone' => 'SBH05', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 5 - Kudat, Kota Marudu, Pitas, Pulau Banggi' ),
    array( 'Zone' => 'SBH03', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 3 - Lahad Datu, Kunak, Silabukan, Tungku, Sahabat, Semporna' ),
    array( 'Zone' => 'SBH02', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 2 - Pinangah, Terusan, Beluran, Kuamut, Telupit' ),
    array( 'Zone' => 'SBH01', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 1 - Sandakan, Bdr. Bkt. Garam, Semawang, Temanggong, Tambisan' ),
    array( 'Zone' => 'SBH04', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 4 - Tawau, Balong, Merotai, Kalabakan' ),

    array( 'Zone' => 'SWK01', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 1 - Limbang, Sundar, Terusan, Lawas' ),
    array( 'Zone' => 'SWK08', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 8 - Kuching, Bau, Lundu,Sematan' ),
    array( 'Zone' => 'SWK07', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 7 - Samarahan, Simunjan, Serian, Sebuyau, Meludam' ),
    array( 'Zone' => 'SWK06', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 6 - Kabong, Lingga, Sri Aman, Engkelili, Betong, Spaoh, Pusa, Saratok, Roban, Debak' ),
    array( 'Zone' => 'SWK05', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 5 - Belawai, Matu, Daro, Sarikei, Julau, Bitangor, Rajang' ),
    array( 'Zone' => 'SWK04', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 4 - Igan, Kanowit, Sibu, Dalat, Oya' ),
    array( 'Zone' => 'SWK03', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 3 - Song, Belingan, Sebauh, Bintulu, Tatau, Kapit' ),
    array( 'Zone' => 'SWK02', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 2 - Niah, Belaga, Sibuti, Miri, Bekenu, Marudi' ),

    array( 'Zone' => 'SGR01', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Gombak,H.Selangor,Rawang,H.Langat,Sepang,Petaling,S.Alam' ),
    array( 'Zone' => 'SGR02', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Sabak Bernam, Kuala Selangor, Klang, Kuala Langat' ),
    array( 'Zone' => 'SGR03', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Kuala Lumpur' ),
    array( 'Zone' => 'SGR04', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Putrajaya' ),

    array( 'Zone' => 'TRG01', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Kuala Terengganu, Marang' ),
    array( 'Zone' => 'TRG04', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Kemaman Dungun' ),
    array( 'Zone' => 'TRG03', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Hulu Terengganu' ),
    array( 'Zone' => 'TRG02', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Besut, Setiu' ),

    array( 'Zone' => 'WLY02', 'Negeri' => 'WILAYAH PERSEKUTUAN LABUAN' , 'Lokasi' => 'Labuan' )

);

//create zone data
/*
scraperwiki::sqliteexecute("drop table if exists zone"); 
scraperwiki::sqliteexecute('CREATE TABLE `zone` (`Zone` text,`Negeri` text,`Lokasi` text)');
scraperwiki::save_sqlite(array('Zone', 'Negeri'), $zones,$table_name="zone");
*/

//scraperwiki::sqliteexecute("drop table if exists solat"); 
scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS `solat` (`Zone` text, `Tarikh` text, `Hari` text,`Imsak` text,`Subuh` text,  `Syuruk` text, `Zohor` text, `Asar` text, `Maghrib` text, `Isyak` text )');

foreach($zones as $zone){
    $rows = array();
    for($month = 1; $month <= 12 ; $month++){
        $html = scraperWiki::scrape('http://www.e-solat.gov.my/waktusolat.php?zone='.$zone['Zone'].'&state=&year='.date('Y').'&jenis=year&bulan='.$month.'&LG=BM');         
        $dom = new simple_html_dom();
        $dom->load($html);
        
        $trs = $dom->find('table',9)->find('tr');
        echo count($trs);
        $day = 0;
        
        foreach(  $trs as $tr){
            
            if(($day>0) && ($day < (count($trs) - 2))){
                $daily = array();
                $daily['Zone'] = $zone['Zone'];
                $daily['Tarikh'] = date('Y').'-'.str_pad($month,2,'0',STR_PAD_LEFT).'-'.str_pad($day,2,'0',STR_PAD_LEFT);
                $daily['Hari'] = $tr->find('td',1)->plaintext;
                $daily['Imsak'] = $tr->find('td',2)->plaintext;
                $daily['Subuh'] = $tr->find('td',3)->plaintext;
                $daily['Syuruk'] = $tr->find('td',4)->plaintext;
                $daily['Zohor'] = $tr->find('td',5)->plaintext;
                $daily['Asar'] = $tr->find('td',6)->plaintext;
                $daily['Maghrib'] = $tr->find('td',7)->plaintext;
                $daily['Isyak'] = $tr->find('td',8)->plaintext;
                $rows[] = $daily;
            }
            $day++;
        }
        
    }
    scraperwiki::save_sqlite(array('Zone', 'Tarikh'), $rows,$table_name="solat");
}




?><?php

require 'scraperwiki/simple_html_dom.php';  

$zones = array(
    array( 'Zone' => 'JHR02', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Kota Tinggi, Mersing, Johor Bahru' ),
    array( 'Zone' => 'JHR04', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Batu Pahat, Muar, Segamat, Gemas' ),
    array( 'Zone' => 'JHR03', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Kluang dan Pontian' ),
    array( 'Zone' => 'JHR01', 'Negeri' => 'JOHOR' , 'Lokasi' => 'Pulau Aur dan Pemanggil' ),

    array( 'Zone' => 'KDH06', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Puncak Gunung Jerai' ),
    array( 'Zone' => 'KDH01', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Kota Setar, Kubang Pasu, Pokok Sena' ),
    array( 'Zone' => 'KDH05', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Langkawi' ),
    array( 'Zone' => 'KDH02', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Pendang, Kuala Muda, Yan' ),
    array( 'Zone' => 'KDH03', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Padang Terap, Sik, Baling' ),
    array( 'Zone' => 'KDH04', 'Negeri' => 'KEDAH' , 'Lokasi' => 'Kulim, Bandar Baharu' ),

    array( 'Zone' => 'KTN03', 'Negeri' => 'KELANTAN' , 'Lokasi' => 'Jeli, Gua Musang (Mukim Galas, Bertam)' ),
    array( 'Zone' => 'KTN01', 'Negeri' => 'KELANTAN' , 'Lokasi' => 'K.Bharu,Bachok,Pasir Puteh,Tumpat,Pasir Mas,Tnh. Merah,Machang,Kuala Krai,Mukim Chiku' ),

    array( 'Zone' => 'MLK01', 'Negeri' => 'MELAKA' , 'Lokasi' => 'Bandar Melaka, Alor Gajah, Jasin, Masjid Tanah, Merlimau, Nyalas' ),

    array( 'Zone' => 'NGS02', 'Negeri' => 'NEGERI SEMBILAN' , 'Lokasi' => 'Port Dickson, Seremban, Kuala Pilah, Jelebu, Rembau' ),
    array( 'Zone' => 'NGS01', 'Negeri' => 'NEGERI SEMBILAN' , 'Lokasi' => 'Jempol, Tampin' ),

    array( 'Zone' => 'PHG05', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Genting Sempah, Janda Baik, Bukit Tinggi' ),
    array( 'Zone' => 'PHG04', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Bentong, Raub, Kuala Lipis' ),
    array( 'Zone' => 'PHG03', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Maran, Chenor, Temerloh, Bera, Jerantut' ),
    array( 'Zone' => 'PHG06', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Bukit Fraser, Genting Higlands, Cameron Higlands' ),
    array( 'Zone' => 'PHG02', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Kuantan, Pekan, Rompin, Muadzam Shah' ),
    array( 'Zone' => 'PHG01', 'Negeri' => 'PAHANG' , 'Lokasi' => 'Pulau Tioman' ),

    array( 'Zone' => 'PRK07', 'Negeri' => 'PERAK' , 'Lokasi' => 'Bukit Larut' ),
    array( 'Zone' => 'PRK02', 'Negeri' => 'PERAK' , 'Lokasi' => 'Ipoh, Batu Gajah, Kampar, Sg. Siput dan Kuala Kangsar' ),
    array( 'Zone' => 'PRK01', 'Negeri' => 'PERAK' , 'Lokasi' => 'Tapah,Slim River dan Tanjung Malim' ),
    array( 'Zone' => 'PRK03', 'Negeri' => 'PERAK' , 'Lokasi' => 'Pengkalan Hulu, Grik dan Lenggong ' ),
    array( 'Zone' => 'PRK04', 'Negeri' => 'PERAK' , 'Lokasi' => 'Temengor dan Belum' ),
    array( 'Zone' => 'PRK05', 'Negeri' => 'PERAK' , 'Lokasi' => 'Teluk Intan, Bagan Datoh, Kg.Gajah,Sri Iskandar, Beruas,Parit,Lumut,Setiawan dan Pulau Pangkor' ),
    array( 'Zone' => 'PRK06', 'Negeri' => 'PERAK' , 'Lokasi' => 'Selama, Taiping, Bagan Serai dan Parit Buntar' ),

    array( 'Zone' => 'PLS01', 'Negeri' => 'PERLIS' , 'Lokasi' => 'Kangar, Padang Besar, Arau' ),
    array( 'Zone' => 'PNG01', 'Negeri' => 'PULAU PINANG' , 'Lokasi' => 'Seluruh Negeri Pulau Pinang' ),

    array( 'Zone' => 'SBH09', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 9 - Sipitang, Membakut, Beaufort, Kuala Penyu, Weston, Tenom, Long Pa Sia' ),
    array( 'Zone' => 'SBH08', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 8 - Pensiangan, Keningau, Tambunan, Nabawan' ),
    array( 'Zone' => 'SBH07', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 7 - Papar, Ranau, Kota Belud, Tuaran, Penampang, Kota Kinabalu' ),
    array( 'Zone' => 'SBH06', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 6 - Gunung Kinabalu' ),
    array( 'Zone' => 'SBH05', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 5 - Kudat, Kota Marudu, Pitas, Pulau Banggi' ),
    array( 'Zone' => 'SBH03', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 3 - Lahad Datu, Kunak, Silabukan, Tungku, Sahabat, Semporna' ),
    array( 'Zone' => 'SBH02', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 2 - Pinangah, Terusan, Beluran, Kuamut, Telupit' ),
    array( 'Zone' => 'SBH01', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 1 - Sandakan, Bdr. Bkt. Garam, Semawang, Temanggong, Tambisan' ),
    array( 'Zone' => 'SBH04', 'Negeri' => 'SABAH' , 'Lokasi' => 'Zon 4 - Tawau, Balong, Merotai, Kalabakan' ),

    array( 'Zone' => 'SWK01', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 1 - Limbang, Sundar, Terusan, Lawas' ),
    array( 'Zone' => 'SWK08', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 8 - Kuching, Bau, Lundu,Sematan' ),
    array( 'Zone' => 'SWK07', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 7 - Samarahan, Simunjan, Serian, Sebuyau, Meludam' ),
    array( 'Zone' => 'SWK06', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 6 - Kabong, Lingga, Sri Aman, Engkelili, Betong, Spaoh, Pusa, Saratok, Roban, Debak' ),
    array( 'Zone' => 'SWK05', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 5 - Belawai, Matu, Daro, Sarikei, Julau, Bitangor, Rajang' ),
    array( 'Zone' => 'SWK04', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 4 - Igan, Kanowit, Sibu, Dalat, Oya' ),
    array( 'Zone' => 'SWK03', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 3 - Song, Belingan, Sebauh, Bintulu, Tatau, Kapit' ),
    array( 'Zone' => 'SWK02', 'Negeri' => 'SARAWAK' , 'Lokasi' => 'Zon 2 - Niah, Belaga, Sibuti, Miri, Bekenu, Marudi' ),

    array( 'Zone' => 'SGR01', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Gombak,H.Selangor,Rawang,H.Langat,Sepang,Petaling,S.Alam' ),
    array( 'Zone' => 'SGR02', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Sabak Bernam, Kuala Selangor, Klang, Kuala Langat' ),
    array( 'Zone' => 'SGR03', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Kuala Lumpur' ),
    array( 'Zone' => 'SGR04', 'Negeri' => 'SELANGOR DAN WILAYAH PERSEKUTUAN' , 'Lokasi' => 'Putrajaya' ),

    array( 'Zone' => 'TRG01', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Kuala Terengganu, Marang' ),
    array( 'Zone' => 'TRG04', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Kemaman Dungun' ),
    array( 'Zone' => 'TRG03', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Hulu Terengganu' ),
    array( 'Zone' => 'TRG02', 'Negeri' => 'TERENGGANU' , 'Lokasi' => 'Besut, Setiu' ),

    array( 'Zone' => 'WLY02', 'Negeri' => 'WILAYAH PERSEKUTUAN LABUAN' , 'Lokasi' => 'Labuan' )

);

//create zone data
/*
scraperwiki::sqliteexecute("drop table if exists zone"); 
scraperwiki::sqliteexecute('CREATE TABLE `zone` (`Zone` text,`Negeri` text,`Lokasi` text)');
scraperwiki::save_sqlite(array('Zone', 'Negeri'), $zones,$table_name="zone");
*/

//scraperwiki::sqliteexecute("drop table if exists solat"); 
scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS `solat` (`Zone` text, `Tarikh` text, `Hari` text,`Imsak` text,`Subuh` text,  `Syuruk` text, `Zohor` text, `Asar` text, `Maghrib` text, `Isyak` text )');

foreach($zones as $zone){
    $rows = array();
    for($month = 1; $month <= 12 ; $month++){
        $html = scraperWiki::scrape('http://www.e-solat.gov.my/waktusolat.php?zone='.$zone['Zone'].'&state=&year='.date('Y').'&jenis=year&bulan='.$month.'&LG=BM');         
        $dom = new simple_html_dom();
        $dom->load($html);
        
        $trs = $dom->find('table',9)->find('tr');
        echo count($trs);
        $day = 0;
        
        foreach(  $trs as $tr){
            
            if(($day>0) && ($day < (count($trs) - 2))){
                $daily = array();
                $daily['Zone'] = $zone['Zone'];
                $daily['Tarikh'] = date('Y').'-'.str_pad($month,2,'0',STR_PAD_LEFT).'-'.str_pad($day,2,'0',STR_PAD_LEFT);
                $daily['Hari'] = $tr->find('td',1)->plaintext;
                $daily['Imsak'] = $tr->find('td',2)->plaintext;
                $daily['Subuh'] = $tr->find('td',3)->plaintext;
                $daily['Syuruk'] = $tr->find('td',4)->plaintext;
                $daily['Zohor'] = $tr->find('td',5)->plaintext;
                $daily['Asar'] = $tr->find('td',6)->plaintext;
                $daily['Maghrib'] = $tr->find('td',7)->plaintext;
                $daily['Isyak'] = $tr->find('td',8)->plaintext;
                $rows[] = $daily;
            }
            $day++;
        }
        
    }
    scraperwiki::save_sqlite(array('Zone', 'Tarikh'), $rows,$table_name="solat");
}




?>