#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys


con = None
exists = False

try:
     
    con = psycopg2.connect(database='sami', user='sami') 
    cur = con.cursor()
    table_str = "test"
    cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
    exists = cur.fetchone()[0]
    print exists
    cur.close()
except psycopg2.Error as e:
    print e
