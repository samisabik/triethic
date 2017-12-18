from flask import Flask, request, jsonify, render_template
import datetime,time
import psycopg2
import sys

con = None

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def add_message():

    ts = datetime.datetime.now().strftime("%d%m%y-%H:%M")
    content = request.get_json(silent=True)
    print "SENSOR ID : " + content['ID']
    print "SENSOR VALUE : " + content['data']
    print "TIME : " + str(ts)
    try:
     
        con = psycopg2.connect(database='triethoic', user='admin', password='KrOQpkWVZeZPGF4O') 
        cur = con.cursor()
        cur.execute("INSERT INTO " + content['ID'].lower() + "(data,ts) VALUES(" + content['data'] +",'"+ str(ts) +"')")
        #cur.execute("INSERT INTO " + content['ID'].lower() + "(data) VALUES(" + content['data'] +")")
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