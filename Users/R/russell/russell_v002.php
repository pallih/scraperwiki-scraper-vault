<?php
    ini_set('display_errors',1); 
    error_reporting(E_ALL ^ E_NOTICE);

    require "https://scraperwiki.com/editor/raw/webbrowser";
    //require_once "support/simple_html_dom.php";

    // Simple HTML DOM tends to leak RAM like
    // a sieve.  Declare what you will need here.
    // Objects are reusable.
    // $html = new simple_html_dom();

    $url = "https://scraperwiki.com/login/";
    $web = new WebBrowser();
    $result = $web->Process($url);

    if (!$result["success"])  echo "Error retrieving URL.  " . $result["error"] . "\n";
    else if ($result["response"]["code"] != 200)  echo "Error retrieving URL.  Server returned:  " . $result["response"]["code"] . " " . $result["response"]["meaning"] . "\n";
    else
    {
      

        $postvars = array (
            "user_or_email" => "russell",
            "password" => "blabla1rc",
            "csrfmiddlewaretoken" => $input_csrfmiddlewaretoken,
            "submit" => "Log in",
        );
        $tempoptions = array (
            //"protocol" => "ssl",
            "method" => "POST",
            "postvars" => $postvars,
        );
        $url = $url;
        $result2 = $web->Process($url,'auto',$tempoptions);
        echo "RESULT 2 IS DONE<br><br>";
        echo "<pre>";
        print_r($result2);
        echo "</pre>";

    }

?>






   <?php
    ini_set('display_errors',1); 
    error_reporting(E_ALL ^ E_NOTICE);

    require "https://scraperwiki.com/editor/raw/webbrowser";
    //require_once "support/simple_html_dom.php";

    // Simple HTML DOM tends to leak RAM like
    // a sieve.  Declare what you will need here.
    // Objects are reusable.
    // $html = new simple_html_dom();

    $url = "https://scraperwiki.com/login/";
    $web = new WebBrowser();
    $result = $web->Process($url);

    if (!$result["success"])  echo "Error retrieving URL.  " . $result["error"] . "\n";
    else if ($result["response"]["code"] != 200)  echo "Error retrieving URL.  Server returned:  " . $result["response"]["code"] . " " . $result["response"]["meaning"] . "\n";
    else
    {
      

        $postvars = array (
            "user_or_email" => "russell",
            "password" => "blabla1rc",
            "csrfmiddlewaretoken" => $input_csrfmiddlewaretoken,
            "submit" => "Log in",
        );
        $tempoptions = array (
            //"protocol" => "ssl",
            "method" => "POST",
            "postvars" => $postvars,
        );
        $url = $url;
        $result2 = $web->Process($url,'auto',$tempoptions);
        echo "RESULT 2 IS DONE<br><br>";
        echo "<pre>";
        print_r($result2);
        echo "</pre>";

    }

?>






   