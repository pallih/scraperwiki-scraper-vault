<?php
require 'scraperwiki/simple_html_dom.php';           

function startsWith($haystack, $needle) {
    return !strncmp($haystack, $needle, strlen($needle));
}

function endsWith($haystack, $needle) {
    $length = strlen($needle);
    if ($length == 0)
        return true;

    return (substr($haystack, -$length) === $needle);
}


// Uncomment to reset all data
//scraperwiki::sqliteexecute("DROP TABLE films");
//scraperwiki::sqlitecommit();

$unfinished = array();
try {
    $unfinished = scraperwiki::select("* FROM films WHERE done = 0 LIMIT 100");

} catch(Exception $e) {

        $id = 0;
        $html = str_get_html(scraperwiki::scrape(
            "http://www.imsdb.com/all%20scripts/"));

        foreach ($html->find("body > br + table.body td + td[valign=top] p a") as $el) {
            print $el->innertext . "\n";
            scraperwiki::save_sqlite(array("film"), array(
                "film" => $id++,
                "name" => $el->innertext,
                "link" => $el->href,
                "done" => false
            ), "films");
        }
    
        die();
}



foreach ($unfinished as $film) {

        echo "===== ". $film['name'] . " =====\n";
        $html = str_get_html(scraperwiki::scrape(
            str_replace(" ", "%20", "http://www.imsdb.com" . $film['link'])
        ));

        foreach ($html->find(".script-details a") as $el) {
            
            try {
                scraperwiki::sqliteexecute(
                    "DELETE FROM writers WHERE film = ?", array($film["film"]));
                scraperwiki::sqlitecommit();
            } catch(Exception $e) {}

            if (startsWith($el->href, "/writer.php")) {
                echo "Writer: ". $el->innertext . "\n";
                scraperwiki::save_sqlite(array(), array(
                    "writer" => $el->innertext,
                    "film"   => $film["film"]
                ), "writers");
            }

            try {
                 scraperwiki::sqliteexecute(
                    "DELETE FROM genres WHERE film = ?", array($film["film"]));
                 scraperwiki::sqlitecommit();

            } catch(Exception $e) {}

            if (startsWith($el->href, "/genre/")) {
                echo "Genre: ". $el->innertext . "\n";
                scraperwiki::save_sqlite(array(), array(
                    "genre" => $el->innertext,
                    "film" => $film["film"]
                ), "genres");
            }

            try {
                scraperwiki::sqliteexecute(
                    "DELETE FROM fulltext WHERE film = ?", array($film["film"]));
                scraperwiki::sqlitecommit();
            } catch(Exception $e) {}

            if (startsWith($el->href, "/scripts/")) {

                $scra = scraperwiki::scrape("http://www.imsdb.com" . $el->href);

                $hear = false;
                $data = array();
                foreach(preg_split("/((\r\n?)|(\n\r?))/", $scra) as $line){
                    
                    if (preg_match('/<pre>/i', $line)) {
                        $data = array();
                        $hear = true;
                        continue;
                    }
                    if (preg_match('/<\/pre>/i', $line)) {
                        $hear = false;
                        continue;
                    }
                    if ($hear) {
                        array_push($data, $line);
                    }
                }

                echo "Lines: ". sizeof($data) . "\n";
                $text = "";
                foreach ($data as $i => $line) {
                    $text .= $line . "\n";
                }

                scraperwiki::save_sqlite(array("film"), array(
                    "text" => utf8_encode($text),
                    "film" => $film["film"]
                ), "fulltext");
            }
        }    

        scraperwiki::sqliteexecute("UPDATE films SET done = 1 WHERE film = ?", array($film["film"]));
        scraperwiki::sqlitecommit();
}

<?php
require 'scraperwiki/simple_html_dom.php';           

function startsWith($haystack, $needle) {
    return !strncmp($haystack, $needle, strlen($needle));
}

function endsWith($haystack, $needle) {
    $length = strlen($needle);
    if ($length == 0)
        return true;

    return (substr($haystack, -$length) === $needle);
}


// Uncomment to reset all data
//scraperwiki::sqliteexecute("DROP TABLE films");
//scraperwiki::sqlitecommit();

$unfinished = array();
try {
    $unfinished = scraperwiki::select("* FROM films WHERE done = 0 LIMIT 100");

} catch(Exception $e) {

        $id = 0;
        $html = str_get_html(scraperwiki::scrape(
            "http://www.imsdb.com/all%20scripts/"));

        foreach ($html->find("body > br + table.body td + td[valign=top] p a") as $el) {
            print $el->innertext . "\n";
            scraperwiki::save_sqlite(array("film"), array(
                "film" => $id++,
                "name" => $el->innertext,
                "link" => $el->href,
                "done" => false
            ), "films");
        }
    
        die();
}



foreach ($unfinished as $film) {

        echo "===== ". $film['name'] . " =====\n";
        $html = str_get_html(scraperwiki::scrape(
            str_replace(" ", "%20", "http://www.imsdb.com" . $film['link'])
        ));

        foreach ($html->find(".script-details a") as $el) {
            
            try {
                scraperwiki::sqliteexecute(
                    "DELETE FROM writers WHERE film = ?", array($film["film"]));
                scraperwiki::sqlitecommit();
            } catch(Exception $e) {}

            if (startsWith($el->href, "/writer.php")) {
                echo "Writer: ". $el->innertext . "\n";
                scraperwiki::save_sqlite(array(), array(
                    "writer" => $el->innertext,
                    "film"   => $film["film"]
                ), "writers");
            }

            try {
                 scraperwiki::sqliteexecute(
                    "DELETE FROM genres WHERE film = ?", array($film["film"]));
                 scraperwiki::sqlitecommit();

            } catch(Exception $e) {}

            if (startsWith($el->href, "/genre/")) {
                echo "Genre: ". $el->innertext . "\n";
                scraperwiki::save_sqlite(array(), array(
                    "genre" => $el->innertext,
                    "film" => $film["film"]
                ), "genres");
            }

            try {
                scraperwiki::sqliteexecute(
                    "DELETE FROM fulltext WHERE film = ?", array($film["film"]));
                scraperwiki::sqlitecommit();
            } catch(Exception $e) {}

            if (startsWith($el->href, "/scripts/")) {

                $scra = scraperwiki::scrape("http://www.imsdb.com" . $el->href);

                $hear = false;
                $data = array();
                foreach(preg_split("/((\r\n?)|(\n\r?))/", $scra) as $line){
                    
                    if (preg_match('/<pre>/i', $line)) {
                        $data = array();
                        $hear = true;
                        continue;
                    }
                    if (preg_match('/<\/pre>/i', $line)) {
                        $hear = false;
                        continue;
                    }
                    if ($hear) {
                        array_push($data, $line);
                    }
                }

                echo "Lines: ". sizeof($data) . "\n";
                $text = "";
                foreach ($data as $i => $line) {
                    $text .= $line . "\n";
                }

                scraperwiki::save_sqlite(array("film"), array(
                    "text" => utf8_encode($text),
                    "film" => $film["film"]
                ), "fulltext");
            }
        }    

        scraperwiki::sqliteexecute("UPDATE films SET done = 1 WHERE film = ?", array($film["film"]));
        scraperwiki::sqlitecommit();
}

