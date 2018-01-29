<html>
 <head>
  <title>TrieEthic - Tableau de Bord</title>
  <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" type="text/css" href="style.css">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/css/bootstrap-editable.css" rel="stylesheet">
  <script src="http://code.jquery.com/jquery-2.0.3.min.js"></script> 
  <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/x-editable/1.5.1/bootstrap3-editable/js/bootstrap-editable.js"></script>
  
 </head>
 <body>
  <div class="container">
    <div class="row text-center">
      <img src="assets/logo.png" alt="logo" style="width:30%">
    </div>   
    <br />
    <h1> Capteurs en fonctionnement </h1>
   <table class="table">
    <thead class="thead-dark">
     <tr>
      <th width="20%">Capteur</th>
      <th width="30%">Localisation</th>
      <th width="10%">Mesure</th>
      <th width="10%">Etat</th>
      <th width="10%">Alerte</th>
      <th width="30%">Alerte email</th>
     </tr>
    </thead>
    <tbody id="sensor_data">
    </tbody>
   </table>
 </body>
</html>



<script type="text/javascript" language="javascript" >
$(document).ready(function(){
 
 function fetch_sensor_data()
 {
  $.ajax({
   url:"fetch.php",
   method:"POST",
   dataType:"json",
   success:function(data)
   {
    for(var count=0; count<data.length; count++)
    {
     var html_data = '<tr><td>'
     +data[count].device_id+'</td>';
     html_data += '<td data-name="sensor_location" class="sensor_location" data-type="text" data-pk="'
     +data[count].device_id+'">'+data[count].sensor_location+'</td>';
     html_data += '<td data-name="last_value" class="last_value" data-type="text" data-pk="'
     +data[count].device_id+'">'+data[count].last_value+' cm</td>';
     html_data += '<td data-name="last_seen" class="last_seen" data-type="text" data-pk="'
     +data[count].device_id+'">';

    var today = new Date();
    var today = today.getDate() + "-" + today.getMonth() + "-" + today.getFullYear();
    var timestamp = new Date(data[count].last_seen*1000);
    var timestamp = timestamp.getDate() + "-" + timestamp.getMonth() + "-" + timestamp.getFullYear();

    if (timestamp == today) {
      html_data += '<img src="assets/true.png" alt="ALIVE" height="16" width="16"></td>'
    }
    else {
      html_data += '<img src="assets/false.png" alt="DEAD" height="16" width="16"></td>'
    };

    html_data += '<td data-name="alarm" class="alarm" data-type="text" data-pk="'+data[count].device_id+'">'
    if (data[count].alarm == "t") {
      html_data += '<img src="assets/false.png" alt="ALARM" height="16" width="16"></td>'
    }
    else {
      html_data += '</td>'
    };

    html_data += '<td data-name="email_alarm" class="email_alarm" data-type="text" data-pk="'+data[count].device_id+'">'+data[count].email_alarm+'</td></tr>';
     $('#sensor_data').append(html_data);
    }
   }
  })
 }
 
 fetch_sensor_data();
 
 $('#sensor_data').editable({
  container: 'body',
  selector: 'td.sensor_location',
  url: "update.php",
  title: 'Localisation',
  type: "POST",
  //dataType: 'json',
  validate: function(value){
   if($.trim(value) == '')
   {
    return 'This field is required';
   }
  }
 });
 
 $('#sensor_data').editable({
  container: 'body',
  selector: 'td.email_alarm',
  url: "update.php",
  title: 'email',
  type: "POST",
  dataType: 'json',
  validate: function(value){
   if($.trim(value) == '')
   {
    return 'This field is required';
   }
  }
 });
 
 
 
});
</script>