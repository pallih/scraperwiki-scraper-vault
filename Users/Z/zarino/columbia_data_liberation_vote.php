<?php

scraperwiki::httpresponseheader('Content-Type', 'application/json');

// Clear datastore
// scraperwiki::sqliteexecute("delete from swdata");
// scraperwiki::sqlitecommit();

if(isset($_GET['add'])){

    if(count(scraperwiki::select("* from swdata where url=?", array($_GET['add']))) > 0){
        scraperwiki::sqliteexecute("update swdata set votes=votes+1 where url=?", array($_GET['add']));
        scraperwiki::sqlitecommit();
    } else {
        $data = array("url" => $_GET['add']);
        if(isset($_GET['why'])){
            $data['why'] = $_GET['why'];
        }
        $data['votes'] = 1;
        scraperwiki::save_sqlite(array("url"),$data);
    }
    
}

if(isset($_GET['vote'])){
    
    scraperwiki::sqliteexecute("update swdata set votes=votes+1 where url=?", array($_GET['vote']));
    scraperwiki::sqlitecommit();
    
}

if(isset($_GET['reset'])){
    
    scraperwiki::sqliteexecute("update swdata set votes='1' where url=?", array($_GET['reset']));
    scraperwiki::sqlitecommit();
    
}

if(isset($_GET['delete'])){
    
    scraperwiki::sqliteexecute("delete from swdata where url=?", array($_GET['delete'])); 
    scraperwiki::sqlitecommit(); 
    
}


$rows = scraperwiki::select("* from swdata order by votes desc, url asc");

// if(isset($_SERVER['HTTP_X_REQUESTED_WITH'])){
//
// }

if(isset($_GET['callback'])){
    echo $_GET['callback'] . '(';
}

if(sizeof($rows)){
    echo json_encode($rows);
} else {
    echo json_encode(array());
}

if(isset($_GET['callback'])){
    echo ')';
}

?>
<?php

scraperwiki::httpresponseheader('Content-Type', 'application/json');

// Clear datastore
// scraperwiki::sqliteexecute("delete from swdata");
// scraperwiki::sqlitecommit();

if(isset($_GET['add'])){

    if(count(scraperwiki::select("* from swdata where url=?", array($_GET['add']))) > 0){
        scraperwiki::sqliteexecute("update swdata set votes=votes+1 where url=?", array($_GET['add']));
        scraperwiki::sqlitecommit();
    } else {
        $data = array("url" => $_GET['add']);
        if(isset($_GET['why'])){
            $data['why'] = $_GET['why'];
        }
        $data['votes'] = 1;
        scraperwiki::save_sqlite(array("url"),$data);
    }
    
}

if(isset($_GET['vote'])){
    
    scraperwiki::sqliteexecute("update swdata set votes=votes+1 where url=?", array($_GET['vote']));
    scraperwiki::sqlitecommit();
    
}

if(isset($_GET['reset'])){
    
    scraperwiki::sqliteexecute("update swdata set votes='1' where url=?", array($_GET['reset']));
    scraperwiki::sqlitecommit();
    
}

if(isset($_GET['delete'])){
    
    scraperwiki::sqliteexecute("delete from swdata where url=?", array($_GET['delete'])); 
    scraperwiki::sqlitecommit(); 
    
}


$rows = scraperwiki::select("* from swdata order by votes desc, url asc");

// if(isset($_SERVER['HTTP_X_REQUESTED_WITH'])){
//
// }

if(isset($_GET['callback'])){
    echo $_GET['callback'] . '(';
}

if(sizeof($rows)){
    echo json_encode($rows);
} else {
    echo json_encode(array());
}

if(isset($_GET['callback'])){
    echo ')';
}

?>
