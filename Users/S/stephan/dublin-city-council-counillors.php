<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.dublincity.ie/YourCouncil/Councillors/Pages/FullCouncillorList.aspx");

preg_match_all('|href="(/YourCouncil/Councillors/YourLocalCouncillors/Pages/(.*?).aspx)"|',$html,$arr);

foreach ($arr[1] as $link) {
    
    $html = scraperwiki::scrape("http://www.dublincity.ie".$link);
    $html = oneline($html);

    preg_match_all('|<h1>&nbsp;(.*?)</h1>|',$html,$name);
    if (isset($name[1][0])) { $name= $name[1][0]; } else { $name= ''; }
    
    preg_match_all('|<img alt="(.*?)"  src="(/YourCouncil/Councillors/YourLocalCouncillors/PublishingImages/.*?\.jpg)"  class="right" />|',$html,$img);
    if (isset($img[2][0])) { $img = $img[2][0]; } else { $img = ''; }

    preg_match_all('|<dt>Area:</dt>.*?<dd>(.*?)</dd>|',$html,$area);
    if (isset($area [1][0])) { $area = $area [1][0]; } else { $area = ''; }
    

    preg_match_all('|<dt>Ward:</dt>.*?<dd>(.*?)</dd>|',$html,$ward);
    if (isset($ward[1][0])) { $ward= $ward[1][0]; } else { $ward= ''; }
    
    preg_match_all('|<dt>Elected:</dt>.*?<dd>(.*?)</dd>|',$html,$elected);
    if (isset($elected[1][0])) { $elected= $elected[1][0]; } else { $elected= ''; }
    
    preg_match_all('|<dt>Party:</dt>.*?<dd>(.*?)</dd>|',$html,$party);
    if (isset($party[1][0])) { $party= $party[1][0]; } else { $party= ''; }
    
    preg_match_all('|<h5>Address:</h5>.*?<address>.*?<div id="ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField" style="display:inline">(.*?)</div>.*?</address>|',$html,$address);
    if (isset($address[1][0])) { $address= $address[1][0]; } else { $address= ''; }
    
    preg_match_all('|"mailto:(.*?)"|',$html,$email);
    if (isset($email[1][0])) { $email= $email[1][0]; } else { $email= ''; }
    
    preg_match_all('|<h5>Phone:</h5>.*?<p>.*?&nbsp;<div id="ctl00_PlaceHolderMain_ctl10__ControlWrapper_RichHtmlField" style="display:inline"><p>(.*?)</p></div></p>|',$html,$phone);
    if (isset($phone[1][0])) { $phone= $phone[1][0]; } else { $phone= ''; }

 preg_match_all('|h5>Mobile:</h5>.*?<p>.*?&nbsp;<div id="ctl00_PlaceHolderMain_ctl11__ControlWrapper_RichHtmlField" style="display:inline">(.*?)</div></p>|',$html,$mobile);
    if (isset($mobile[1][0])) { $mobile= $mobile[1][0]; } else { $mobile= ''; }

 preg_match_all('|<h5>Fax:</h5>.*?<p>.*?&nbsp;<div id="ctl00_PlaceHolderMain_ctl12__ControlWrapper_RichHtmlField" style="display:inline"><p>(.*?)</p>|',$html,$fax);
    if (isset($fax[1][0])) { $fax= $fax[1][0]; } else { $fax= ''; }

    scraperwiki::save( array('name'), array('name' => clean($name), 'area'=>clean($area), 'ward'=>clean($ward) ,'elected'=>clean($elected) ,'party'=>clean($party),'image'=>'http://www.dublincity.ie'.clean($img),'address'=>clean($address),'email'=>clean($email),'phone'=>clean($phone)
,'mobile'=>clean($mobile),'fax'=>clean($fax) ) );



}

    function clean($val) {
        $val = str_replace('&nbsp;','',$val);
        $val = strip_tags($val);
        $val = trim($val);
        $val = utf8_decode($val);
        return($val);
    }
    
    function oneline($code) {

        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);

        return $code;

    }




?>