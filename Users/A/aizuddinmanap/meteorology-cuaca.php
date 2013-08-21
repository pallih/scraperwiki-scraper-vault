<?php
require 'scraperwiki/simple_html_dom.php';

$regions = array(
    //Johor
    array('Id' => '3354', 'Daerah' => 'Batu Pahat'),
    array('Id' => '3358', 'Daerah' => 'Johor Bahru'),
    array('Id' => '3360', 'Daerah' => 'Kluang'),
    array('Id' => '3364', 'Daerah' => 'Kota Tinggi'),
    array('Id' => '3350', 'Daerah' => 'Ledang'),
    array('Id' => '3362', 'Daerah' => 'Mersing'),
    array('Id' => '3352', 'Daerah' => 'Muar'),
    array('Id' => '3366', 'Daerah' => 'Nusajaya'),
    array('Id' => '3348', 'Daerah' => 'Segamat'),
    array('Id' => '3356', 'Daerah' => 'Pontian'),
        
    //Kedah
    array('Id' => '3452', 'Daerah' => 'Baling'),
    array('Id' => '3450', 'Daerah' => 'Kuala Muda'),
    array('Id' => '3438', 'Daerah' => 'Kubang Pasu'),
    array('Id' => '3456', 'Daerah' => 'Kulim'),
    array('Id' => '3442', 'Daerah' => 'Kota Setar'),
    array('Id' => '3460', 'Daerah' => 'Langkawi'),
    array('Id' => '3440', 'Daerah' => 'Padang Terap'),
    array('Id' => '3444', 'Daerah' => 'Pendang'),
    array('Id' => '3458', 'Daerah' => 'Pokok Sena'),
    array('Id' => '3448', 'Daerah' => 'Sik'),
    array('Id' => '3446', 'Daerah' => 'Yan'),
        
        
    //Kelantan
    array('Id' => '3294', 'Daerah' => 'Bachok'),
    array('Id' => '3306', 'Daerah' => 'Gua Musang'),
    array('Id' => '3302', 'Daerah' => 'Jeli'),
    array('Id' => '3290', 'Daerah' => 'Kota Bharu'),
    array('Id' => '3304', 'Daerah' => 'Kuala Krai'),
    array('Id' => '3310', 'Daerah' => 'Lojing'),
    array('Id' => '3298', 'Daerah' => 'Machang'),
    array('Id' => '3300', 'Daerah' => 'Pasir Mas'),
    array('Id' => '3296', 'Daerah' => 'Pasir Puteh'),
    array('Id' => '3308', 'Daerah' => 'Tanah Merah'),
    array('Id' => '3292', 'Daerah' => 'Tumpat'),

    //Kuala Lumpur
    array('Id' => '3406', 'Daerah' => 'Kuala Lumpur'),

    //Labuan
    array('Id' => '3480', 'Daerah' => 'Labuan'),
        
    //Melaka
    array('Id' => '3368', 'Daerah' => 'Alor Gajah'),
    array('Id' => '3372', 'Daerah' => 'Jasin'),
    array('Id' => '3370', 'Daerah' => 'Melaka Tengah'),

    //Negeri Sembilan
    array('Id' => '3374', 'Daerah' => 'Jelebu'),
    array('Id' => '3384', 'Daerah' => 'Jempol'),    
    array('Id' => '3382', 'Daerah' => 'Kuala Pilah'),
    array('Id' => '3378', 'Daerah' => 'Port Dickson'),
    array('Id' => '3380', 'Daerah' => 'Rembau'),
    array('Id' => '3376', 'Daerah' => 'Seremban'),
    array('Id' => '3386', 'Daerah' => 'Tampin'),

    //Pahang
    array('Id' => '3334', 'Daerah' => 'Bentong'),
    array('Id' => '3344', 'Daerah' => 'Bera'),
    array('Id' => '3326', 'Daerah' => 'Cameron Highland'),
    array('Id' => '3330', 'Daerah' => 'Jerantut'),
    array('Id' => '3340', 'Daerah' => 'Kuantan'),
    array('Id' => '3328', 'Daerah' => 'Lipis'),
    array('Id' => '3338', 'Daerah' => 'Maran'),
    array('Id' => '3342', 'Daerah' => 'Pekan'),
    array('Id' => '3332', 'Daerah' => 'Raub'),
    array('Id' => '3346', 'Daerah' => 'Rompin'),
    array('Id' => '3336', 'Daerah' => 'Temerloh'),
        
    //Penang'
    array('Id' => '3434', 'Daerah' => 'Barat Daya'),
    array('Id' => '3432', 'Daerah' => 'Seberang Prai Selatan'),
    array('Id' => '3430', 'Daerah' => 'Seberang Prai Tengah'),
    array('Id' => '3428', 'Daerah' => 'Seberang Prai Utara'),
    array('Id' => '3436', 'Daerah' => 'Timur Laut'),
        
    //Perak
    array('Id' => '3426', 'Daerah' => 'Batang Padang'),
    array('Id' => '3424', 'Daerah' => 'Hilir Perak'),
    array('Id' => '3414', 'Daerah' => 'Hulu Perak'),
    array('Id' => '3410', 'Daerah' => 'Kerian'),
    array('Id' => '3422', 'Daerah' => 'Kinta'),
    array('Id' => '3416', 'Daerah' => 'Kuala Kangsar'),
    array('Id' => '3412', 'Daerah' => 'Larut'),
    array('Id' => '3418', 'Daerah' => 'Manjung'),
    array('Id' => '3420', 'Daerah' => 'Perak Tengah'),

    //Perlis
    array('Id' => '3468', 'Daerah' => 'Arau'),
    array('Id' => '3466', 'Daerah' => 'Kangar'),
    array('Id' => '3464', 'Daerah' => 'Padang Besar Selatan'),
    array('Id' => '3462', 'Daerah' => 'Padang Besar Utara'),
        
        
    //Putrajaya
    array('Id' => '3408', 'Daerah' => 'Putrajaya'),    
        
    //Sabah
    array('Id' => '3470', 'Daerah' => 'Kudat'),
    array('Id' => '3472', 'Daerah' => 'Pantai Barat'),
    array('Id' => '3476', 'Daerah' => 'Pedalaman'),
    array('Id' => '3474', 'Daerah' => 'Sandakan'),
    array('Id' => '3478', 'Daerah' => 'Tawau'),

    //Sarawak
    array('Id' => '3488', 'Daerah' => 'Betong'),
    array('Id' => '3496', 'Daerah' => 'Bintulu'),
    array('Id' => '3498', 'Daerah' => 'Kapit'),
    array('Id' => '3482', 'Daerah' => 'Kuching'),
    array('Id' => '3502', 'Daerah' => 'Limbang'),
    array('Id' => '3500', 'Daerah' => 'Miri'),
    array('Id' => '3494', 'Daerah' => 'Mukah'),
    array('Id' => '3484', 'Daerah' => 'Samarahan'),
    array('Id' => '3490', 'Daerah' => 'Sarikei'),
    array('Id' => '3492', 'Daerah' => 'Sibu'),
    array('Id' => '3486', 'Daerah' => 'Sri Aman'),
        
    //Selangor
    array('Id' => '3394', 'Daerah' => 'Gombak'),
    array('Id' => '3404', 'Daerah' => 'Hulu Langat'),
    array('Id' => '3392', 'Daerah' => 'Hulu Selangor'),
    array('Id' => '3396', 'Daerah' => 'Kelang'),
    array('Id' => '3400', 'Daerah' => 'Kuala Langat'),
    array('Id' => '3390', 'Daerah' => 'Kuala Selangor'),
    array('Id' => '3398', 'Daerah' => 'Petaling Jaya'),
    array('Id' => '3388', 'Daerah' => 'Sabak Bernam'),
    array('Id' => '3402', 'Daerah' => 'Sepang'),

    //Terengganu
    array('Id' => '3312', 'Daerah' => 'Besut'),
    array('Id' => '3322', 'Daerah' => 'Dungun'),
    array('Id' => '3318', 'Daerah' => 'Hulu Terengganu'),
    array('Id' => '3324', 'Daerah' => 'Kemaman'),
    array('Id' => '3316', 'Daerah' => 'Kuala Terengganu'),
    array('Id' => '3320', 'Daerah' => 'Marang'),
    array('Id' => '3314', 'Daerah' => 'Setiu')
);

scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS `regions` (`Id` text,`Daerah` text)');
scraperwiki::save_sqlite(array('Id'), $regions, $table_name='regions');

scraperwiki::sqliteexecute('CREATE TABLE IF NOT EXISTS `cuaca` (`RegionId` text, `Hari` text, `Tarikh` text, `Pagi` text, `Petang` text, `Malam` text, `Minimum` text, `Maksimum` text)');

foreach ($regions as $region) {
    $day = array();
    $html = scraperWiki::scrape('http://www.met.gov.my/index.php?option=com_content&task=view&id='.$region['Id']);
    $dom = new simple_html_dom();
    $dom->load($html);
    $trs = $dom->find('table[@id="table18"]');

    if (count($trs) > 0) {
        foreach($trs as $tr) {
            $date = explode(', ', clean(str_replace(' &nbsp;', '', $tr->find('tr', 0)->plaintext)));
            $min = clean(str_replace(' &deg;C', '', $tr->find('tr', 4)->plaintext));
            $min = str_replace('Minimum : ', '', $min);
            $max = clean(str_replace(' &deg;C', '', $tr->find('tr', 5)->plaintext));
            $max = str_replace('Maksimum : ', '', $max);

            $day['Hari'] = $date[0];
            $day['Tarikh'] = date('Y-m-d', strtotime(str_replace('/', '-', $date[1])));
            $day['Pagi'] = clean(str_replace('Pagi : ', '', $tr->find('tr', 1)->find('td', 1)->plaintext));
            $day['Petang'] = clean(str_replace('Petang : ', '', $tr->find('tr', 2)->plaintext));
            $day['Malam'] = clean(str_replace('Malam : ', '', $tr->find('tr', 3)->plaintext));
            $day['Minimum'] = ($min === '&nbsp;') ? '0' : $min;
            $day['Maksimum'] = ($max === '&nbsp;') ? '0' : $max;
            $day['RegionId'] = $region['Id'];

            scraperwiki::save_sqlite(array('RegionId', 'Tarikh'), $day, $table_name='cuaca');
            unset($day);
        }

        $html->clear();
    }
}

function clean($str = '') {
    $str = strip_tags($str);
    $str = trim($str);

    return $str;
}