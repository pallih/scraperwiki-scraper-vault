<?php

// scraper for https://bountify.co/4s

$states = array
(
    '01' => 'ABIA',
    '02' => 'ADAMAWA',
    '03' => 'AKWA-IBOM',
    '04' => 'ANAMBRA',
    '05' => 'BAUCHI',
    '06' => 'BAYELSA',
    '07' => 'BENUE',
    '08' => 'BORNO',
    '09' => 'CROSS RIVER',
    '10' => 'DELTA',
    '11' => 'EBONYI',
    '12' => 'EDO',
    '13' => 'EKITI',
    '14' => 'ENUGU',
    '15' => 'FCT',
    '16' => 'GOMBE',
    '17' => 'IMO',
    '18' => 'JIGAWA',
    '19' => 'KADUNA',
    '20' => 'KANO',
    '21' => 'KATSINA',
    '22' => 'KEBBI',
    '23' => 'KOGI',
    '24' => 'KWARA',
    '25' => 'LAGOS',
    '26' => 'NASARAWA',
    '27' => 'NIGER',
    '28' => 'OGUN',
    '29' => 'ONDO',
    '30' => 'OSUN',
    '31' => 'OYO',
    '32' => 'PLATEAU',
    '33' => 'RIVERS',
    '34' => 'SOKOTO',
    '35' => 'TARABA',
    '36' => 'YOBE',
    '37' => 'ZAMFARA',
);

if (count(scraperwiki::show_tables()) == 0)
{
    $queries = array
    (
        'CREATE TABLE IF NOT EXISTS "swdata" ("date" text(7), "state" text(16), "births" int);',
        'PRAGMA busy_timeout = 0;',
    );

    foreach ($queries as $query)
    {
        scraperwiki::sqliteexecute($query);
    }

    $bulk = CURL::Uni('https://gist.github.com/anonymous/44dda309daf00452e3a0/raw/bb2285a0c52ccb91e219599af93b8c0df2ec9b94/nigeria_births.json');

    if ($bulk !== false)
    {
        scraperwiki::save_sqlite(array('date', 'state'), json_decode($bulk, true), 'swdata', 0);
    }
}

$urls = array();

foreach ($states as $key => $value)
{
    foreach (new DatePeriod(new DateTime('2011-01'), new DateInterval('P1M'), new DateTime('this month')) as $date)
    {
        $total = null;
        $query = 'SELECT COUNT(*) FROM "swdata" WHERE "date" = ? AND "state" = ? LIMIT 1;';

        if (strcmp(date('Y-m'), $date->format('Y-m')) !== 0)
        {
            $total = scraperwiki::sqliteexecute($query, array($date->format('Y-m'), $value));
        }

        if ((isset($total->data[0][0]) !== true) || (intval($total->data[0][0]) == 0))
        {
            $urls[sprintf('%s/%s', $key, $date->format('Y-m'))] = sprintf('http://rapidsmsnigeria.org/br/monthly/%s/%s', $key, $date->format('Y/n'));
        }
    }
}

if (count($urls) > 0)
{
    $options = array
    (
        CURLOPT_FORBID_REUSE => false,
        CURLOPT_FRESH_CONNECT => false,
    );

    foreach ($urls as $key => $value)
    {
        $urls[$key] = CURL::Uni($value, null, 'GET', null, $options, 0);
    }

    $urls = CURL::Multi($urls, 'RapidSMS_Nigeria', 8);
}

$csv = array();
$dates = scraperwiki::select('DISTINCT("date") FROM "swdata" ORDER BY "date" ASC;');

foreach ($dates as $key => $value)
{
    $dates[$key] = $value['date'];
}

$csv[0] = implode(',', array_merge(array(''), $dates));

foreach ($states as $state)
{
    $records = scraperwiki::select('"births" FROM "swdata" WHERE "state" = ? ORDER BY "date" ASC;', array($state));

    foreach ($records as $key => $value)
    {
        $records[$key] = $value['births'];
    }

    $csv[$state] = implode(',', array_merge(array($state), $records));
}

$path = sprintf('nigeria_births_%s.csv', date('Y-m-d'));
$gist = Gist(array($path => implode("\n", $csv)), 'CSV Dump of Nigeria Births (per Month)');

\scraperwiki::sw_dumpMessage(array
(
    'message_type' => 'console',
    'content' => sprintf('All done! A up-to-date CSV file is available at: %s', $gist),
));

function Gist($files, $description = null)
{
    $data = array
    (
        'description' => $description,
        'public' => false,
        'files' => array(),
    );

    $options = array
    (
        CURLOPT_USERAGENT => sprintf('PHP/%s', PHP_VERSION),
    );

    if ((is_array($files) === true) && (count($files) > 0))
    {
        foreach ($files as $key => $value)
        {
            $data['files'][$key] = array('content' => $value);
        }

        if (($result = CURL::Uni('https://api.github.com/gists', json_encode(array_filter($data, 'count')), 'POST', null, $options)) !== false)
        {
            if (is_array($result = json_decode($result, true)) === true)
            {
                return sprintf('https://gist.github.com/anonymous/%s', $result['id']);
            }
        }
    }

    return false;
}

function RapidSMS_Nigeria($body, $info, $id)
{
    global $states;

    if ((sscanf($id, '%i/%s', $key, $date) == 2) && (array_key_exists(sprintf('%02s', $key), $states) === true))
    {
        $data = array
        (
            'date' => $date,
            'state' => $states[sprintf('%02s', $key)],
            'births' => array_sum(str_replace(',', '', array_map('trim', CURL::Verse($body, '//div[@class="qt-body"]')))),
        );

        scraperwiki::save_sqlite(array('date', 'state'), $data, 'swdata', 2);
    }

    return true;
}

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

    public static function Multi($handles, $callback = null, $concurrent = null)
    {
        if (is_array($handles) === true)
        {
            $result = array();

            if ((isset($concurrent) === true) && (count($handles) > $concurrent))
            {
                foreach (array_chunk($handles, max(1, $concurrent), true) as $handles)
                {
                    $result = array_merge($result, self::Multi($handles, $callback, null));
                }

                return $result;
            }

            if (is_resource($curl = curl_multi_init()) === true)
            {
                $handles = array_filter($handles, function ($handle) use ($curl)
                {
                    if ((is_resource($handle) === true) && (strcmp('curl', get_resource_type($handle)) === 0))
                    {
                        return (curl_multi_add_handle($curl, $handle) === CURLM_OK);
                    }

                    return false;
                });

                do
                {
                    do
                    {
                        $status = curl_multi_exec($curl, $active);
                    }
                    while ($status === CURLM_CALL_MULTI_PERFORM);

                    while (is_array($value = curl_multi_info_read($curl)) === true)
                    {
                        if (($key = array_search($handle = $value['handle'], $handles, true)) !== false)
                        {
                            $result[$key] = false;

                            if ($value['result'] === CURLE_OK)
                            {
                                if ((isset($callback) === true) && (is_callable($callback) === true))
                                {
                                    $result[$key] = call_user_func($callback, curl_multi_getcontent($handle), curl_getinfo($handle), $key);
                                }

                                else
                                {
                                    $result[$key] = curl_multi_getcontent($handle);
                                }
                            }

                            curl_multi_remove_handle($curl, $handle); curl_close($handle);
                        }
                    }

                    if (($active > 0) && ($status === CURLM_OK) && (curl_multi_select($curl, 1.0) === -1))
                    {
                        usleep(100);
                    }
                }
                while (($active > 0) && ($status === CURLM_OK));

                if ($status !== CURLM_OK)
                {
                    foreach ($handles as $handle)
                    {
                        curl_multi_remove_handle($curl, $handle); curl_close($handle);
                    }
                }

                curl_multi_close($curl);
            }

            return $result;
        }

        return false;
    }

    public static function Verse($html, $xpath = null, $key = null, $default = false)
    {
        if (is_string($html) === true)
        {
            $dom = new \DOMDocument();

            if (libxml_use_internal_errors(true) === true)
            {
                libxml_clear_errors();
            }

            if (@$dom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8')) === true)
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
<?php

// scraper for https://bountify.co/4s

$states = array
(
    '01' => 'ABIA',
    '02' => 'ADAMAWA',
    '03' => 'AKWA-IBOM',
    '04' => 'ANAMBRA',
    '05' => 'BAUCHI',
    '06' => 'BAYELSA',
    '07' => 'BENUE',
    '08' => 'BORNO',
    '09' => 'CROSS RIVER',
    '10' => 'DELTA',
    '11' => 'EBONYI',
    '12' => 'EDO',
    '13' => 'EKITI',
    '14' => 'ENUGU',
    '15' => 'FCT',
    '16' => 'GOMBE',
    '17' => 'IMO',
    '18' => 'JIGAWA',
    '19' => 'KADUNA',
    '20' => 'KANO',
    '21' => 'KATSINA',
    '22' => 'KEBBI',
    '23' => 'KOGI',
    '24' => 'KWARA',
    '25' => 'LAGOS',
    '26' => 'NASARAWA',
    '27' => 'NIGER',
    '28' => 'OGUN',
    '29' => 'ONDO',
    '30' => 'OSUN',
    '31' => 'OYO',
    '32' => 'PLATEAU',
    '33' => 'RIVERS',
    '34' => 'SOKOTO',
    '35' => 'TARABA',
    '36' => 'YOBE',
    '37' => 'ZAMFARA',
);

if (count(scraperwiki::show_tables()) == 0)
{
    $queries = array
    (
        'CREATE TABLE IF NOT EXISTS "swdata" ("date" text(7), "state" text(16), "births" int);',
        'PRAGMA busy_timeout = 0;',
    );

    foreach ($queries as $query)
    {
        scraperwiki::sqliteexecute($query);
    }

    $bulk = CURL::Uni('https://gist.github.com/anonymous/44dda309daf00452e3a0/raw/bb2285a0c52ccb91e219599af93b8c0df2ec9b94/nigeria_births.json');

    if ($bulk !== false)
    {
        scraperwiki::save_sqlite(array('date', 'state'), json_decode($bulk, true), 'swdata', 0);
    }
}

$urls = array();

foreach ($states as $key => $value)
{
    foreach (new DatePeriod(new DateTime('2011-01'), new DateInterval('P1M'), new DateTime('this month')) as $date)
    {
        $total = null;
        $query = 'SELECT COUNT(*) FROM "swdata" WHERE "date" = ? AND "state" = ? LIMIT 1;';

        if (strcmp(date('Y-m'), $date->format('Y-m')) !== 0)
        {
            $total = scraperwiki::sqliteexecute($query, array($date->format('Y-m'), $value));
        }

        if ((isset($total->data[0][0]) !== true) || (intval($total->data[0][0]) == 0))
        {
            $urls[sprintf('%s/%s', $key, $date->format('Y-m'))] = sprintf('http://rapidsmsnigeria.org/br/monthly/%s/%s', $key, $date->format('Y/n'));
        }
    }
}

if (count($urls) > 0)
{
    $options = array
    (
        CURLOPT_FORBID_REUSE => false,
        CURLOPT_FRESH_CONNECT => false,
    );

    foreach ($urls as $key => $value)
    {
        $urls[$key] = CURL::Uni($value, null, 'GET', null, $options, 0);
    }

    $urls = CURL::Multi($urls, 'RapidSMS_Nigeria', 8);
}

$csv = array();
$dates = scraperwiki::select('DISTINCT("date") FROM "swdata" ORDER BY "date" ASC;');

foreach ($dates as $key => $value)
{
    $dates[$key] = $value['date'];
}

$csv[0] = implode(',', array_merge(array(''), $dates));

foreach ($states as $state)
{
    $records = scraperwiki::select('"births" FROM "swdata" WHERE "state" = ? ORDER BY "date" ASC;', array($state));

    foreach ($records as $key => $value)
    {
        $records[$key] = $value['births'];
    }

    $csv[$state] = implode(',', array_merge(array($state), $records));
}

$path = sprintf('nigeria_births_%s.csv', date('Y-m-d'));
$gist = Gist(array($path => implode("\n", $csv)), 'CSV Dump of Nigeria Births (per Month)');

\scraperwiki::sw_dumpMessage(array
(
    'message_type' => 'console',
    'content' => sprintf('All done! A up-to-date CSV file is available at: %s', $gist),
));

function Gist($files, $description = null)
{
    $data = array
    (
        'description' => $description,
        'public' => false,
        'files' => array(),
    );

    $options = array
    (
        CURLOPT_USERAGENT => sprintf('PHP/%s', PHP_VERSION),
    );

    if ((is_array($files) === true) && (count($files) > 0))
    {
        foreach ($files as $key => $value)
        {
            $data['files'][$key] = array('content' => $value);
        }

        if (($result = CURL::Uni('https://api.github.com/gists', json_encode(array_filter($data, 'count')), 'POST', null, $options)) !== false)
        {
            if (is_array($result = json_decode($result, true)) === true)
            {
                return sprintf('https://gist.github.com/anonymous/%s', $result['id']);
            }
        }
    }

    return false;
}

function RapidSMS_Nigeria($body, $info, $id)
{
    global $states;

    if ((sscanf($id, '%i/%s', $key, $date) == 2) && (array_key_exists(sprintf('%02s', $key), $states) === true))
    {
        $data = array
        (
            'date' => $date,
            'state' => $states[sprintf('%02s', $key)],
            'births' => array_sum(str_replace(',', '', array_map('trim', CURL::Verse($body, '//div[@class="qt-body"]')))),
        );

        scraperwiki::save_sqlite(array('date', 'state'), $data, 'swdata', 2);
    }

    return true;
}

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

    public static function Multi($handles, $callback = null, $concurrent = null)
    {
        if (is_array($handles) === true)
        {
            $result = array();

            if ((isset($concurrent) === true) && (count($handles) > $concurrent))
            {
                foreach (array_chunk($handles, max(1, $concurrent), true) as $handles)
                {
                    $result = array_merge($result, self::Multi($handles, $callback, null));
                }

                return $result;
            }

            if (is_resource($curl = curl_multi_init()) === true)
            {
                $handles = array_filter($handles, function ($handle) use ($curl)
                {
                    if ((is_resource($handle) === true) && (strcmp('curl', get_resource_type($handle)) === 0))
                    {
                        return (curl_multi_add_handle($curl, $handle) === CURLM_OK);
                    }

                    return false;
                });

                do
                {
                    do
                    {
                        $status = curl_multi_exec($curl, $active);
                    }
                    while ($status === CURLM_CALL_MULTI_PERFORM);

                    while (is_array($value = curl_multi_info_read($curl)) === true)
                    {
                        if (($key = array_search($handle = $value['handle'], $handles, true)) !== false)
                        {
                            $result[$key] = false;

                            if ($value['result'] === CURLE_OK)
                            {
                                if ((isset($callback) === true) && (is_callable($callback) === true))
                                {
                                    $result[$key] = call_user_func($callback, curl_multi_getcontent($handle), curl_getinfo($handle), $key);
                                }

                                else
                                {
                                    $result[$key] = curl_multi_getcontent($handle);
                                }
                            }

                            curl_multi_remove_handle($curl, $handle); curl_close($handle);
                        }
                    }

                    if (($active > 0) && ($status === CURLM_OK) && (curl_multi_select($curl, 1.0) === -1))
                    {
                        usleep(100);
                    }
                }
                while (($active > 0) && ($status === CURLM_OK));

                if ($status !== CURLM_OK)
                {
                    foreach ($handles as $handle)
                    {
                        curl_multi_remove_handle($curl, $handle); curl_close($handle);
                    }
                }

                curl_multi_close($curl);
            }

            return $result;
        }

        return false;
    }

    public static function Verse($html, $xpath = null, $key = null, $default = false)
    {
        if (is_string($html) === true)
        {
            $dom = new \DOMDocument();

            if (libxml_use_internal_errors(true) === true)
            {
                libxml_clear_errors();
            }

            if (@$dom->loadHTML(mb_convert_encoding($html, 'HTML-ENTITIES', 'UTF-8')) === true)
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
