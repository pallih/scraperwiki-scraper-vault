<?php
######################################
# Basic PHP scraper
######################################

$html = scraperwiki::scrape('http://www.valleycollege.edu/eSchedule/online/Schedule/V/2012SP/index.html');
$html = online($html);

      preg_match_all('|<td><a name=".*?"></a><a href="../../../(.*?)">(.*?)</a></td>|', $html, $arr);
      //count = 0;
      foreach ($arr[2] as  $key => $val){
        $Subject = $arr[2][$key];
        $url = "http://www.valleycollege.edu/eSchedule/Online/" . $arr[1][$key];
        $premhtml = scraperwiki::scrape($url);
        $premhtml = online($premhtml);
        preg_match_all('|<td><a href="../../../(.*?)">(.*?)</a></td>|', $premhtml, $arr2);
        
        foreach($arr2[1] as $key => $val){
           //$Subject = $arr2[2][$key];
           $course = $arr2[2][$key];
           $url2 = "http://www.valleycollege.edu/eSchedule/Online/" . $arr2[0][$key];
           //$urlCourse = array();
           //$urlCourse[] = $course;
           //if(isset($course))
           //  continue;
           scraperwiki::save(array('Subject', 'Course'), array('Subject' => $Subject, 'Course' => $course));
           }
        //count++;
        //$record = ;   
         
      }
      
      function clean($val) {
        $val = str_replace('&nbsp;',' ',$val);
        $val = str_replace('&amp;','&',$val);
        $val = html_entity_decode($val);
        $val = strip_tags($val);
        $val = trim($val);
        $val = utf8_decode($val);
        return($val);
     }


     function online($code) {
        $code = str_replace("\n",'',$code);
        $code = str_replace("\r",'',$code);
        return $code;
    }



     ?>