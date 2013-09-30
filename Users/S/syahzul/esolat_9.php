<?php
require 'scraperwiki/simple_html_dom.php';  

// debug
//scraperwiki::sqliteexecute("drop table if exists `zones`");
scraperwiki::sqliteexecute("create table if not exists `zones` (`code` text,`state` text,`location` text)");

$zones = array(
    array( 'code' => 'JHR01', 'state' => 'Johor' , 'location' => 'Pulau Aur dan Pemanggil' ),
    array( 'code' => 'JHR02', 'state' => 'Johor' , 'location' => 'Kota Tinggi, Mersing, Johor Bahru' ),
    array( 'code' => 'JHR03', 'state' => 'Johor' , 'location' => 'Kluang dan Pontian' ),
    array( 'code' => 'JHR04', 'state' => 'Johor' , 'location' => 'Batu Pahat, Muar, Segamat, Gemas' ),

    array( 'code' => 'KDH01', 'state' => 'Kedah' , 'location' => 'Kota Setar, Kubang Pasu, Pokok Sena' ),
    array( 'code' => 'KDH02', 'state' => 'Kedah' , 'location' => 'Pendang, Kuala Muda, Yan' ),
    array( 'code' => 'KDH03', 'state' => 'Kedah' , 'location' => 'Padang Terap, Sik, Baling' ),
    array( 'code' => 'KDH04', 'state' => 'Kedah' , 'location' => 'Kulim, Bandar Baharu' ),
    array( 'code' => 'KDH05', 'state' => 'Kedah' , 'location' => 'Langkawi' ),
    array( 'code' => 'KDH06', 'state' => 'Kedah' , 'location' => 'Puncak Gunung Jerai' ),

    array( 'code' => 'KTN01', 'state' => 'Kelantan' , 'location' => 'Kota Bharu, Bachok, Pasir Puteh, Tumpat, Pasir Mas, Tanah Merah, Machang, Kuala Krai, Mukim Chiku' ),
    array( 'code' => 'KTN03', 'state' => 'Kelantan' , 'location' => 'Jeli, Gua Musang (Mukim Galas, Bertam)' ),


    array( 'code' => 'MLK01', 'state' => 'Melaka' , 'location' => 'Bandar Melaka, Alor Gajah, Jasin, Masjid Tanah, Merlimau, Nyalas' ),

    array( 'code' => 'NGS01', 'state' => 'Negeri Sembilan' , 'location' => 'Jempol, Tampin' ),
    array( 'code' => 'NGS02', 'state' => 'Negeri Sembilan' , 'location' => 'Port Dickson, Seremban, Kuala Pilah, Jelebu, Rembau' ),


    array( 'code' => 'PHG01', 'state' => 'Pahang' , 'location' => 'Pulau Tioman' ),
    array( 'code' => 'PHG02', 'state' => 'Pahang' , 'location' => 'Kuantan, Pekan, Rompin, Muadzam Shah' ),
    array( 'code' => 'PHG03', 'state' => 'Pahang' , 'location' => 'Maran, Chenor, Temerloh, Bera, Jerantut' ),
    array( 'code' => 'PHG04', 'state' => 'Pahang' , 'location' => 'Bentong, Raub, Kuala Lipis' ),
    array( 'code' => 'PHG05', 'state' => 'Pahang' , 'location' => 'Genting Sempah, Janda Baik, Bukit Tinggi' ),
    array( 'code' => 'PHG06', 'state' => 'Pahang' , 'location' => 'Bukit Fraser, Genting Higlands, Cameron Higlands' ),

    array( 'code' => 'PRK01', 'state' => 'Perak' , 'location' => 'Tapah, Slim River, Tanjung Malim' ),
    array( 'code' => 'PRK02', 'state' => 'Perak' , 'location' => 'Ipoh, Batu Gajah, Kampar, Sg. Siput, Kuala Kangsar' ),
    array( 'code' => 'PRK03', 'state' => 'Perak' , 'location' => 'Pengkalan Hulu, Grik, Lenggong ' ),
    array( 'code' => 'PRK04', 'state' => 'Perak' , 'location' => 'Temengor dan Belum' ),
    array( 'code' => 'PRK05', 'state' => 'Perak' , 'location' => 'Teluk Intan, Bagan Datoh, Kg. Gajah, Sri Iskandar, Beruas, Parit, Lumut, Setiawan, Pulau Pangkor' ),
    array( 'code' => 'PRK06', 'state' => 'Perak' , 'location' => 'Selama, Taiping, Bagan Serai, Parit Buntar' ),
    array( 'code' => 'PRK07', 'state' => 'Perak' , 'location' => 'Bukit Larut' ),

    array( 'code' => 'PLS01', 'state' => 'Perlis' , 'location' => 'Kangar, Padang Besar, Arau' ),
    array( 'code' => 'PNG01', 'state' => 'Pulau Pinang' , 'location' => 'Seluruh negeri Pulau Pinang' ),

    array( 'code' => 'SBH01', 'state' => 'Sabah' , 'location' => 'Zon 1 - Sandakan, Bdr. Bkt. Garam, Semawang, Temanggong, Tambisan' ),
    array( 'code' => 'SBH02', 'state' => 'Sabah' , 'location' => 'Zon 2 - Pinangah, Terusan, Beluran, Kuamut, Telupit' ),
    array( 'code' => 'SBH03', 'state' => 'Sabah' , 'location' => 'Zon 3 - Lahad Datu, Kunak, Silabukan, Tungku, Sahabat, Semporna' ),
    array( 'code' => 'SBH04', 'state' => 'Sabah' , 'location' => 'Zon 4 - Tawau, Balong, Merotai, Kalabakan' ),
    array( 'code' => 'SBH05', 'state' => 'Sabah' , 'location' => 'Zon 5 - Kudat, Kota Marudu, Pitas, Pulau Banggi' ),
    array( 'code' => 'SBH06', 'state' => 'Sabah' , 'location' => 'Zon 6 - Gunung Kinabalu' ),
    array( 'code' => 'SBH07', 'state' => 'Sabah' , 'location' => 'Zon 7 - Papar, Ranau, Kota Belud, Tuaran, Penampang, Kota Kinabalu' ),
    array( 'code' => 'SBH08', 'state' => 'Sabah' , 'location' => 'Zon 8 - Pensiangan, Keningau, Tambunan, Nabawan' ),
    array( 'code' => 'SBH09', 'state' => 'Sabah' , 'location' => 'Zon 9 - Sipitang, Membakut, Beaufort, Kuala Penyu, Weston, Tenom, Long Pa Sia' ),

    array( 'code' => 'SWK01', 'state' => 'Sarawak' , 'location' => 'Zon 1 - Limbang, Sundar, Terusan, Lawas' ),
    array( 'code' => 'SWK02', 'state' => 'Sarawak' , 'location' => 'Zon 2 - Niah, Belaga, Sibuti, Miri, Bekenu, Marudi' ),
    array( 'code' => 'SWK03', 'state' => 'Sarawak' , 'location' => 'Zon 3 - Song, Belingan, Sebauh, Bintulu, Tatau, Kapit' ),
    array( 'code' => 'SWK04', 'state' => 'Sarawak' , 'location' => 'Zon 4 - Igan, Kanowit, Sibu, Dalat, Oya' ),
    array( 'code' => 'SWK05', 'state' => 'Sarawak' , 'location' => 'Zon 5 - Belawai, Matu, Daro, Sarikei, Julau, Bitangor, Rajang' ),
    array( 'code' => 'SWK06', 'state' => 'Sarawak' , 'location' => 'Zon 6 - Kabong, Lingga, Sri Aman, Engkelili, Betong, Spaoh, Pusa, Saratok, Roban, Debak' ),
    array( 'code' => 'SWK07', 'state' => 'Sarawak' , 'location' => 'Zon 7 - Samarahan, Simunjan, Serian, Sebuyau, Meludam' ),
    array( 'code' => 'SWK08', 'state' => 'Sarawak' , 'location' => 'Zon 8 - Kuching, Bau, Lundu, Sematan' ),

    array( 'code' => 'SGR01', 'state' => 'Selangor' , 'location' => 'Gombak, Hulu Selangor, Rawang, Sepang, Petaling, Shah Alam' ),
    array( 'code' => 'SGR02', 'state' => 'Selangor' , 'location' => 'Sabak Bernam, Kuala Selangor, Klang, Kuala Langat' ),
    array( 'code' => 'SGR03', 'state' => 'Kuala Lumpur' , 'location' => 'Kuala Lumpur' ),
    array( 'code' => 'SGR04', 'state' => 'Putrajaya' , 'location' => 'Putrajaya' ),

    array( 'code' => 'TRG01', 'state' => 'Terengganu' , 'location' => 'Kuala Terengganu, Marang' ),
    array( 'code' => 'TRG02', 'state' => 'Terengganu' , 'location' => 'Besut, Setiu' ),
    array( 'code' => 'TRG03', 'state' => 'Terengganu' , 'location' => 'Hulu Terengganu' ),
    array( 'code' => 'TRG04', 'state' => 'Terengganu' , 'location' => 'Kemaman Dungun' ),

    array( 'code' => 'WLY02', 'state' => 'Wilayah Persekutuan Labuan' , 'location' => 'Labuan' )

);

//create zone data
//scraperwiki::save_sqlite(array('code', 'state'), $zones, $table_name = "zones");

scraperwiki::sqliteexecute("create table if not exists `timetables` (`code` text, `date` text, `day` text,`imsak` text,`subuh` text, `syuruk` text, `zuhur` text, `asar` text, `maghrib` text, `isyak` text )");

//print_r($zones);

//foreach ($zones as $zone => $val)
for ($x = 0; $x < count($zones); $x++)
{
    if ( ! empty($zones[$x]['code']))
    {
        // make sure the record not exists
        $result = scraperwiki::sqliteexecute("select * from zones where code = '".$zones[$x]['code']."'");
        if ( ! $result)
        {
            scraperwiki::sqliteexecute("insert into zones values (?, ?, ?)", array($zones[$x]['code'], $zones[$x]['state'], $zones[$x]['location']));
        }

        $rows = array();

        for ($month = 1; $month <= 12 ; $month++)
        {
            $rows = fetchData($zones[$x]['code'], $month);
        }
        scraperwiki::save_sqlite(array('code', 'date'), $rows, $table_name="timetables");
    }
}

function fetchData($zone, $month)
{
    $html = scraperWiki::scrape('http://www.e-solat.gov.my/web/waktusolat.php?zone='.$zone.'&state=&year='.date('Y').'&jenis=year&bulan='.$month.'&LG=BM');         
    
    $rows = array();

    $dom = new simple_html_dom();
    $dom->load($html);
            
    if ($dom->find('table', 9))
    {  
        $trs = $dom->find('table',9)->find('tr');
        $day = 0;
                
        foreach ($trs as $tr)
        {
            if (($day > 0) && ($day < (count($trs) - 2)))
            {
                $daily = array();
                $daily['code']     = $zone;
                $daily['date']     = date('Y').'-'.str_pad($month,2,'0',STR_PAD_LEFT).'-'.str_pad($day,2,'0',STR_PAD_LEFT);
                $daily['day']      = getDayNum($tr->find('td', 1)->plaintext);
                $daily['imsak']    = formatTime(trim($tr->find('td', 2)->plaintext));
                $daily['subuh']    = formatTime(trim($tr->find('td', 3)->plaintext));
                $daily['syuruk']   = formatTime(trim($tr->find('td', 4)->plaintext));
                $daily['zuhur']    = formatTime(trim($tr->find('td', 5)->plaintext));
                $daily['asar']     = formatTime(trim($tr->find('td', 6)->plaintext));
                $daily['maghrib']  = formatTime(trim($tr->find('td', 7)->plaintext));
                $daily['isyak']    = formatTime(trim($tr->find('td', 8)->plaintext));
                $rows[] = $daily;
            }
            $day++;
        }
    }
    else
    {
        fetchData($zone, $month);
    }
    return $rows;
}

function getDayNum($day)
{
    $num = 0;
    $day = trim($day);
    switch ($day)
    {
        case 'Isnin':
            $num = 1;
            break;
        case 'Selasa':
            $num =  2;
            break;
        case 'Rabu':
            $num =  3;
            break;
        case 'Khamis':
            $num =  4;
            break;
        case 'Jumaat':
            $num =  5;
            break;
        case 'Sabtu':
            $num =  6;
            break;
        case 'Ahad':
            $num =  0;
            break;
    }
    return $num;
}

function formatTime($time)
{
    $time = str_replace(';', ':', $time);
    $time = date('H:i', strtotime($time));
    return $time;
}<?php
require 'scraperwiki/simple_html_dom.php';  

// debug
//scraperwiki::sqliteexecute("drop table if exists `zones`");
scraperwiki::sqliteexecute("create table if not exists `zones` (`code` text,`state` text,`location` text)");

$zones = array(
    array( 'code' => 'JHR01', 'state' => 'Johor' , 'location' => 'Pulau Aur dan Pemanggil' ),
    array( 'code' => 'JHR02', 'state' => 'Johor' , 'location' => 'Kota Tinggi, Mersing, Johor Bahru' ),
    array( 'code' => 'JHR03', 'state' => 'Johor' , 'location' => 'Kluang dan Pontian' ),
    array( 'code' => 'JHR04', 'state' => 'Johor' , 'location' => 'Batu Pahat, Muar, Segamat, Gemas' ),

    array( 'code' => 'KDH01', 'state' => 'Kedah' , 'location' => 'Kota Setar, Kubang Pasu, Pokok Sena' ),
    array( 'code' => 'KDH02', 'state' => 'Kedah' , 'location' => 'Pendang, Kuala Muda, Yan' ),
    array( 'code' => 'KDH03', 'state' => 'Kedah' , 'location' => 'Padang Terap, Sik, Baling' ),
    array( 'code' => 'KDH04', 'state' => 'Kedah' , 'location' => 'Kulim, Bandar Baharu' ),
    array( 'code' => 'KDH05', 'state' => 'Kedah' , 'location' => 'Langkawi' ),
    array( 'code' => 'KDH06', 'state' => 'Kedah' , 'location' => 'Puncak Gunung Jerai' ),

    array( 'code' => 'KTN01', 'state' => 'Kelantan' , 'location' => 'Kota Bharu, Bachok, Pasir Puteh, Tumpat, Pasir Mas, Tanah Merah, Machang, Kuala Krai, Mukim Chiku' ),
    array( 'code' => 'KTN03', 'state' => 'Kelantan' , 'location' => 'Jeli, Gua Musang (Mukim Galas, Bertam)' ),


    array( 'code' => 'MLK01', 'state' => 'Melaka' , 'location' => 'Bandar Melaka, Alor Gajah, Jasin, Masjid Tanah, Merlimau, Nyalas' ),

    array( 'code' => 'NGS01', 'state' => 'Negeri Sembilan' , 'location' => 'Jempol, Tampin' ),
    array( 'code' => 'NGS02', 'state' => 'Negeri Sembilan' , 'location' => 'Port Dickson, Seremban, Kuala Pilah, Jelebu, Rembau' ),


    array( 'code' => 'PHG01', 'state' => 'Pahang' , 'location' => 'Pulau Tioman' ),
    array( 'code' => 'PHG02', 'state' => 'Pahang' , 'location' => 'Kuantan, Pekan, Rompin, Muadzam Shah' ),
    array( 'code' => 'PHG03', 'state' => 'Pahang' , 'location' => 'Maran, Chenor, Temerloh, Bera, Jerantut' ),
    array( 'code' => 'PHG04', 'state' => 'Pahang' , 'location' => 'Bentong, Raub, Kuala Lipis' ),
    array( 'code' => 'PHG05', 'state' => 'Pahang' , 'location' => 'Genting Sempah, Janda Baik, Bukit Tinggi' ),
    array( 'code' => 'PHG06', 'state' => 'Pahang' , 'location' => 'Bukit Fraser, Genting Higlands, Cameron Higlands' ),

    array( 'code' => 'PRK01', 'state' => 'Perak' , 'location' => 'Tapah, Slim River, Tanjung Malim' ),
    array( 'code' => 'PRK02', 'state' => 'Perak' , 'location' => 'Ipoh, Batu Gajah, Kampar, Sg. Siput, Kuala Kangsar' ),
    array( 'code' => 'PRK03', 'state' => 'Perak' , 'location' => 'Pengkalan Hulu, Grik, Lenggong ' ),
    array( 'code' => 'PRK04', 'state' => 'Perak' , 'location' => 'Temengor dan Belum' ),
    array( 'code' => 'PRK05', 'state' => 'Perak' , 'location' => 'Teluk Intan, Bagan Datoh, Kg. Gajah, Sri Iskandar, Beruas, Parit, Lumut, Setiawan, Pulau Pangkor' ),
    array( 'code' => 'PRK06', 'state' => 'Perak' , 'location' => 'Selama, Taiping, Bagan Serai, Parit Buntar' ),
    array( 'code' => 'PRK07', 'state' => 'Perak' , 'location' => 'Bukit Larut' ),

    array( 'code' => 'PLS01', 'state' => 'Perlis' , 'location' => 'Kangar, Padang Besar, Arau' ),
    array( 'code' => 'PNG01', 'state' => 'Pulau Pinang' , 'location' => 'Seluruh negeri Pulau Pinang' ),

    array( 'code' => 'SBH01', 'state' => 'Sabah' , 'location' => 'Zon 1 - Sandakan, Bdr. Bkt. Garam, Semawang, Temanggong, Tambisan' ),
    array( 'code' => 'SBH02', 'state' => 'Sabah' , 'location' => 'Zon 2 - Pinangah, Terusan, Beluran, Kuamut, Telupit' ),
    array( 'code' => 'SBH03', 'state' => 'Sabah' , 'location' => 'Zon 3 - Lahad Datu, Kunak, Silabukan, Tungku, Sahabat, Semporna' ),
    array( 'code' => 'SBH04', 'state' => 'Sabah' , 'location' => 'Zon 4 - Tawau, Balong, Merotai, Kalabakan' ),
    array( 'code' => 'SBH05', 'state' => 'Sabah' , 'location' => 'Zon 5 - Kudat, Kota Marudu, Pitas, Pulau Banggi' ),
    array( 'code' => 'SBH06', 'state' => 'Sabah' , 'location' => 'Zon 6 - Gunung Kinabalu' ),
    array( 'code' => 'SBH07', 'state' => 'Sabah' , 'location' => 'Zon 7 - Papar, Ranau, Kota Belud, Tuaran, Penampang, Kota Kinabalu' ),
    array( 'code' => 'SBH08', 'state' => 'Sabah' , 'location' => 'Zon 8 - Pensiangan, Keningau, Tambunan, Nabawan' ),
    array( 'code' => 'SBH09', 'state' => 'Sabah' , 'location' => 'Zon 9 - Sipitang, Membakut, Beaufort, Kuala Penyu, Weston, Tenom, Long Pa Sia' ),

    array( 'code' => 'SWK01', 'state' => 'Sarawak' , 'location' => 'Zon 1 - Limbang, Sundar, Terusan, Lawas' ),
    array( 'code' => 'SWK02', 'state' => 'Sarawak' , 'location' => 'Zon 2 - Niah, Belaga, Sibuti, Miri, Bekenu, Marudi' ),
    array( 'code' => 'SWK03', 'state' => 'Sarawak' , 'location' => 'Zon 3 - Song, Belingan, Sebauh, Bintulu, Tatau, Kapit' ),
    array( 'code' => 'SWK04', 'state' => 'Sarawak' , 'location' => 'Zon 4 - Igan, Kanowit, Sibu, Dalat, Oya' ),
    array( 'code' => 'SWK05', 'state' => 'Sarawak' , 'location' => 'Zon 5 - Belawai, Matu, Daro, Sarikei, Julau, Bitangor, Rajang' ),
    array( 'code' => 'SWK06', 'state' => 'Sarawak' , 'location' => 'Zon 6 - Kabong, Lingga, Sri Aman, Engkelili, Betong, Spaoh, Pusa, Saratok, Roban, Debak' ),
    array( 'code' => 'SWK07', 'state' => 'Sarawak' , 'location' => 'Zon 7 - Samarahan, Simunjan, Serian, Sebuyau, Meludam' ),
    array( 'code' => 'SWK08', 'state' => 'Sarawak' , 'location' => 'Zon 8 - Kuching, Bau, Lundu, Sematan' ),

    array( 'code' => 'SGR01', 'state' => 'Selangor' , 'location' => 'Gombak, Hulu Selangor, Rawang, Sepang, Petaling, Shah Alam' ),
    array( 'code' => 'SGR02', 'state' => 'Selangor' , 'location' => 'Sabak Bernam, Kuala Selangor, Klang, Kuala Langat' ),
    array( 'code' => 'SGR03', 'state' => 'Kuala Lumpur' , 'location' => 'Kuala Lumpur' ),
    array( 'code' => 'SGR04', 'state' => 'Putrajaya' , 'location' => 'Putrajaya' ),

    array( 'code' => 'TRG01', 'state' => 'Terengganu' , 'location' => 'Kuala Terengganu, Marang' ),
    array( 'code' => 'TRG02', 'state' => 'Terengganu' , 'location' => 'Besut, Setiu' ),
    array( 'code' => 'TRG03', 'state' => 'Terengganu' , 'location' => 'Hulu Terengganu' ),
    array( 'code' => 'TRG04', 'state' => 'Terengganu' , 'location' => 'Kemaman Dungun' ),

    array( 'code' => 'WLY02', 'state' => 'Wilayah Persekutuan Labuan' , 'location' => 'Labuan' )

);

//create zone data
//scraperwiki::save_sqlite(array('code', 'state'), $zones, $table_name = "zones");

scraperwiki::sqliteexecute("create table if not exists `timetables` (`code` text, `date` text, `day` text,`imsak` text,`subuh` text, `syuruk` text, `zuhur` text, `asar` text, `maghrib` text, `isyak` text )");

//print_r($zones);

//foreach ($zones as $zone => $val)
for ($x = 0; $x < count($zones); $x++)
{
    if ( ! empty($zones[$x]['code']))
    {
        // make sure the record not exists
        $result = scraperwiki::sqliteexecute("select * from zones where code = '".$zones[$x]['code']."'");
        if ( ! $result)
        {
            scraperwiki::sqliteexecute("insert into zones values (?, ?, ?)", array($zones[$x]['code'], $zones[$x]['state'], $zones[$x]['location']));
        }

        $rows = array();

        for ($month = 1; $month <= 12 ; $month++)
        {
            $rows = fetchData($zones[$x]['code'], $month);
        }
        scraperwiki::save_sqlite(array('code', 'date'), $rows, $table_name="timetables");
    }
}

function fetchData($zone, $month)
{
    $html = scraperWiki::scrape('http://www.e-solat.gov.my/web/waktusolat.php?zone='.$zone.'&state=&year='.date('Y').'&jenis=year&bulan='.$month.'&LG=BM');         
    
    $rows = array();

    $dom = new simple_html_dom();
    $dom->load($html);
            
    if ($dom->find('table', 9))
    {  
        $trs = $dom->find('table',9)->find('tr');
        $day = 0;
                
        foreach ($trs as $tr)
        {
            if (($day > 0) && ($day < (count($trs) - 2)))
            {
                $daily = array();
                $daily['code']     = $zone;
                $daily['date']     = date('Y').'-'.str_pad($month,2,'0',STR_PAD_LEFT).'-'.str_pad($day,2,'0',STR_PAD_LEFT);
                $daily['day']      = getDayNum($tr->find('td', 1)->plaintext);
                $daily['imsak']    = formatTime(trim($tr->find('td', 2)->plaintext));
                $daily['subuh']    = formatTime(trim($tr->find('td', 3)->plaintext));
                $daily['syuruk']   = formatTime(trim($tr->find('td', 4)->plaintext));
                $daily['zuhur']    = formatTime(trim($tr->find('td', 5)->plaintext));
                $daily['asar']     = formatTime(trim($tr->find('td', 6)->plaintext));
                $daily['maghrib']  = formatTime(trim($tr->find('td', 7)->plaintext));
                $daily['isyak']    = formatTime(trim($tr->find('td', 8)->plaintext));
                $rows[] = $daily;
            }
            $day++;
        }
    }
    else
    {
        fetchData($zone, $month);
    }
    return $rows;
}

function getDayNum($day)
{
    $num = 0;
    $day = trim($day);
    switch ($day)
    {
        case 'Isnin':
            $num = 1;
            break;
        case 'Selasa':
            $num =  2;
            break;
        case 'Rabu':
            $num =  3;
            break;
        case 'Khamis':
            $num =  4;
            break;
        case 'Jumaat':
            $num =  5;
            break;
        case 'Sabtu':
            $num =  6;
            break;
        case 'Ahad':
            $num =  0;
            break;
    }
    return $num;
}

function formatTime($time)
{
    $time = str_replace(';', ':', $time);
    $time = date('H:i', strtotime($time));
    return $time;
}