<?php

if (class_exists('scraperwiki') === true)
{
    class CURL
    {
        public static function Uni($url, $data = null, $method = 'GET', $cookie = null, $options = null, $retries = 3)
        {
            $result = false;

            if (is_resource($curl = curl_init()) === true)
            {
                $url = rtrim($url, '?&');
                $default = array
                (
                    CURLOPT_ENCODING => '',
                    CURLOPT_AUTOREFERER => true,
                    CURLOPT_FAILONERROR => true,
                    CURLOPT_FORBID_REUSE => true,
                    CURLOPT_FRESH_CONNECT => true,
                    CURLOPT_RETURNTRANSFER => true,
                    CURLOPT_SSL_VERIFYHOST => false,
                    CURLOPT_SSL_VERIFYPEER => false,
                );

                if (preg_match('~^(?:POST|PUT)$~i', $method) > 0)
                {
                    if (is_array($data) === true)
                    {
                        foreach (preg_grep('~^@~', $data) as $key => $value)
                        {
                            $data[$key] = sprintf('@%s', realpath(ltrim($value, '@')));
                        }

                        if (count($data) != count($data, COUNT_RECURSIVE))
                        {
                            $data = http_build_query($data, '', '&');
                        }
                    }

                    $default += array(CURLOPT_POSTFIELDS => $data);
                }

                else if ((is_array($data) === true) && (strlen($data = http_build_query($data, '', '&')) > 0))
                {
                    $url = sprintf('%s%s%s', $url, (strpos($url, '?') === false) ? '?' : '&', $data);
                }

                if (preg_match('~^(?:HEAD|OPTIONS)$~i', $method) > 0)
                {
                    $default += array(CURLOPT_HEADER => true, CURLOPT_NOBODY => true);
                }

                $default += array(CURLOPT_URL => $url, CURLOPT_CUSTOMREQUEST => strtoupper($method));

                if (isset($cookie) === true)
                {
                    if ($cookie === true)
                    {
                        $cookie = sprintf('%s.txt', parse_url($url, PHP_URL_HOST));
                    }

                    if (strcmp('.', dirname($cookie)) === 0)
                    {
                        $cookie = sprintf('%s/%s', realpath(sys_get_temp_dir()), $cookie);
                    }

                    $default += array_fill_keys(array(CURLOPT_COOKIEJAR, CURLOPT_COOKIEFILE), $cookie);
                }

                if ((intval(ini_get('safe_mode')) == 0) && (ini_set('open_basedir', null) !== false))
                {
                    $default += array(CURLOPT_MAXREDIRS => 3, CURLOPT_FOLLOWLOCATION => true);
                }

                curl_setopt_array($curl, (array) $options + $default);

                if (empty($retries) === true)
                {
                    return $curl;
                }

                for ($i = 1; $i <= $retries; ++$i)
                {
                    $result = curl_exec($curl);

                    if (($i == $retries) || ($result !== false))
                    {
                        break;
                    }

                    usleep(pow(2, $i - 2) * 1000000);
                }

                curl_close($curl);
            }

            return $result;
        }

        public static function Multi()
        {
            $result = array();
            $arguments = new RecursiveIteratorIterator(new RecursiveArrayIterator(func_get_args()));

            if (is_resource($curl = curl_multi_init()) === true)
            {
                foreach ($arguments as $argument)
                {
                    if ((is_resource($argument) === true) && (strcmp('curl', get_resource_type($argument)) === 0))
                    {
                        curl_multi_add_handle($curl, $result[intval($argument)] = $argument);
                    }
                }

                do
                {
                    do
                    {
                        $status = curl_multi_exec($curl, $active);
                    }
                    while ($status === CURLM_CALL_MULTI_PERFORM);

                    while ($done = curl_multi_info_read($curl))
                    {
                        $result[$id = intval($handle = $done['handle'])] = false;

                        if ($done['result'] === CURLE_OK)
                        {
                            $result[$id] = curl_multi_getcontent($handle);
                        }

                        curl_multi_remove_handle($curl, $handle); curl_close($handle);
                    }

                    if (($active > 0) && ($status === CURLM_OK) && (curl_multi_select($curl, 1.0) === -1))
                    {
                        usleep(100);
                    }
                }
                while (($active > 0) && ($status === CURLM_OK));

                if ($status !== CURLM_OK)
                {
                    foreach ($result as $handle)
                    {
                        curl_multi_remove_handle($curl, $handle); curl_close($handle);
                    }
                }

                curl_multi_close($curl);
            }

            return array_values($result);
        }

        public static function Verse($html, $xpath = null, $key = null, $default = false)
        {
            if (is_string($html) === true)
            {
                $dom = new DOMDocument();

                if (libxml_use_internal_errors(true) === true)
                {
                    libxml_clear_errors();
                }

                if ($dom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8')) === true)
                {
                    return self::Verse(simplexml_import_dom($dom), $xpath, $key, $default);
                }
            }

            else if (is_object($html) === true)
            {
                if (isset($xpath) === true)
                {
                    $html = $html->xpath($xpath);
                }

                if (isset($key) === true)
                {
                    if (is_array($key) !== true)
                    {
                        $key = explode('.', $key);
                    }

                    foreach ((array) $key as $value)
                    {
                        $html = (is_object($html) === true) ? get_object_vars($html) : $html;

                        if ((is_array($html) !== true) || (array_key_exists($value, $html) !== true))
                        {
                            return $default;
                        }

                        $html = $html[$value];
                    }
                }

                return $html;
            }

            return false;
        }
    }
}

else
{
    die('This script must be ran from scraperwiki.com.');
}

if (count(scraperwiki::show_tables()) == 0)
{
    $draws = array();
    $draws[0] = array();
    $draws[0]['date'] = '2012-10-26 21:30:00 Europe/Paris';
    $draws[0]['draw'] = '[["09","05","06","38","27"],["05","11"]]';
    $draws[1] = array();
    $draws[1]['date'] = '2012-10-30 21:30:00 Europe/Paris';
    $draws[1]['draw'] = '[["23","44","25","24","31"],["02","03"]]';
    $draws[2] = array();
    $draws[2]['date'] = '2012-11-02 21:30:00 Europe/Paris';
    $draws[2]['draw'] = '[["06","10","03","44","11"],["03","04"]]';
    $draws[3] = array();
    $draws[3]['date'] = '2012-11-06 21:30:00 Europe/Paris';
    $draws[3]['draw'] = '[["35","25","20","41","07"],["01","09"]]';
    $draws[4] = array();
    $draws[4]['date'] = '2012-11-09 21:30:00 Europe/Paris';
    $draws[4]['draw'] = '[["47","28","14","21","22"],["05","04"]]';
    $draws[5] = array();
    $draws[5]['date'] = '2012-11-13 21:30:00 Europe/Paris';
    $draws[5]['draw'] = '[["29","11","21","24","16"],["06","02"]]';
    $draws[6] = array();
    $draws[6]['date'] = '2012-11-16 21:30:00 Europe/Paris';
    $draws[6]['draw'] = '[["15","19","41","23","10"],["02","09"]]';
    $draws[7] = array();
    $draws[7]['date'] = '2012-11-20 21:30:00 Europe/Paris';
    $draws[7]['draw'] = '[["42","28","45","30","49"],["10","05"]]';
    $draws[8] = array();
    $draws[8]['date'] = '2012-11-23 21:30:00 Europe/Paris';
    $draws[8]['draw'] = '[["11","20","40","09","01"],["05","01"]]';
    $draws[9] = array();
    $draws[9]['date'] = '2012-11-27 21:30:00 Europe/Paris';
    $draws[9]['draw'] = '[["49","44","06","10","23"],["07","01"]]';
    $draws[10] = array();
    $draws[10]['date'] = '2012-11-30 21:30:00 Europe/Paris';
    $draws[10]['draw'] = '[["18","23","40","24","10"],["03","04"]]';
    $draws[11] = array();
    $draws[11]['date'] = '2012-12-04 21:30:00 Europe/Paris';
    $draws[11]['draw'] = '[["29","05","28","44","10"],["02","04"]]';
    $draws[12] = array();
    $draws[12]['date'] = '2012-12-07 21:30:00 Europe/Paris';
    $draws[12]['draw'] = '[["10","18","31","42","16"],["02","05"]]';
    $draws[13] = array();
    $draws[13]['date'] = '2012-12-11 21:30:00 Europe/Paris';
    $draws[13]['draw'] = '[["50","04","09","01","43"],["06","08"]]';
    $draws[14] = array();
    $draws[14]['date'] = '2012-12-14 21:30:00 Europe/Paris';
    $draws[14]['draw'] = '[["40","29","11","43","10"],["11","03"]]';
    $draws[15] = array();
    $draws[15]['date'] = '2012-12-18 21:30:00 Europe/Paris';
    $draws[15]['draw'] = '[["35","14","44","18","20"],["05","02"]]';
    $draws[16] = array();
    $draws[16]['date'] = '2004-02-13 21:30:00 Europe/Paris';
    $draws[16]['draw'] = '[["32","16","29","41","36"],["09","07"]]';
    $draws[17] = array();
    $draws[17]['date'] = '2004-02-20 21:30:00 Europe/Paris';
    $draws[17]['draw'] = '[["13","50","47","07","39"],["02","05"]]';
    $draws[18] = array();
    $draws[18]['date'] = '2004-02-27 21:30:00 Europe/Paris';
    $draws[18]['draw'] = '[["37","19","18","14","31"],["05","04"]]';
    $draws[19] = array();
    $draws[19]['date'] = '2004-03-05 21:30:00 Europe/Paris';
    $draws[19]['draw'] = '[["39","37","04","07","33"],["05","01"]]';
    $draws[20] = array();
    $draws[20]['date'] = '2004-03-12 21:30:00 Europe/Paris';
    $draws[20]['draw'] = '[["44","47","15","28","24"],["04","05"]]';
    $draws[21] = array();
    $draws[21]['date'] = '2004-03-19 21:30:00 Europe/Paris';
    $draws[21]['draw'] = '[["42","45","33","37","36"],["09","04"]]';
    $draws[22] = array();
    $draws[22]['date'] = '2004-03-26 21:30:00 Europe/Paris';
    $draws[22]['draw'] = '[["23","43","03","04","10"],["02","04"]]';
    $draws[23] = array();
    $draws[23]['date'] = '2004-04-02 21:30:00 Europe/Paris';
    $draws[23]['draw'] = '[["04","24","12","36","27"],["02","09"]]';
    $draws[24] = array();
    $draws[24]['date'] = '2004-04-09 21:30:00 Europe/Paris';
    $draws[24]['draw'] = '[["23","19","10","01","04"],["02","08"]]';
    $draws[25] = array();
    $draws[25]['date'] = '2004-04-16 21:30:00 Europe/Paris';
    $draws[25]['draw'] = '[["28","40","14","15","35"],["03","01"]]';
    $draws[26] = array();
    $draws[26]['date'] = '2004-04-23 21:30:00 Europe/Paris';
    $draws[26]['draw'] = '[["45","21","06","49","10"],["05","03"]]';
    $draws[27] = array();
    $draws[27]['date'] = '2004-04-30 21:30:00 Europe/Paris';
    $draws[27]['draw'] = '[["27","16","06","05","23"],["07","06"]]';
    $draws[28] = array();
    $draws[28]['date'] = '2004-05-07 21:30:00 Europe/Paris';
    $draws[28]['draw'] = '[["38","36","15","16","21"],["01","05"]]';
    $draws[29] = array();
    $draws[29]['date'] = '2004-05-14 21:30:00 Europe/Paris';
    $draws[29]['draw'] = '[["32","03","01","39","21"],["02","06"]]';
    $draws[30] = array();
    $draws[30]['date'] = '2004-05-21 21:30:00 Europe/Paris';
    $draws[30]['draw'] = '[["37","39","29","15","49"],["04","09"]]';
    $draws[31] = array();
    $draws[31]['date'] = '2004-05-28 21:30:00 Europe/Paris';
    $draws[31]['draw'] = '[["41","44","06","35","11"],["06","05"]]';
    $draws[32] = array();
    $draws[32]['date'] = '2004-06-04 21:30:00 Europe/Paris';
    $draws[32]['draw'] = '[["41","42","34","13","09"],["07","03"]]';
    $draws[33] = array();
    $draws[33]['date'] = '2004-06-11 21:30:00 Europe/Paris';
    $draws[33]['draw'] = '[["07","02","47","10","08"],["01","07"]]';
    $draws[34] = array();
    $draws[34]['date'] = '2004-06-18 21:30:00 Europe/Paris';
    $draws[34]['draw'] = '[["28","02","40","23","43"],["06","02"]]';
    $draws[35] = array();
    $draws[35]['date'] = '2004-06-25 21:30:00 Europe/Paris';
    $draws[35]['draw'] = '[["30","21","35","03","34"],["01","02"]]';
    $draws[36] = array();
    $draws[36]['date'] = '2004-07-02 21:30:00 Europe/Paris';
    $draws[36]['draw'] = '[["04","28","24","23","34"],["01","03"]]';
    $draws[37] = array();
    $draws[37]['date'] = '2004-07-09 21:30:00 Europe/Paris';
    $draws[37]['draw'] = '[["44","19","05","12","02"],["08","09"]]';
    $draws[38] = array();
    $draws[38]['date'] = '2004-07-16 21:30:00 Europe/Paris';
    $draws[38]['draw'] = '[["26","50","31","24","38"],["08","05"]]';
    $draws[39] = array();
    $draws[39]['date'] = '2004-07-23 21:30:00 Europe/Paris';
    $draws[39]['draw'] = '[["10","27","07","34","31"],["08","03"]]';
    $draws[40] = array();
    $draws[40]['date'] = '2004-07-30 21:30:00 Europe/Paris';
    $draws[40]['draw'] = '[["50","10","09","19","37"],["06","01"]]';
    $draws[41] = array();
    $draws[41]['date'] = '2004-08-06 21:30:00 Europe/Paris';
    $draws[41]['draw'] = '[["05","35","44","15","24"],["06","05"]]';
    $draws[42] = array();
    $draws[42]['date'] = '2004-08-13 21:30:00 Europe/Paris';
    $draws[42]['draw'] = '[["20","27","41","43","50"],["05","08"]]';
    $draws[43] = array();
    $draws[43]['date'] = '2004-08-20 21:30:00 Europe/Paris';
    $draws[43]['draw'] = '[["27","10","35","09","06"],["06","08"]]';
    $draws[44] = array();
    $draws[44]['date'] = '2004-08-27 21:30:00 Europe/Paris';
    $draws[44]['draw'] = '[["28","01","44","22","11"],["01","09"]]';
    $draws[45] = array();
    $draws[45]['date'] = '2004-09-03 21:30:00 Europe/Paris';
    $draws[45]['draw'] = '[["14","12","15","34","08"],["07","06"]]';
    $draws[46] = array();
    $draws[46]['date'] = '2004-09-10 21:30:00 Europe/Paris';
    $draws[46]['draw'] = '[["05","38","36","25","33"],["05","02"]]';
    $draws[47] = array();
    $draws[47]['date'] = '2004-09-17 21:30:00 Europe/Paris';
    $draws[47]['draw'] = '[["41","39","15","18","29"],["08","05"]]';
    $draws[48] = array();
    $draws[48]['date'] = '2004-09-24 21:30:00 Europe/Paris';
    $draws[48]['draw'] = '[["48","21","26","27","44"],["01","07"]]';
    $draws[49] = array();
    $draws[49]['date'] = '2004-10-01 21:30:00 Europe/Paris';
    $draws[49]['draw'] = '[["48","20","45","21","12"],["06","05"]]';
    $draws[50] = array();
    $draws[50]['date'] = '2004-10-08 21:30:00 Europe/Paris';
    $draws[50]['draw'] = '[["12","10","48","01","16"],["02","06"]]';
    $draws[51] = array();
    $draws[51]['date'] = '2004-10-15 21:30:00 Europe/Paris';
    $draws[51]['draw'] = '[["37","21","14","43","22"],["05","08"]]';
    $draws[52] = array();
    $draws[52]['date'] = '2004-10-22 21:30:00 Europe/Paris';
    $draws[52]['draw'] = '[["09","25","01","40","23"],["03","09"]]';
    $draws[53] = array();
    $draws[53]['date'] = '2004-10-29 21:30:00 Europe/Paris';
    $draws[53]['draw'] = '[["32","01","38","35","08"],["09","04"]]';
    $draws[54] = array();
    $draws[54]['date'] = '2004-11-05 21:30:00 Europe/Paris';
    $draws[54]['draw'] = '[["25","42","49","19","06"],["01","07"]]';
    $draws[55] = array();
    $draws[55]['date'] = '2004-11-12 21:30:00 Europe/Paris';
    $draws[55]['draw'] = '[["12","13","04","32","11"],["09","03"]]';
    $draws[56] = array();
    $draws[56]['date'] = '2004-11-19 21:30:00 Europe/Paris';
    $draws[56]['draw'] = '[["37","29","34","18","01"],["06","02"]]';
    $draws[57] = array();
    $draws[57]['date'] = '2004-11-26 21:30:00 Europe/Paris';
    $draws[57]['draw'] = '[["24","01","34","04","36"],["08","06"]]';
    $draws[58] = array();
    $draws[58]['date'] = '2004-12-03 21:30:00 Europe/Paris';
    $draws[58]['draw'] = '[["15","42","11","01","49"],["04","03"]]';
    $draws[59] = array();
    $draws[59]['date'] = '2004-12-10 21:30:00 Europe/Paris';
    $draws[59]['draw'] = '[["03","13","43","01","16"],["07","02"]]';
    $draws[60] = array();
    $draws[60]['date'] = '2004-12-17 21:30:00 Europe/Paris';
    $draws[60]['draw'] = '[["49","22","19","15","46"],["09","02"]]';
    $draws[61] = array();
    $draws[61]['date'] = '2004-12-24 21:30:00 Europe/Paris';
    $draws[61]['draw'] = '[["03","27","29","04","37"],["06","05"]]';
    $draws[62] = array();
    $draws[62]['date'] = '2004-12-31 21:30:00 Europe/Paris';
    $draws[62]['draw'] = '[["08","07","47","25","24"],["08","09"]]';
    $draws[63] = array();
    $draws[63]['date'] = '2005-01-07 21:30:00 Europe/Paris';
    $draws[63]['draw'] = '[["50","27","47","03","23"],["03","02"]]';
    $draws[64] = array();
    $draws[64]['date'] = '2005-01-14 21:30:00 Europe/Paris';
    $draws[64]['draw'] = '[["11","14","29","06","19"],["03","01"]]';
    $draws[65] = array();
    $draws[65]['date'] = '2005-01-21 21:30:00 Europe/Paris';
    $draws[65]['draw'] = '[["12","14","10","26","24"],["08","05"]]';
    $draws[66] = array();
    $draws[66]['date'] = '2005-01-28 21:30:00 Europe/Paris';
    $draws[66]['draw'] = '[["26","21","07","43","45"],["05","07"]]';
    $draws[67] = array();
    $draws[67]['date'] = '2005-02-04 21:30:00 Europe/Paris';
    $draws[67]['draw'] = '[["11","01","40","30","08"],["07","08"]]';
    $draws[68] = array();
    $draws[68]['date'] = '2005-02-11 21:30:00 Europe/Paris';
    $draws[68]['draw'] = '[["11","13","25","32","50"],["07","04"]]';
    $draws[69] = array();
    $draws[69]['date'] = '2005-02-18 21:30:00 Europe/Paris';
    $draws[69]['draw'] = '[["32","46","20","21","26"],["08","09"]]';
    $draws[70] = array();
    $draws[70]['date'] = '2005-02-25 21:30:00 Europe/Paris';
    $draws[70]['draw'] = '[["43","03","27","44","30"],["08","04"]]';
    $draws[71] = array();
    $draws[71]['date'] = '2005-03-04 21:30:00 Europe/Paris';
    $draws[71]['draw'] = '[["12","32","37","39","24"],["07","09"]]';
    $draws[72] = array();
    $draws[72]['date'] = '2005-03-11 21:30:00 Europe/Paris';
    $draws[72]['draw'] = '[["40","12","43","23","08"],["01","04"]]';
    $draws[73] = array();
    $draws[73]['date'] = '2005-03-18 21:30:00 Europe/Paris';
    $draws[73]['draw'] = '[["48","39","23","06","43"],["05","07"]]';
    $draws[74] = array();
    $draws[74]['date'] = '2005-03-25 21:30:00 Europe/Paris';
    $draws[74]['draw'] = '[["29","33","38","04","37"],["09","06"]]';
    $draws[75] = array();
    $draws[75]['date'] = '2005-04-01 21:30:00 Europe/Paris';
    $draws[75]['draw'] = '[["26","44","47","25","41"],["03","07"]]';
    $draws[76] = array();
    $draws[76]['date'] = '2005-04-08 21:30:00 Europe/Paris';
    $draws[76]['draw'] = '[["31","50","25","11","07"],["03","01"]]';
    $draws[77] = array();
    $draws[77]['date'] = '2005-04-15 21:30:00 Europe/Paris';
    $draws[77]['draw'] = '[["06","31","42","38","28"],["09","03"]]';
    $draws[78] = array();
    $draws[78]['date'] = '2005-04-22 21:30:00 Europe/Paris';
    $draws[78]['draw'] = '[["13","10","24","47","03"],["09","05"]]';
    $draws[79] = array();
    $draws[79]['date'] = '2005-04-29 21:30:00 Europe/Paris';
    $draws[79]['draw'] = '[["42","35","09","03","39"],["01","08"]]';
    $draws[80] = array();
    $draws[80]['date'] = '2005-05-06 21:30:00 Europe/Paris';
    $draws[80]['draw'] = '[["44","21","12","07","26"],["06","08"]]';
    $draws[81] = array();
    $draws[81]['date'] = '2005-05-13 21:30:00 Europe/Paris';
    $draws[81]['draw'] = '[["12","40","31","17","32"],["09","02"]]';
    $draws[82] = array();
    $draws[82]['date'] = '2005-05-20 21:30:00 Europe/Paris';
    $draws[82]['draw'] = '[["28","06","47","07","13"],["08","05"]]';
    $draws[83] = array();
    $draws[83]['date'] = '2005-05-27 21:30:00 Europe/Paris';
    $draws[83]['draw'] = '[["50","48","31","02","24"],["09","04"]]';
    $draws[84] = array();
    $draws[84]['date'] = '2005-06-03 21:30:00 Europe/Paris';
    $draws[84]['draw'] = '[["08","11","03","17","50"],["05","01"]]';
    $draws[85] = array();
    $draws[85]['date'] = '2005-06-10 21:30:00 Europe/Paris';
    $draws[85]['draw'] = '[["37","32","47","07","06"],["07","01"]]';
    $draws[86] = array();
    $draws[86]['date'] = '2005-06-17 21:30:00 Europe/Paris';
    $draws[86]['draw'] = '[["08","04","10","21","18"],["07","01"]]';
    $draws[87] = array();
    $draws[87]['date'] = '2005-06-24 21:30:00 Europe/Paris';
    $draws[87]['draw'] = '[["06","15","08","14","45"],["07","08"]]';
    $draws[88] = array();
    $draws[88]['date'] = '2005-07-01 21:30:00 Europe/Paris';
    $draws[88]['draw'] = '[["23","28","05","04","25"],["03","04"]]';
    $draws[89] = array();
    $draws[89]['date'] = '2005-07-08 21:30:00 Europe/Paris';
    $draws[89]['draw'] = '[["42","46","36","35","49"],["08","02"]]';
    $draws[90] = array();
    $draws[90]['date'] = '2005-07-15 21:30:00 Europe/Paris';
    $draws[90]['draw'] = '[["42","23","01","11","12"],["06","03"]]';
    $draws[91] = array();
    $draws[91]['date'] = '2005-07-22 21:30:00 Europe/Paris';
    $draws[91]['draw'] = '[["49","14","41","03","48"],["01","04"]]';
    $draws[92] = array();
    $draws[92]['date'] = '2005-07-29 21:30:00 Europe/Paris';
    $draws[92]['draw'] = '[["50","03","19","49","26"],["05","04"]]';
    $draws[93] = array();
    $draws[93]['date'] = '2005-08-05 21:30:00 Europe/Paris';
    $draws[93]['draw'] = '[["21","11","02","22","30"],["04","06"]]';
    $draws[94] = array();
    $draws[94]['date'] = '2005-08-12 21:30:00 Europe/Paris';
    $draws[94]['draw'] = '[["37","23","40","15","30"],["07","09"]]';
    $draws[95] = array();
    $draws[95]['date'] = '2005-08-19 21:30:00 Europe/Paris';
    $draws[95]['draw'] = '[["41","29","11","24","31"],["03","01"]]';
    $draws[96] = array();
    $draws[96]['date'] = '2005-08-26 21:30:00 Europe/Paris';
    $draws[96]['draw'] = '[["29","35","40","41","09"],["06","01"]]';
    $draws[97] = array();
    $draws[97]['date'] = '2005-09-02 21:30:00 Europe/Paris';
    $draws[97]['draw'] = '[["43","03","04","50","14"],["03","06"]]';
    $draws[98] = array();
    $draws[98]['date'] = '2005-09-09 21:30:00 Europe/Paris';
    $draws[98]['draw'] = '[["31","12","50","19","08"],["07","06"]]';
    $draws[99] = array();
    $draws[99]['date'] = '2005-09-16 21:30:00 Europe/Paris';
    $draws[99]['draw'] = '[["19","38","12","13","21"],["03","09"]]';
    $draws[100] = array();
    $draws[100]['date'] = '2005-09-23 21:30:00 Europe/Paris';
    $draws[100]['draw'] = '[["01","31","34","26","47"],["04","09"]]';
    $draws[101] = array();
    $draws[101]['date'] = '2005-09-30 21:30:00 Europe/Paris';
    $draws[101]['draw'] = '[["11","50","48","06","47"],["01","06"]]';
    $draws[102] = array();
    $draws[102]['date'] = '2005-10-07 21:30:00 Europe/Paris';
    $draws[102]['draw'] = '[["26","44","21","13","02"],["03","09"]]';
    $draws[103] = array();
    $draws[103]['date'] = '2005-10-14 21:30:00 Europe/Paris';
    $draws[103]['draw'] = '[["10","19","11","23","20"],["06","01"]]';
    $draws[104] = array();
    $draws[104]['date'] = '2005-10-21 21:30:00 Europe/Paris';
    $draws[104]['draw'] = '[["19","14","33","01","29"],["01","08"]]';
    $draws[105] = array();
    $draws[105]['date'] = '2005-10-28 21:30:00 Europe/Paris';
    $draws[105]['draw'] = '[["14","50","47","44","36"],["03","05"]]';
    $draws[106] = array();
    $draws[106]['date'] = '2005-11-04 21:30:00 Europe/Paris';
    $draws[106]['draw'] = '[["38","42","36","37","26"],["02","06"]]';
    $draws[107] = array();
    $draws[107]['date'] = '2005-11-11 21:30:00 Europe/Paris';
    $draws[107]['draw'] = '[["41","16","36","42","15"],["05","03"]]';
    $draws[108] = array();
    $draws[108]['date'] = '2005-11-18 21:30:00 Europe/Paris';
    $draws[108]['draw'] = '[["34","17","18","48","25"],["03","02"]]';
    $draws[109] = array();
    $draws[109]['date'] = '2005-11-25 21:30:00 Europe/Paris';
    $draws[109]['draw'] = '[["27","39","47","06","01"],["06","01"]]';
    $draws[110] = array();
    $draws[110]['date'] = '2005-12-02 21:30:00 Europe/Paris';
    $draws[110]['draw'] = '[["01","30","20","09","23"],["04","07"]]';
    $draws[111] = array();
    $draws[111]['date'] = '2005-12-09 21:30:00 Europe/Paris';
    $draws[111]['draw'] = '[["11","42","38","35","18"],["01","05"]]';
    $draws[112] = array();
    $draws[112]['date'] = '2005-12-16 21:30:00 Europe/Paris';
    $draws[112]['draw'] = '[["02","18","03","15","32"],["07","06"]]';
    $draws[113] = array();
    $draws[113]['date'] = '2005-12-23 21:30:00 Europe/Paris';
    $draws[113]['draw'] = '[["31","42","37","36","15"],["01","07"]]';
    $draws[114] = array();
    $draws[114]['date'] = '2005-12-30 21:30:00 Europe/Paris';
    $draws[114]['draw'] = '[["19","45","43","08","16"],["01","04"]]';
    $draws[115] = array();
    $draws[115]['date'] = '2006-01-06 21:30:00 Europe/Paris';
    $draws[115]['draw'] = '[["06","26","14","09","02"],["04","05"]]';
    $draws[116] = array();
    $draws[116]['date'] = '2006-01-13 21:30:00 Europe/Paris';
    $draws[116]['draw'] = '[["12","19","33","34","08"],["01","06"]]';
    $draws[117] = array();
    $draws[117]['date'] = '2006-01-20 21:30:00 Europe/Paris';
    $draws[117]['draw'] = '[["15","12","50","33","44"],["06","02"]]';
    $draws[118] = array();
    $draws[118]['date'] = '2006-01-27 21:30:00 Europe/Paris';
    $draws[118]['draw'] = '[["09","21","15","40","49"],["04","01"]]';
    $draws[119] = array();
    $draws[119]['date'] = '2006-02-03 21:30:00 Europe/Paris';
    $draws[119]['draw'] = '[["30","39","09","21","50"],["03","01"]]';
    $draws[120] = array();
    $draws[120]['date'] = '2006-02-10 21:30:00 Europe/Paris';
    $draws[120]['draw'] = '[["05","38","06","48","50"],["06","07"]]';
    $draws[121] = array();
    $draws[121]['date'] = '2006-02-17 21:30:00 Europe/Paris';
    $draws[121]['draw'] = '[["04","23","38","24","26"],["04","02"]]';
    $draws[122] = array();
    $draws[122]['date'] = '2006-02-24 21:30:00 Europe/Paris';
    $draws[122]['draw'] = '[["18","19","01","47","11"],["07","03"]]';
    $draws[123] = array();
    $draws[123]['date'] = '2006-03-03 21:30:00 Europe/Paris';
    $draws[123]['draw'] = '[["05","44","10","08","03"],["03","05"]]';
    $draws[124] = array();
    $draws[124]['date'] = '2006-03-10 21:30:00 Europe/Paris';
    $draws[124]['draw'] = '[["01","33","21","45","49"],["04","08"]]';
    $draws[125] = array();
    $draws[125]['date'] = '2006-03-17 21:30:00 Europe/Paris';
    $draws[125]['draw'] = '[["50","44","05","45","32"],["07","01"]]';
    $draws[126] = array();
    $draws[126]['date'] = '2006-03-24 21:30:00 Europe/Paris';
    $draws[126]['draw'] = '[["17","47","28","33","35"],["04","09"]]';
    $draws[127] = array();
    $draws[127]['date'] = '2006-03-31 21:30:00 Europe/Paris';
    $draws[127]['draw'] = '[["50","03","45","20","31"],["07","06"]]';
    $draws[128] = array();
    $draws[128]['date'] = '2006-04-07 21:30:00 Europe/Paris';
    $draws[128]['draw'] = '[["13","12","29","50","44"],["04","05"]]';
    $draws[129] = array();
    $draws[129]['date'] = '2006-04-14 21:30:00 Europe/Paris';
    $draws[129]['draw'] = '[["34","35","26","16","49"],["06","02"]]';
    $draws[130] = array();
    $draws[130]['date'] = '2006-04-21 21:30:00 Europe/Paris';
    $draws[130]['draw'] = '[["46","01","22","20","37"],["01","09"]]';
    $draws[131] = array();
    $draws[131]['date'] = '2006-04-28 21:30:00 Europe/Paris';
    $draws[131]['draw'] = '[["17","05","33","22","10"],["07","05"]]';
    $draws[132] = array();
    $draws[132]['date'] = '2006-05-05 21:30:00 Europe/Paris';
    $draws[132]['draw'] = '[["08","50","16","04","14"],["09","03"]]';
    $draws[133] = array();
    $draws[133]['date'] = '2006-05-12 21:30:00 Europe/Paris';
    $draws[133]['draw'] = '[["23","05","20","34","50"],["01","05"]]';
    $draws[134] = array();
    $draws[134]['date'] = '2006-05-19 21:30:00 Europe/Paris';
    $draws[134]['draw'] = '[["49","34","25","03","05"],["08","05"]]';
    $draws[135] = array();
    $draws[135]['date'] = '2006-05-26 21:30:00 Europe/Paris';
    $draws[135]['draw'] = '[["21","41","12","02","49"],["03","07"]]';
    $draws[136] = array();
    $draws[136]['date'] = '2006-06-02 21:30:00 Europe/Paris';
    $draws[136]['draw'] = '[["41","07","48","27","08"],["06","01"]]';
    $draws[137] = array();
    $draws[137]['date'] = '2006-06-09 21:30:00 Europe/Paris';
    $draws[137]['draw'] = '[["03","34","39","15","12"],["04","06"]]';
    $draws[138] = array();
    $draws[138]['date'] = '2006-06-16 21:30:00 Europe/Paris';
    $draws[138]['draw'] = '[["26","36","01","16","30"],["09","03"]]';
    $draws[139] = array();
    $draws[139]['date'] = '2006-06-23 21:30:00 Europe/Paris';
    $draws[139]['draw'] = '[["44","30","09","21","43"],["09","01"]]';
    $draws[140] = array();
    $draws[140]['date'] = '2006-06-30 21:30:00 Europe/Paris';
    $draws[140]['draw'] = '[["16","06","15","40","43"],["01","02"]]';
    $draws[141] = array();
    $draws[141]['date'] = '2006-07-07 21:30:00 Europe/Paris';
    $draws[141]['draw'] = '[["35","09","07","43","18"],["07","05"]]';
    $draws[142] = array();
    $draws[142]['date'] = '2006-07-14 21:30:00 Europe/Paris';
    $draws[142]['draw'] = '[["01","31","07","17","16"],["08","02"]]';
    $draws[143] = array();
    $draws[143]['date'] = '2006-07-21 21:30:00 Europe/Paris';
    $draws[143]['draw'] = '[["50","04","38","02","09"],["08","06"]]';
    $draws[144] = array();
    $draws[144]['date'] = '2006-07-28 21:30:00 Europe/Paris';
    $draws[144]['draw'] = '[["03","43","29","08","12"],["06","07"]]';
    $draws[145] = array();
    $draws[145]['date'] = '2006-08-04 21:30:00 Europe/Paris';
    $draws[145]['draw'] = '[["26","15","32","14","01"],["07","03"]]';
    $draws[146] = array();
    $draws[146]['date'] = '2006-08-11 21:30:00 Europe/Paris';
    $draws[146]['draw'] = '[["47","31","46","28","27"],["05","02"]]';
    $draws[147] = array();
    $draws[147]['date'] = '2006-08-18 21:30:00 Europe/Paris';
    $draws[147]['draw'] = '[["37","40","50","12","39"],["01","02"]]';
    $draws[148] = array();
    $draws[148]['date'] = '2006-08-25 21:30:00 Europe/Paris';
    $draws[148]['draw'] = '[["47","10","28","48","40"],["08","06"]]';
    $draws[149] = array();
    $draws[149]['date'] = '2006-09-01 21:30:00 Europe/Paris';
    $draws[149]['draw'] = '[["25","50","07","45","03"],["09","06"]]';
    $draws[150] = array();
    $draws[150]['date'] = '2006-09-08 21:30:00 Europe/Paris';
    $draws[150]['draw'] = '[["12","10","32","33","01"],["08","01"]]';
    $draws[151] = array();
    $draws[151]['date'] = '2006-09-15 21:30:00 Europe/Paris';
    $draws[151]['draw'] = '[["10","49","26","06","16"],["07","09"]]';
    $draws[152] = array();
    $draws[152]['date'] = '2006-09-22 21:30:00 Europe/Paris';
    $draws[152]['draw'] = '[["30","45","49","29","10"],["08","03"]]';
    $draws[153] = array();
    $draws[153]['date'] = '2006-09-29 21:30:00 Europe/Paris';
    $draws[153]['draw'] = '[["01","03","24","06","18"],["05","08"]]';
    $draws[154] = array();
    $draws[154]['date'] = '2006-10-06 21:30:00 Europe/Paris';
    $draws[154]['draw'] = '[["05","35","11","22","38"],["07","08"]]';
    $draws[155] = array();
    $draws[155]['date'] = '2006-10-13 21:30:00 Europe/Paris';
    $draws[155]['draw'] = '[["02","32","38","41","25"],["05","03"]]';
    $draws[156] = array();
    $draws[156]['date'] = '2006-10-20 21:30:00 Europe/Paris';
    $draws[156]['draw'] = '[["10","34","47","19","45"],["06","03"]]';
    $draws[157] = array();
    $draws[157]['date'] = '2006-10-27 21:30:00 Europe/Paris';
    $draws[157]['draw'] = '[["03","50","44","04","08"],["08","07"]]';
    $draws[158] = array();
    $draws[158]['date'] = '2006-11-03 21:30:00 Europe/Paris';
    $draws[158]['draw'] = '[["13","11","44","24","49"],["09","03"]]';
    $draws[159] = array();
    $draws[159]['date'] = '2006-11-10 21:30:00 Europe/Paris';
    $draws[159]['draw'] = '[["36","30","14","27","21"],["02","03"]]';
    $draws[160] = array();
    $draws[160]['date'] = '2006-11-17 21:30:00 Europe/Paris';
    $draws[160]['draw'] = '[["36","12","33","22","32"],["02","06"]]';
    $draws[161] = array();
    $draws[161]['date'] = '2006-11-24 21:30:00 Europe/Paris';
    $draws[161]['draw'] = '[["08","05","40","25","17"],["05","01"]]';
    $draws[162] = array();
    $draws[162]['date'] = '2006-12-01 21:30:00 Europe/Paris';
    $draws[162]['draw'] = '[["16","37","08","41","04"],["02","05"]]';
    $draws[163] = array();
    $draws[163]['date'] = '2006-12-08 21:30:00 Europe/Paris';
    $draws[163]['draw'] = '[["47","36","17","16","18"],["01","02"]]';
    $draws[164] = array();
    $draws[164]['date'] = '2006-12-15 21:30:00 Europe/Paris';
    $draws[164]['draw'] = '[["35","37","09","42","23"],["03","07"]]';
    $draws[165] = array();
    $draws[165]['date'] = '2006-12-22 21:30:00 Europe/Paris';
    $draws[165]['draw'] = '[["20","11","43","09","38"],["02","03"]]';
    $draws[166] = array();
    $draws[166]['date'] = '2006-12-29 21:30:00 Europe/Paris';
    $draws[166]['draw'] = '[["14","09","06","13","35"],["03","04"]]';
    $draws[167] = array();
    $draws[167]['date'] = '2007-01-05 21:30:00 Europe/Paris';
    $draws[167]['draw'] = '[["17","45","36","29","19"],["06","05"]]';
    $draws[168] = array();
    $draws[168]['date'] = '2007-01-12 21:30:00 Europe/Paris';
    $draws[168]['draw'] = '[["14","08","25","19","11"],["03","05"]]';
    $draws[169] = array();
    $draws[169]['date'] = '2007-01-19 21:30:00 Europe/Paris';
    $draws[169]['draw'] = '[["27","05","13","33","42"],["04","02"]]';
    $draws[170] = array();
    $draws[170]['date'] = '2007-01-26 21:30:00 Europe/Paris';
    $draws[170]['draw'] = '[["38","11","23","15","30"],["04","09"]]';
    $draws[171] = array();
    $draws[171]['date'] = '2007-02-02 21:30:00 Europe/Paris';
    $draws[171]['draw'] = '[["36","14","27","23","30"],["01","06"]]';
    $draws[172] = array();
    $draws[172]['date'] = '2007-02-09 21:30:00 Europe/Paris';
    $draws[172]['draw'] = '[["36","16","46","30","14"],["08","02"]]';
    $draws[173] = array();
    $draws[173]['date'] = '2007-02-16 21:30:00 Europe/Paris';
    $draws[173]['draw'] = '[["19","39","20","50","08"],["06","09"]]';
    $draws[174] = array();
    $draws[174]['date'] = '2007-02-23 21:30:00 Europe/Paris';
    $draws[174]['draw'] = '[["20","02","22","18","15"],["05","02"]]';
    $draws[175] = array();
    $draws[175]['date'] = '2007-03-02 21:30:00 Europe/Paris';
    $draws[175]['draw'] = '[["03","16","48","34","38"],["08","05"]]';
    $draws[176] = array();
    $draws[176]['date'] = '2007-03-09 21:30:00 Europe/Paris';
    $draws[176]['draw'] = '[["43","25","03","02","48"],["09","06"]]';
    $draws[177] = array();
    $draws[177]['date'] = '2007-03-16 21:30:00 Europe/Paris';
    $draws[177]['draw'] = '[["45","04","31","49","14"],["09","04"]]';
    $draws[178] = array();
    $draws[178]['date'] = '2007-03-23 21:30:00 Europe/Paris';
    $draws[178]['draw'] = '[["43","17","05","40","13"],["03","01"]]';
    $draws[179] = array();
    $draws[179]['date'] = '2007-03-30 21:30:00 Europe/Paris';
    $draws[179]['draw'] = '[["19","09","46","17","41"],["01","08"]]';
    $draws[180] = array();
    $draws[180]['date'] = '2007-04-06 21:30:00 Europe/Paris';
    $draws[180]['draw'] = '[["41","48","29","23","15"],["06","03"]]';
    $draws[181] = array();
    $draws[181]['date'] = '2007-04-13 21:30:00 Europe/Paris';
    $draws[181]['draw'] = '[["20","41","38","07","25"],["03","07"]]';
    $draws[182] = array();
    $draws[182]['date'] = '2007-04-20 21:30:00 Europe/Paris';
    $draws[182]['draw'] = '[["41","26","32","45","23"],["03","07"]]';
    $draws[183] = array();
    $draws[183]['date'] = '2007-04-27 21:30:00 Europe/Paris';
    $draws[183]['draw'] = '[["44","18","07","36","27"],["01","02"]]';
    $draws[184] = array();
    $draws[184]['date'] = '2007-05-04 21:30:00 Europe/Paris';
    $draws[184]['draw'] = '[["17","41","35","06","45"],["01","05"]]';
    $draws[185] = array();
    $draws[185]['date'] = '2007-05-11 21:30:00 Europe/Paris';
    $draws[185]['draw'] = '[["12","26","49","07","29"],["06","02"]]';
    $draws[186] = array();
    $draws[186]['date'] = '2007-05-18 21:30:00 Europe/Paris';
    $draws[186]['draw'] = '[["49","37","34","26","39"],["02","06"]]';
    $draws[187] = array();
    $draws[187]['date'] = '2007-05-25 21:30:00 Europe/Paris';
    $draws[187]['draw'] = '[["49","26","50","29","25"],["08","07"]]';
    $draws[188] = array();
    $draws[188]['date'] = '2007-06-01 21:30:00 Europe/Paris';
    $draws[188]['draw'] = '[["22","41","42","37","06"],["06","09"]]';
    $draws[189] = array();
    $draws[189]['date'] = '2007-06-08 21:30:00 Europe/Paris';
    $draws[189]['draw'] = '[["15","17","25","45","01"],["08","02"]]';
    $draws[190] = array();
    $draws[190]['date'] = '2007-06-15 21:30:00 Europe/Paris';
    $draws[190]['draw'] = '[["05","14","40","07","21"],["03","08"]]';
    $draws[191] = array();
    $draws[191]['date'] = '2007-06-22 21:30:00 Europe/Paris';
    $draws[191]['draw'] = '[["22","17","16","11","24"],["05","06"]]';
    $draws[192] = array();
    $draws[192]['date'] = '2007-06-29 21:30:00 Europe/Paris';
    $draws[192]['draw'] = '[["28","08","33","45","12"],["01","03"]]';
    $draws[193] = array();
    $draws[193]['date'] = '2007-07-06 21:30:00 Europe/Paris';
    $draws[193]['draw'] = '[["39","41","04","19","05"],["09","08"]]';
    $draws[194] = array();
    $draws[194]['date'] = '2007-07-13 21:30:00 Europe/Paris';
    $draws[194]['draw'] = '[["13","09","31","15","48"],["06","03"]]';
    $draws[195] = array();
    $draws[195]['date'] = '2007-07-20 21:30:00 Europe/Paris';
    $draws[195]['draw'] = '[["50","26","10","21","25"],["09","04"]]';
    $draws[196] = array();
    $draws[196]['date'] = '2007-07-27 21:30:00 Europe/Paris';
    $draws[196]['draw'] = '[["04","29","21","01","41"],["08","07"]]';
    $draws[197] = array();
    $draws[197]['date'] = '2007-08-03 21:30:00 Europe/Paris';
    $draws[197]['draw'] = '[["41","33","37","30","10"],["01","08"]]';
    $draws[198] = array();
    $draws[198]['date'] = '2007-08-10 21:30:00 Europe/Paris';
    $draws[198]['draw'] = '[["40","43","49","42","23"],["06","02"]]';
    $draws[199] = array();
    $draws[199]['date'] = '2007-08-17 21:30:00 Europe/Paris';
    $draws[199]['draw'] = '[["02","13","42","03","38"],["07","08"]]';
    $draws[200] = array();
    $draws[200]['date'] = '2007-08-24 21:30:00 Europe/Paris';
    $draws[200]['draw'] = '[["16","03","42","01","48"],["02","03"]]';
    $draws[201] = array();
    $draws[201]['date'] = '2007-08-31 21:30:00 Europe/Paris';
    $draws[201]['draw'] = '[["22","37","23","18","06"],["06","05"]]';
    $draws[202] = array();
    $draws[202]['date'] = '2007-09-07 21:30:00 Europe/Paris';
    $draws[202]['draw'] = '[["42","03","34","02","33"],["05","03"]]';
    $draws[203] = array();
    $draws[203]['date'] = '2007-09-14 21:30:00 Europe/Paris';
    $draws[203]['draw'] = '[["33","29","05","09","11"],["07","09"]]';
    $draws[204] = array();
    $draws[204]['date'] = '2007-09-21 21:30:00 Europe/Paris';
    $draws[204]['draw'] = '[["35","37","17","01","32"],["08","01"]]';
    $draws[205] = array();
    $draws[205]['date'] = '2007-09-28 21:30:00 Europe/Paris';
    $draws[205]['draw'] = '[["22","34","44","30","35"],["04","05"]]';
    $draws[206] = array();
    $draws[206]['date'] = '2007-10-05 21:30:00 Europe/Paris';
    $draws[206]['draw'] = '[["20","27","35","44","11"],["05","02"]]';
    $draws[207] = array();
    $draws[207]['date'] = '2007-10-12 21:30:00 Europe/Paris';
    $draws[207]['draw'] = '[["36","47","21","32","46"],["03","04"]]';
    $draws[208] = array();
    $draws[208]['date'] = '2007-10-19 21:30:00 Europe/Paris';
    $draws[208]['draw'] = '[["07","18","34","35","40"],["07","08"]]';
    $draws[209] = array();
    $draws[209]['date'] = '2007-10-26 21:30:00 Europe/Paris';
    $draws[209]['draw'] = '[["20","07","38","40","43"],["08","01"]]';
    $draws[210] = array();
    $draws[210]['date'] = '2007-11-02 21:30:00 Europe/Paris';
    $draws[210]['draw'] = '[["40","16","03","19","18"],["02","01"]]';
    $draws[211] = array();
    $draws[211]['date'] = '2007-11-09 21:30:00 Europe/Paris';
    $draws[211]['draw'] = '[["14","25","36","05","22"],["06","05"]]';
    $draws[212] = array();
    $draws[212]['date'] = '2007-11-16 21:30:00 Europe/Paris';
    $draws[212]['draw'] = '[["23","18","33","37","09"],["01","08"]]';
    $draws[213] = array();
    $draws[213]['date'] = '2007-11-23 21:30:00 Europe/Paris';
    $draws[213]['draw'] = '[["22","02","48","29","10"],["09","03"]]';
    $draws[214] = array();
    $draws[214]['date'] = '2007-11-30 21:30:00 Europe/Paris';
    $draws[214]['draw'] = '[["38","20","12","19","30"],["09","07"]]';
    $draws[215] = array();
    $draws[215]['date'] = '2007-12-07 21:30:00 Europe/Paris';
    $draws[215]['draw'] = '[["48","43","04","02","32"],["01","07"]]';
    $draws[216] = array();
    $draws[216]['date'] = '2007-12-14 21:30:00 Europe/Paris';
    $draws[216]['draw'] = '[["08","30","36","25","44"],["04","03"]]';
    $draws[217] = array();
    $draws[217]['date'] = '2007-12-21 21:30:00 Europe/Paris';
    $draws[217]['draw'] = '[["37","07","44","28","09"],["07","06"]]';
    $draws[218] = array();
    $draws[218]['date'] = '2007-12-28 21:30:00 Europe/Paris';
    $draws[218]['draw'] = '[["45","31","20","22","21"],["09","07"]]';
    $draws[219] = array();
    $draws[219]['date'] = '2008-01-04 21:30:00 Europe/Paris';
    $draws[219]['draw'] = '[["41","24","10","12","25"],["03","05"]]';
    $draws[220] = array();
    $draws[220]['date'] = '2008-01-11 21:30:00 Europe/Paris';
    $draws[220]['draw'] = '[["24","36","50","08","49"],["04","08"]]';
    $draws[221] = array();
    $draws[221]['date'] = '2008-01-18 21:30:00 Europe/Paris';
    $draws[221]['draw'] = '[["46","40","16","14","23"],["08","04"]]';
    $draws[222] = array();
    $draws[222]['date'] = '2008-01-25 21:30:00 Europe/Paris';
    $draws[222]['draw'] = '[["02","19","09","45","06"],["07","08"]]';
    $draws[223] = array();
    $draws[223]['date'] = '2008-02-01 21:30:00 Europe/Paris';
    $draws[223]['draw'] = '[["30","49","45","47","22"],["04","09"]]';
    $draws[224] = array();
    $draws[224]['date'] = '2008-02-08 21:30:00 Europe/Paris';
    $draws[224]['draw'] = '[["17","38","28","44","30"],["01","04"]]';
    $draws[225] = array();
    $draws[225]['date'] = '2008-02-15 21:30:00 Europe/Paris';
    $draws[225]['draw'] = '[["27","45","12","29","46"],["07","04"]]';
    $draws[226] = array();
    $draws[226]['date'] = '2008-02-22 21:30:00 Europe/Paris';
    $draws[226]['draw'] = '[["46","50","04","27","32"],["08","09"]]';
    $draws[227] = array();
    $draws[227]['date'] = '2008-02-29 21:30:00 Europe/Paris';
    $draws[227]['draw'] = '[["37","47","49","40","12"],["09","02"]]';
    $draws[228] = array();
    $draws[228]['date'] = '2008-03-07 21:30:00 Europe/Paris';
    $draws[228]['draw'] = '[["14","17","07","35","02"],["06","01"]]';
    $draws[229] = array();
    $draws[229]['date'] = '2008-03-14 21:30:00 Europe/Paris';
    $draws[229]['draw'] = '[["13","48","35","21","25"],["04","08"]]';
    $draws[230] = array();
    $draws[230]['date'] = '2008-03-21 21:30:00 Europe/Paris';
    $draws[230]['draw'] = '[["10","02","22","18","36"],["06","04"]]';
    $draws[231] = array();
    $draws[231]['date'] = '2008-03-28 21:30:00 Europe/Paris';
    $draws[231]['draw'] = '[["39","09","29","05","17"],["03","06"]]';
    $draws[232] = array();
    $draws[232]['date'] = '2008-04-04 21:30:00 Europe/Paris';
    $draws[232]['draw'] = '[["18","37","47","13","11"],["06","01"]]';
    $draws[233] = array();
    $draws[233]['date'] = '2008-04-11 21:30:00 Europe/Paris';
    $draws[233]['draw'] = '[["50","30","25","45","06"],["05","07"]]';
    $draws[234] = array();
    $draws[234]['date'] = '2008-04-18 21:30:00 Europe/Paris';
    $draws[234]['draw'] = '[["27","06","07","50","03"],["05","09"]]';
    $draws[235] = array();
    $draws[235]['date'] = '2008-04-25 21:30:00 Europe/Paris';
    $draws[235]['draw'] = '[["04","30","26","19","27"],["08","03"]]';
    $draws[236] = array();
    $draws[236]['date'] = '2008-05-02 21:30:00 Europe/Paris';
    $draws[236]['draw'] = '[["26","48","45","37","02"],["08","04"]]';
    $draws[237] = array();
    $draws[237]['date'] = '2008-05-09 21:30:00 Europe/Paris';
    $draws[237]['draw'] = '[["08","09","42","40","45"],["07","06"]]';
    $draws[238] = array();
    $draws[238]['date'] = '2008-05-16 21:30:00 Europe/Paris';
    $draws[238]['draw'] = '[["06","38","09","25","15"],["04","09"]]';
    $draws[239] = array();
    $draws[239]['date'] = '2008-05-23 21:30:00 Europe/Paris';
    $draws[239]['draw'] = '[["05","38","09","19","21"],["01","07"]]';
    $draws[240] = array();
    $draws[240]['date'] = '2008-05-30 21:30:00 Europe/Paris';
    $draws[240]['draw'] = '[["14","20","49","07","05"],["08","02"]]';
    $draws[241] = array();
    $draws[241]['date'] = '2008-06-06 21:30:00 Europe/Paris';
    $draws[241]['draw'] = '[["21","40","19","50","07"],["02","09"]]';
    $draws[242] = array();
    $draws[242]['date'] = '2008-06-13 21:30:00 Europe/Paris';
    $draws[242]['draw'] = '[["16","37","44","50","13"],["09","01"]]';
    $draws[243] = array();
    $draws[243]['date'] = '2008-06-20 21:30:00 Europe/Paris';
    $draws[243]['draw'] = '[["11","08","36","37","45"],["03","05"]]';
    $draws[244] = array();
    $draws[244]['date'] = '2008-06-27 21:30:00 Europe/Paris';
    $draws[244]['draw'] = '[["20","44","05","50","26"],["05","07"]]';
    $draws[245] = array();
    $draws[245]['date'] = '2008-07-04 21:30:00 Europe/Paris';
    $draws[245]['draw'] = '[["19","22","48","07","27"],["07","05"]]';
    $draws[246] = array();
    $draws[246]['date'] = '2008-07-11 21:30:00 Europe/Paris';
    $draws[246]['draw'] = '[["37","19","11","13","09"],["03","04"]]';
    $draws[247] = array();
    $draws[247]['date'] = '2008-07-18 21:30:00 Europe/Paris';
    $draws[247]['draw'] = '[["16","14","44","10","29"],["06","05"]]';
    $draws[248] = array();
    $draws[248]['date'] = '2008-07-25 21:30:00 Europe/Paris';
    $draws[248]['draw'] = '[["29","07","15","24","11"],["07","02"]]';
    $draws[249] = array();
    $draws[249]['date'] = '2008-08-01 21:30:00 Europe/Paris';
    $draws[249]['draw'] = '[["25","40","22","50","01"],["01","08"]]';
    $draws[250] = array();
    $draws[250]['date'] = '2008-08-08 21:30:00 Europe/Paris';
    $draws[250]['draw'] = '[["15","05","16","45","04"],["07","04"]]';
    $draws[251] = array();
    $draws[251]['date'] = '2008-08-15 21:30:00 Europe/Paris';
    $draws[251]['draw'] = '[["18","11","17","26","31"],["06","05"]]';
    $draws[252] = array();
    $draws[252]['date'] = '2008-08-22 21:30:00 Europe/Paris';
    $draws[252]['draw'] = '[["50","27","29","39","07"],["07","05"]]';
    $draws[253] = array();
    $draws[253]['date'] = '2008-08-29 21:30:00 Europe/Paris';
    $draws[253]['draw'] = '[["02","20","37","25","39"],["08","05"]]';
    $draws[254] = array();
    $draws[254]['date'] = '2008-09-05 21:30:00 Europe/Paris';
    $draws[254]['draw'] = '[["17","12","39","16","07"],["03","08"]]';
    $draws[255] = array();
    $draws[255]['date'] = '2008-09-12 21:30:00 Europe/Paris';
    $draws[255]['draw'] = '[["23","33","37","19","50"],["07","03"]]';
    $draws[256] = array();
    $draws[256]['date'] = '2008-09-19 21:30:00 Europe/Paris';
    $draws[256]['draw'] = '[["14","16","19","31","20"],["09","06"]]';
    $draws[257] = array();
    $draws[257]['date'] = '2008-09-26 21:30:00 Europe/Paris';
    $draws[257]['draw'] = '[["31","29","33","14","37"],["02","01"]]';
    $draws[258] = array();
    $draws[258]['date'] = '2008-10-03 21:30:00 Europe/Paris';
    $draws[258]['draw'] = '[["04","38","13","19","23"],["02","03"]]';
    $draws[259] = array();
    $draws[259]['date'] = '2008-10-10 21:30:00 Europe/Paris';
    $draws[259]['draw'] = '[["15","31","22","04","41"],["06","01"]]';
    $draws[260] = array();
    $draws[260]['date'] = '2008-10-17 21:30:00 Europe/Paris';
    $draws[260]['draw'] = '[["50","12","10","03","42"],["01","05"]]';
    $draws[261] = array();
    $draws[261]['date'] = '2008-10-24 21:30:00 Europe/Paris';
    $draws[261]['draw'] = '[["45","07","15","16","17"],["06","09"]]';
    $draws[262] = array();
    $draws[262]['date'] = '2008-10-31 21:30:00 Europe/Paris';
    $draws[262]['draw'] = '[["34","25","03","41","18"],["05","02"]]';
    $draws[263] = array();
    $draws[263]['date'] = '2008-11-07 21:30:00 Europe/Paris';
    $draws[263]['draw'] = '[["09","01","17","12","18"],["03","04"]]';
    $draws[264] = array();
    $draws[264]['date'] = '2008-11-14 21:30:00 Europe/Paris';
    $draws[264]['draw'] = '[["14","26","10","08","21"],["04","03"]]';
    $draws[265] = array();
    $draws[265]['date'] = '2008-11-21 21:30:00 Europe/Paris';
    $draws[265]['draw'] = '[["50","49","21","09","14"],["08","03"]]';
    $draws[266] = array();
    $draws[266]['date'] = '2008-11-28 21:30:00 Europe/Paris';
    $draws[266]['draw'] = '[["08","25","11","41","16"],["04","02"]]';
    $draws[267] = array();
    $draws[267]['date'] = '2008-12-05 21:30:00 Europe/Paris';
    $draws[267]['draw'] = '[["35","08","21","45","04"],["05","08"]]';
    $draws[268] = array();
    $draws[268]['date'] = '2008-12-12 21:30:00 Europe/Paris';
    $draws[268]['draw'] = '[["02","19","42","28","49"],["07","02"]]';
    $draws[269] = array();
    $draws[269]['date'] = '2008-12-19 21:30:00 Europe/Paris';
    $draws[269]['draw'] = '[["29","50","46","28","40"],["05","07"]]';
    $draws[270] = array();
    $draws[270]['date'] = '2008-12-26 21:30:00 Europe/Paris';
    $draws[270]['draw'] = '[["44","26","02","01","50"],["01","07"]]';
    $draws[271] = array();
    $draws[271]['date'] = '2009-01-02 21:30:00 Europe/Paris';
    $draws[271]['draw'] = '[["48","30","29","37","36"],["01","06"]]';
    $draws[272] = array();
    $draws[272]['date'] = '2009-01-09 21:30:00 Europe/Paris';
    $draws[272]['draw'] = '[["22","07","15","28","48"],["04","01"]]';
    $draws[273] = array();
    $draws[273]['date'] = '2009-01-16 21:30:00 Europe/Paris';
    $draws[273]['draw'] = '[["50","22","17","03","49"],["03","06"]]';
    $draws[274] = array();
    $draws[274]['date'] = '2009-01-23 21:30:00 Europe/Paris';
    $draws[274]['draw'] = '[["36","49","33","40","32"],["02","08"]]';
    $draws[275] = array();
    $draws[275]['date'] = '2009-01-30 21:30:00 Europe/Paris';
    $draws[275]['draw'] = '[["04","34","35","46","29"],["05","08"]]';
    $draws[276] = array();
    $draws[276]['date'] = '2009-02-06 21:30:00 Europe/Paris';
    $draws[276]['draw'] = '[["36","30","20","40","10"],["03","05"]]';
    $draws[277] = array();
    $draws[277]['date'] = '2009-02-13 21:30:00 Europe/Paris';
    $draws[277]['draw'] = '[["33","36","40","22","42"],["01","02"]]';
    $draws[278] = array();
    $draws[278]['date'] = '2009-02-20 21:30:00 Europe/Paris';
    $draws[278]['draw'] = '[["13","48","09","12","14"],["01","02"]]';
    $draws[279] = array();
    $draws[279]['date'] = '2009-02-27 21:30:00 Europe/Paris';
    $draws[279]['draw'] = '[["09","44","05","37","45"],["09","06"]]';
    $draws[280] = array();
    $draws[280]['date'] = '2009-03-06 21:30:00 Europe/Paris';
    $draws[280]['draw'] = '[["13","35","25","17","19"],["05","06"]]';
    $draws[281] = array();
    $draws[281]['date'] = '2009-03-13 21:30:00 Europe/Paris';
    $draws[281]['draw'] = '[["36","42","26","12","24"],["01","04"]]';
    $draws[282] = array();
    $draws[282]['date'] = '2009-03-20 21:30:00 Europe/Paris';
    $draws[282]['draw'] = '[["31","12","35","23","16"],["04","06"]]';
    $draws[283] = array();
    $draws[283]['date'] = '2009-03-27 21:30:00 Europe/Paris';
    $draws[283]['draw'] = '[["25","42","36","33","38"],["06","07"]]';
    $draws[284] = array();
    $draws[284]['date'] = '2009-04-03 21:30:00 Europe/Paris';
    $draws[284]['draw'] = '[["46","24","32","20","02"],["01","09"]]';
    $draws[285] = array();
    $draws[285]['date'] = '2009-04-10 21:30:00 Europe/Paris';
    $draws[285]['draw'] = '[["37","14","09","46","16"],["02","04"]]';
    $draws[286] = array();
    $draws[286]['date'] = '2009-04-17 21:30:00 Europe/Paris';
    $draws[286]['draw'] = '[["07","04","21","44","47"],["01","05"]]';
    $draws[287] = array();
    $draws[287]['date'] = '2009-04-24 21:30:00 Europe/Paris';
    $draws[287]['draw'] = '[["21","04","24","14","41"],["05","08"]]';
    $draws[288] = array();
    $draws[288]['date'] = '2009-05-01 21:30:00 Europe/Paris';
    $draws[288]['draw'] = '[["38","47","31","19","05"],["03","05"]]';
    $draws[289] = array();
    $draws[289]['date'] = '2009-05-08 21:30:00 Europe/Paris';
    $draws[289]['draw'] = '[["04","29","23","31","24"],["09","08"]]';
    $draws[290] = array();
    $draws[290]['date'] = '2009-05-15 21:30:00 Europe/Paris';
    $draws[290]['draw'] = '[["19","08","42","18","20"],["05","09"]]';
    $draws[291] = array();
    $draws[291]['date'] = '2009-05-22 21:30:00 Europe/Paris';
    $draws[291]['draw'] = '[["43","04","14","33","13"],["06","01"]]';
    $draws[292] = array();
    $draws[292]['date'] = '2009-05-29 21:30:00 Europe/Paris';
    $draws[292]['draw'] = '[["30","47","02","37","05"],["06","03"]]';
    $draws[293] = array();
    $draws[293]['date'] = '2009-06-05 21:30:00 Europe/Paris';
    $draws[293]['draw'] = '[["35","19","40","26","11"],["02","05"]]';
    $draws[294] = array();
    $draws[294]['date'] = '2009-06-12 21:30:00 Europe/Paris';
    $draws[294]['draw'] = '[["50","14","06","16","34"],["06","04"]]';
    $draws[295] = array();
    $draws[295]['date'] = '2009-06-19 21:30:00 Europe/Paris';
    $draws[295]['draw'] = '[["20","17","16","04","29"],["07","05"]]';
    $draws[296] = array();
    $draws[296]['date'] = '2009-06-26 21:30:00 Europe/Paris';
    $draws[296]['draw'] = '[["21","06","11","39","30"],["08","02"]]';
    $draws[297] = array();
    $draws[297]['date'] = '2009-07-03 21:30:00 Europe/Paris';
    $draws[297]['draw'] = '[["29","47","46","34","21"],["06","08"]]';
    $draws[298] = array();
    $draws[298]['date'] = '2009-07-10 21:30:00 Europe/Paris';
    $draws[298]['draw'] = '[["42","20","06","16","46"],["01","06"]]';
    $draws[299] = array();
    $draws[299]['date'] = '2009-07-17 21:30:00 Europe/Paris';
    $draws[299]['draw'] = '[["17","50","08","02","32"],["03","07"]]';
    $draws[300] = array();
    $draws[300]['date'] = '2009-07-24 21:30:00 Europe/Paris';
    $draws[300]['draw'] = '[["15","47","35","25","14"],["09","05"]]';
    $draws[301] = array();
    $draws[301]['date'] = '2009-07-31 21:30:00 Europe/Paris';
    $draws[301]['draw'] = '[["26","09","20","21","05"],["06","03"]]';
    $draws[302] = array();
    $draws[302]['date'] = '2009-08-07 21:30:00 Europe/Paris';
    $draws[302]['draw'] = '[["22","10","31","24","20"],["07","02"]]';
    $draws[303] = array();
    $draws[303]['date'] = '2009-08-14 21:30:00 Europe/Paris';
    $draws[303]['draw'] = '[["30","05","08","49","24"],["09","03"]]';
    $draws[304] = array();
    $draws[304]['date'] = '2009-08-21 21:30:00 Europe/Paris';
    $draws[304]['draw'] = '[["16","42","31","07","04"],["05","03"]]';
    $draws[305] = array();
    $draws[305]['date'] = '2009-08-28 21:30:00 Europe/Paris';
    $draws[305]['draw'] = '[["37","41","49","36","08"],["07","05"]]';
    $draws[306] = array();
    $draws[306]['date'] = '2009-09-04 21:30:00 Europe/Paris';
    $draws[306]['draw'] = '[["20","39","06","09","38"],["09","03"]]';
    $draws[307] = array();
    $draws[307]['date'] = '2009-09-11 21:30:00 Europe/Paris';
    $draws[307]['draw'] = '[["42","15","12","35","43"],["06","04"]]';
    $draws[308] = array();
    $draws[308]['date'] = '2009-09-18 21:30:00 Europe/Paris';
    $draws[308]['draw'] = '[["30","16","41","38","06"],["02","04"]]';
    $draws[309] = array();
    $draws[309]['date'] = '2009-09-25 21:30:00 Europe/Paris';
    $draws[309]['draw'] = '[["06","21","18","17","34"],["09","03"]]';
    $draws[310] = array();
    $draws[310]['date'] = '2009-10-02 21:30:00 Europe/Paris';
    $draws[310]['draw'] = '[["44","29","24","23","22"],["05","01"]]';
    $draws[311] = array();
    $draws[311]['date'] = '2009-10-09 21:30:00 Europe/Paris';
    $draws[311]['draw'] = '[["29","11","46","07","50"],["04","07"]]';
    $draws[312] = array();
    $draws[312]['date'] = '2009-10-16 21:30:00 Europe/Paris';
    $draws[312]['draw'] = '[["23","30","31","47","12"],["03","04"]]';
    $draws[313] = array();
    $draws[313]['date'] = '2009-10-23 21:30:00 Europe/Paris';
    $draws[313]['draw'] = '[["20","06","18","29","31"],["08","02"]]';
    $draws[314] = array();
    $draws[314]['date'] = '2009-10-30 21:30:00 Europe/Paris';
    $draws[314]['draw'] = '[["35","09","33","38","40"],["06","02"]]';
    $draws[315] = array();
    $draws[315]['date'] = '2009-11-06 21:30:00 Europe/Paris';
    $draws[315]['draw'] = '[["19","43","45","34","11"],["05","09"]]';
    $draws[316] = array();
    $draws[316]['date'] = '2009-11-13 21:30:00 Europe/Paris';
    $draws[316]['draw'] = '[["15","25","32","26","13"],["04","03"]]';
    $draws[317] = array();
    $draws[317]['date'] = '2009-11-20 21:30:00 Europe/Paris';
    $draws[317]['draw'] = '[["47","09","28","05","43"],["02","09"]]';
    $draws[318] = array();
    $draws[318]['date'] = '2009-11-27 21:30:00 Europe/Paris';
    $draws[318]['draw'] = '[["33","15","13","05","08"],["08","09"]]';
    $draws[319] = array();
    $draws[319]['date'] = '2009-12-04 21:30:00 Europe/Paris';
    $draws[319]['draw'] = '[["25","30","19","18","44"],["03","01"]]';
    $draws[320] = array();
    $draws[320]['date'] = '2009-12-11 21:30:00 Europe/Paris';
    $draws[320]['draw'] = '[["41","43","44","46","20"],["02","09"]]';
    $draws[321] = array();
    $draws[321]['date'] = '2009-12-18 21:30:00 Europe/Paris';
    $draws[321]['draw'] = '[["49","30","35","32","14"],["08","03"]]';
    $draws[322] = array();
    $draws[322]['date'] = '2009-12-25 21:30:00 Europe/Paris';
    $draws[322]['draw'] = '[["04","17","05","34","14"],["05","03"]]';
    $draws[323] = array();
    $draws[323]['date'] = '2010-01-01 21:30:00 Europe/Paris';
    $draws[323]['draw'] = '[["22","24","27","36","09"],["07","05"]]';
    $draws[324] = array();
    $draws[324]['date'] = '2010-01-08 21:30:00 Europe/Paris';
    $draws[324]['draw'] = '[["44","05","14","04","46"],["09","08"]]';
    $draws[325] = array();
    $draws[325]['date'] = '2010-01-15 21:30:00 Europe/Paris';
    $draws[325]['draw'] = '[["49","50","26","29","11"],["04","07"]]';
    $draws[326] = array();
    $draws[326]['date'] = '2010-01-22 21:30:00 Europe/Paris';
    $draws[326]['draw'] = '[["04","44","27","22","36"],["09","07"]]';
    $draws[327] = array();
    $draws[327]['date'] = '2010-01-29 21:30:00 Europe/Paris';
    $draws[327]['draw'] = '[["39","43","30","17","09"],["07","05"]]';
    $draws[328] = array();
    $draws[328]['date'] = '2010-02-05 21:30:00 Europe/Paris';
    $draws[328]['draw'] = '[["46","38","34","35","39"],["03","04"]]';
    $draws[329] = array();
    $draws[329]['date'] = '2010-02-12 21:30:00 Europe/Paris';
    $draws[329]['draw'] = '[["05","45","01","38","18"],["06","04"]]';
    $draws[330] = array();
    $draws[330]['date'] = '2010-02-19 21:30:00 Europe/Paris';
    $draws[330]['draw'] = '[["37","12","38","31","43"],["03","02"]]';
    $draws[331] = array();
    $draws[331]['date'] = '2010-02-26 21:30:00 Europe/Paris';
    $draws[331]['draw'] = '[["42","11","29","07","18"],["07","06"]]';
    $draws[332] = array();
    $draws[332]['date'] = '2010-03-05 21:30:00 Europe/Paris';
    $draws[332]['draw'] = '[["19","18","49","12","43"],["09","03"]]';
    $draws[333] = array();
    $draws[333]['date'] = '2010-03-12 21:30:00 Europe/Paris';
    $draws[333]['draw'] = '[["46","01","26","36","33"],["07","06"]]';
    $draws[334] = array();
    $draws[334]['date'] = '2010-03-19 21:30:00 Europe/Paris';
    $draws[334]['draw'] = '[["38","28","30","39","10"],["07","02"]]';
    $draws[335] = array();
    $draws[335]['date'] = '2010-03-26 21:30:00 Europe/Paris';
    $draws[335]['draw'] = '[["18","37","08","16","43"],["02","06"]]';
    $draws[336] = array();
    $draws[336]['date'] = '2010-04-02 21:30:00 Europe/Paris';
    $draws[336]['draw'] = '[["26","18","12","24","45"],["05","04"]]';
    $draws[337] = array();
    $draws[337]['date'] = '2010-04-09 21:30:00 Europe/Paris';
    $draws[337]['draw'] = '[["44","23","24","21","07"],["03","04"]]';
    $draws[338] = array();
    $draws[338]['date'] = '2010-04-16 21:30:00 Europe/Paris';
    $draws[338]['draw'] = '[["17","11","26","40","09"],["09","03"]]';
    $draws[339] = array();
    $draws[339]['date'] = '2010-04-23 21:30:00 Europe/Paris';
    $draws[339]['draw'] = '[["46","03","07","08","43"],["06","08"]]';
    $draws[340] = array();
    $draws[340]['date'] = '2010-04-30 21:30:00 Europe/Paris';
    $draws[340]['draw'] = '[["06","36","22","25","24"],["03","08"]]';
    $draws[341] = array();
    $draws[341]['date'] = '2010-05-07 21:30:00 Europe/Paris';
    $draws[341]['draw'] = '[["15","21","06","03","32"],["07","09"]]';
    $draws[342] = array();
    $draws[342]['date'] = '2010-05-14 21:30:00 Europe/Paris';
    $draws[342]['draw'] = '[["17","31","43","47","01"],["03","02"]]';
    $draws[343] = array();
    $draws[343]['date'] = '2010-05-21 21:30:00 Europe/Paris';
    $draws[343]['draw'] = '[["38","19","50","07","30"],["04","07"]]';
    $draws[344] = array();
    $draws[344]['date'] = '2010-05-28 21:30:00 Europe/Paris';
    $draws[344]['draw'] = '[["09","31","32","33","04"],["03","07"]]';
    $draws[345] = array();
    $draws[345]['date'] = '2010-06-04 21:30:00 Europe/Paris';
    $draws[345]['draw'] = '[["34","42","17","40","04"],["09","04"]]';
    $draws[346] = array();
    $draws[346]['date'] = '2010-06-11 21:30:00 Europe/Paris';
    $draws[346]['draw'] = '[["44","02","36","22","24"],["02","01"]]';
    $draws[347] = array();
    $draws[347]['date'] = '2010-06-18 21:30:00 Europe/Paris';
    $draws[347]['draw'] = '[["02","29","31","38","32"],["04","01"]]';
    $draws[348] = array();
    $draws[348]['date'] = '2010-06-25 21:30:00 Europe/Paris';
    $draws[348]['draw'] = '[["18","01","08","28","31"],["09","08"]]';
    $draws[349] = array();
    $draws[349]['date'] = '2010-07-02 21:30:00 Europe/Paris';
    $draws[349]['draw'] = '[["46","41","36","13","12"],["08","01"]]';
    $draws[350] = array();
    $draws[350]['date'] = '2010-07-09 21:30:00 Europe/Paris';
    $draws[350]['draw'] = '[["37","09","49","24","39"],["03","09"]]';
    $draws[351] = array();
    $draws[351]['date'] = '2010-07-16 21:30:00 Europe/Paris';
    $draws[351]['draw'] = '[["49","46","45","39","38"],["07","08"]]';
    $draws[352] = array();
    $draws[352]['date'] = '2010-07-23 21:30:00 Europe/Paris';
    $draws[352]['draw'] = '[["04","13","37","35","46"],["09","03"]]';
    $draws[353] = array();
    $draws[353]['date'] = '2010-07-30 21:30:00 Europe/Paris';
    $draws[353]['draw'] = '[["39","11","03","04","28"],["08","02"]]';
    $draws[354] = array();
    $draws[354]['date'] = '2010-08-06 21:30:00 Europe/Paris';
    $draws[354]['draw'] = '[["42","28","13","29","25"],["04","05"]]';
    $draws[355] = array();
    $draws[355]['date'] = '2010-08-13 21:30:00 Europe/Paris';
    $draws[355]['draw'] = '[["15","09","47","21","04"],["07","02"]]';
    $draws[356] = array();
    $draws[356]['date'] = '2010-08-20 21:30:00 Europe/Paris';
    $draws[356]['draw'] = '[["27","31","05","42","40"],["06","01"]]';
    $draws[357] = array();
    $draws[357]['date'] = '2010-08-27 21:30:00 Europe/Paris';
    $draws[357]['draw'] = '[["13","06","30","01","49"],["01","09"]]';
    $draws[358] = array();
    $draws[358]['date'] = '2010-09-03 21:30:00 Europe/Paris';
    $draws[358]['draw'] = '[["24","49","47","26","13"],["04","08"]]';
    $draws[359] = array();
    $draws[359]['date'] = '2010-09-10 21:30:00 Europe/Paris';
    $draws[359]['draw'] = '[["35","41","21","45","17"],["05","01"]]';
    $draws[360] = array();
    $draws[360]['date'] = '2010-09-17 21:30:00 Europe/Paris';
    $draws[360]['draw'] = '[["50","27","38","17","29"],["03","01"]]';
    $draws[361] = array();
    $draws[361]['date'] = '2010-09-24 21:30:00 Europe/Paris';
    $draws[361]['draw'] = '[["01","16","48","04","40"],["01","09"]]';
    $draws[362] = array();
    $draws[362]['date'] = '2010-10-01 21:30:00 Europe/Paris';
    $draws[362]['draw'] = '[["04","27","06","48","01"],["01","06"]]';
    $draws[363] = array();
    $draws[363]['date'] = '2010-10-08 21:30:00 Europe/Paris';
    $draws[363]['draw'] = '[["46","35","39","30","09"],["06","08"]]';
    $draws[364] = array();
    $draws[364]['date'] = '2010-10-15 21:30:00 Europe/Paris';
    $draws[364]['draw'] = '[["38","31","02","36","43"],["07","03"]]';
    $draws[365] = array();
    $draws[365]['date'] = '2010-10-22 21:30:00 Europe/Paris';
    $draws[365]['draw'] = '[["39","05","11","09","04"],["03","05"]]';
    $draws[366] = array();
    $draws[366]['date'] = '2010-10-29 21:30:00 Europe/Paris';
    $draws[366]['draw'] = '[["32","22","16","42","20"],["08","09"]]';
    $draws[367] = array();
    $draws[367]['date'] = '2010-11-05 21:30:00 Europe/Paris';
    $draws[367]['draw'] = '[["21","23","33","50","40"],["05","04"]]';
    $draws[368] = array();
    $draws[368]['date'] = '2010-11-12 21:30:00 Europe/Paris';
    $draws[368]['draw'] = '[["23","47","07","19","29"],["06","01"]]';
    $draws[369] = array();
    $draws[369]['date'] = '2010-11-19 21:30:00 Europe/Paris';
    $draws[369]['draw'] = '[["36","12","15","45","32"],["09","07"]]';
    $draws[370] = array();
    $draws[370]['date'] = '2010-11-26 21:30:00 Europe/Paris';
    $draws[370]['draw'] = '[["09","41","36","49","28"],["07","05"]]';
    $draws[371] = array();
    $draws[371]['date'] = '2010-12-03 21:30:00 Europe/Paris';
    $draws[371]['draw'] = '[["28","32","46","08","19"],["04","07"]]';
    $draws[372] = array();
    $draws[372]['date'] = '2010-12-10 21:30:00 Europe/Paris';
    $draws[372]['draw'] = '[["46","02","10","03","33"],["08","07"]]';
    $draws[373] = array();
    $draws[373]['date'] = '2010-12-17 21:30:00 Europe/Paris';
    $draws[373]['draw'] = '[["03","35","29","42","20"],["03","08"]]';
    $draws[374] = array();
    $draws[374]['date'] = '2010-12-24 21:30:00 Europe/Paris';
    $draws[374]['draw'] = '[["46","19","42","36","38"],["08","02"]]';
    $draws[375] = array();
    $draws[375]['date'] = '2010-12-31 21:30:00 Europe/Paris';
    $draws[375]['draw'] = '[["02","24","43","38","34"],["01","07"]]';
    $draws[376] = array();
    $draws[376]['date'] = '2011-01-07 21:30:00 Europe/Paris';
    $draws[376]['draw'] = '[["32","22","01","48","50"],["07","06"]]';
    $draws[377] = array();
    $draws[377]['date'] = '2011-01-14 21:30:00 Europe/Paris';
    $draws[377]['draw'] = '[["44","02","34","14","39"],["07","06"]]';
    $draws[378] = array();
    $draws[378]['date'] = '2011-01-21 21:30:00 Europe/Paris';
    $draws[378]['draw'] = '[["21","11","13","03","18"],["05","04"]]';
    $draws[379] = array();
    $draws[379]['date'] = '2011-01-28 21:30:00 Europe/Paris';
    $draws[379]['draw'] = '[["41","24","23","42","13"],["05","01"]]';
    $draws[380] = array();
    $draws[380]['date'] = '2011-02-04 21:30:00 Europe/Paris';
    $draws[380]['draw'] = '[["47","35","11","02","24"],["05","09"]]';
    $draws[381] = array();
    $draws[381]['date'] = '2011-02-11 21:30:00 Europe/Paris';
    $draws[381]['draw'] = '[["15","14","12","19","23"],["07","08"]]';
    $draws[382] = array();
    $draws[382]['date'] = '2011-02-18 21:30:00 Europe/Paris';
    $draws[382]['draw'] = '[["45","03","49","15","02"],["09","05"]]';
    $draws[383] = array();
    $draws[383]['date'] = '2011-02-25 21:30:00 Europe/Paris';
    $draws[383]['draw'] = '[["42","45","13","48","12"],["03","09"]]';
    $draws[384] = array();
    $draws[384]['date'] = '2011-03-04 21:30:00 Europe/Paris';
    $draws[384]['draw'] = '[["28","41","25","11","27"],["08","05"]]';
    $draws[385] = array();
    $draws[385]['date'] = '2011-03-11 21:30:00 Europe/Paris';
    $draws[385]['draw'] = '[["17","24","37","19","46"],["02","07"]]';
    $draws[386] = array();
    $draws[386]['date'] = '2011-03-18 21:30:00 Europe/Paris';
    $draws[386]['draw'] = '[["50","13","26","01","20"],["07","06"]]';
    $draws[387] = array();
    $draws[387]['date'] = '2011-03-25 21:30:00 Europe/Paris';
    $draws[387]['draw'] = '[["12","21","06","33","27"],["07","03"]]';
    $draws[388] = array();
    $draws[388]['date'] = '2011-04-01 21:30:00 Europe/Paris';
    $draws[388]['draw'] = '[["17","33","22","21","04"],["04","08"]]';
    $draws[389] = array();
    $draws[389]['date'] = '2011-04-08 21:30:00 Europe/Paris';
    $draws[389]['draw'] = '[["21","47","23","38","50"],["06","02"]]';
    $draws[390] = array();
    $draws[390]['date'] = '2011-04-15 21:30:00 Europe/Paris';
    $draws[390]['draw'] = '[["04","41","06","21","39"],["02","06"]]';
    $draws[391] = array();
    $draws[391]['date'] = '2011-04-22 21:30:00 Europe/Paris';
    $draws[391]['draw'] = '[["22","45","48","11","36"],["01","04"]]';
    $draws[392] = array();
    $draws[392]['date'] = '2011-04-29 21:30:00 Europe/Paris';
    $draws[392]['draw'] = '[["38","40","25","15","41"],["01","02"]]';
    $draws[393] = array();
    $draws[393]['date'] = '2011-05-06 21:30:00 Europe/Paris';
    $draws[393]['draw'] = '[["28","16","20","22","11"],["04","09"]]';
    $draws[394] = array();
    $draws[394]['date'] = '2011-05-10 21:30:00 Europe/Paris';
    $draws[394]['draw'] = '[["28","03","45","10","15"],["07","05"]]';
    $draws[395] = array();
    $draws[395]['date'] = '2011-05-13 21:30:00 Europe/Paris';
    $draws[395]['draw'] = '[["17","47","11","36","09"],["02","01"]]';
    $draws[396] = array();
    $draws[396]['date'] = '2011-05-17 21:30:00 Europe/Paris';
    $draws[396]['draw'] = '[["37","20","21","45","46"],["03","02"]]';
    $draws[397] = array();
    $draws[397]['date'] = '2011-05-20 21:30:00 Europe/Paris';
    $draws[397]['draw'] = '[["42","25","10","20","14"],["08","11"]]';
    $draws[398] = array();
    $draws[398]['date'] = '2011-05-24 21:30:00 Europe/Paris';
    $draws[398]['draw'] = '[["16","23","24","29","26"],["02","09"]]';
    $draws[399] = array();
    $draws[399]['date'] = '2011-05-27 21:30:00 Europe/Paris';
    $draws[399]['draw'] = '[["28","09","49","25","17"],["09","08"]]';
    $draws[400] = array();
    $draws[400]['date'] = '2011-05-31 21:30:00 Europe/Paris';
    $draws[400]['draw'] = '[["22","09","10","50","01"],["11","05"]]';
    $draws[401] = array();
    $draws[401]['date'] = '2011-06-03 21:30:00 Europe/Paris';
    $draws[401]['draw'] = '[["49","40","50","39","04"],["02","05"]]';
    $draws[402] = array();
    $draws[402]['date'] = '2011-06-07 21:30:00 Europe/Paris';
    $draws[402]['draw'] = '[["25","38","40","06","36"],["10","04"]]';
    $draws[403] = array();
    $draws[403]['date'] = '2011-06-10 21:30:00 Europe/Paris';
    $draws[403]['draw'] = '[["37","20","03","48","19"],["08","11"]]';
    $draws[404] = array();
    $draws[404]['date'] = '2011-06-14 21:30:00 Europe/Paris';
    $draws[404]['draw'] = '[["41","19","48","05","12"],["08","10"]]';
    $draws[405] = array();
    $draws[405]['date'] = '2011-06-17 21:30:00 Europe/Paris';
    $draws[405]['draw'] = '[["11","22","21","16","44"],["08","03"]]';
    $draws[406] = array();
    $draws[406]['date'] = '2011-06-21 21:30:00 Europe/Paris';
    $draws[406]['draw'] = '[["49","50","20","17","35"],["04","03"]]';
    $draws[407] = array();
    $draws[407]['date'] = '2011-06-24 21:30:00 Europe/Paris';
    $draws[407]['draw'] = '[["41","20","05","30","16"],["11","06"]]';
    $draws[408] = array();
    $draws[408]['date'] = '2011-06-28 21:30:00 Europe/Paris';
    $draws[408]['draw'] = '[["16","15","44","30","50"],["03","02"]]';
    $draws[409] = array();
    $draws[409]['date'] = '2011-07-01 21:30:00 Europe/Paris';
    $draws[409]['draw'] = '[["11","23","31","08","46"],["09","08"]]';
    $draws[410] = array();
    $draws[410]['date'] = '2011-07-05 21:30:00 Europe/Paris';
    $draws[410]['draw'] = '[["28","47","29","11","49"],["05","01"]]';
    $draws[411] = array();
    $draws[411]['date'] = '2011-07-08 21:30:00 Europe/Paris';
    $draws[411]['draw'] = '[["12","13","40","49","23"],["07","10"]]';
    $draws[412] = array();
    $draws[412]['date'] = '2011-07-12 21:30:00 Europe/Paris';
    $draws[412]['draw'] = '[["19","17","42","45","38"],["09","10"]]';
    $draws[413] = array();
    $draws[413]['date'] = '2011-07-15 21:30:00 Europe/Paris';
    $draws[413]['draw'] = '[["26","06","33","39","34"],["03","04"]]';
    $draws[414] = array();
    $draws[414]['date'] = '2011-07-19 21:30:00 Europe/Paris';
    $draws[414]['draw'] = '[["16","03","25","35","26"],["05","09"]]';
    $draws[415] = array();
    $draws[415]['date'] = '2011-07-22 21:30:00 Europe/Paris';
    $draws[415]['draw'] = '[["04","50","15","49","23"],["02","06"]]';
    $draws[416] = array();
    $draws[416]['date'] = '2011-07-26 21:30:00 Europe/Paris';
    $draws[416]['draw'] = '[["05","01","25","48","22"],["11","03"]]';
    $draws[417] = array();
    $draws[417]['date'] = '2011-07-29 21:30:00 Europe/Paris';
    $draws[417]['draw'] = '[["37","38","19","27","12"],["05","10"]]';
    $draws[418] = array();
    $draws[418]['date'] = '2011-08-02 21:30:00 Europe/Paris';
    $draws[418]['draw'] = '[["08","33","14","24","05"],["08","03"]]';
    $draws[419] = array();
    $draws[419]['date'] = '2011-08-05 21:30:00 Europe/Paris';
    $draws[419]['draw'] = '[["34","32","18","14","13"],["01","10"]]';
    $draws[420] = array();
    $draws[420]['date'] = '2011-08-09 21:30:00 Europe/Paris';
    $draws[420]['draw'] = '[["36","24","34","07","23"],["11","08"]]';
    $draws[421] = array();
    $draws[421]['date'] = '2011-08-12 21:30:00 Europe/Paris';
    $draws[421]['draw'] = '[["07","20","37","10","27"],["07","04"]]';
    $draws[422] = array();
    $draws[422]['date'] = '2011-08-16 21:30:00 Europe/Paris';
    $draws[422]['draw'] = '[["45","18","01","13","17"],["08","03"]]';
    $draws[423] = array();
    $draws[423]['date'] = '2011-08-19 21:30:00 Europe/Paris';
    $draws[423]['draw'] = '[["16","06","31","28","14"],["11","02"]]';
    $draws[424] = array();
    $draws[424]['date'] = '2011-08-23 21:30:00 Europe/Paris';
    $draws[424]['draw'] = '[["42","50","06","14","04"],["02","04"]]';
    $draws[425] = array();
    $draws[425]['date'] = '2011-08-26 21:30:00 Europe/Paris';
    $draws[425]['draw'] = '[["25","45","22","33","12"],["05","07"]]';
    $draws[426] = array();
    $draws[426]['date'] = '2011-08-30 21:30:00 Europe/Paris';
    $draws[426]['draw'] = '[["46","08","02","10","19"],["05","09"]]';
    $draws[427] = array();
    $draws[427]['date'] = '2011-09-02 21:30:00 Europe/Paris';
    $draws[427]['draw'] = '[["37","12","26","38","44"],["04","07"]]';
    $draws[428] = array();
    $draws[428]['date'] = '2011-09-06 21:30:00 Europe/Paris';
    $draws[428]['draw'] = '[["42","35","50","48","47"],["09","08"]]';
    $draws[429] = array();
    $draws[429]['date'] = '2011-09-09 21:30:00 Europe/Paris';
    $draws[429]['draw'] = '[["21","05","34","31","28"],["02","01"]]';
    $draws[430] = array();
    $draws[430]['date'] = '2011-09-13 21:30:00 Europe/Paris';
    $draws[430]['draw'] = '[["28","32","49","09","30"],["09","10"]]';
    $draws[431] = array();
    $draws[431]['date'] = '2011-09-16 21:30:00 Europe/Paris';
    $draws[431]['draw'] = '[["39","02","42","17","08"],["03","10"]]';
    $draws[432] = array();
    $draws[432]['date'] = '2011-09-20 21:30:00 Europe/Paris';
    $draws[432]['draw'] = '[["25","38","19","09","36"],["11","07"]]';
    $draws[433] = array();
    $draws[433]['date'] = '2011-09-23 21:30:00 Europe/Paris';
    $draws[433]['draw'] = '[["06","33","48","14","34"],["06","02"]]';
    $draws[434] = array();
    $draws[434]['date'] = '2011-09-27 21:30:00 Europe/Paris';
    $draws[434]['draw'] = '[["28","18","40","27","35"],["03","05"]]';
    $draws[435] = array();
    $draws[435]['date'] = '2011-09-30 21:30:00 Europe/Paris';
    $draws[435]['draw'] = '[["28","15","44","31","05"],["01","06"]]';
    $draws[436] = array();
    $draws[436]['date'] = '2011-10-04 21:30:00 Europe/Paris';
    $draws[436]['draw'] = '[["14","16","23","45","38"],["08","11"]]';
    $draws[437] = array();
    $draws[437]['date'] = '2011-10-07 21:30:00 Europe/Paris';
    $draws[437]['draw'] = '[["42","34","18","38","26"],["08","05"]]';
    $draws[438] = array();
    $draws[438]['date'] = '2011-10-11 21:30:00 Europe/Paris';
    $draws[438]['draw'] = '[["12","16","04","01","48"],["09","10"]]';
    $draws[439] = array();
    $draws[439]['date'] = '2011-10-14 21:30:00 Europe/Paris';
    $draws[439]['draw'] = '[["47","23","12","29","32"],["03","05"]]';
    $draws[440] = array();
    $draws[440]['date'] = '2011-10-18 21:30:00 Europe/Paris';
    $draws[440]['draw'] = '[["46","18","37","48","23"],["02","10"]]';
    $draws[441] = array();
    $draws[441]['date'] = '2011-10-21 21:30:00 Europe/Paris';
    $draws[441]['draw'] = '[["37","19","02","33","46"],["05","08"]]';
    $draws[442] = array();
    $draws[442]['date'] = '2011-10-25 21:30:00 Europe/Paris';
    $draws[442]['draw'] = '[["39","28","22","12","27"],["04","10"]]';
    $draws[443] = array();
    $draws[443]['date'] = '2011-10-28 21:30:00 Europe/Paris';
    $draws[443]['draw'] = '[["39","16","20","17","50"],["04","08"]]';
    $draws[444] = array();
    $draws[444]['date'] = '2011-11-01 21:30:00 Europe/Paris';
    $draws[444]['draw'] = '[["20","45","23","14","46"],["01","11"]]';
    $draws[445] = array();
    $draws[445]['date'] = '2011-11-04 21:30:00 Europe/Paris';
    $draws[445]['draw'] = '[["41","50","11","43","14"],["09","02"]]';
    $draws[446] = array();
    $draws[446]['date'] = '2011-11-08 21:30:00 Europe/Paris';
    $draws[446]['draw'] = '[["40","15","04","29","01"],["01","05"]]';
    $draws[447] = array();
    $draws[447]['date'] = '2011-11-11 21:30:00 Europe/Paris';
    $draws[447]['draw'] = '[["38","18","01","04","23"],["03","07"]]';
    $draws[448] = array();
    $draws[448]['date'] = '2011-11-15 21:30:00 Europe/Paris';
    $draws[448]['draw'] = '[["47","17","22","06","45"],["03","11"]]';
    $draws[449] = array();
    $draws[449]['date'] = '2011-11-18 21:30:00 Europe/Paris';
    $draws[449]['draw'] = '[["39","44","24","04","12"],["02","04"]]';
    $draws[450] = array();
    $draws[450]['date'] = '2011-11-22 21:30:00 Europe/Paris';
    $draws[450]['draw'] = '[["16","40","38","24","18"],["02","04"]]';
    $draws[451] = array();
    $draws[451]['date'] = '2011-11-25 21:30:00 Europe/Paris';
    $draws[451]['draw'] = '[["34","14","26","19","28"],["05","08"]]';
    $draws[452] = array();
    $draws[452]['date'] = '2011-11-29 21:30:00 Europe/Paris';
    $draws[452]['draw'] = '[["25","50","11","45","41"],["07","02"]]';
    $draws[453] = array();
    $draws[453]['date'] = '2011-12-02 21:30:00 Europe/Paris';
    $draws[453]['draw'] = '[["27","40","07","43","30"],["09","08"]]';
    $draws[454] = array();
    $draws[454]['date'] = '2011-12-06 21:30:00 Europe/Paris';
    $draws[454]['draw'] = '[["34","21","20","38","19"],["09","03"]]';
    $draws[455] = array();
    $draws[455]['date'] = '2011-12-09 21:30:00 Europe/Paris';
    $draws[455]['draw'] = '[["21","12","47","44","29"],["02","01"]]';
    $draws[456] = array();
    $draws[456]['date'] = '2011-12-13 21:30:00 Europe/Paris';
    $draws[456]['draw'] = '[["12","37","18","33","07"],["01","11"]]';
    $draws[457] = array();
    $draws[457]['date'] = '2011-12-16 21:30:00 Europe/Paris';
    $draws[457]['draw'] = '[["10","02","23","31","05"],["05","02"]]';
    $draws[458] = array();
    $draws[458]['date'] = '2011-12-20 21:30:00 Europe/Paris';
    $draws[458]['draw'] = '[["14","48","01","09","12"],["07","01"]]';
    $draws[459] = array();
    $draws[459]['date'] = '2011-12-23 21:30:00 Europe/Paris';
    $draws[459]['draw'] = '[["22","07","24","28","21"],["01","11"]]';
    $draws[460] = array();
    $draws[460]['date'] = '2011-12-27 21:30:00 Europe/Paris';
    $draws[460]['draw'] = '[["26","21","25","19","44"],["07","03"]]';
    $draws[461] = array();
    $draws[461]['date'] = '2011-12-30 21:30:00 Europe/Paris';
    $draws[461]['draw'] = '[["36","44","43","16","50"],["08","07"]]';
    $draws[462] = array();
    $draws[462]['date'] = '2012-01-03 21:30:00 Europe/Paris';
    $draws[462]['draw'] = '[["42","30","45","03","49"],["05","10"]]';
    $draws[463] = array();
    $draws[463]['date'] = '2012-01-06 21:30:00 Europe/Paris';
    $draws[463]['draw'] = '[["01","06","10","31","12"],["07","02"]]';
    $draws[464] = array();
    $draws[464]['date'] = '2012-01-10 21:30:00 Europe/Paris';
    $draws[464]['draw'] = '[["09","04","30","10","40"],["09","02"]]';
    $draws[465] = array();
    $draws[465]['date'] = '2012-01-13 21:30:00 Europe/Paris';
    $draws[465]['draw'] = '[["39","13","21","14","27"],["08","06"]]';
    $draws[466] = array();
    $draws[466]['date'] = '2012-01-17 21:30:00 Europe/Paris';
    $draws[466]['draw'] = '[["12","44","22","30","31"],["05","06"]]';
    $draws[467] = array();
    $draws[467]['date'] = '2012-01-20 21:30:00 Europe/Paris';
    $draws[467]['draw'] = '[["10","28","27","02","22"],["08","06"]]';
    $draws[468] = array();
    $draws[468]['date'] = '2012-01-24 21:30:00 Europe/Paris';
    $draws[468]['draw'] = '[["01","20","06","02","36"],["11","08"]]';
    $draws[469] = array();
    $draws[469]['date'] = '2012-01-27 21:30:00 Europe/Paris';
    $draws[469]['draw'] = '[["10","19","44","13","39"],["06","02"]]';
    $draws[470] = array();
    $draws[470]['date'] = '2012-01-31 21:30:00 Europe/Paris';
    $draws[470]['draw'] = '[["43","34","38","09","45"],["04","02"]]';
    $draws[471] = array();
    $draws[471]['date'] = '2012-02-03 21:30:00 Europe/Paris';
    $draws[471]['draw'] = '[["16","20","19","25","28"],["01","10"]]';
    $draws[472] = array();
    $draws[472]['date'] = '2012-02-07 21:30:00 Europe/Paris';
    $draws[472]['draw'] = '[["15","03","17","33","28"],["02","04"]]';
    $draws[473] = array();
    $draws[473]['date'] = '2012-02-10 21:30:00 Europe/Paris';
    $draws[473]['draw'] = '[["03","14","31","41","08"],["07","11"]]';
    $draws[474] = array();
    $draws[474]['date'] = '2012-02-14 21:30:00 Europe/Paris';
    $draws[474]['draw'] = '[["36","14","42","46","27"],["11","08"]]';
    $draws[475] = array();
    $draws[475]['date'] = '2012-02-17 21:30:00 Europe/Paris';
    $draws[475]['draw'] = '[["11","04","47","28","38"],["11","10"]]';
    $draws[476] = array();
    $draws[476]['date'] = '2012-02-21 21:30:00 Europe/Paris';
    $draws[476]['draw'] = '[["11","24","14","25","29"],["11","07"]]';
    $draws[477] = array();
    $draws[477]['date'] = '2012-02-24 21:30:00 Europe/Paris';
    $draws[477]['draw'] = '[["34","03","12","26","07"],["10","08"]]';
    $draws[478] = array();
    $draws[478]['date'] = '2012-02-28 21:30:00 Europe/Paris';
    $draws[478]['draw'] = '[["10","48","01","17","33"],["02","03"]]';
    $draws[479] = array();
    $draws[479]['date'] = '2012-03-02 21:30:00 Europe/Paris';
    $draws[479]['draw'] = '[["44","05","11","06","30"],["06","02"]]';
    $draws[480] = array();
    $draws[480]['date'] = '2012-03-06 21:30:00 Europe/Paris';
    $draws[480]['draw'] = '[["23","47","27","37","24"],["06","02"]]';
    $draws[481] = array();
    $draws[481]['date'] = '2012-03-09 21:30:00 Europe/Paris';
    $draws[481]['draw'] = '[["39","36","32","47","03"],["06","09"]]';
    $draws[482] = array();
    $draws[482]['date'] = '2012-03-13 21:30:00 Europe/Paris';
    $draws[482]['draw'] = '[["47","01","25","10","43"],["08","09"]]';
    $draws[483] = array();
    $draws[483]['date'] = '2012-03-16 21:30:00 Europe/Paris';
    $draws[483]['draw'] = '[["12","04","50","03","23"],["04","07"]]';
    $draws[484] = array();
    $draws[484]['date'] = '2012-03-20 21:30:00 Europe/Paris';
    $draws[484]['draw'] = '[["28","30","15","16","46"],["03","04"]]';
    $draws[485] = array();
    $draws[485]['date'] = '2012-03-23 21:30:00 Europe/Paris';
    $draws[485]['draw'] = '[["50","15","09","23","31"],["08","11"]]';
    $draws[486] = array();
    $draws[486]['date'] = '2012-03-27 21:30:00 Europe/Paris';
    $draws[486]['draw'] = '[["29","36","27","34","24"],["07","08"]]';
    $draws[487] = array();
    $draws[487]['date'] = '2012-03-30 21:30:00 Europe/Paris';
    $draws[487]['draw'] = '[["46","17","23","04","36"],["10","06"]]';
    $draws[488] = array();
    $draws[488]['date'] = '2012-04-03 21:30:00 Europe/Paris';
    $draws[488]['draw'] = '[["01","08","18","25","30"],["10","09"]]';
    $draws[489] = array();
    $draws[489]['date'] = '2012-04-06 21:30:00 Europe/Paris';
    $draws[489]['draw'] = '[["11","35","45","20","30"],["02","03"]]';
    $draws[490] = array();
    $draws[490]['date'] = '2012-04-10 21:30:00 Europe/Paris';
    $draws[490]['draw'] = '[["37","27","22","25","36"],["09","05"]]';
    $draws[491] = array();
    $draws[491]['date'] = '2012-04-13 21:30:00 Europe/Paris';
    $draws[491]['draw'] = '[["08","39","43","13","26"],["03","05"]]';
    $draws[492] = array();
    $draws[492]['date'] = '2012-04-17 21:30:00 Europe/Paris';
    $draws[492]['draw'] = '[["10","28","49","48","33"],["10","01"]]';
    $draws[493] = array();
    $draws[493]['date'] = '2012-04-20 21:30:00 Europe/Paris';
    $draws[493]['draw'] = '[["32","41","29","03","06"],["11","10"]]';
    $draws[494] = array();
    $draws[494]['date'] = '2012-04-24 21:30:00 Europe/Paris';
    $draws[494]['draw'] = '[["08","24","48","43","09"],["03","05"]]';
    $draws[495] = array();
    $draws[495]['date'] = '2012-04-27 21:30:00 Europe/Paris';
    $draws[495]['draw'] = '[["36","43","30","27","20"],["01","06"]]';
    $draws[496] = array();
    $draws[496]['date'] = '2012-05-01 21:30:00 Europe/Paris';
    $draws[496]['draw'] = '[["04","15","41","05","19"],["11","09"]]';
    $draws[497] = array();
    $draws[497]['date'] = '2012-05-04 21:30:00 Europe/Paris';
    $draws[497]['draw'] = '[["26","41","40","39","03"],["01","02"]]';
    $draws[498] = array();
    $draws[498]['date'] = '2012-05-08 21:30:00 Europe/Paris';
    $draws[498]['draw'] = '[["03","34","48","38","21"],["05","08"]]';
    $draws[499] = array();
    $draws[499]['date'] = '2012-05-11 21:30:00 Europe/Paris';
    $draws[499]['draw'] = '[["01","17","13","44","38"],["02","11"]]';
    $draws[500] = array();
    $draws[500]['date'] = '2012-05-15 21:30:00 Europe/Paris';
    $draws[500]['draw'] = '[["13","02","50","11","26"],["05","02"]]';
    $draws[501] = array();
    $draws[501]['date'] = '2012-05-18 21:30:00 Europe/Paris';
    $draws[501]['draw'] = '[["29","50","43","47","13"],["09","11"]]';
    $draws[502] = array();
    $draws[502]['date'] = '2012-05-22 21:30:00 Europe/Paris';
    $draws[502]['draw'] = '[["31","32","41","16","37"],["07","01"]]';
    $draws[503] = array();
    $draws[503]['date'] = '2012-05-25 21:30:00 Europe/Paris';
    $draws[503]['draw'] = '[["35","12","22","49","46"],["02","08"]]';
    $draws[504] = array();
    $draws[504]['date'] = '2012-05-29 21:30:00 Europe/Paris';
    $draws[504]['draw'] = '[["28","17","25","15","08"],["03","11"]]';
    $draws[505] = array();
    $draws[505]['date'] = '2012-06-01 21:30:00 Europe/Paris';
    $draws[505]['draw'] = '[["26","02","36","14","04"],["09","10"]]';
    $draws[506] = array();
    $draws[506]['date'] = '2012-06-05 21:30:00 Europe/Paris';
    $draws[506]['draw'] = '[["13","49","37","47","34"],["08","09"]]';
    $draws[507] = array();
    $draws[507]['date'] = '2012-06-08 21:30:00 Europe/Paris';
    $draws[507]['draw'] = '[["11","22","05","34","40"],["09","11"]]';
    $draws[508] = array();
    $draws[508]['date'] = '2012-06-12 21:30:00 Europe/Paris';
    $draws[508]['draw'] = '[["30","26","48","15","08"],["09","10"]]';
    $draws[509] = array();
    $draws[509]['date'] = '2012-06-15 21:30:00 Europe/Paris';
    $draws[509]['draw'] = '[["48","38","27","22","10"],["03","07"]]';
    $draws[510] = array();
    $draws[510]['date'] = '2012-06-19 21:30:00 Europe/Paris';
    $draws[510]['draw'] = '[["17","20","50","07","35"],["05","11"]]';
    $draws[511] = array();
    $draws[511]['date'] = '2012-06-22 21:30:00 Europe/Paris';
    $draws[511]['draw'] = '[["18","14","19","43","49"],["07","03"]]';
    $draws[512] = array();
    $draws[512]['date'] = '2012-06-26 21:30:00 Europe/Paris';
    $draws[512]['draw'] = '[["11","22","35","20","01"],["10","08"]]';
    $draws[513] = array();
    $draws[513]['date'] = '2012-06-29 21:30:00 Europe/Paris';
    $draws[513]['draw'] = '[["14","17","28","39","29"],["11","01"]]';
    $draws[514] = array();
    $draws[514]['date'] = '2012-07-03 21:30:00 Europe/Paris';
    $draws[514]['draw'] = '[["22","07","02","40","27"],["06","03"]]';
    $draws[515] = array();
    $draws[515]['date'] = '2012-07-06 21:30:00 Europe/Paris';
    $draws[515]['draw'] = '[["40","42","38","31","32"],["03","01"]]';
    $draws[516] = array();
    $draws[516]['date'] = '2012-07-10 21:30:00 Europe/Paris';
    $draws[516]['draw'] = '[["37","01","24","16","03"],["08","01"]]';
    $draws[517] = array();
    $draws[517]['date'] = '2012-07-13 21:30:00 Europe/Paris';
    $draws[517]['draw'] = '[["18","46","35","25","08"],["09","04"]]';
    $draws[518] = array();
    $draws[518]['date'] = '2012-07-17 21:30:00 Europe/Paris';
    $draws[518]['draw'] = '[["24","02","43","07","46"],["10","08"]]';
    $draws[519] = array();
    $draws[519]['date'] = '2012-07-20 21:30:00 Europe/Paris';
    $draws[519]['draw'] = '[["19","23","10","45","49"],["09","10"]]';
    $draws[520] = array();
    $draws[520]['date'] = '2012-07-24 21:30:00 Europe/Paris';
    $draws[520]['draw'] = '[["18","25","04","16","44"],["11","01"]]';
    $draws[521] = array();
    $draws[521]['date'] = '2012-07-27 21:30:00 Europe/Paris';
    $draws[521]['draw'] = '[["15","48","14","23","21"],["02","10"]]';
    $draws[522] = array();
    $draws[522]['date'] = '2012-07-31 21:30:00 Europe/Paris';
    $draws[522]['draw'] = '[["35","39","29","09","08"],["09","08"]]';
    $draws[523] = array();
    $draws[523]['date'] = '2012-08-03 21:30:00 Europe/Paris';
    $draws[523]['draw'] = '[["34","35","42","24","46"],["05","01"]]';
    $draws[524] = array();
    $draws[524]['date'] = '2012-08-07 21:30:00 Europe/Paris';
    $draws[524]['draw'] = '[["20","50","34","46","27"],["03","02"]]';
    $draws[525] = array();
    $draws[525]['date'] = '2012-08-10 21:30:00 Europe/Paris';
    $draws[525]['draw'] = '[["50","21","17","48","11"],["09","10"]]';
    $draws[526] = array();
    $draws[526]['date'] = '2012-08-14 21:30:00 Europe/Paris';
    $draws[526]['draw'] = '[["45","16","42","01","38"],["09","10"]]';
    $draws[527] = array();
    $draws[527]['date'] = '2012-08-17 21:30:00 Europe/Paris';
    $draws[527]['draw'] = '[["19","25","33","44","28"],["08","02"]]';
    $draws[528] = array();
    $draws[528]['date'] = '2012-08-21 21:30:00 Europe/Paris';
    $draws[528]['draw'] = '[["17","05","38","04","48"],["04","03"]]';
    $draws[529] = array();
    $draws[529]['date'] = '2012-08-24 21:30:00 Europe/Paris';
    $draws[529]['draw'] = '[["06","05","19","37","12"],["07","03"]]';
    $draws[530] = array();
    $draws[530]['date'] = '2012-08-28 21:30:00 Europe/Paris';
    $draws[530]['draw'] = '[["01","26","25","44","18"],["05","04"]]';
    $draws[531] = array();
    $draws[531]['date'] = '2012-08-31 21:30:00 Europe/Paris';
    $draws[531]['draw'] = '[["31","28","16","48","33"],["11","07"]]';
    $draws[532] = array();
    $draws[532]['date'] = '2012-09-04 21:30:00 Europe/Paris';
    $draws[532]['draw'] = '[["18","39","17","44","11"],["10","05"]]';
    $draws[533] = array();
    $draws[533]['date'] = '2012-09-07 21:30:00 Europe/Paris';
    $draws[533]['draw'] = '[["15","35","13","30","42"],["04","06"]]';
    $draws[534] = array();
    $draws[534]['date'] = '2012-09-11 21:30:00 Europe/Paris';
    $draws[534]['draw'] = '[["15","06","37","22","44"],["02","04"]]';
    $draws[535] = array();
    $draws[535]['date'] = '2012-09-14 21:30:00 Europe/Paris';
    $draws[535]['draw'] = '[["27","10","44","23","03"],["09","07"]]';
    $draws[536] = array();
    $draws[536]['date'] = '2012-09-18 21:30:00 Europe/Paris';
    $draws[536]['draw'] = '[["38","07","39","44","06"],["07","09"]]';
    $draws[537] = array();
    $draws[537]['date'] = '2012-09-21 21:30:00 Europe/Paris';
    $draws[537]['draw'] = '[["41","04","34","43","19"],["07","11"]]';
    $draws[538] = array();
    $draws[538]['date'] = '2012-09-25 21:30:00 Europe/Paris';
    $draws[538]['draw'] = '[["48","25","27","49","07"],["01","04"]]';
    $draws[539] = array();
    $draws[539]['date'] = '2012-09-28 21:30:00 Europe/Paris';
    $draws[539]['draw'] = '[["20","26","30","33","23"],["06","09"]]';
    $draws[540] = array();
    $draws[540]['date'] = '2012-10-02 21:30:00 Europe/Paris';
    $draws[540]['draw'] = '[["16","42","21","36","04"],["08","07"]]';
    $draws[541] = array();
    $draws[541]['date'] = '2012-10-05 21:30:00 Europe/Paris';
    $draws[541]['draw'] = '[["19","16","18","21","09"],["03","02"]]';
    $draws[542] = array();
    $draws[542]['date'] = '2012-10-09 21:30:00 Europe/Paris';
    $draws[542]['draw'] = '[["23","08","10","25","02"],["08","09"]]';
    $draws[543] = array();
    $draws[543]['date'] = '2012-10-12 21:30:00 Europe/Paris';
    $draws[543]['draw'] = '[["35","07","17","43","06"],["02","08"]]';
    $draws[544] = array();
    $draws[544]['date'] = '2012-10-16 21:30:00 Europe/Paris';
    $draws[544]['draw'] = '[["41","10","40","49","32"],["02","08"]]';
    $draws[545] = array();
    $draws[545]['date'] = '2012-10-19 21:30:00 Europe/Paris';
    $draws[545]['draw'] = '[["16","40","44","37","29"],["08","10"]]';
    $draws[546] = array();
    $draws[546]['date'] = '2012-10-23 21:30:00 Europe/Paris';
    $draws[546]['draw'] = '[["01","35","38","50","28"],["02","10"]]';
    $draws[547] = array();
    $draws[547]['date'] = '2012-12-21 21:30:00 Europe/Paris';
    $draws[547]['draw'] = '[["40","05","03","42","22"],["03","10"]]';
    $draws[548] = array();
    $draws[548]['date'] = '2012-12-25 21:30:00 Europe/Paris';
    $draws[548]['draw'] = '[["14","20","32","23","18"],["03","10"]]';
    $draws[549] = array();
    $draws[549]['date'] = '2012-12-28 21:30:00 Europe/Paris';
    $draws[549]['draw'] = '[["26","49","27","24","17"],["03","05"]]';
    $draws[550] = array();
    $draws[550]['date'] = '2013-01-01 21:30:00 Europe/Paris';
    $draws[550]['draw'] = '[["36","49","02","07","08"],["11","01"]]';
    $draws[551] = array();
    $draws[551]['date'] = '2013-01-04 21:30:00 Europe/Paris';
    $draws[551]['draw'] = '[["04","10","27","22","41"],["10","08"]]';
    $draws[552] = array();
    $draws[552]['date'] = '2013-01-08 21:30:00 Europe/Paris';
    $draws[552]['draw'] = '[["22","26","47","02","20"],["09","05"]]';
    $draws[553] = array();
    $draws[553]['date'] = '2013-01-11 21:30:00 Europe/Paris';
    $draws[553]['draw'] = '[["37","22","29","04","41"],["07","04"]]';
    $draws[554] = array();
    $draws[554]['date'] = '2013-01-15 21:30:00 Europe/Paris';
    $draws[554]['draw'] = '[["47","42","22","40","38"],["11","01"]]';
    $draws[555] = array();
    $draws[555]['date'] = '2013-01-18 21:30:00 Europe/Paris';
    $draws[555]['draw'] = '[["39","26","27","30","04"],["10","03"]]';
    $draws[556] = array();
    $draws[556]['date'] = '2013-01-22 21:30:00 Europe/Paris';
    $draws[556]['draw'] = '[["45","10","48","01","44"],["04","01"]]';
    $draws[557] = array();
    $draws[557]['date'] = '2013-01-25 21:30:00 Europe/Paris';
    $draws[557]['draw'] = '[["03","10","37","18","31"],["02","04"]]';
    $draws[558] = array();
    $draws[558]['date'] = '2013-01-29 21:30:00 Europe/Paris';
    $draws[558]['draw'] = '[["09","16","36","26","39"],["06","02"]]';
    $draws[559] = array();
    $draws[559]['date'] = '2013-02-01 21:30:00 Europe/Paris';
    $draws[559]['draw'] = '[["37","05","34","38","21"],["01","06"]]';
    $draws[560] = array();
    $draws[560]['date'] = '2013-02-05 21:30:00 Europe/Paris';
    $draws[560]['draw'] = '[["25","06","45","40","31"],["06","07"]]';
    $draws[561] = array();
    $draws[561]['date'] = '2013-02-08 21:30:00 Europe/Paris';
    $draws[561]['draw'] = '[["14","44","11","34","09"],["11","10"]]';
    $draws[562] = array();
    $draws[562]['date'] = '2013-02-12 21:30:00 Europe/Paris';
    $draws[562]['draw'] = '[["28","25","05","11","16"],["07","09"]]';
    $draws[563] = array();
    $draws[563]['date'] = '2013-02-15 21:30:00 Europe/Paris';
    $draws[563]['draw'] = '[["02","04","42","28","22"],["04","09"]]';
    $draws[564] = array();
    $draws[564]['date'] = '2013-02-19 21:30:00 Europe/Paris';
    $draws[564]['draw'] = '[["28","30","44","12","15"],["09","08"]]';
    $draws[565] = array();
    $draws[565]['date'] = '2013-02-22 21:30:00 Europe/Paris';
    $draws[565]['draw'] = '[["15","37","36","16","28"],["02","11"]]';
    $draws[566] = array();
    $draws[566]['date'] = '2013-02-26 21:30:00 Europe/Paris';
    $draws[566]['draw'] = '[["12","13","17","03","30"],["06","02"]]';
    $draws[567] = array();
    $draws[567]['date'] = '2013-03-01 21:30:00 Europe/Paris';
    $draws[567]['draw'] = '[["01","11","36","29","42"],["04","05"]]';
    $draws[568] = array();
    $draws[568]['date'] = '2013-03-05 21:30:00 Europe/Paris';
    $draws[568]['draw'] = '[["33","31","19","08","39"],["07","02"]]';
    $draws[569] = array();
    $draws[569]['date'] = '2013-03-08 21:30:00 Europe/Paris';
    $draws[569]['draw'] = '[["20","42","23","28","03"],["08","11"]]';
    $draws[570] = array();
    $draws[570]['date'] = '2013-03-12 21:30:00 Europe/Paris';
    $draws[570]['draw'] = '[["50","04","10","02","22"],["05","08"]]';
    $draws[571] = array();
    $draws[571]['date'] = '2013-03-15 21:30:00 Europe/Paris';
    $draws[571]['draw'] = '[["24","14","39","04","21"],["10","03"]]';
    $draws[572] = array();
    $draws[572]['date'] = '2013-03-19 21:30:00 Europe/Paris';
    $draws[572]['draw'] = '[["44","32","19","37","35"],["09","01"]]';
    $draws[573] = array();
    $draws[573]['date'] = '2013-03-22 21:30:00 Europe/Paris';
    $draws[573]['draw'] = '[["27","32","12","34","49"],["09","08"]]';
    $draws[574] = array();
    $draws[574]['date'] = '2013-03-26 21:30:00 Europe/Paris';
    $draws[574]['draw'] = '[["44","30","26","42","04"],["06","11"]]';
    $draws[575] = array();
    $draws[575]['date'] = '2013-03-29 21:30:00 Europe/Paris';
    $draws[575]['draw'] = '[["44","30","46","43","13"],["09","05"]]';
    $draws[576] = array();
    $draws[576]['date'] = '2013-04-02 21:30:00 Europe/Paris';
    $draws[576]['draw'] = '[["17","12","41","29","25"],["01","04"]]';

    foreach ($draws as $draw)
    {
        scraperwiki::save(array('date'), $draw);
    }
}

$options = array
(
    CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.8.1.7) Gecko/20070914 Firefox/2.0.0.7',
);

$html = CURL::Uni($url = 'https://www.jogossantacasa.pt/web/SCCartazResult/euroMilhoes', null, 'GET', null, $options);
$contests = array_slice(array_reverse(array_map('trim', CURL::Verse($html, '//form[@name="frmContestSelection"]//option/@value'))), -4);

foreach ($contests as $key => $value)
{
    $contests[$key] = CURL::Uni(sprintf('%s?selectContest=%s', $url, $value), null, 'GET', null, $options, 0);
}

$contests = CURL::Multi($contests);
$timezone = new DateTimeZone('Europe/Paris');

foreach (array_filter($contests, 'strlen') as $contest)
{
    $dom = CURL::Verse($contest);
    $result = array
    (
        'date' => substr(trim(CURL::Verse($dom, '//span[@class="dataInfo"]', 0)), -10),
        'draw' => explode('|', preg_replace('~[\D]+~', '|', trim(CURL::Verse($dom, '//div[@class="betMiddle twocol regPad"]/ul/li[2]', 0)))),
    );

    if (count($result['draw'] = array_filter($result['draw'], 'strlen')) == 7)
    {
        foreach ($result['draw'] as $key => $value)
        {
            $result['draw'][$key] = str_pad($value, 2, '0', STR_PAD_LEFT);
        }

        scraperwiki::save(array('date'), array
        (
            'date' => DateTime::createFromFormat('d/m/Y', $result['date'], $timezone)->setTime(21, 30)->format('Y-m-d H:i:s e'),
            'draw' => json_encode(array_chunk($result['draw'], 5)),
        ));
    }
}
