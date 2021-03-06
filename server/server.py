from flask import Flask, request, jsonify, render_template
import datetime,time
import psycopg2
import sys
import smtplib

full_limit = 30
con = None
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def read_data():
    rx_data = request.get_json(silent=True)
    print rx_data
    sensor_ID = rx_data['device']
    sensor_level = int(rx_data['data'],16)
    sensor_rssi = rx_data['rssi']
    ts = time.time()

    try:
        con = psycopg2.connect(database='triethic', user='admin', password='KrOQpkWVZeZPGF4O')
        cur = con.cursor()

        cur.execute("INSERT INTO d_" + str(sensor_ID).lower() + " (timestamp, value) VALUES ('" + str(ts) + "','" + str(sensor_level) + "')")

        cur.execute("UPDATE device_list SET last_value = " + str(sensor_level) + ",last_seen = " + str(ts) + ",last_rssi = " + str(sensor_rssi) + " WHERE device_id = '" + str(sensor_ID) + "'")
        if (sensor_level < full_limit):
			cur.execute("SELECT sensor_location,email_alarm FROM device_list WHERE device_id = '" + str(sensor_ID) + "'")
			data_tmp = cur.fetchone()
			email = str(data_tmp[1])
			location = str(data_tmp[0])
			server = smtplib.SMTP('smtp.gmail.com:587')
			server.ehlo()
			server.starttls()
			server.login("triethic.sensor@gmail.com", "EEbsoYoy")
			msg = "Le bac situ\xe9 " + str(location) + " est plein"
			server.sendmail('triethic.sensor@gmail.com', email, msg)
			cur.execute("UPDATE device_list SET alarm = TRUE WHERE device_id = '" + str(sensor_ID) + "'")
        else:
        	cur.execute("UPDATE device_list SET alarm = FALSE WHERE device_id = '" + str(sensor_ID) + "'")

        con.commit()
        
    except psycopg2.DatabaseError, e:
        print 'Error %s' % e    
        sys.exit(1)

    finally:
        if con:
            con.close()
    return ('', 200)

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=False)