<?php

/*

Fetch members of Nth Dail Eireann and store details.
Currently does not either parse or store details.  Pretty good at forenames and surnames tho

*/

function remove_honorifics($string) {
    $remove = array(
        # Actual honorifics and fragments
        "Mr. ", ", Count", "Count ", "Professor ", "Countess ", " de", "Dr. ", "General ", "Ms. ", "Mrs. ","Sir ", "Major ","Capt. ",
        # And some other random strings
        "(Cork West)", "(Sceig) ", " (Major-General)", " (Snr.)"," (Major)"," (Captain)",
        );
    foreach($remove as $current) {
        $string = str_replace($remove, "", $string);
        }

    # Replace o-fadas with o-fada-nbsp to retain surnames' integrity
    $string = str_replace("Mac ", "Mac&nbsp;",str_replace("Ó ","Ó&nbsp;",$string));
    return $string;
}

require  'scraperwiki/simple_html_dom.php';

$url = 'http://www.oireachtas.ie/members-hist/default.asp?housetype=0&HouseNum=4&disp=mem';
$dom = new simple_html_dom();
$html = scraperwiki::scrape($url);

$dom->load($html);

foreach($dom->find("ul[id=memberslist] li") as $row) {

    // Remove honorifics (will need expanding later to get Generals and Countesses)

    $name = remove_honorifics($row->children(1)->plaintext);

    // Split name into surname (word following last space) and forename (the rest)

    $spliced = array_reverse(explode(" ",$name));
    $surname = str_replace("Mac&nbsp;", "Mac ",str_replace("Ó&nbsp;","Ó ",$spliced[0])); # Fix previously-munged names
    unset($spliced[0]);
    $forename = implode(" ",array_reverse($spliced));

    echo  $surname . ", " . $forename . "\n";

}
?>
