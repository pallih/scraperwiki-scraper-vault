<?php

######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape("http://www.hel.fi/hki/ksv/fi/Liikennesuunnittelu/Ajankohtaista+liikennesuunnittelussa");
#print $html;

# Loads HTML
$dom = new simple_html_dom();
$dom->load($html);

# Finds the correct datatable
$table = $dom->find('div.wpsPortletBody table table table', 2); // Third element wpsPortletBody

$i = 0;

# Goes trought the datatable one paragraph by paragraph
foreach ($table->find('p') as $paragraph)
{
    // Breaks foreach when news items are finished
    if ($paragraph->plaintext === "&#160;")
    {
        break;
    }

    // Simple html dom -functions do not seem to work here (?)

    // Text
    $text = $paragraph->plaintext;
    $start = strpos($text, "</a>");
    $text = substr($text, $start);

    $data[$i]['text'] = $text;

    // URL
    $start = strpos($paragraph, "<a href=\"") + 9; // Number is length of the seed
    $end = strpos($paragraph, "\" >");
    $length = $end - $start;
    $url = substr($paragraph, $start, $length);

    $data[$i]['url'] = $url;

    // Linktext
    $start = strpos($paragraph, "\" >") + 3;// Number is length of the seed
    $end = strpos($paragraph, "</a>");
    $length = $end - $start;
    $linktext = substr($paragraph, $start, $length);

    $data[$i]['linktext'] = $linktext;

    // Date
    $end = strpos($text, " / ");
    $date = substr($text, 0, $end); // copies everything before the last slash

    $start = strrpos($date, " "); // finds last space
    $date = substr($date, $start);

    // converts date to RFC 2822
    $date_array = explode(".", $date); // splits to array...
    date_default_timezone_set('EET'); // Finnish time
    $date_rfc2822 = date("r", mktime(12, 0, 0, $date_array[1], $date_array[0], $date_array[2])); // creates RDF2822-date based on the array

    $data[$i]['date'] = $date_rfc2822;

    // GUID is generated from $text + url (this combination is assumed to be unique)
    $guid = md5("$text . $url");

    $data[$i]['guid'] = $guid;

    $i++;
}


foreach($data as $k => $v)
{
    # Store data in the datastore
    scraperwiki::save(array('text'), $v);
}

?>