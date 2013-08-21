<?php 

// Include the library.
require 'scraperwiki/simple_html_dom.php';

// We'll need this unchanging element throughout.
define("SCHEME_TO_HOST", "://");

// The base URL.
$base_url = "http://www.thule.com/en-US/US/Products";

// The counter.
$total = 1;

// Get the necessary components.
$base_url_scheme = parse_url($base_url, PHP_URL_SCHEME);
$base_url_host = parse_url($base_url, PHP_URL_HOST);

$products = array(
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1008",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1010",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1011",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1012",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1013",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1014",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/13704",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/13702",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/17868",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1018",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/5118",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/5278",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/5304",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1019",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/11986",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/249648",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1020",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/8362",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/18992",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/17878",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/16048",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1022",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1023",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/13900",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/13902",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/18996",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/18998",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/17852",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/34826",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/30404",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/481650",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/481651",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1679913",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1065",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1067",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1068",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1069",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/13692",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/14096",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/30940",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1089",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1009",
  "http://www.thule.com/en-US/US/Products/Base-Racks/Feet/1024",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/ARB43999",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/ARB47999",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/ARB53999",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/ARB60999",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/1025",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/1036",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/1040",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/1042",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/3282",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/3283",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/5258",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/10822",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/8344",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/32012",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/8346",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/32014",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/8348",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/32016",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/9396",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/32018",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/21460",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/21462",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/22508",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/6432999",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/9928",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/10962",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/6238999",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/6270999",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/13812",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/13806",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/220646",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/13808",
  "http://www.thule.com/en-US/US/Products/Base-Racks/LoadBars/15258",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/50765099",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/220648",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/220647",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/22500",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/22504",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/1032",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/8350",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/1053",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/8352",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/16188",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/8354",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/18342",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/5546509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/1055",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/13896",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/13898",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/5116",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/3291",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/13804",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/4294",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/4286",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RoofCarriers/13904",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1258650",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1259651",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1260650",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1260651",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1266650 0",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1267650",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1268650",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/21584",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/5806509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/21574",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/5796519",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/22380",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/5826519",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/18318",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4766509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/916XTR",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/18320",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4776509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/917XTR",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/18322",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4786509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/918XTR",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1077",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1078",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1079",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1080",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1081",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1082",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1083",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4034",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4362",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/11336",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16208",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/11338",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16210",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/11364",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16212",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/11366",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16214",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4898",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4900",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4888",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/4890",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16216",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/21726",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16204",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16206",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16334",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/21728",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/220649",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/5826529",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/220650",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/5826539",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1096",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1097",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1100",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1101",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1102",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1103",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/31308",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/5776509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1104",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/1105",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/11398",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16218",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/11396",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16220",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/11500",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Hitch/16222",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/583650",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/18222",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/16002",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/9006999",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1679939",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/9007999",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1679940",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/9009999",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1679936",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/9010999",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1679938",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/30044",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/4796509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/30046",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/4806509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/16198",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/16200",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/8308",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/8310",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/18676",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/18678",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1091",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1092",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1093",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1094",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/RearDoor/1095",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/TruckBed/18344",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/TruckBed/4880",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/TruckBed/5816509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/TruckBed/4884",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/TruckBed/5786509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/TruckBed/BRLB999",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/SpareTire/1088",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/SpareTire/16258",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/SpareTire/963PRO",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/SpareTire/5826509",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/SpareTire/963XTR",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/16190",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/1038",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/13696",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/16296",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/22508",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/13806",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/13808",
  "http://www.thule.com/en-US/US/Products/Bike-Carriers/Accessories/24712",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/31",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/32",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/29704",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/29706",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/29708",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/29710",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/33",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/611000",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/34",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/35",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/22462",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/36",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/21",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/24",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/25",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/31146",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16308",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/26",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/31148",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16310",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/27",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/31150",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16312",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/5624",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/7932",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/18432",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/18430",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/18428",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/6192",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/7934",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/7296",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/9430",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/10542",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/12382",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16298",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/12384",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16300",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/12386",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16302",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/10206",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/682000",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/159646",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/159645",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16316",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16322",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/159653",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/159654",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/687001",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/687000",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/688001",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/688000",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16304",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/16306",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/28634",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Boxes/28636",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Bags/22462",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Bags/9456",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Bags/14220",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Bags/16254",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Baskets/1049",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Baskets/16244",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Baskets/37643",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Baskets/16250",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/Baskets/16252",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/HitchCargo/31144",
  "http://www.thule.com/en-US/US/Products/Cargo-Carriers/HitchCargo/14214",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/14332",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/1046",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/1047",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/1058",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/1062",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/1063",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/1064",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/29506",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/5180",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiCarriers/29508",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiBoxes/29704",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiBoxes/31148",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiBoxes/159646",
  "http://www.thule.com/en-US/US/Products/Snowsports/SkiBoxes/159645",
  "http://www.thule.com/en-US/US/Products/Snowsports/HitchSki/1678763",
  "http://www.thule.com/en-US/US/Products/Snowsports/HitchSki/1103",
  "http://www.thule.com/en-US/US/Products/Snowsports/HitchSki/14878",
  "http://www.thule.com/en-US/US/Products/Snowsports/Accessories/1356451",
  "http://www.thule.com/en-US/US/Products/Snowsports/Accessories/7118",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/1030",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/1041",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/14450",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/13882",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/809999",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/8109999",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/21710",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/13694",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/1636655",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/4886",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/31306",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/13884",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/31304",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/16192",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/1072",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/13582",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/1073",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/8356",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/13886",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/13888",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/16194",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/13706",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/220645",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/11984",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/196658",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/16196",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/18974",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/9644",
  "http://www.thule.com/en-US/US/Products/Watersports/WatersportCarriers/1048",
  "http://www.thule.com/en-US/US/Products/Watersports/Accessories/1035",
  "http://www.thule.com/en-US/US/Products/Watersports/Accessories/1039",
  "http://www.thule.com/en-US/US/Products/Watersports/Accessories/5258",
  "http://www.thule.com/en-US/US/Products/Watersports/Accessories/13698",
  "http://www.thule.com/en-US/US/Products/Watersports/Accessories/85500999",
  "http://www.thule.com/en-US/US/Products/Watersports/Accessories/15250"
);

function handle_products($product_link)
{
    global $base_url_host, $base_url_scheme, $total;
    if(!empty($product_link)){


      $link_3 = $product_link;

      $cat_raw = str_replace("http://www.thule.com/en-US/US/Products/", "", $product_link);

      $cats = dirname($cat_raw);
      
      $cat_terms = array("Base-Racks/Feet", "Base-Racks/LoadAccessories", "Base-Racks/LoadBars", "Bike-Carriers/Accessories", "Bike-Carriers/Hitch", "Bike-Carriers/RearDoor", "Bike-Carriers/RoofCarriers", "Bike-Carriers/SpareTire", "Bike-Carriers/TruckBed", "Cargo-Carriers/Bags", "Cargo-Carriers/Baskets", "Cargo-Carriers/Boxes", "Cargo-Carriers/HitchCargo", "Luggage/DaypacksAndMessengers", "Luggage/LaptopAndTablet", "Luggage/LuggageAndDuffels", "Snow-Chains/SnowChains", "Snowsports/Accessories", "Snowsports/HitchSki", "Snowsports/SkiBoxes", "Snowsports/SkiCarriers", "Watersports/Accessories", "Watersports/WatersportCarriers");

      $cat_cleaned = array("Base Racks/Feet", "Base Racks/Load Accessories", "Base Racks/Load Bars", "Bike Carriers/Accessories", "Bike Carriers/Hitch", "Bike Carriers/Rear Door", "Bike Carriers/Roof Carriers", "Bike Carriers/Spare Tire", "Bike Carriers/Truck Bed", "Cargo Carriers/Bags", "Cargo Carriers/Baskets", "Cargo Carriers/Boxes", "Cargo Carriers/Hitch Cargo", "Luggage/Daypacks And Messengers", "Luggage/Laptop And Tablet", "Luggage/Luggage And Duffels", "Snow Chains/Snow Chains", "Snowsports/Accessories", "Snowsports/Hitch Ski", "Snowsports/Ski Boxes", "Snowsports/Ski Carriers", "Watersports/Accessories", "Watersports/Watersport Carriers");

      $cat = str_replace($cat_terms, $cat_cleaned, $cats);

      $html_content = scraperwiki::scrape($link_3);
      $html = str_get_html($html_content);
      
      $name_raw = trim($html->find("div[@class='column details_overview'] h2 span",0));
      $name = (!empty($name_raw)) ? strip_tags($name_raw) : "";
      
      $desc_raw = trim($html->find("div[@class='column details_overview'] h3 span",0));
      $desc = (!empty($desc_raw)) ? strip_tags($desc_raw) : "";

      $price_raw = trim($html->find("div[@class='pricing'] span[@id='phcontent_0_ctl00_lblPriceText']",0));
      $price = strip_tags($price_raw);
      $price = str_replace("MSRP $", "", $price);
      $price = trim(str_replace(" (USD)", "", $price));
      $image = $html->find("img[@id='imgProductBomImage_0']",0)->src;

echo "$name: $image\n";


      // Add it to an array.
      $record = array(
          'id' => $total,
          'product_name' => trim($name),
          'desciption' => trim($desc),
          'price' => $price,
          'img' => $image,
          'category' => $cat
      );

      // Add it to the table.
      scraperwiki::save_sqlite(array('id'), array($record), "products_support", 2);

      // Increment the 'id' counter.
      $total++;
     
    }
}

function cleanProductName($string)
{
    if($string){
        $string = str_replace("-", " ", $string);
        $str = preg_replace("/[^A-Za-z0-9\s]/", "", $string);
        return $str;
    }
}

foreach($products AS $product){
    handle_products($product);
}

echo "Number of products: " . $total;

?>