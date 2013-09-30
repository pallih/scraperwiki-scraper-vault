<?php

namespace alixaxel;

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

namespace datamilk\PT;

class SICAE
{
    public static $cae = array
    (
        '01111', '01112', '01120', '01130', '01140', '01150', '01160', '01191', '01192', '01210', '01220', '01230', '01240', '01251', '01252', '01261', '01262',
        '01270', '01280', '01290', '01300', '01410', '01420', '01430', '01440', '01450', '01460', '01470', '01491', '01492', '01493', '01494', '01500', '01610',
        '01620', '01630', '01640', '01701', '01702', '02100', '02200', '02300', '02400', '03111', '03112', '03121', '03122', '03210', '03220', '05100', '05200',
        '06100', '06200', '07100', '07210', '07290', '08111', '08112', '08113', '08114', '08115', '08121', '08122', '08910', '08920', '08931', '08932', '08991',
        '08992', '09100', '09900', '10110', '10120', '10130', '10201', '10202', '10203', '10204', '10310', '10320', '10391', '10392', '10393', '10394', '10395',
        '10411', '10412', '10413', '10414', '10420', '10510', '10520', '10611', '10612', '10613', '10620', '10711', '10712', '10720', '10730', '10810', '10821',
        '10822', '10830', '10840', '10850', '10860', '10891', '10892', '10893', '10911', '10912', '10913', '10920', '11011', '11012', '11013', '11021', '11022',
        '11030', '11040', '11050', '11060', '11071', '11072', '12000', '13101', '13102', '13103', '13104', '13105', '13201', '13202', '13203', '13301', '13302',
        '13303', '13910', '13920', '13930', '13941', '13942', '13950', '13961', '13962', '13991', '13992', '13993', '14110', '14120', '14131', '14132', '14133',
        '14140', '14190', '14200', '14310', '14390', '15111', '15112', '15113', '15120', '15201', '15202', '16101', '16102', '16211', '16212', '16213', '16220',
        '16230', '16240', '16291', '16292', '16293', '16294', '16295', '17110', '17120', '17211', '17212', '17220', '17230', '17240', '17290', '18110', '18120',
        '18130', '18140', '18200', '19100', '19201', '19202', '19203', '20110', '20120', '20130', '20141', '20142', '20143', '20144', '20151', '20152', '20160',
        '20170', '20200', '20301', '20302', '20303', '20411', '20412', '20420', '20510', '20520', '20530', '20591', '20592', '20593', '20594', '20600', '21100',
        '21201', '21202', '22111', '22112', '22191', '22192', '22210', '22220', '22230', '22291', '22292', '23110', '23120', '23131', '23132', '23140', '23190',
        '23200', '23311', '23312', '23321', '23322', '23323', '23324', '23411', '23412', '23413', '23414', '23420', '23430', '23440', '23490', '23510', '23521',
        '23522', '23610', '23620', '23630', '23640', '23650', '23690', '23701', '23702', '23703', '23910', '23991', '23992', '24100', '24200', '24310', '24320',
        '24330', '24340', '24410', '24420', '24430', '24440', '24450', '24460', '24510', '24520', '24530', '24540', '25110', '25120', '25210', '25290', '25300',
        '25401', '25402', '25501', '25502', '25610', '25620', '25710', '25720', '25731', '25732', '25733', '25734', '25910', '25920', '25931', '25932', '25933',
        '25940', '25991', '25992', '26110', '26120', '26200', '26300', '26400', '26511', '26512', '26520', '26600', '26701', '26702', '26800', '27110', '27121',
        '27122', '27200', '27310', '27320', '27330', '27400', '27510', '27520', '27900', '28110', '28120', '28130', '28140', '28150', '28210', '28221', '28222',
        '28230', '28240', '28250', '28291', '28292', '28293', '28300', '28410', '28490', '28910', '28920', '28930', '28940', '28950', '28960', '28991', '28992',
        '29100', '29200', '29310', '29320', '30111', '30112', '30120', '30200', '30300', '30400', '30910', '30920', '30990', '31010', '31020', '31030', '31091',
        '31092', '31093', '31094', '32110', '32121', '32122', '32123', '32130', '32200', '32300', '32400', '32501', '32502', '32910', '32991', '32992', '32993',
        '32994', '32995', '32996', '33110', '33120', '33130', '33140', '33150', '33160', '33170', '33190', '33200', '35111', '35112', '35113', '35120', '35130',
        '35140', '35210', '35220', '35230', '35301', '35302', '36001', '36002', '37001', '37002', '38111', '38112', '38120', '38211', '38212', '38220', '38311',
        '38312', '38313', '38321', '38322', '39000', '41100', '41200', '42110', '42120', '42130', '42210', '42220', '42910', '42990', '43110', '43120', '43130',
        '43210', '43221', '43222', '43290', '43310', '43320', '43330', '43340', '43390', '43910', '43991', '43992', '45110', '45190', '45200', '45310', '45320',
        '45401', '45402', '46110', '46120', '46130', '46140', '46150', '46160', '46170', '46180', '46190', '46211', '46212', '46213', '46214', '46220', '46230',
        '46240', '46311', '46312', '46320', '46331', '46332', '46341', '46342', '46350', '46361', '46362', '46370', '46381', '46382', '46390', '46410', '46421',
        '46422', '46430', '46441', '46442', '46450', '46460', '46470', '46480', '46491', '46492', '46493', '46494', '46510', '46520', '46610', '46620', '46630',
        '46640', '46650', '46660', '46690', '46711', '46712', '46720', '46731', '46732', '46740', '46750', '46761', '46762', '46771', '46772', '46773', '46900',
        '47111', '47112', '47191', '47192', '47210', '47220', '47230', '47240', '47250', '47260', '47291', '47292', '47293', '47300', '47410', '47420', '47430',
        '47510', '47521', '47522', '47523', '47530', '47540', '47591', '47592', '47593', '47610', '47620', '47630', '47640', '47650', '47711', '47712', '47721',
        '47722', '47730', '47740', '47750', '47761', '47762', '47770', '47781', '47782', '47783', '47784', '47790', '47810', '47820', '47890', '47910', '47990',
        '49100', '49200', '49310', '49320', '49391', '49392', '49410', '49420', '49500', '50101', '50102', '50200', '50300', '50400', '51100', '51210', '51220',
        '52101', '52102', '52211', '52212', '52213', '52220', '52230', '52240', '52291', '52292', '53100', '53200', '55111', '55112', '55113', '55114', '55115',
        '55116', '55117', '55118', '55119', '55121', '55122', '55123', '55124', '55201', '55202', '55203', '55204', '55300', '55900', '56101', '56102', '56103',
        '56104', '56105', '56106', '56107', '56210', '56290', '56301', '56302', '56303', '56304', '56305', '58110', '58120', '58130', '58140', '58190', '58210',
        '58290', '59110', '59120', '59130', '59140', '59200', '60100', '60200', '61100', '61200', '61300', '61900', '62010', '62020', '62030', '62090', '63110',
        '63120', '63910', '63990', '64110', '64190', '64201', '64202', '64300', '64910', '64921', '64922', '64923', '64991', '64992', '65111', '65112', '65120',
        '65200', '65300', '66110', '66120', '66190', '66210', '66220', '66290', '66300', '68100', '68200', '68311', '68312', '68313', '68321', '68322', '69101',
        '69102', '69200', '70100', '70210', '70220', '71110', '71120', '71200', '72110', '72190', '72200', '73110', '73120', '73200', '74100', '74200', '74300',
        '74900', '75000', '77110', '77120', '77210', '77220', '77290', '77310', '77320', '77330', '77340', '77350', '77390', '77400', '78100', '78200', '78300',
        '79110', '79120', '79900', '80100', '80200', '80300', '81100', '81210', '81220', '81291', '81292', '81300', '82110', '82190', '82200', '82300', '82910',
        '82921', '82922', '82990', '84111', '84112', '84113', '84114', '84121', '84122', '84123', '84130', '84210', '84220', '84230', '84240', '84250', '84300',
        '85100', '85201', '85202', '85310', '85320', '85410', '85420', '85510', '85520', '85530', '85591', '85592', '85593', '85600', '86100', '86210', '86220',
        '86230', '86901', '86902', '86903', '86904', '86905', '86906', '87100', '87200', '87301', '87302', '87901', '87902', '88101', '88102', '88910', '88990',
        '90010', '90020', '90030', '90040', '91011', '91012', '91020', '91030', '91041', '91042', '92000', '93110', '93120', '93130', '93191', '93192', '93210',
        '93291', '93292', '93293', '93294', '94110', '94120', '94200', '94910', '94920', '94991', '94992', '94993', '94994', '94995', '95110', '95120', '95210',
        '95220', '95230', '95240', '95250', '95290', '96010', '96021', '96022', '96030', '96040', '96091', '96092', '96093', '97000', '98100', '98200', '99000',
    );

    private static function _()
    {
        static $result = array();

        if (empty($result) === true)
        {
            if (($html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx')) !== false)
            {
                foreach (\alixaxel\CURL::Verse($html, '//form[@action="Consulta.aspx"]//input[starts-with(@name,"__")]') as $input)
                {
                    $result[strval($input['name'])] = strval($input['value']);
                }
            }
        }

        return $result;
    }

    private static function _refine($name)
    {
        $name = str_replace(array('"', '\\', '¿'), array('', '', ' '), $name);

        if (strpos($name, '-') !== false)
        {
            $name = preg_replace(array('~(\S)-\s+~S', '~\s+-(\S)~S'), array('$1 - ', ' - $1'), $name);
        }

        if (strpbrk($name, '()') !== false)
        {
            $name = preg_replace('~[(]\s+(.+?)\s+[)]~S', '($1)', $name);
        }

        return trim(preg_replace(array('~\s*([,:;])\s*~S', '~\s+~S'), array('$1 ', ' '), $name));
    }

    public static function CAE($cae = null, $resume = true)
    {
        $result = array();

        if (is_null($cae) === true)
        {
            foreach (self::$cae as $cae)
            {
                $result = array_merge($result, self::CAE($cae, $resume));
            }
        }

        else if (in_array($cae, self::$cae) === true)
        {
            $data = array_merge(array
            (
                'ctl00$MainContent$ipCae' => $cae,
                'ctl00$MainContent$btnPesquisa' => 'Aguarde',
            ), self::_());

            $html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx', $data, 'POST');

            if (sscanf(trim(\alixaxel\CURL::Verse($html, '//span[@id="ctl00_MainContent_lblpagecount"]', 0)), 'Página 1 de %i', $pages) == 1)
            {
                if (class_exists('\\scraperwiki', false) === true)
                {
                    \scraperwiki::sw_dumpMessage(array
                    (
                        'message_type' => 'console',
                        'content' => sprintf('CAE %s has %u page(s) (~%u records).', $cae, $pages, $pages * 10),
                    ));

                    $total = \scraperwiki::sqliteexecute('SELECT COUNT("caePrimary") FROM "swdata" WHERE "caePrimary" = ? LIMIT 1;', array($cae));

                    if ((($total = intval($total->data[0][0])) > 0) && ($resume === true))
                    {
                        $pages = max(1, min($pages, $pages - floor($total / 10) + 0));
                    }

                    \scraperwiki::sw_dumpMessage(array
                    (
                        'message_type' => 'console',
                        'content' => sprintf('Scraping %u page(s) of CAE %s (%u records in datastore).', $pages, $cae, $total),
                    ));
                }

                for ($i = 1; $i <= $pages; ++$i)
                {
                    if ($i > 1)
                    {
                        foreach (\alixaxel\CURL::Verse($html, '//form[@action="Consulta.aspx"]//input[starts-with(@name,"__")]') as $input)
                        {
                            $data[strval($input['name'])] = strval($input['value']);
                        }

                        if (array_key_exists('ctl00$MainContent$btnPesquisa', $data) === true)
                        {
                            $data['ctl00$MainContent$btnNext'] = 'Próximo'; unset($data['ctl00$MainContent$btnPesquisa']);
                        }

                        $html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx', $data, 'POST');
                    }

                    $companies = \alixaxel\CURL::Verse($html, '//table[@id="ctl00_MainContent_ConsultaDataGrid"]/tr');

                    if ((is_array($companies) === true) && (count($companies) > 1))
                    {
                        foreach (array_slice($companies, 1) as $company)
                        {
                            if (preg_match('~^[125689][0-9]{8}$~', $id = trim($company->td[0])) > 0)
                            {
                                $result[] = array
                                (
                                    'id' => $id,
                                    'name' => self::_refine($company->td[1]),
                                    'caePrimary' => trim($company->td[2]->div),
                                    'caeSecondary' => trim(implode('|', array_map('trim', iterator_to_array($company->td[3]->div, false))), '|'),
                                    'dateCreated' => new \DateTime('now', new \DateTimeZone('UTC')),
                                );

                                if (class_exists('\\scraperwiki', false) === true)
                                {
                                    \scraperwiki::sw_dumpMessage(array
                                    (
                                        'message_type' => 'data',
                                        'content' => array
                                        (
                                            'ID' => $id,
                                            'CAE' => trim($company->td[2]->div),
                                        ),
                                    ));
                                }
                            }
                        }

                        if ((class_exists('\\scraperwiki', false) === true) && (count($result) >= 100))
                        {
                            $done = \scraperwiki::sqliteexecute('SELECT COUNT("id") FROM "swdata" WHERE "id" = ? LIMIT 1;', array($id));

                            \scraperwiki::save_sqlite(array('id'), $result, 'swdata', 0); $result = array();

                            if ((($done = intval($done->data[0][0])) > 0) && ($resume === true))
                            {
                                \scraperwiki::sw_dumpMessage(array
                                (
                                    'message_type' => 'console',
                                    'content' => sprintf('Done %u page(s) of CAE %s.', $pages, $cae),
                                ));

                                break;
                            }
                        }
                    }
                }

                if ((class_exists('\\scraperwiki', false) === true) && (count($result) > 0))
                {
                    \scraperwiki::save_sqlite(array('id'), $result, 'swdata', 0); $result = array();
                }
            }
        }

        else
        {
            return false;
        }

        return $result;
    }

    public static function NIPC($nipc)
    {
        $result = array();

        if (preg_match('~^[125689][0-9]{8}$~', $nipc) > 0)
        {
            $data = array_merge(array
            (
                'ctl00$MainContent$ipNipc' => $nipc,
                'ctl00$MainContent$btnPesquisa' => 'Aguarde',
            ), self::_());

            $html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx', $data, 'POST');
            $companies = \alixaxel\CURL::Verse($html, '//table[@id="ctl00_MainContent_ConsultaDataGrid"]/tr');

            if ((is_array($companies) === true) && (count($companies) == 2))
            {
                foreach (array_slice($companies, 1) as $company)
                {
                    if (preg_match('~^[125689][0-9]{8}$~', $id = trim($company->td[0])) > 0)
                    {
                        $result = array
                        (
                            'id' => $id,
                            'name' => self::_refine($company->td[1]),
                            'caePrimary' => trim($company->td[2]->div),
                            'caeSecondary' => trim(implode('|', array_map('trim', iterator_to_array($company->td[3]->div, false))), '|'),
                        );
                    }
                }
            }
        }

        else
        {
            return false;
        }

        return $result;
    }
}

if (class_exists('\\scraperwiki', false) === true)
{
    $queries = array
    (
        'PRAGMA busy_timeout=8;',
        'PRAGMA cache_size=8192;',
        #'PRAGMA locking_mode=EXCLUSIVE;',
        #'PRAGMA locking_mode=NORMAL;',
    );
    
    if (count(\scraperwiki::show_tables()) == 0)
    {
        $queries = array_merge($queries, array
        (
            'CREATE TABLE IF NOT EXISTS "swdata" ("id" integer(9), "name" text, "caePrimary" text(5), "caeSecondary" text(17), "dateCreated" text(24));',
            'CREATE UNIQUE INDEX IF NOT EXISTS "swdata_id" ON "swdata" ("id");',
            'CREATE INDEX IF NOT EXISTS "swdata_caePrimary" ON "swdata" ("caePrimary");',
            'CREATE INDEX IF NOT EXISTS "swdata_dateCreated" ON "swdata" ("dateCreated");',
        ));
    }

    else
    {
        #$queries[] = 'VACUUM;';
    }

    foreach ($queries as $query)
    {
        \scraperwiki::sqliteexecute($query);
    }

    \datamilk\PT\SICAE::CAE(null, true);
    \scraperwiki::sqliteexecute('PRAGMA locking_mode=NORMAL;');
}
<?php

namespace alixaxel;

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

namespace datamilk\PT;

class SICAE
{
    public static $cae = array
    (
        '01111', '01112', '01120', '01130', '01140', '01150', '01160', '01191', '01192', '01210', '01220', '01230', '01240', '01251', '01252', '01261', '01262',
        '01270', '01280', '01290', '01300', '01410', '01420', '01430', '01440', '01450', '01460', '01470', '01491', '01492', '01493', '01494', '01500', '01610',
        '01620', '01630', '01640', '01701', '01702', '02100', '02200', '02300', '02400', '03111', '03112', '03121', '03122', '03210', '03220', '05100', '05200',
        '06100', '06200', '07100', '07210', '07290', '08111', '08112', '08113', '08114', '08115', '08121', '08122', '08910', '08920', '08931', '08932', '08991',
        '08992', '09100', '09900', '10110', '10120', '10130', '10201', '10202', '10203', '10204', '10310', '10320', '10391', '10392', '10393', '10394', '10395',
        '10411', '10412', '10413', '10414', '10420', '10510', '10520', '10611', '10612', '10613', '10620', '10711', '10712', '10720', '10730', '10810', '10821',
        '10822', '10830', '10840', '10850', '10860', '10891', '10892', '10893', '10911', '10912', '10913', '10920', '11011', '11012', '11013', '11021', '11022',
        '11030', '11040', '11050', '11060', '11071', '11072', '12000', '13101', '13102', '13103', '13104', '13105', '13201', '13202', '13203', '13301', '13302',
        '13303', '13910', '13920', '13930', '13941', '13942', '13950', '13961', '13962', '13991', '13992', '13993', '14110', '14120', '14131', '14132', '14133',
        '14140', '14190', '14200', '14310', '14390', '15111', '15112', '15113', '15120', '15201', '15202', '16101', '16102', '16211', '16212', '16213', '16220',
        '16230', '16240', '16291', '16292', '16293', '16294', '16295', '17110', '17120', '17211', '17212', '17220', '17230', '17240', '17290', '18110', '18120',
        '18130', '18140', '18200', '19100', '19201', '19202', '19203', '20110', '20120', '20130', '20141', '20142', '20143', '20144', '20151', '20152', '20160',
        '20170', '20200', '20301', '20302', '20303', '20411', '20412', '20420', '20510', '20520', '20530', '20591', '20592', '20593', '20594', '20600', '21100',
        '21201', '21202', '22111', '22112', '22191', '22192', '22210', '22220', '22230', '22291', '22292', '23110', '23120', '23131', '23132', '23140', '23190',
        '23200', '23311', '23312', '23321', '23322', '23323', '23324', '23411', '23412', '23413', '23414', '23420', '23430', '23440', '23490', '23510', '23521',
        '23522', '23610', '23620', '23630', '23640', '23650', '23690', '23701', '23702', '23703', '23910', '23991', '23992', '24100', '24200', '24310', '24320',
        '24330', '24340', '24410', '24420', '24430', '24440', '24450', '24460', '24510', '24520', '24530', '24540', '25110', '25120', '25210', '25290', '25300',
        '25401', '25402', '25501', '25502', '25610', '25620', '25710', '25720', '25731', '25732', '25733', '25734', '25910', '25920', '25931', '25932', '25933',
        '25940', '25991', '25992', '26110', '26120', '26200', '26300', '26400', '26511', '26512', '26520', '26600', '26701', '26702', '26800', '27110', '27121',
        '27122', '27200', '27310', '27320', '27330', '27400', '27510', '27520', '27900', '28110', '28120', '28130', '28140', '28150', '28210', '28221', '28222',
        '28230', '28240', '28250', '28291', '28292', '28293', '28300', '28410', '28490', '28910', '28920', '28930', '28940', '28950', '28960', '28991', '28992',
        '29100', '29200', '29310', '29320', '30111', '30112', '30120', '30200', '30300', '30400', '30910', '30920', '30990', '31010', '31020', '31030', '31091',
        '31092', '31093', '31094', '32110', '32121', '32122', '32123', '32130', '32200', '32300', '32400', '32501', '32502', '32910', '32991', '32992', '32993',
        '32994', '32995', '32996', '33110', '33120', '33130', '33140', '33150', '33160', '33170', '33190', '33200', '35111', '35112', '35113', '35120', '35130',
        '35140', '35210', '35220', '35230', '35301', '35302', '36001', '36002', '37001', '37002', '38111', '38112', '38120', '38211', '38212', '38220', '38311',
        '38312', '38313', '38321', '38322', '39000', '41100', '41200', '42110', '42120', '42130', '42210', '42220', '42910', '42990', '43110', '43120', '43130',
        '43210', '43221', '43222', '43290', '43310', '43320', '43330', '43340', '43390', '43910', '43991', '43992', '45110', '45190', '45200', '45310', '45320',
        '45401', '45402', '46110', '46120', '46130', '46140', '46150', '46160', '46170', '46180', '46190', '46211', '46212', '46213', '46214', '46220', '46230',
        '46240', '46311', '46312', '46320', '46331', '46332', '46341', '46342', '46350', '46361', '46362', '46370', '46381', '46382', '46390', '46410', '46421',
        '46422', '46430', '46441', '46442', '46450', '46460', '46470', '46480', '46491', '46492', '46493', '46494', '46510', '46520', '46610', '46620', '46630',
        '46640', '46650', '46660', '46690', '46711', '46712', '46720', '46731', '46732', '46740', '46750', '46761', '46762', '46771', '46772', '46773', '46900',
        '47111', '47112', '47191', '47192', '47210', '47220', '47230', '47240', '47250', '47260', '47291', '47292', '47293', '47300', '47410', '47420', '47430',
        '47510', '47521', '47522', '47523', '47530', '47540', '47591', '47592', '47593', '47610', '47620', '47630', '47640', '47650', '47711', '47712', '47721',
        '47722', '47730', '47740', '47750', '47761', '47762', '47770', '47781', '47782', '47783', '47784', '47790', '47810', '47820', '47890', '47910', '47990',
        '49100', '49200', '49310', '49320', '49391', '49392', '49410', '49420', '49500', '50101', '50102', '50200', '50300', '50400', '51100', '51210', '51220',
        '52101', '52102', '52211', '52212', '52213', '52220', '52230', '52240', '52291', '52292', '53100', '53200', '55111', '55112', '55113', '55114', '55115',
        '55116', '55117', '55118', '55119', '55121', '55122', '55123', '55124', '55201', '55202', '55203', '55204', '55300', '55900', '56101', '56102', '56103',
        '56104', '56105', '56106', '56107', '56210', '56290', '56301', '56302', '56303', '56304', '56305', '58110', '58120', '58130', '58140', '58190', '58210',
        '58290', '59110', '59120', '59130', '59140', '59200', '60100', '60200', '61100', '61200', '61300', '61900', '62010', '62020', '62030', '62090', '63110',
        '63120', '63910', '63990', '64110', '64190', '64201', '64202', '64300', '64910', '64921', '64922', '64923', '64991', '64992', '65111', '65112', '65120',
        '65200', '65300', '66110', '66120', '66190', '66210', '66220', '66290', '66300', '68100', '68200', '68311', '68312', '68313', '68321', '68322', '69101',
        '69102', '69200', '70100', '70210', '70220', '71110', '71120', '71200', '72110', '72190', '72200', '73110', '73120', '73200', '74100', '74200', '74300',
        '74900', '75000', '77110', '77120', '77210', '77220', '77290', '77310', '77320', '77330', '77340', '77350', '77390', '77400', '78100', '78200', '78300',
        '79110', '79120', '79900', '80100', '80200', '80300', '81100', '81210', '81220', '81291', '81292', '81300', '82110', '82190', '82200', '82300', '82910',
        '82921', '82922', '82990', '84111', '84112', '84113', '84114', '84121', '84122', '84123', '84130', '84210', '84220', '84230', '84240', '84250', '84300',
        '85100', '85201', '85202', '85310', '85320', '85410', '85420', '85510', '85520', '85530', '85591', '85592', '85593', '85600', '86100', '86210', '86220',
        '86230', '86901', '86902', '86903', '86904', '86905', '86906', '87100', '87200', '87301', '87302', '87901', '87902', '88101', '88102', '88910', '88990',
        '90010', '90020', '90030', '90040', '91011', '91012', '91020', '91030', '91041', '91042', '92000', '93110', '93120', '93130', '93191', '93192', '93210',
        '93291', '93292', '93293', '93294', '94110', '94120', '94200', '94910', '94920', '94991', '94992', '94993', '94994', '94995', '95110', '95120', '95210',
        '95220', '95230', '95240', '95250', '95290', '96010', '96021', '96022', '96030', '96040', '96091', '96092', '96093', '97000', '98100', '98200', '99000',
    );

    private static function _()
    {
        static $result = array();

        if (empty($result) === true)
        {
            if (($html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx')) !== false)
            {
                foreach (\alixaxel\CURL::Verse($html, '//form[@action="Consulta.aspx"]//input[starts-with(@name,"__")]') as $input)
                {
                    $result[strval($input['name'])] = strval($input['value']);
                }
            }
        }

        return $result;
    }

    private static function _refine($name)
    {
        $name = str_replace(array('"', '\\', '¿'), array('', '', ' '), $name);

        if (strpos($name, '-') !== false)
        {
            $name = preg_replace(array('~(\S)-\s+~S', '~\s+-(\S)~S'), array('$1 - ', ' - $1'), $name);
        }

        if (strpbrk($name, '()') !== false)
        {
            $name = preg_replace('~[(]\s+(.+?)\s+[)]~S', '($1)', $name);
        }

        return trim(preg_replace(array('~\s*([,:;])\s*~S', '~\s+~S'), array('$1 ', ' '), $name));
    }

    public static function CAE($cae = null, $resume = true)
    {
        $result = array();

        if (is_null($cae) === true)
        {
            foreach (self::$cae as $cae)
            {
                $result = array_merge($result, self::CAE($cae, $resume));
            }
        }

        else if (in_array($cae, self::$cae) === true)
        {
            $data = array_merge(array
            (
                'ctl00$MainContent$ipCae' => $cae,
                'ctl00$MainContent$btnPesquisa' => 'Aguarde',
            ), self::_());

            $html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx', $data, 'POST');

            if (sscanf(trim(\alixaxel\CURL::Verse($html, '//span[@id="ctl00_MainContent_lblpagecount"]', 0)), 'Página 1 de %i', $pages) == 1)
            {
                if (class_exists('\\scraperwiki', false) === true)
                {
                    \scraperwiki::sw_dumpMessage(array
                    (
                        'message_type' => 'console',
                        'content' => sprintf('CAE %s has %u page(s) (~%u records).', $cae, $pages, $pages * 10),
                    ));

                    $total = \scraperwiki::sqliteexecute('SELECT COUNT("caePrimary") FROM "swdata" WHERE "caePrimary" = ? LIMIT 1;', array($cae));

                    if ((($total = intval($total->data[0][0])) > 0) && ($resume === true))
                    {
                        $pages = max(1, min($pages, $pages - floor($total / 10) + 0));
                    }

                    \scraperwiki::sw_dumpMessage(array
                    (
                        'message_type' => 'console',
                        'content' => sprintf('Scraping %u page(s) of CAE %s (%u records in datastore).', $pages, $cae, $total),
                    ));
                }

                for ($i = 1; $i <= $pages; ++$i)
                {
                    if ($i > 1)
                    {
                        foreach (\alixaxel\CURL::Verse($html, '//form[@action="Consulta.aspx"]//input[starts-with(@name,"__")]') as $input)
                        {
                            $data[strval($input['name'])] = strval($input['value']);
                        }

                        if (array_key_exists('ctl00$MainContent$btnPesquisa', $data) === true)
                        {
                            $data['ctl00$MainContent$btnNext'] = 'Próximo'; unset($data['ctl00$MainContent$btnPesquisa']);
                        }

                        $html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx', $data, 'POST');
                    }

                    $companies = \alixaxel\CURL::Verse($html, '//table[@id="ctl00_MainContent_ConsultaDataGrid"]/tr');

                    if ((is_array($companies) === true) && (count($companies) > 1))
                    {
                        foreach (array_slice($companies, 1) as $company)
                        {
                            if (preg_match('~^[125689][0-9]{8}$~', $id = trim($company->td[0])) > 0)
                            {
                                $result[] = array
                                (
                                    'id' => $id,
                                    'name' => self::_refine($company->td[1]),
                                    'caePrimary' => trim($company->td[2]->div),
                                    'caeSecondary' => trim(implode('|', array_map('trim', iterator_to_array($company->td[3]->div, false))), '|'),
                                    'dateCreated' => new \DateTime('now', new \DateTimeZone('UTC')),
                                );

                                if (class_exists('\\scraperwiki', false) === true)
                                {
                                    \scraperwiki::sw_dumpMessage(array
                                    (
                                        'message_type' => 'data',
                                        'content' => array
                                        (
                                            'ID' => $id,
                                            'CAE' => trim($company->td[2]->div),
                                        ),
                                    ));
                                }
                            }
                        }

                        if ((class_exists('\\scraperwiki', false) === true) && (count($result) >= 100))
                        {
                            $done = \scraperwiki::sqliteexecute('SELECT COUNT("id") FROM "swdata" WHERE "id" = ? LIMIT 1;', array($id));

                            \scraperwiki::save_sqlite(array('id'), $result, 'swdata', 0); $result = array();

                            if ((($done = intval($done->data[0][0])) > 0) && ($resume === true))
                            {
                                \scraperwiki::sw_dumpMessage(array
                                (
                                    'message_type' => 'console',
                                    'content' => sprintf('Done %u page(s) of CAE %s.', $pages, $cae),
                                ));

                                break;
                            }
                        }
                    }
                }

                if ((class_exists('\\scraperwiki', false) === true) && (count($result) > 0))
                {
                    \scraperwiki::save_sqlite(array('id'), $result, 'swdata', 0); $result = array();
                }
            }
        }

        else
        {
            return false;
        }

        return $result;
    }

    public static function NIPC($nipc)
    {
        $result = array();

        if (preg_match('~^[125689][0-9]{8}$~', $nipc) > 0)
        {
            $data = array_merge(array
            (
                'ctl00$MainContent$ipNipc' => $nipc,
                'ctl00$MainContent$btnPesquisa' => 'Aguarde',
            ), self::_());

            $html = \alixaxel\CURL::Uni('http://www.sicae.pt/Consulta.aspx', $data, 'POST');
            $companies = \alixaxel\CURL::Verse($html, '//table[@id="ctl00_MainContent_ConsultaDataGrid"]/tr');

            if ((is_array($companies) === true) && (count($companies) == 2))
            {
                foreach (array_slice($companies, 1) as $company)
                {
                    if (preg_match('~^[125689][0-9]{8}$~', $id = trim($company->td[0])) > 0)
                    {
                        $result = array
                        (
                            'id' => $id,
                            'name' => self::_refine($company->td[1]),
                            'caePrimary' => trim($company->td[2]->div),
                            'caeSecondary' => trim(implode('|', array_map('trim', iterator_to_array($company->td[3]->div, false))), '|'),
                        );
                    }
                }
            }
        }

        else
        {
            return false;
        }

        return $result;
    }
}

if (class_exists('\\scraperwiki', false) === true)
{
    $queries = array
    (
        'PRAGMA busy_timeout=8;',
        'PRAGMA cache_size=8192;',
        #'PRAGMA locking_mode=EXCLUSIVE;',
        #'PRAGMA locking_mode=NORMAL;',
    );
    
    if (count(\scraperwiki::show_tables()) == 0)
    {
        $queries = array_merge($queries, array
        (
            'CREATE TABLE IF NOT EXISTS "swdata" ("id" integer(9), "name" text, "caePrimary" text(5), "caeSecondary" text(17), "dateCreated" text(24));',
            'CREATE UNIQUE INDEX IF NOT EXISTS "swdata_id" ON "swdata" ("id");',
            'CREATE INDEX IF NOT EXISTS "swdata_caePrimary" ON "swdata" ("caePrimary");',
            'CREATE INDEX IF NOT EXISTS "swdata_dateCreated" ON "swdata" ("dateCreated");',
        ));
    }

    else
    {
        #$queries[] = 'VACUUM;';
    }

    foreach ($queries as $query)
    {
        \scraperwiki::sqliteexecute($query);
    }

    \datamilk\PT\SICAE::CAE(null, true);
    \scraperwiki::sqliteexecute('PRAGMA locking_mode=NORMAL;');
}
