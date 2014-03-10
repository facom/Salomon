import MySQLdb as mdb
from sys import exit,argv
import random
import numpy as np
import copy
import pickle
from os import system

###################################################
#CONFIGURACION
###################################################
CSVLOCATION="tmp/EspaciosFacultad/SalomonFinal/"
BASENAME="Salomon"
DATABASE="salomon_1401"
USER="salomon"
PASSWORD="123"

def pickleSalomon(fpickle,salomon):
    with open(fpickle,"wb") as fdump:
        pickle.dump(salomon,fdump)
    fdump.close()

def unpickleSalomon(fpickle):
    with open(fpickle,"rb") as fdump:
        salomon=pickle.load(fdump)
    fdump.close()
    return salomon

def splitString(string,separator):
    return string.split(separator)[:-1]

class dict2obj(object):
    def __init__(self,dic={}):self.__dict__.update(dic)
    def __add__(self,other):
        for attr in other.__dict__.keys():
            exec("self.%s=other.%s"%(attr,attr))
        return self

def shuffleList(l):
    o=list(l)
    r=[]
    for i in xrange(len(o)):
        element=random.choice(o)
        o.remove(element)
        r.append(element)
    return r

def loadDatabase(server='localhost',
                 user='salomon',
                 password='123',
                 database='salomon_1401'):
    con=mdb.connect(server,user,password,database)
    with con:
        dbdict=dict()
        db=con.cursor()
        db.execute("show tables;")
        tables=db.fetchall()
        for table in tables:
            table=table[0]
            dbdict[table]=dict()
            
            db.execute("show columns from %s;"%table)
            fields=db.fetchall()
            dbdict[table]['fields']=[]
            for field in fields:
                fieldname=field[0]
                fieldtype=field[3]
                dbdict[table]['fields']+=[fieldname]
                if fieldtype=='PRI':
                    dbdict[table]['primary']=fieldname

            db.execute("select * from %s;"%table)
            rows=db.fetchall()

            dbdict[table]['rows']=dict()
            for row in rows:
                rowdict=dict()
                i=0
                for field in dbdict[table]['fields']:
                    rowdict[field]=row[i]
                    if field==dbdict[table]['primary']:
                        primary=row[i]
                    i+=1
                dbdict[table]['rows'][primary]=rowdict

    return dbdict,con

def updateDatabase(dbdict,con):
    with con:
        db=con.cursor()
        for table in dbdict.keys():
            for row in dbdict[table]['rows'].keys():
                sql="update %s set "%table;
                for field in dbdict[table]['fields']:
                    if field==dbdict[table]['primary']:
                        suffix="where %s='%s'"%(field,dbdict[table]['rows'][row][field])
                        continue
                    sql+="%s = '%s',"%(field,dbdict[table]['rows'][row][field])
                sql=sql.strip(",")+" %s;"%suffix
                db.execute(sql);
