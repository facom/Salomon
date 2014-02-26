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
jr=1000
print "use salomon_1401;"
for row in data:
    if i==0:
        fields=""
        fields_rec=""
        j=0
        for field in row:
            if field=="recurso_id":
                jr=j
            if j>jr:
                fields_rec+="%s,"%field
            else:
                fields+="%s,"%field
            j+=1
        campos="(%s)"%(fields.strip(","))
        campos_rec="(%srecurso_id,espacio_id)"%(fields_rec)
    else:
        values=""
        values_rec=""
        j=0
        for value in row:
            if j==jr:recursoid=value
            if j>jr:
                values_rec+="'%s',"%value
            else:
                values+="'%s',"%value
            j+=1
        values=values.strip(",")
        values_rec=values_rec+"%s,%s"%(recursoid,recursoid)

        sql="insert into %s %s values (%s);"%(tabla,campos,values)
        print sql
        sql="insert into %s %s values (%s);"%("recursos",campos_rec,values_rec)
        print sql

    i+=1
