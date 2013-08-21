<?php

require 'scraperwiki/simple_html_dom.php';

$links_html = str_get_html('
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-58-january-26-last-episode-kbc/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-57-january-25/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-56-january-20/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-55-january-19/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-54-january-18/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-53-january-13/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-52-january-12-5-crore-episode/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-51-january-11/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-50-january-6/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-49-january-5/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-48-january-4/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-47-december-30/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-46-december-29/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-45-december-28-jodi-special/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-44-december-22/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-43-december-21-school-champs-special/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-42-december-16/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-41-december-15/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-40-december-14/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-39-december-9/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-38-december-8/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-37-december-7/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-36-december-2/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-35-december-1/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-34-november-30/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-33-november-25/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-32-november-24/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-31-november-23/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-30-november-18/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-29-november-17/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-28-november-16/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-27-november-10/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-26-november-9-2012/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-25-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-24-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-23-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-22-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-21-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-20-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-19-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-18-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-17-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-16-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-15-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-14-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-13-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-episode-12-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-episode-11-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-10-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-9-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-8-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-7-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-6-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-5-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-4-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-3-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-2-questions/" ></a>
<a href="http://www.iqgarage.com/kbc-questions-and-answers/kbc-6-episode-1-questions/" ></a>
');

$count =0;
       
foreach($links_html->find('a') as $element) 
        {
             
             $url = $element->href;
             $html = file_get_html($url);
        
            
            $string = $html->find('.entry',0);            

            //echo "<hr><h3>Page no: ".(++$count)."</h3>";          
            echo  $string;

        // you must call $dom->clear() to free memory if call file_get_dom() more then once. 
        $html->clear(); 
        unset($html);

        }
        
?>
