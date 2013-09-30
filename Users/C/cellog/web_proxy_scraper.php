<?php

require 'scraperwiki/simple_html_dom.php';
function getIp($text)
{
    return gethostbyname(str_replace('/','',preg_replace('@https?://@', '', preg_replace('/:\\d+/', '', $text))));
}

function grab($url) {
    $html = scraperWiki::scrape($url);           
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".proxy_list tr td.proxy a") as $data){
        $name = $data->plaintext;
        $ip = getIp($name);
        $record = array(
            'ip' => $ip,
            'name' => $name
        );
        scraperwiki::save(array('ip'), $record); 
    }
}

function grab2($url) {
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("li a") as $data) {
        $name = $data->plaintext;
        $ip = getIp($name);
        $record = array(
            'ip' => $ip,
            'name' => $name
        );
        scraperwiki::save(array('ip'), $record); 
    }
}

function grab3($url) {
    $txt = scraperWiki::scrape($url);
    $txt = preg_replace('/:\d+/', '', $txt);
    $txt = explode("\n", $txt);
    foreach ($txt as $ip) {
        scraperWiki::save(array('ip'), array('ip' => $ip, 'name' => $ip));
    }
}

function grab4($url) {
    $html = scraperWiki::scrape($url);           
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div.proxy a") as $data){
        $name = $data->plaintext;
        $ip = getIp($name);
        $record = array(
            'ip' => $ip,
            'name' => $name
        );
        scraperwiki::save(array('ip'), $record); 
    }
}

function grab5($url)
{
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("a[@rel='nofollow']") as $data) {
        $name = $data->plaintext;
        $ip = getIp($name);
        if (!preg_match('/\d+\.\d+\.\d+\.\d+/', $ip)) continue;
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab6($url)
{
    $html = scraperWiki::scrape($url);
    preg_match_all("/\d+\.\d+\.\d+\.\d+/", $html, $ips);
    foreach ($ips[0] as $ip) {
        $record = array(
            'ip' => $ip,
            'name' => $url
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab7($url)
{
    $html = scraperWiki::scrape($url);
    preg_match_all("/\">([^<']+)'\);/", $html, $names);
    foreach ($names[1] as $name) {
        $record = array(
            'ip' => getIp($name),
            'name' => $name
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab8($url)
{
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("td.pthtdd a") as $data) {
        $name = $data->plaintext;
        $ip = getIp($name);
        if (!preg_match('/\d+\.\d+\.\d+\.\d+/', $ip)) continue;
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab9($url)
{
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("#proxylist tr td") as $data) {
        $ip = $data->plaintext;
        if (!preg_match('/\d+\.\d+\.\d+\.\d+/', $ip)) continue;
        $record = array(
            'ip' => $ip,
            'name' => 'nntime.com proxy',
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab10($url, $name)
{
    $html = scraperWiki::scrape($url);
    preg_match_all('/(\d+\.\d+\.\d+\.\d+):\d+/', $html, $ips);
    foreach ($ips[1] as $ip) {
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab11($url)
{
    $csv = explode("\n", scraperWiki::scrape($url));
    array_shift($csv);
    foreach ($csv as $line) {
        $data = explode(",", $line);
        $record = array(
            'ip' => $data[1],
            'name' => $data[0]
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab12($url, $name)
{
    $html = scraperWiki::scrape($url);
    $html = preg_replace('/<span style="display:none">(\d+)<\/span>/', '', $html);
    $html = preg_replace('/<span class="\d+">(\d+)<\/span>/', '\1', $html);
    preg_match_all('/\d+\.\d+\.\d+\.\d+/', $html, $ips);
    foreach ($ips[0] as $ip) {
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function getSubLists()
{
    $html = scraperWiki::scrape("http://proxylistfree.jimdo.com/");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("a[@target='_blank']") as $data) {
        grab5($data->href);
    }
}

function getRuList()
{
    $html = scraperWiki::scrape("http://spys.ru/en/proxy-by-country/");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("tr.spy1x td.menu1 a") as $data) {
        $subhtml = scraperWiki::scrape("http://spys.ru" . $data->href);
        preg_match_all("@" . str_replace('t/','t\d+/', $data->href) . "@", $subhtml, $pages);
        grab6("http://spys.ru" . $data->href);
        foreach (array_unique($pages[0]) as $page) {
            grab6("http://spys.ru" . $page);
        }
    }
    foreach ($dom->find("tr.spy1x td.menu2 a") as $data) {
        $subhtml = scraperWiki::scrape($data->href);
        preg_match_all("@" . str_replace('t/','t\d+/', $data->href) . "@", $subhtml, $pages);
        grab6("http://spys.ru" . $data->href);
        foreach (array_unique($pages[0]) as $page) {
            grab6("http://spys.ru" . $page);
        }
    }
}

//grab10("http://www.ip-adress.com/proxy_list/", "ip-address.com proxy");

for ($i = 1; $i <= 15; $i++) {
    grab12("http://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc/page:$i", "cool-proxy.net proxy");
}

grab11("http://proxylists.me/api.php?cmd=downloadOpenProxies&responseType=text");

for ($i = 1; $i <= 15; $i++) {
    $t = $i;
    if ($t < 10) $t = "0$t";
    grab10("http://www.samair.ru/proxy/ip-address-$t.htm", "samair.ru proxy");
}

grab4("http://proxylist4all.com/category.php?id=51");
grab4("http://proxylist4all.com/category.php?id=53");
grab4("http://proxylist4all.com/category.php?id=57");
for ($i = 0;$i < 3*50;$i+=50) {
    grab4("http://proxylist4all.com/category.php?id=58?start=$i");
}


grab10("http://best-proxy-list-ips.blogspot.com/", 'best-proxy-list-ips proxy');

for ($i = 0;$i < 13*30;$i+=30) {
    grab4("http://www.ufor.org/new-proxies.php?start=$i");
}

for ($i = 0;$i < 96*25;$i+=25) {
    grab4("http://www.atproxy.net/category.php?id=44&start=$i");
}
grab4("http://www.atproxy.net/category.php?id=45");
grab4("http://www.atproxy.net/category.php?id=46");
grab4("http://www.atproxy.net/category.php?id=47");
grab4("http://www.atproxy.net/category.php?id=48");
grab4("http://www.atproxy.net/category.php?id=49");
grab4("http://www.atproxy.net/category.php?id=50");
for ($i = 0;$i < 39*25;$i+=25) {
    grab4("http://www.atproxy.net/category.php?id=51&start=$i");
}

for ($i = 1; $i <= 12; $i++) {
    if ($i < 10) {
        $name = "0$i";
    } else {
        $name = $i;
    }
    grab9("http://nntime.com/proxy-list-$name.htm");
}

getRuList();

for ($i = 1; $i <= 15; $i++) {
    grab8("http://www.publicproxyservers.com/proxy/list$i.html");
}

grab7("http://www.kamranweb.com/proxy/proxylist.js");

grab5("http://goldproxylist.com/");

grab6("http://anonymizer.nntime.com/js/country.js");

grab5("http://proxybay.info/");

getSubLists();

for ($i = 0;$i < 21*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=44&start=$i");
}
for ($i = 0;$i < 12*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=45&start=$i");
}
for ($i = 0;$i < 2*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=46&start=$i");
}
for ($i = 0;$i < 4*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=47&start=$i");
}
grab4("http://www.allproxysites.com/category.php?id=48");
for ($i = 0;$i < 3*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=49&start=$i");
}
for ($i = 0;$i < 6*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=50&start=$i");
}
for ($i = 0;$i < 53*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=51&start=$i");
}

grab3("http://multiproxy.org/txt_anon/proxy.txt");

grab2("http://www.cybersyndrome.net/pla5.html");

for ($i = 0;$i < 12*25;$i+=25) {
    grab("http://www.megaproxylist.com/?start=$i");
}

for ($i = 0;$i < 97*15;$i+=15) {
    grab("http://www.workingproxies.info/proxies.shtml?start=$i");
}

for ($i = 0;$i < 4*50;$i+=50) {
    grab("http://proxyliberty.com/recent-proxies.php?start=$i");
}

for ($i = 0;$i < 4*50;$i+=50) {
    grab("http://proxyliberty.com/top-proxies.php?start=$i");
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';
function getIp($text)
{
    return gethostbyname(str_replace('/','',preg_replace('@https?://@', '', preg_replace('/:\\d+/', '', $text))));
}

function grab($url) {
    $html = scraperWiki::scrape($url);           
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find(".proxy_list tr td.proxy a") as $data){
        $name = $data->plaintext;
        $ip = getIp($name);
        $record = array(
            'ip' => $ip,
            'name' => $name
        );
        scraperwiki::save(array('ip'), $record); 
    }
}

function grab2($url) {
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("li a") as $data) {
        $name = $data->plaintext;
        $ip = getIp($name);
        $record = array(
            'ip' => $ip,
            'name' => $name
        );
        scraperwiki::save(array('ip'), $record); 
    }
}

function grab3($url) {
    $txt = scraperWiki::scrape($url);
    $txt = preg_replace('/:\d+/', '', $txt);
    $txt = explode("\n", $txt);
    foreach ($txt as $ip) {
        scraperWiki::save(array('ip'), array('ip' => $ip, 'name' => $ip));
    }
}

function grab4($url) {
    $html = scraperWiki::scrape($url);           
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach($dom->find("div.proxy a") as $data){
        $name = $data->plaintext;
        $ip = getIp($name);
        $record = array(
            'ip' => $ip,
            'name' => $name
        );
        scraperwiki::save(array('ip'), $record); 
    }
}

function grab5($url)
{
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("a[@rel='nofollow']") as $data) {
        $name = $data->plaintext;
        $ip = getIp($name);
        if (!preg_match('/\d+\.\d+\.\d+\.\d+/', $ip)) continue;
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab6($url)
{
    $html = scraperWiki::scrape($url);
    preg_match_all("/\d+\.\d+\.\d+\.\d+/", $html, $ips);
    foreach ($ips[0] as $ip) {
        $record = array(
            'ip' => $ip,
            'name' => $url
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab7($url)
{
    $html = scraperWiki::scrape($url);
    preg_match_all("/\">([^<']+)'\);/", $html, $names);
    foreach ($names[1] as $name) {
        $record = array(
            'ip' => getIp($name),
            'name' => $name
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab8($url)
{
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("td.pthtdd a") as $data) {
        $name = $data->plaintext;
        $ip = getIp($name);
        if (!preg_match('/\d+\.\d+\.\d+\.\d+/', $ip)) continue;
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab9($url)
{
    $html = scraperWiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("#proxylist tr td") as $data) {
        $ip = $data->plaintext;
        if (!preg_match('/\d+\.\d+\.\d+\.\d+/', $ip)) continue;
        $record = array(
            'ip' => $ip,
            'name' => 'nntime.com proxy',
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab10($url, $name)
{
    $html = scraperWiki::scrape($url);
    preg_match_all('/(\d+\.\d+\.\d+\.\d+):\d+/', $html, $ips);
    foreach ($ips[1] as $ip) {
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab11($url)
{
    $csv = explode("\n", scraperWiki::scrape($url));
    array_shift($csv);
    foreach ($csv as $line) {
        $data = explode(",", $line);
        $record = array(
            'ip' => $data[1],
            'name' => $data[0]
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function grab12($url, $name)
{
    $html = scraperWiki::scrape($url);
    $html = preg_replace('/<span style="display:none">(\d+)<\/span>/', '', $html);
    $html = preg_replace('/<span class="\d+">(\d+)<\/span>/', '\1', $html);
    preg_match_all('/\d+\.\d+\.\d+\.\d+/', $html, $ips);
    foreach ($ips[0] as $ip) {
        $record = array(
            'ip' => $ip,
            'name' => $name,
        );
        scraperWiki::save(array('ip'), $record);
    }
}

function getSubLists()
{
    $html = scraperWiki::scrape("http://proxylistfree.jimdo.com/");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("a[@target='_blank']") as $data) {
        grab5($data->href);
    }
}

function getRuList()
{
    $html = scraperWiki::scrape("http://spys.ru/en/proxy-by-country/");
    $dom = new simple_html_dom();
    $dom->load($html);
    foreach ($dom->find("tr.spy1x td.menu1 a") as $data) {
        $subhtml = scraperWiki::scrape("http://spys.ru" . $data->href);
        preg_match_all("@" . str_replace('t/','t\d+/', $data->href) . "@", $subhtml, $pages);
        grab6("http://spys.ru" . $data->href);
        foreach (array_unique($pages[0]) as $page) {
            grab6("http://spys.ru" . $page);
        }
    }
    foreach ($dom->find("tr.spy1x td.menu2 a") as $data) {
        $subhtml = scraperWiki::scrape($data->href);
        preg_match_all("@" . str_replace('t/','t\d+/', $data->href) . "@", $subhtml, $pages);
        grab6("http://spys.ru" . $data->href);
        foreach (array_unique($pages[0]) as $page) {
            grab6("http://spys.ru" . $page);
        }
    }
}

//grab10("http://www.ip-adress.com/proxy_list/", "ip-address.com proxy");

for ($i = 1; $i <= 15; $i++) {
    grab12("http://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc/page:$i", "cool-proxy.net proxy");
}

grab11("http://proxylists.me/api.php?cmd=downloadOpenProxies&responseType=text");

for ($i = 1; $i <= 15; $i++) {
    $t = $i;
    if ($t < 10) $t = "0$t";
    grab10("http://www.samair.ru/proxy/ip-address-$t.htm", "samair.ru proxy");
}

grab4("http://proxylist4all.com/category.php?id=51");
grab4("http://proxylist4all.com/category.php?id=53");
grab4("http://proxylist4all.com/category.php?id=57");
for ($i = 0;$i < 3*50;$i+=50) {
    grab4("http://proxylist4all.com/category.php?id=58?start=$i");
}


grab10("http://best-proxy-list-ips.blogspot.com/", 'best-proxy-list-ips proxy');

for ($i = 0;$i < 13*30;$i+=30) {
    grab4("http://www.ufor.org/new-proxies.php?start=$i");
}

for ($i = 0;$i < 96*25;$i+=25) {
    grab4("http://www.atproxy.net/category.php?id=44&start=$i");
}
grab4("http://www.atproxy.net/category.php?id=45");
grab4("http://www.atproxy.net/category.php?id=46");
grab4("http://www.atproxy.net/category.php?id=47");
grab4("http://www.atproxy.net/category.php?id=48");
grab4("http://www.atproxy.net/category.php?id=49");
grab4("http://www.atproxy.net/category.php?id=50");
for ($i = 0;$i < 39*25;$i+=25) {
    grab4("http://www.atproxy.net/category.php?id=51&start=$i");
}

for ($i = 1; $i <= 12; $i++) {
    if ($i < 10) {
        $name = "0$i";
    } else {
        $name = $i;
    }
    grab9("http://nntime.com/proxy-list-$name.htm");
}

getRuList();

for ($i = 1; $i <= 15; $i++) {
    grab8("http://www.publicproxyservers.com/proxy/list$i.html");
}

grab7("http://www.kamranweb.com/proxy/proxylist.js");

grab5("http://goldproxylist.com/");

grab6("http://anonymizer.nntime.com/js/country.js");

grab5("http://proxybay.info/");

getSubLists();

for ($i = 0;$i < 21*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=44&start=$i");
}
for ($i = 0;$i < 12*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=45&start=$i");
}
for ($i = 0;$i < 2*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=46&start=$i");
}
for ($i = 0;$i < 4*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=47&start=$i");
}
grab4("http://www.allproxysites.com/category.php?id=48");
for ($i = 0;$i < 3*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=49&start=$i");
}
for ($i = 0;$i < 6*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=50&start=$i");
}
for ($i = 0;$i < 53*15;$i+=15) {
    grab4("http://www.allproxysites.com/category.php?id=51&start=$i");
}

grab3("http://multiproxy.org/txt_anon/proxy.txt");

grab2("http://www.cybersyndrome.net/pla5.html");

for ($i = 0;$i < 12*25;$i+=25) {
    grab("http://www.megaproxylist.com/?start=$i");
}

for ($i = 0;$i < 97*15;$i+=15) {
    grab("http://www.workingproxies.info/proxies.shtml?start=$i");
}

for ($i = 0;$i < 4*50;$i+=50) {
    grab("http://proxyliberty.com/recent-proxies.php?start=$i");
}

for ($i = 0;$i < 4*50;$i+=50) {
    grab("http://proxyliberty.com/top-proxies.php?start=$i");
}
?>
