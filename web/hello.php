<?php
// Connecting, selecting database
$dbconn = pg_connect("host=localhost dbname=triethic user=admin password=KrOQpkWVZeZPGF4O")
    or die('Could not connect: ' . pg_last_error());

// Performing SQL query
$query = 'SELECT date,time,data FROM d_37319c ORDER BY id DESC LIMIT 1';
$result = pg_query($query) or die('Query failed: ' . pg_last_error());

// Printing results in HTML
echo "d_37319c";
echo "<table>\n";
while ($line = pg_fetch_array($result, null, PGSQL_ASSOC)) {
        echo "\t<tr><th>Date</th><th>Time</th><th>Distance</th></tr>";
        echo "\t<tr>\n";
    foreach ($line as $col_value) {
        echo "\t\t<td>$col_value</td>\n";
    }
    echo "\t</tr>\n";
}
echo "</table>\n";

// Free resultset
pg_free_result($result);

// Closing connection
pg_close($dbconn);
?>