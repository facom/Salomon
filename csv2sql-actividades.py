from csv import *
from sys import argv,exit

tabledir="tmp/EspaciosFacultad/"
basename="Salomon-BasesDatos"

#SIMPLE
tablas=["Programas","Dependencias"]
for tabla in tablas:
    fl=open(tabledir+basename+"-%s.csv"%(tabla),"rU")
    data=reader(fl,delimiter=";")
    i=0
    print "use salomon_1401;"
    for row in data:
        if i==0:
            fields=",".join(row)
            campos="(%s)"%fields
        else:
            valores="('"+"','".join(row)+"')"
            sql="insert into %s %s values %s;"%(tabla,campos,valores)
            print sql
        i+=1

#ESPACIOS

#PROGRAMACION
