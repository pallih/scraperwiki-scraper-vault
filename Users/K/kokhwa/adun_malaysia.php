<?php
    require 'scraperwiki/simple_html_dom.php';

    $strUrl = 'http://en.wikipedia.org/wiki/List_of_State_Seats_Representatives_in_Malaysia';
    $strReturn = scraperwiki::scrape($strUrl);

    while($intStart = stripos($strReturn, '<span class="mw-headline"')){
        $strReturn = substr($strReturn, $intStart);
        // Find the end tag
        $intEnd = stripos($strReturn, '</span>');
        // Get the full span tag
        $strSpan = substr($strReturn, 0, $intEnd+strlen('</span>'));
        $objXml = new simple_html_dom();
        $objXml->load($strSpan);
        $e = $objXml->find('span', 0);
        $strState = $e->plaintext;
        
        // Find the table
        $intStart = stripos($strReturn, '<table class="wikitable">');
        if ($intStart){
            $intEnd = stripos($strReturn, '</table>');
            $intEnd = $intEnd + strlen('</table>');
            $strTable = substr($strReturn, $intStart, $intEnd - $intStart);
            $objXml = str_get_html($strTable);
            // 3rd tr
            $row = $objXml->find('tr', 2);
            do {
                $strDunNo = $row->children(0)->plaintext;
                $strDunName = $row->children(1)->plaintext;
                $strAdunName = $row->children(2)->plaintext;
                $strParty = $row->children(3)->plaintext;

                // Save it, with all upper case for easier search in future
                scraperwiki::save_sqlite(array("state", "dun_no"), 
                    array(
                        "state" => strtoupper($strState), 
                        "dun_no" => strtoupper($strDunNo),
                        "dun_name" => strtoupper($strDunName),
                        "adun_name" => strtoupper($strAdunName),
                        "party" => strtoupper($strParty)
                    )
                );
            } while ($row = $row->next_sibling());
        }
        
        // Move to next state
        $strReturn = substr($strReturn, $intEnd);
    } 

    // Sarawak is different breed
    $strUrl = 'http://en.wikipedia.org/wiki/Sarawak_State_Legislative_Assembly';
    $strReturn = scraperwiki::scrape($strUrl);
    while($intStart = stripos($strReturn, 'id="List_of_current_state_assemblymen"')){
        $strReturn = substr($strReturn, $intStart);
        $strState = 'Sarawak';
        // Find the table
        $intStart = stripos($strReturn, '<table class="wikitable">');
        if ($intStart){
            $intEnd = stripos($strReturn, '</table>');
            $intEnd = $intEnd + strlen('</table>');
            $strTable = substr($strReturn, $intStart, $intEnd - $intStart);
            $objXml = str_get_html($strTable);
            // 3rd tr
            $row = $objXml->find('tr', 2);
            do {
                $strDunNo = $row->children(0)->plaintext;
                $strDunName = $row->children(1)->plaintext;
                $strAdunName = $row->children(2)->plaintext;
                $strParty = $row->children(3)->plaintext;

                // Save it, with all upper case for easier search in future
                 scraperwiki::save_sqlite(array("state", "dun_no"), 
                     array(
                         "state" => strtoupper($strState), 
                         "dun_no" => strtoupper($strDunNo),
                         "dun_name" => strtoupper($strDunName),
                         "adun_name" => strtoupper($strAdunName),
                         "party" => strtoupper($strParty)
                     )
                 );
            } while ($row = $row->next_sibling());
        }
        // Nothing else interesting
        break;
    }   

?>
<?php
    require 'scraperwiki/simple_html_dom.php';

    $strUrl = 'http://en.wikipedia.org/wiki/Malaysian_State_Assembly_Representatives_(2008-2013)';
    $strReturn = scraperwiki::scrape($strUrl);

    while($intStart = stripos($strReturn, '<span class="mw-headline"')){
        $strReturn = substr($strReturn, $intStart);
        // Find the end tag
        $intEnd = stripos($strReturn, '</span>');
        // Get the full span tag
        $strSpan = substr($strReturn, 0, $intEnd+strlen('</span>'));
        $objXml = new simple_html_dom();
        $objXml->load($strSpan);
        $e = $objXml->find('span', 0);
        $strState = $e->plaintext;
        
        // Find the table
        $intStart = stripos($strReturn, '<table class="wikitable">');
        if ($intStart){
            $intEnd = stripos($strReturn, '</table>');
            $intEnd = $intEnd + strlen('</table>');
            $strTable = substr($strReturn, $intStart, $intEnd - $intStart);
            $objXml = str_get_html($strTable);
            // 3rd tr
            $row = $objXml->find('tr', 2);
            do {
                $strDunNo = $row->children(0)->plaintext;
                $strDunName = $row->children(1)->plaintext;
                $strAdunName = $row->children(2)->plaintext;
                $strParty = $row->children(3)->plaintext;

                // Save it, with all upper case for easier search in future
                scraperwiki::save_sqlite(array("state", "dun_no"), 
                    array(
                        "state" => strtoupper($strState), 
                        "dun_no" => strtoupper($strDunNo),
                        "dun_name" => strtoupper($strDunName),
                        "adun_name" => strtoupper($strAdunName),
                        "party" => strtoupper($strParty)
                    )
                );
            } while ($row = $row->next_sibling());
        }
        
        // Move to next state
        $strReturn = substr($strReturn, $intEnd);
    } 

    // Sarawak is different breed
    $strUrl = 'http://en.wikipedia.org/wiki/Sarawak_State_Legislative_Assembly';
    $strReturn = scraperwiki::scrape($strUrl);
    while($intStart = stripos($strReturn, 'id="List_of_current_state_assemblymen"')){
        $strReturn = substr($strReturn, $intStart);
        $strState = 'Sarawak';
        // Find the table
        $intStart = stripos($strReturn, '<table class="wikitable">');
        if ($intStart){
            $intEnd = stripos($strReturn, '</table>');
            $intEnd = $intEnd + strlen('</table>');
            $strTable = substr($strReturn, $intStart, $intEnd - $intStart);
            $objXml = str_get_html($strTable);
            // 3rd tr
            $row = $objXml->find('tr', 2);
            do {
                $strDunNo = $row->children(0)->plaintext;
                $strDunName = $row->children(1)->plaintext;
                $strAdunName = $row->children(2)->plaintext;
                $strParty = $row->children(3)->plaintext;

                // Save it, with all upper case for easier search in future
                 scraperwiki::save_sqlite(array("state", "dun_no"), 
                     array(
                         "state" => strtoupper($strState), 
                         "dun_no" => strtoupper($strDunNo),
                         "dun_name" => strtoupper($strDunName),
                         "adun_name" => strtoupper($strAdunName),
                         "party" => strtoupper($strParty)
                     )
                 );
            } while ($row = $row->next_sibling());
        }
        // Nothing else interesting
        break;
    }   

?>
