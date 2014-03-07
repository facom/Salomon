from salomon import *
from csv import *

tabledir=CSVLOCATION
basename=BASENAME

con=mdb.connect("localhost",USER,PASSWORD,DATABASE)
db=con.cursor()

verbose=False
#verbose=True

with con:

    ##################################################
    #RESET
    ##################################################
    for table in ["Dependencias","Programas","Espacios",
                  "Recursos","Actividades","Horarios"]:
        print "Truncando tabla %s..."%table
        sql="truncate table %s;"%table
        if verbose:print sql
        db.execute(sql)

    ##################################################
    #PROGRAMAS Y DEPENDENCIAS
    ##################################################
    tablas=["Programas","Dependencias"]
    for tabla in tablas:
        print "Guardando tabla %s..."%tabla
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
                if verbose:print sql
                db.execute(sql)
            i+=1
        fl.close()

    ##################################################
    #ESPACIOS
    ##################################################
    print "Guardando tabla de Espacios..."
    tabla="Espacios"
    fl=open(tabledir+basename+"-%s.csv"%(tabla),"rU")
    data=reader(fl,delimiter=";")
    
    i=0
    jr=1000
    for row in data:
        if row[0]=='INFORME':break
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
            if verbose:print sql
            db.execute(sql)
            sql="insert into %s %s values (%s);"%("Recursos",campos_rec,values_rec)
            if verbose:print sql
            db.execute(sql)
        i+=1
    fl.close()

    ##################################################
    #ACTIVIDADES
    ##################################################
    for programa in ['Fisica','Biologia','Quimica','Matematicas','Facultad']:
    #for programa in ['fisica']:
        print "Guardando las actividades de %s..."%programa
        fl=open(tabledir+basename+"-Actividades-%s.csv"%programa,"rU")
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
                campos="(%s)"%(fields.strip(","))
                campos_hor="(horario,codigo_id,recurso_id,%s)"%(fields_hor.strip(","))
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

                values=values.strip(",")
                values_hor="'%s','%s','%s',"%(horarioid,codigo,horarioid)+values_hor.strip(",")
                values_rec="'%s',"%recursoid+values_rec.strip(",")

                if qinsert:
                    sql="insert into Actividades %s values (%s);"%(campos,values)
                    if verbose:print sql
                    db.execute(sql)
            
                sql="insert into Horarios %s values (%s);"%(campos_hor,values_hor)
                if verbose:print sql
                db.execute(sql)
                sql="insert into Recursos %s values (%s);"%(campos_rec,values_rec)
                if verbose:print sql
                db.execute(sql)
            i+=1
            #if i>5:break

        for curso in cursos.keys():
            sql="update Actividades set horario_ids='%s' where codigo='%s';"%(cursos[curso],curso)
            if verbose:print sql
            db.execute(sql)
