<?php


$navigation['home']['selected']=TRUE;

// **** PATH INFO BASED REQUESTS ****

$scrape = new Scrape();    
$urls2 = array();
$papers = array();

$urls2['What is changing and why does it matter?] WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F511&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is changing and why does it matter? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F511&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['What is changing and why does it matter? PDF 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Vol1-No1-Briefing-Paper-online&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is changing and why does it matter? PDF 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Vol1-No1-Briefing-Paper-online&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['CETIS Analytics Series: Analytics for the whole institution WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F513&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['CETIS Analytics Series: Analytics for the whole institution WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F513&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['CETIS Analytics Series: Analytics for the whole institution OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Whole-Institution-Vol1-No2&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['CETIS Analytics Series: Analytics for the whole institution OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Whole-Institution-Vol1-No2&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';



$urls2['Analytics for Learning and Teaching? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F516&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Learning and Teaching? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F516&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Analytics for Learning and Teaching? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Learning&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Learning and Teaching? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Learning&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F500&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F500&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Legal-Risk-and&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Legal-Risk-and&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['What is Analytics? Definition and Essential Characteristics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F521&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is Analytics? Definition and Essential Characteristics? WEB 2013']  = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F521&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['What is Analytics? Definition and Essential Characteristics? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=What-is-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is Analytics? Definition and Essential Characteristics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=What-is-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Analytics for Understanding Research? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F518&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Understanding Research? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F518&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Analytics for Understanding Research? OTHER 2012']  = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Understandin&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Understanding Research? OTHER 2013']  = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Understandin&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['A Framework of Characteristics for Analytics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F524&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Framework of Characteristics for Analytics? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F524&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['A Framework of Characteristics for Analytics? OTHER 2012'] = 'http://publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=A-Framework-of-Characteristics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Framework of Characteristics for Analytics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=A-Framework-of-Characteristics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Institutional Readiness for Analytics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F527&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Institutional Readiness for Analytics? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F527&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Institutional Readiness for Analytics? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Institutional-Readiness-for-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Institutional Readiness for Analytics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Institutional-Readiness-for-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['A Brief History of Analytics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F529&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Brief History of Analytics? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F529&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['A Brief History of Analytics? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Brief-History&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Brief History of Analytics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Brief-History&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';



$urls2['The impact of analytics in Higher Educati WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F529&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The impact of analytics in Higher Educati OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Teaching-Practice&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';



$urls2['The Implications of Analytics Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F532&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The Implications of Analytics OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Teaching-Practice&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';




$urls2['Tools and Infrastructure 2013 Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F535&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Tools and Infrastructure 2013 OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Tools-and&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['Case Study, Engaging with Analytics 2013 Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F706&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Case Study, Engaging with Analytics 2013 OTHER'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Engaging-with-Anal&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Acting on Assessment Analytics Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2013%2F750&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Acting on Assessment Analytics OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Assessment-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


//briefing papers

$urls2['MOOCs and Open Education Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F667&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['MOOCs and Open Education OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=MOOCs-and-Open-Education&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

// - //

$urls2['IMS Learning Tools Interoperability WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F473&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['IMS Learning Tools Interoperability  WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F473&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['IMS Learning Tools Interoperability  OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=LTI-Briefing-Paper&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['IMS Learning Tools Interoperability  OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=LTI-Briefing-Paper&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

//reports


$urls2['The roles of libraries and information WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F466&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['The roles of libraries and information  WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F466&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The roles of libraries and information  OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=OER-Libraries&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['The roles of libraries and information  OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=OER-Libraries&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Delivering Web to Mobile WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F492&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Delivering Web to Mobile  WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F492&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Delivering Web to Mobile  OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=delivering-web&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Delivering Web to Mobile OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=delivering-web&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


//Other

$urls2['into the wild Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F601&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['into the wild  OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=into&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['book sprint Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F764&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['book sprint  OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=OER13_booksprints&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['The Learning Registry: Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F770&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The Learning Registry:  OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=LearningRegistry&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['New approaches to describing.. Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F767&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['New approaches to describing.. OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=_resourcediscovery&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$total = 0;
foreach ($urls2 as $name => $url ){ 

$hits = get_hits($url, $scrape);
    $record = array(
                'paper' => $name, 
                'url' => $url,
                'hits' => $hits

            );

$total  = $total + $hits;
    scraperwiki::save(array('paper'), $record);
    print_r($record);
    };


print "total =" . $total;











function get_hits($url,$scrape)
{    
    $hits = 0;
    $scrape->fetch($url); //fetch data
    $data = $scrape->removeNewlines($scrape->result);    
    $data = $scrape->fetchBetween('<table class="aws_data" border="1" cellpadding="2" cellspacing="0" width="100%">','</table>',$data,true);
    $rows = $scrape->fetchAllBetween('<tr','</tr>',$data,true); //grab all the correct data
        
    foreach ($rows as $id => $row){
            $cells = $scrape->fetchAllBetween('<td','</td>',$row,true);
            if (strip_tags($cells[0]) != "Others"){
                if (strip_tags($cells[0]) == ""){}else{
               // print "<tr> <td>" . $key . "</td><td>" .  substr(strip_tags($cells[0]), -20)  . "</td><td>" . strip_tags($cells[1]). "</td></tr>";
     
    $hits = $hits +   strip_tags($cells[1]);
                 };
       };
    };
return $hits;
}

        
function get_between($input, $start, $end)
{
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1));
  return $substr;
} 



class Scrape {
    
    
    public $headers = array();
    public $result;
    public $error;
    
    
    function __construct() {
        
        return true;
        
    }
    
    
    
    function setHeader($header) {
        
        $this->headers[] = $header;
        
    }
    

    
    function fetch($url, $data='', $needlogin = false){
        
        if ($needlogin = true){
           $username=urlencode('othervoices'); $password="g3n3r4t0r";
        }
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, false);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT,true);
        curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"); 
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_MAXREDIRS, 5);
        
        /*
        curl_setopt($ch, CURLOPT_COOKIEFILE, 'C:\Users\BRADINO\Desktop\cookie.txt');
        curl_setopt($ch, CURLOPT_COOKIEJAR, 'C:\Users\BRADINO\Desktop\cookie.txt');
        */
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0); 
    
        
        if (is_array($data) && count($data)>0){
            
            curl_setopt($ch, CURLOPT_POST, true);
            $params = http_build_query($data);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
            
        }
            
        
        if (is_array($this->headers) && count($this->headers)>0){
            
            curl_setopt($ch, CURLOPT_HTTPHEADER, $this->headers);
            
        }
        
        
        $this->result = curl_exec($ch);
        $this->error = curl_error($ch);
        curl_close($ch);    
        
    }
    
    
    
    function fetchBefore($needle,$haystack,$include=false){
        
        $included = strpos($haystack,$needle) + strlen($needle);
        
        $excluded = strpos($haystack,$needle);
        
        if ($included === false || $excluded === false) { return null; }
        
        $length = ($include == true) ? $included : $excluded ;
        
        $substring = substr($haystack, 0, $length);
        
        return trim($substring);
        
    }
    
    
    
    function fetchAfter($needle,$haystack,$include=false){
        
        $included = strpos($haystack,$needle);
        
        $excluded = strpos($haystack,$needle) + strlen($needle);
        
        if ($included === false || $excluded === false) { return null; }
        
        $position = ($include == true) ? $included : $excluded ;
        
        $substring = substr($haystack, $position, strlen($haystack) - $position);
        
        return trim($substring);
        
    }
    
    
    
    function fetchBetween($needle1,$needle2,$haystack,$include=false){
        
        $position = strpos($haystack,$needle1);
        
        if ($position === false) { return null; }
        
        if ($include == false) $position += strlen($needle1);
        
        $position2 = strpos($haystack,$needle2,$position);
        
        if ($position2 === false) { return null; }
        
        if ($include == true) $position2 += strlen($needle2);
        
        $length = $position2 - $position;
        
        $substring = substr($haystack, $position, $length);
        
        return trim($substring);
        
    }
    
    
    
    function fetchAllBetween($needle1,$needle2,$haystack,$include=false){
        
        $matches = array();
        
        $exp = "|{$needle1}(.*){$needle2}|U";
        
        preg_match_all($exp,$haystack,$matches);
        
        $i = ($include == true) ? 0 : 1 ;
        
        return $matches[$i];
        
    }
    
    
    
    function removeNewlines($input){
        
        return str_replace(array("\t","\n","\r","\x20\x20","\0","\x0B"), "", html_entity_decode($input));
        
    }
    
    
    
    function removeTags($input,$allowed=''){
        
        return strip_tags($input,$allowed);
        
    }
    
    
    
}



?>
<?php


$navigation['home']['selected']=TRUE;

// **** PATH INFO BASED REQUESTS ****

$scrape = new Scrape();    
$urls2 = array();
$papers = array();

$urls2['What is changing and why does it matter?] WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F511&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is changing and why does it matter? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F511&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['What is changing and why does it matter? PDF 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Vol1-No1-Briefing-Paper-online&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is changing and why does it matter? PDF 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Vol1-No1-Briefing-Paper-online&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['CETIS Analytics Series: Analytics for the whole institution WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F513&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['CETIS Analytics Series: Analytics for the whole institution WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F513&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['CETIS Analytics Series: Analytics for the whole institution OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Whole-Institution-Vol1-No2&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['CETIS Analytics Series: Analytics for the whole institution OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Whole-Institution-Vol1-No2&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';



$urls2['Analytics for Learning and Teaching? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F516&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Learning and Teaching? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F516&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Analytics for Learning and Teaching? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Learning&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Learning and Teaching? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Learning&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F500&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F500&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Legal-Risk-and&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Legal, Risk and Ethical Aspects of Analytics in Higher Education? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Legal-Risk-and&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['What is Analytics? Definition and Essential Characteristics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F521&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is Analytics? Definition and Essential Characteristics? WEB 2013']  = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F521&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['What is Analytics? Definition and Essential Characteristics? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=What-is-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['What is Analytics? Definition and Essential Characteristics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=What-is-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Analytics for Understanding Research? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F518&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Understanding Research? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F518&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Analytics for Understanding Research? OTHER 2012']  = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Understandin&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Analytics for Understanding Research? OTHER 2013']  = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Understandin&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['A Framework of Characteristics for Analytics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F524&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Framework of Characteristics for Analytics? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F524&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['A Framework of Characteristics for Analytics? OTHER 2012'] = 'http://publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=A-Framework-of-Characteristics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Framework of Characteristics for Analytics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=A-Framework-of-Characteristics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Institutional Readiness for Analytics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F527&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Institutional Readiness for Analytics? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F527&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Institutional Readiness for Analytics? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Institutional-Readiness-for-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Institutional Readiness for Analytics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Institutional-Readiness-for-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['A Brief History of Analytics? WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F529&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Brief History of Analytics? WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F529&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['A Brief History of Analytics? OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Brief-History&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['A Brief History of Analytics? OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Brief-History&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';



$urls2['The impact of analytics in Higher Educati WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F529&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The impact of analytics in Higher Educati OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-for-Teaching-Practice&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';



$urls2['The Implications of Analytics Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2012%2F532&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The Implications of Analytics OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Teaching-Practice&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';




$urls2['Tools and Infrastructure 2013 Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F535&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Tools and Infrastructure 2013 OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Analytics-Tools-and&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['Case Study, Engaging with Analytics 2013 Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F706&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Case Study, Engaging with Analytics 2013 OTHER'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Engaging-with-Anal&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Acting on Assessment Analytics Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=%2F2013%2F750&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Acting on Assessment Analytics OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=Assessment-Analytics&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


//briefing papers

$urls2['MOOCs and Open Education Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F667&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['MOOCs and Open Education OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=MOOCs-and-Open-Education&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

// - //

$urls2['IMS Learning Tools Interoperability WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F473&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['IMS Learning Tools Interoperability  WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F473&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['IMS Learning Tools Interoperability  OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=LTI-Briefing-Paper&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['IMS Learning Tools Interoperability  OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=LTI-Briefing-Paper&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

//reports


$urls2['The roles of libraries and information WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F466&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['The roles of libraries and information  WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F466&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The roles of libraries and information  OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=OER-Libraries&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['The roles of libraries and information  OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=OER-Libraries&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['Delivering Web to Mobile WEB 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F492&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Delivering Web to Mobile  WEB 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F492&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['Delivering Web to Mobile  OTHER 2012'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=delivering-web&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2012&month=all&framename=mainright';
$urls2['Delivering Web to Mobile OTHER 2013'] = 'http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=delivering-web&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


//Other

$urls2['into the wild Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2012%2F601&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['into the wild  OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=into&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['book sprint Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F764&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['book sprint  OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=OER13_booksprints&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$urls2['The Learning Registry: Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F770&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['The Learning Registry:  OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=LearningRegistry&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';


$urls2['New approaches to describing.. Web'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=2013%2F767&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';
$urls2['New approaches to describing.. OTHER'] ='http://davidstats:PassMe@publications.cetis.ac.uk/awstats/awstats.pl?urlfilter=_resourcediscovery&urlfilterex=&output=urldetail&config=publications.cetis.ac.uk&year=2013&month=all&framename=mainright';

$total = 0;
foreach ($urls2 as $name => $url ){ 

$hits = get_hits($url, $scrape);
    $record = array(
                'paper' => $name, 
                'url' => $url,
                'hits' => $hits

            );

$total  = $total + $hits;
    scraperwiki::save(array('paper'), $record);
    print_r($record);
    };


print "total =" . $total;











function get_hits($url,$scrape)
{    
    $hits = 0;
    $scrape->fetch($url); //fetch data
    $data = $scrape->removeNewlines($scrape->result);    
    $data = $scrape->fetchBetween('<table class="aws_data" border="1" cellpadding="2" cellspacing="0" width="100%">','</table>',$data,true);
    $rows = $scrape->fetchAllBetween('<tr','</tr>',$data,true); //grab all the correct data
        
    foreach ($rows as $id => $row){
            $cells = $scrape->fetchAllBetween('<td','</td>',$row,true);
            if (strip_tags($cells[0]) != "Others"){
                if (strip_tags($cells[0]) == ""){}else{
               // print "<tr> <td>" . $key . "</td><td>" .  substr(strip_tags($cells[0]), -20)  . "</td><td>" . strip_tags($cells[1]). "</td></tr>";
     
    $hits = $hits +   strip_tags($cells[1]);
                 };
       };
    };
return $hits;
}

        
function get_between($input, $start, $end)
{
  $substr = substr($input, strlen($start)+strpos($input, $start), (strlen($input) - strpos($input, $end))*(-1));
  return $substr;
} 



class Scrape {
    
    
    public $headers = array();
    public $result;
    public $error;
    
    
    function __construct() {
        
        return true;
        
    }
    
    
    
    function setHeader($header) {
        
        $this->headers[] = $header;
        
    }
    

    
    function fetch($url, $data='', $needlogin = false){
        
        if ($needlogin = true){
           $username=urlencode('othervoices'); $password="g3n3r4t0r";
        }
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_HEADER, false);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FRESH_CONNECT,true);
        curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)"); 
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_MAXREDIRS, 5);
        
        /*
        curl_setopt($ch, CURLOPT_COOKIEFILE, 'C:\Users\BRADINO\Desktop\cookie.txt');
        curl_setopt($ch, CURLOPT_COOKIEJAR, 'C:\Users\BRADINO\Desktop\cookie.txt');
        */
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0); 
    
        
        if (is_array($data) && count($data)>0){
            
            curl_setopt($ch, CURLOPT_POST, true);
            $params = http_build_query($data);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $params);
            
        }
            
        
        if (is_array($this->headers) && count($this->headers)>0){
            
            curl_setopt($ch, CURLOPT_HTTPHEADER, $this->headers);
            
        }
        
        
        $this->result = curl_exec($ch);
        $this->error = curl_error($ch);
        curl_close($ch);    
        
    }
    
    
    
    function fetchBefore($needle,$haystack,$include=false){
        
        $included = strpos($haystack,$needle) + strlen($needle);
        
        $excluded = strpos($haystack,$needle);
        
        if ($included === false || $excluded === false) { return null; }
        
        $length = ($include == true) ? $included : $excluded ;
        
        $substring = substr($haystack, 0, $length);
        
        return trim($substring);
        
    }
    
    
    
    function fetchAfter($needle,$haystack,$include=false){
        
        $included = strpos($haystack,$needle);
        
        $excluded = strpos($haystack,$needle) + strlen($needle);
        
        if ($included === false || $excluded === false) { return null; }
        
        $position = ($include == true) ? $included : $excluded ;
        
        $substring = substr($haystack, $position, strlen($haystack) - $position);
        
        return trim($substring);
        
    }
    
    
    
    function fetchBetween($needle1,$needle2,$haystack,$include=false){
        
        $position = strpos($haystack,$needle1);
        
        if ($position === false) { return null; }
        
        if ($include == false) $position += strlen($needle1);
        
        $position2 = strpos($haystack,$needle2,$position);
        
        if ($position2 === false) { return null; }
        
        if ($include == true) $position2 += strlen($needle2);
        
        $length = $position2 - $position;
        
        $substring = substr($haystack, $position, $length);
        
        return trim($substring);
        
    }
    
    
    
    function fetchAllBetween($needle1,$needle2,$haystack,$include=false){
        
        $matches = array();
        
        $exp = "|{$needle1}(.*){$needle2}|U";
        
        preg_match_all($exp,$haystack,$matches);
        
        $i = ($include == true) ? 0 : 1 ;
        
        return $matches[$i];
        
    }
    
    
    
    function removeNewlines($input){
        
        return str_replace(array("\t","\n","\r","\x20\x20","\0","\x0B"), "", html_entity_decode($input));
        
    }
    
    
    
    function removeTags($input,$allowed=''){
        
        return strip_tags($input,$allowed);
        
    }
    
    
    
}



?>
