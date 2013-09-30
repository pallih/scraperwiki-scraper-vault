<?php
function unhtmlentities($string)
{
    // replace numeric entities
    $string = preg_replace('~&#x([0-9a-f]+);~ei', 'chr(hexdec("\\1"))', $string);
    $string = preg_replace('~&#([0-9]+);~e', 'chr("\\1")', $string);
    // replace literal entities
    $trans_tbl = get_html_translation_table(HTML_ENTITIES);
    $trans_tbl = array_flip($trans_tbl);
    return strtr($string, $trans_tbl);
}


require  'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$domA = new simple_html_dom();
$dom->load(scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report"));
$authorities = array();
foreach ($dom->find("/select[@id=edit-localDrp]/option") as $key=>$option) {
    if ($key == 0) {
        continue;
    }
    $authorities[$option->value] = $option->innertext;
}

$offset = 17;
$authorities = array_slice($authorities, $offset, count($authorities)-$offset, true);
$url = "http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/any/17/any/any/any/any/any/any/any/any/?page=";
foreach ($authorities as $authorityID=>$authorityName) {
    $page = 0;
    while (true) {
        $dom->load(scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/any/17/$authorityID/any/any/any/any/any/any/any/?page=$page"));
//        var_dump(scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/all/all/authority/$authorityID/any/any?page=$page"));
//die();
        //var_dump("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/all/all/authority/$authorityID/any/any?page=$page", scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/all/all/authority/$authorityID/any/any?page=$page"));
        foreach ($dom->find("ul[@class=resultsList]/li") as $provider) {
            $p = $provider->find("/p");
            $span = $provider->find("/p/span");
            $a = $provider->find("/h2/a");

            if (substr($p[0]->innertext, 0, 5) == "URN: ") {
                $addr = new stdClass();
                $addr->innertext = "";
                $p = array_merge(array($addr), $p);
            }

            if (!isset($span[2]->innertext)) {
                $newSpan = array();
                $cursor = 0;
                if (isset($span[$cursor]) && substr(strip_tags($span[$cursor]->innertext), 0, 5) == "Local") {
                    $newSpan[] = $span[$cursor];
                    $cursor++;
                } else {
                    $report = new stdClass();
                    $report->innertext = "Local authority: ";
                    $newSpan[] = $report;
                }

                if (isset($span[$cursor]) && substr(strip_tags($span[$cursor]->innertext), 0, 6) == "Region") {
                    $newSpan[] = $span[$cursor];
                    $cursor++;
                } else {
                    $report = new stdClass();
                    $report->innertext = "Region: ";
                    $newSpan[] = $report;
                }

                if (isset($span[$cursor]) && substr(strip_tags($span[$cursor]->innertext), 0, 6) == "Latest") {
                    $newSpan[] = $span[$cursor];
                    $cursor++;
                } else {
                    $report = new stdClass();
                    $report->innertext = "Latest report: ";
                    $newSpan[] = $report;
                }
                $span = $newSpan;
            }
            
            if (substr(strip_tags($span[2]->innertext), 0, 6) != "Latest") {
                var_dump($provider->innertext);
                var_dump(strip_tags($span[0]->innertext), strip_tags($span[1]->innertext), strip_tags($span[2]->innertext));
                die();
            }
            $data = array(
                "name"=>unhtmlentities(strip_tags($a[0]->innertext)),
                "address"=>unhtmlentities($p[0]->innertext),
                "urn"=>substr($p[1]->innertext, 5),
                "Provider type"=>substr($p[2]->innertext, 15),
                "authority"=>substr(strip_tags($span[0]->innertext), 17),
                "region"=>substr(strip_tags($span[1]->innertext), 8),
                "latest_report"=>substr(strip_tags($span[2]->innertext), 15),
                "details_page"=>"http://www.ofsted.gov.uk".$a[0]->href);
            $domA->load(scraperwiki::scrape($data['details_page']));
            foreach ($domA->find("table[@summary=Previous reports]/tbody/tr/td/a") as $attachment) {
                $at = array("urn"=>$data['urn'], "name"=>trim(substr(strip_tags($attachment->innertext), 4)), "link"=>"http://www.ofsted.gov.uk".$attachment->href);
                scraperwiki::save_sqlite(array("urn", "link"), $at, "attachments");
            }
            scraperwiki::save_sqlite(array("urn"), $data, "provider");
        }
        $page++;
        $a = $dom->find("/ul[@class=pagination]/li/a");
        //var_dump($a[count($a)-1]->href);
        if ($a[count($a)-1]->href != "/inspection-reports/find-inspection-report/results/any/17/$authorityID/any/any/any/any/any/any/any/?page=$page") {
            echo "Next local authority\r\n";
            break;
        } else {
            echo "$authorityName ($authorityID): Page $page\r\n";
        }
    }
}
?>
<?php
function unhtmlentities($string)
{
    // replace numeric entities
    $string = preg_replace('~&#x([0-9a-f]+);~ei', 'chr(hexdec("\\1"))', $string);
    $string = preg_replace('~&#([0-9]+);~e', 'chr("\\1")', $string);
    // replace literal entities
    $trans_tbl = get_html_translation_table(HTML_ENTITIES);
    $trans_tbl = array_flip($trans_tbl);
    return strtr($string, $trans_tbl);
}


require  'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$domA = new simple_html_dom();
$dom->load(scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report"));
$authorities = array();
foreach ($dom->find("/select[@id=edit-localDrp]/option") as $key=>$option) {
    if ($key == 0) {
        continue;
    }
    $authorities[$option->value] = $option->innertext;
}

$offset = 17;
$authorities = array_slice($authorities, $offset, count($authorities)-$offset, true);
$url = "http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/any/17/any/any/any/any/any/any/any/any/?page=";
foreach ($authorities as $authorityID=>$authorityName) {
    $page = 0;
    while (true) {
        $dom->load(scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/any/17/$authorityID/any/any/any/any/any/any/any/?page=$page"));
//        var_dump(scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/all/all/authority/$authorityID/any/any?page=$page"));
//die();
        //var_dump("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/all/all/authority/$authorityID/any/any?page=$page", scraperwiki::scrape("http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/all/all/authority/$authorityID/any/any?page=$page"));
        foreach ($dom->find("ul[@class=resultsList]/li") as $provider) {
            $p = $provider->find("/p");
            $span = $provider->find("/p/span");
            $a = $provider->find("/h2/a");

            if (substr($p[0]->innertext, 0, 5) == "URN: ") {
                $addr = new stdClass();
                $addr->innertext = "";
                $p = array_merge(array($addr), $p);
            }

            if (!isset($span[2]->innertext)) {
                $newSpan = array();
                $cursor = 0;
                if (isset($span[$cursor]) && substr(strip_tags($span[$cursor]->innertext), 0, 5) == "Local") {
                    $newSpan[] = $span[$cursor];
                    $cursor++;
                } else {
                    $report = new stdClass();
                    $report->innertext = "Local authority: ";
                    $newSpan[] = $report;
                }

                if (isset($span[$cursor]) && substr(strip_tags($span[$cursor]->innertext), 0, 6) == "Region") {
                    $newSpan[] = $span[$cursor];
                    $cursor++;
                } else {
                    $report = new stdClass();
                    $report->innertext = "Region: ";
                    $newSpan[] = $report;
                }

                if (isset($span[$cursor]) && substr(strip_tags($span[$cursor]->innertext), 0, 6) == "Latest") {
                    $newSpan[] = $span[$cursor];
                    $cursor++;
                } else {
                    $report = new stdClass();
                    $report->innertext = "Latest report: ";
                    $newSpan[] = $report;
                }
                $span = $newSpan;
            }
            
            if (substr(strip_tags($span[2]->innertext), 0, 6) != "Latest") {
                var_dump($provider->innertext);
                var_dump(strip_tags($span[0]->innertext), strip_tags($span[1]->innertext), strip_tags($span[2]->innertext));
                die();
            }
            $data = array(
                "name"=>unhtmlentities(strip_tags($a[0]->innertext)),
                "address"=>unhtmlentities($p[0]->innertext),
                "urn"=>substr($p[1]->innertext, 5),
                "Provider type"=>substr($p[2]->innertext, 15),
                "authority"=>substr(strip_tags($span[0]->innertext), 17),
                "region"=>substr(strip_tags($span[1]->innertext), 8),
                "latest_report"=>substr(strip_tags($span[2]->innertext), 15),
                "details_page"=>"http://www.ofsted.gov.uk".$a[0]->href);
            $domA->load(scraperwiki::scrape($data['details_page']));
            foreach ($domA->find("table[@summary=Previous reports]/tbody/tr/td/a") as $attachment) {
                $at = array("urn"=>$data['urn'], "name"=>trim(substr(strip_tags($attachment->innertext), 4)), "link"=>"http://www.ofsted.gov.uk".$attachment->href);
                scraperwiki::save_sqlite(array("urn", "link"), $at, "attachments");
            }
            scraperwiki::save_sqlite(array("urn"), $data, "provider");
        }
        $page++;
        $a = $dom->find("/ul[@class=pagination]/li/a");
        //var_dump($a[count($a)-1]->href);
        if ($a[count($a)-1]->href != "/inspection-reports/find-inspection-report/results/any/17/$authorityID/any/any/any/any/any/any/any/?page=$page") {
            echo "Next local authority\r\n";
            break;
        } else {
            echo "$authorityName ($authorityID): Page $page\r\n";
        }
    }
}
?>
