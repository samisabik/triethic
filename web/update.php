<?php
//update.php
$dbconn = pg_connect("host=217.182.169.210 dbname=triethic user=admin password=KrOQpkWVZeZPGF4O")
    or die('Could not connect: ' . pg_last_error());
$query = "UPDATE device_list SET ".$_POST["name"]." = '".$_POST["value"]."' WHERE device_id = '".$_POST["pk"]."'";
pg_query($query);
?>