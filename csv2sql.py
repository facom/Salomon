from csv import *
from sys import argv,exit

try:
    tabla=argv[1]
except:
    print "Ninguna tabla pasada."
    exit(0)

dir="tmp/EspaciosFacultad/"
file="%s.csv"%tabla
fl=open(dir+file,"rU")
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
