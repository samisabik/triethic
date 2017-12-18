from flask import Flask, request, jsonify, render_template
import datetime,time
import psycopg2
import sys

con = None
exists = False

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def read_data():

    ts = datetime.datetime.now().strftime("%d%m%y-%H:%M")
    content = request.get_json(silent=True)
    device_ID = str(content['device']).lower()
    value = content['data']
    
    try:
        con = psycopg2.connect(database='triethic', user='admin', password='KrOQpkWVZeZPGF4O')
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='d_" + device_ID + "')")
        exists = cur.fetchone()[0]
        
        if not exists:
            print "Creating table for " + device_ID
            cur.execute("CREATE TABLE d_"+ device_ID + "(id SERIAL, ts TEXT, data INT)")
            con.commit()
        
        cur.execute("INSERT INTO d_" + device_ID + "(ts,data) VALUES(" + value +",'"+ str(ts) +"')")
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