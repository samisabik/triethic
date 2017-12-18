
#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


con = None
exists = False

try:

    con = psycopg2.connect(database='triethic', user='admin', password='KrOQpkWVZeZPGF4O')
    cur = con.cursor()

    device_ID = "XZ56GU"
    cur.execute("select exists(select relname from pg_class where relname='" + device_ID.lower() + "')")
    exists = cur.fetchone()[0]
    print exists
    if not exists:
        print "Creating table for "+device_ID
        cur.execute("CREATE TABLE "+device_ID+"(ID SERIAL, TS TEXT, VALUE INT)")
        con.commit()
    cur.close()

except psycopg2.Error as e:
    print e
