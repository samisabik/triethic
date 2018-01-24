from flask import Flask, request, jsonify, render_template
import datetime,time
import psycopg2
import sys

con = None
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def read_data():

    rx_data = request.get_json(silent=True)
    sensor_ID = rx_data['device']
    sensor_level = int(rx_data['data'],16)
    sensor_rssi = rx_data['rssi']
    ts = time.time()

    try:
        con = psycopg2.connect(database='triethic', user='admin', password='KrOQpkWVZeZPGF4O')
        cur = con.cursor()
        cur.execute("UPDATE device_list SET last_value = " + str(sensor_level) + ",last_seen = " + str(ts) + ",last_rssi = " + str(sensor_rssi) + " WHERE device_id = 'd_" + str(sensor_ID).lower + "'")
        if (rx_data['data'] < 30):
        	cur.execute("UPDATE device_list SET alarm = TRUE WHERE device_id = 'd_" + sensor_ID + "'")
        else:
        	cur.execute("UPDATE device_list SET alarm = FALSE WHERE device_id = 'd_" + sensor_ID + "'")

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