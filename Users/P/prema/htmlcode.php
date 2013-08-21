
<?php

class tagSpider
{

var $crl; // this will hold our curl instance
var $html; // this is where we dump the html we get
var $binary; // set for binary type transfer
var $url; // this is the url we are going to do a pass on



function tagSpider()
{
    $this->html = "";
    $this->binary = 0;
    $this->url = "";
}


function fetchPage($url)
{


    $this->url = $url;
    if (isset($this->url)) {

                $this->ch = curl_init (); // start cURL instance
                curl_setopt ($this->ch, CURLOPT_RETURNTRANSFER, 1); // this tells cUrl to return the data
                curl_setopt ($this->ch, CURLOPT_URL, $this->url); // set the url to download
                curl_setopt($this->ch, CURLOPT_FOLLOWLOCATION, true); // follow redirects if any
                curl_setopt($this->ch, CURLOPT_BINARYTRANSFER, $this->binary); // tell cURL if the data is binary data or not
                $this->html = curl_exec($this->ch); // grabs the webpage from the internet
                curl_close ($this->ch); // closes the connection
                }
}


function parse_array($beg_tag, $close_tag) // this function takes the grabbed html and picked out the pieces we want
{
    preg_match_all("($beg_tag.*$close_tag)siU", $this->html, $matching_data); // match data between specificed tags
    return $matching_data[0];
}


}
?>


