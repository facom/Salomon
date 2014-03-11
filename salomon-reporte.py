from salomon import *

#############################################################
#LOAD DATABASE
#############################################################
salomon,connection=loadDatabase(server='localhost',
                     user='salomon',
                     password='123',
                     database='salomon_1401')

#############################################################
#REPORTE
#############################################################
try:
    reporte=argv[1]
except:
    print "Debes indicar un tipo de reporte"
    print "Reportes validos: coincidencias"
    exit(0)

verbose=False
#verbose=True
if reporte=="coincidencias":
    #############################################################
    #COINCIDENCIAS
    #############################################################
    espacios=salomon['Espacios']['rows'].keys()
    mism=dict()

    fr=open("salomon-mismatches.txt","w")
    fr.write("%-12s"%"#0:espacio")
    balance=dict()
    qhead=False

    for espacioid in espacios:
        espacio=salomon['Espacios']['rows'][espacioid]
        d="\t"*0
        print d,"Reportando faltantes de Espacio: %s"%espacioid

        mism[espacioid]=dict()
        recurso=salomon['Recursos']['rows']['R%s'%espacioid]
        i=0
        for reskey in recurso.keys():
            if reskey=='recurso' or reskey=='capacidad':continue
            mism[espacioid][reskey]=0
            if not qhead:
                balance[reskey]=0
                restr=reskey[0:2]+reskey[len(reskey)/2:len(reskey)/2+2]
                restr=reskey[0:2]+reskey[-2:]
                head="%s"%(restr)
                fr.write("%-5s"%head)
            i+=1

        if not qhead:
            fr.write("\n")
            qhead=True

        horarios=espacio['horario_ids'].split(";")
        for horarioid in horarios:
            if horarioid is "":continue
            d="\t"*1
            if verbose:print d,"Mismatch para horario %s"%horarioid
            horario=salomon['Horarios']['rows'][horarioid]
            cid=horario['coincidencia_id']
            coincidencia=salomon['Coincidencias']['rows'][cid]
            rid=coincidencia['recurso_id']
            mismatches=salomon['Recursos']['rows'][rid]
            reskeys=mismatches.keys()                

            
            for reskey in reskeys:
                if reskey=='recurso' or reskey=='capacidad':continue
                result=mismatches[reskey]
                d="\t"*2
                if verbose:print d,"Result for %s: %s"%(reskey,result)
                if result=='No':
                    mism[espacioid][reskey]+=1
        
        fr.write("%-12s"%espacioid)
        for reskey in reskeys:
            if reskey=='recurso' or reskey=='capacidad':continue
            if mism[espacioid][reskey]>0:balance[reskey]+=1
            fr.write("%-5d"%mism[espacioid][reskey])
        fr.write("\n")

        fr.flush()
        if verbose:print mism

    for i in xrange(len(reskeys)-2+2):fr.write("="*5)
    fr.write("\n")

    fr.write("%-12s"%"balance")
    for reskey in reskeys:
        if reskey=='recurso' or reskey=='capacidad':continue
        fr.write("%-5d"%balance[reskey])
    fr.write("\n")

    fr.write("\n")
    for reskey in reskeys:
        if reskey=='recurso' or reskey=='capacidad':continue
        restr=reskey[0:2]+reskey[-2:]
        fr.write("%s = %s\n"%(restr,reskey))
        
    fr.close()
        
else:
    if verbose:print "Reporte '%s' desconocido..."%reporte


