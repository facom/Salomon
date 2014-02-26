from csv import *
from sys import argv,exit

tabledir="tmp/EspaciosFacultad/"
basename="Salomon-BasesDatos"

#USE
print """use salomon_1401;
truncate table Dependencias;
truncate table Programas;
truncate table Espacios;
truncate table Recursos;
truncate table Actividades;
truncate table Horarios;
"""

"""
#SIMPLE
tablas=["Programas","Dependencias"]
for tabla in tablas:
    fl=open(tabledir+basename+"-%s.csv"%(tabla),"rU")
    data=reader(fl,delimiter=";")
    i=0
    for row in data:
        if i==0:
            fields=",".join(row)
            campos="(%s)"%fields
        else:
            valores="('"+"','".join(row)+"')"
            sql="insert into %s %s values %s;"%(tabla,campos,valores)
            print sql
        i+=1
    fl.close()

#ESPACIOS
tabla="Espacios"
fl=open(tabledir+basename+"-%s.csv"%(tabla),"rU")
data=reader(fl,delimiter=";")

i=0
jr=1000
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
        campos_rec="(%srecurso)"%(fields_rec)
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
        values_rec=values_rec+"'%s'"%(recursoid)

        sql="insert into %s %s values (%s);"%(tabla,campos,values)
        print sql
        sql="insert into %s %s values (%s);"%("Recursos",campos_rec,values_rec)
        print sql

    i+=1

fl.close()
#"""

#"""
#ACTIVIDADES
tabla="Actividades"
#fl=open(tabledir+basename+"-%s.csv"%(tabla),"rU")
fl=open(tabledir+"actividades-fisica.csv","rU")

data=reader(fl,delimiter=";")

i=0
jh=10000
jr=10000
cursos=dict()
first=True
n=0
for row in data:
    if i==0:
        fields=""
        fields_hor=""
        fields_rec=""
        j=0
        kh=0
        kr=0
        for field in row:
            if field=="horario_id":
                hid=j
            if field=="recurso_id":
                rid=j
            if field=="dia":
                jh=j
            if field=="capacidad":
                jr=j
            if j>=jh and kh<3:
                fields_hor+="%s,"%field
                kh+=1
            if j>=jr and kr<100:
                fields_rec+="%s,"%field
                kr+=1
            if kh<=3 and kr<=3 and j<jh:
                if field!='horario_id' and field!="espacio_id" and field!="recurso_id":
                    fields+="%s,"%field
            j+=1
        campos="(recurso_id,%s)"%(fields.strip(","))
        campos_hor="(horario,%s)"%(fields_hor.strip(","))
        campos_rec="(recurso,%s)"%(fields_rec.strip(","))
    else:
        values=""
        values_hor=""
        values_rec=""
        j=0
        horarioid=""
        recursoid=""
        for value in row:
            if j==0:
                codigo=value
                if value not in cursos.keys():
                    n+=1
                    cursos[value]=""
                    qinsert=True
                    """
                    sql="insert into %s (codigo) values ('%s');"%(tabla,value)
                    print sql
                    """
                else:
                    qinsert=False
            if j<jh-3:
                values+="'%s',"%value.strip()
            elif j>=jh and j<jr and 'id' not in value:
                values_hor+="'%s',"%value.strip()
            elif j>=jr and 'id' not in value:
                values_rec+="'%s',"%value.strip()
            else:
                pass
            if j==hid:
                horarioid=value
                cursos[codigo]+="%s;"%horarioid
            if j==rid:
                recursoid=value
            j+=1
        values="'A%s'"%codigo+","+values.strip(",")
        values_hor="'"+horarioid+"',"+values_hor.strip(",")
        values_rec="'"+recursoid+"',"+values_rec.strip(",")

        #sql="delete from %s where codigo='%s';\n"%(tabla,codigo)
        if qinsert:
            sql="select 'Inserting course %d %s';\n"%(n,codigo)
            sql+="insert into %s %s values (%s);"%(tabla,campos,values)
            print sql
        sql="insert into Horarios %s values (%s);"%(campos_hor,values_hor)
        print sql
        sql="insert into Recursos %s values (%s);"%(campos_rec,values_rec)
        print sql
    i+=1
    #if i>5:break

for curso in cursos.keys():
    sql="update Actividades set horario_ids='%s' where codigo='%s';"%(cursos[curso],curso)
    print sql

#"""
