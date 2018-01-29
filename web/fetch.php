<?php
//fetch.php

$dbconn = pg_connect("host=217.182.169.210 dbname=triethic user=admin password=KrOQpkWVZeZPGF4O")
    or die('Could not connect: ' . pg_last_error());

$query = 'SELECT device_id,sensor_location,last_value,last_seen,alarm,email_alarm FROM device_list ORDER BY id ASC';
$result = pg_query($query) or die('Query failed: ' . pg_last_error());
$output = array();
while($row = pg_fetch_assoc($result))
{
 $output[] = $row;
}
echo json_encode($output);
?>