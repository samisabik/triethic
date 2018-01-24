from flask import Flask, request, jsonify, render_template
import datetime,time
import psycopg2
import sys

con = None
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def read_data():

    rx_data = request.get_json(silent=True)
    sensor_ID = str(rx_data['device']).lower()
    sensor_level = str(rx_data['data'])
    sensor_rssi = str(rx_data['rssi'])
    ts = str(time.time())

    try:
        con = psycopg2.connect(database='triethic', user='admin', password='KrOQpkWVZeZPGF4O')
        cur = con.cursor()
        cur.execute("UPDATE device_list SET last_value = " + sensor_level + ",last_seen = " + ts + ",last_rssi = " + sensor_rssi + " WHERE device_id = 'd_" + sensor_ID + "'")
        if (rx_data['data'] < 30):
        	cur.execute("UPDATE device_list SET alarm = TRUE WHERE device_id = 'd_" + sensor_ID + "'")
        else:
        	cur.execute("UPDATE device_list SET alarm = FLASE WHERE device_id = 'd_" + sensor_ID + "'")

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