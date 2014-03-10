from salomon import *

#############################################################
#PARAMETERS
#############################################################
verbose1=1
verbose2=0
verbose3=0
verbose4=0
verbose5=0
continuar=False

#AVAILABILITY

#CUPO SCORE
conf=dict2obj(dict())
conf.betaref=1.2
conf.weight_cupo=10.0

#BLOQUE SCORE
conf.weight_bloque=10.0

#COINCIDENCE SCORE
conf.weight_coincidence=10.0

#SCORING 
conf.weight_matching=10.0

#############################################################
#LOAD DATABASE
#############################################################
salomon,connection=loadDatabase(server='localhost',
                     user='salomon',
                     password='123',
                     database='salomon_1401')
print "Hola";
exit(0)
#############################################################
#GET BLOCKS PER PROGRAM
#############################################################
Bloques=dict()
for programa in salomon['Programas']['rows'].keys():
    if verbose5:print "Programa:",programa
    Bloques[programa]=[]
    for dependencia in salomon['Dependencias']['rows'].keys():
        if verbose5:print "\tPrueba dependencia:",dependencia
        progs=salomon['Dependencias']['rows'][dependencia]['programa_ids']
        blocks=salomon['Dependencias']['rows'][dependencia]['bloques']
        if verbose5:print "\tProgramas:",progs
        if programa in progs:
            if verbose5:print "\tPrograma %s en dependencia %s"%(programa,dependencia) 
            Bloques[programa]+=blocks.split(";")[:-1]

#############################################################
#PICKLE PRESENT STATUS OF DATABASE
#############################################################
system("rm -rf soluciones/*")
pickleSalomon("soluciones/salomon-%05d.sal"%(0),salomon)

#############################################################
#GET BLOCKS PER PROGRAM
#############################################################
try:
    Nsol=int(argv[1])
except:
    Nsol=10

random.seed(1)
fsol=open("soluciones/salomon-soluciones.txt","w")
for solution in xrange(1,Nsol+1):
    d="\t"
    if verbose1:print d,"Solution: %d"%solution
    salomon_test=copy.deepcopy(salomon)

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #LOOP OVER SHUFFLED ACTIVITIES
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    actividades=salomon_test['Actividades']['rows'].keys()

    seats_occupied=0
    seats_available=0
    average_efficiency=0

    scoresolution=0
    actividad_count=0
    horario_count=0
    for actividadid in shuffleList(actividades):
        actividad_count+=1;
        actividad=salomon_test['Actividades']['rows'][actividadid]
        d="\t"*2
        nombre=actividad['nombre']
        codigo=actividad['codigo']
        if verbose2:print d,"Actividad %d: %s (%s)"%(actividad_count,nombre,codigo)

        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #GET BLOQUES
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        d="\t"*3                
        programas=splitString(actividad['programa_ids'],";")
        if verbose4:print d,"Programas actividad: ",programas
        bloques=[]
        for programa in programas:
            bloques+=Bloques[programa]
        if verbose4:print d,"Bloques de la dependencia: ",bloques

        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #GET HORARIOS
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        horarioids=splitString(actividad['horario_ids'],";")

        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #LOOP OVER HORARIOS
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #LOOP OVER HORARIOS
        #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        if verbose4:print d,"Probando Horarios:"
        d="\t"*4
        for horarioid in horarioids:
            horario_count+=1;
            rooms=[]
            for hid in horarioids:
                hor=salomon_test['Horarios']['rows'][hid]
                rooms+=[hor['espacio_id']]
            if verbose4:print d,"Rooms asignados a otros horarios: ",rooms

            horario=salomon_test['Horarios']['rows'][horarioid]
            dia=horario['dia']
            hora=int(horario['hora'])
            duracion=int(horario['duracion'])
            horaend=hora+duracion
            recursoid=horario['recurso_id']
            coincidenciaid="A"+horario['recurso_id']
            
            if verbose4:print d,"Dia: ",dia
            if verbose4:print d,"Hora: ",hora
            if verbose4:print d,"Duracion: ",duracion

            #****************************************
            #GET REQUIRED RESOURCES
            #****************************************
            requirements=salomon_test['Recursos']['rows'][recursoid]
            coincidencia=salomon_test['Recursos']['rows'][coincidenciaid]

            cupo=requirements['capacidad']
            if verbose4:print d,"Cupo: ",cupo

            #****************************************
            #LOOP OVER ESPACIOS
            #****************************************
            espaciosids=salomon_test['Espacios']['rows'].keys()
            if verbose4:print d,"Probando espacios:"
            scores=[]
            roomsol=[]
            capsol=[]
            for espacioid in shuffleList(espaciosids):
                espacio=salomon_test['Espacios']['rows'][espacioid]
                d="\t"*4
                if verbose4:print d,"Testing espacio: %s"%espacioid

                bloque=espacio['bloque']
                recursoid=espacio['recurso_id']
                resources=salomon_test['Recursos']['rows'][recursoid]
                capacidad=resources['capacidad']
                horaespacioids=splitString(espacio['horario_ids'],";")
                
                d="\t"*5
                if verbose4:print d,"Bloque: %s"%bloque
                if verbose4:print d,"Capacidad: %s"%capacidad
                if verbose4:print d,"Horarios: ",horaespacioids

                #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                #SCORING
                #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                score=0

                #==================================================
                #CRITERIUM 0: AVAILABILITY
                #==================================================
                d="\t"*6
                unavailable=False
                if len(horaespacioids)!=0:
                    for horaespacioid in horaespacioids:
                        ehorario=salomon_test['Horarios']['rows'][horaespacioid]
                        edia=ehorario['dia']
                        ehora=int(ehorario['hora'])
                        eduracion=int(ehorario['duracion'])
                        ehoraend=ehora+eduracion
                        d="\t"*6
                        if verbose4:print d,"Horario espacio: ",edia,ehora,eduracion
                        if edia==dia:
                            difhora=max(horaend,ehoraend)-min(hora,ehora)
                            d="\t"*7
                            if verbose4:print d,"Diferencia horaria: ",difhora
                            if verbose4:print d,"Duracion combinada: ",duracion+eduracion
                            d="\t"*8
                            if difhora<duracion+eduracion:
                                if verbose4:print d,"No disponible"
                                unavailable=True
                                break
                            else:
                                if verbose4:print d,"Horario no incompatible"
                d="\t"*5
                if unavailable:
                    if verbose4:print d,"Espacio no disponible"
                    continue
                if verbose4:print d,"Espacio disponible"
                
                #==================================================
                #CRITERIUM 1: CAPACITY VS. CUPO
                #==================================================
                d="\t"*5
                u=int(cupo)
                a=int(capacidad)
                
                if a<u:score1=conf.weight_cupo*(1.0-(1.*u)/a)
                else:score1=conf.weight_cupo*(conf.betaref-(1.*a)/u)
                if verbose4:print d,"Score Cupo (u=%d,a=%d):"%(u,a),score1
                score+=score1
                
                #==================================================
                #CRITERIUM 2: VECINDAD
                #==================================================
                if bloque in bloques:
                    score2=+1*conf.weight_bloque
                else:
                    score2=-1*conf.weight_bloque

                if verbose4:print d,"Score vecindad:",score2

                score+=score2
                #==================================================
                #CRITERIUM 3: COURSE COINCIDENCE
                #==================================================
                nmis=0
                for room in rooms:
                    if room=='':continue
                    if espacioid!=room:
                        nmis+=1;
                if nmis>0:
                    score3=-conf.weight_coincidence*1./nmis
                else:score3=0
                if verbose4:print d,"Score coincidencia:",score3
                d="\t"*6
                if verbose4:print d,"Numero de divergencias:",nmis
                
                score+=score3

                #==================================================
                #CRITERIUM 4: MATCHING REQUIREMENTS AND RESOURCES
                #==================================================
                d="\t"*5
                if verbose4:print d,"Scoring matching:"
                reskeys=resources.keys()
                nmatch=0
                nmiss=0
                ncoin=0
                nmiss=0
                ntot=0
                required=True
                for reskey in reskeys:
                    d="\t"*6
                    if reskey=='capacidad' or reskey=='recurso':continue
                    req=requirements[reskey]
                    res=resources[reskey]
                    
                    if reskey=='salacomputo' and res=='1' and req=='0':
                        if verbose4:print d,"Este espacio es sala de computo y no es requerido"
                        required=False
                        break

                    if reskey=='aulalab' and res=='1' and req=='1':
                        if verbose4:print d,"Este espacio es aula laboratorio y tiene valor especial"
                        ncoin+=10
                        break

                    if req=='0':continue                    
                    if verbose4:print d,"Resource %s: Required: %s, Resource: %s"%(reskey,req,res)
                    if res=='1':
                        if verbose4:print d,"Match"
                        ncoin+=1
                    else:
                        if verbose4:print d,"Missmatch"
                        nmiss+=1
                        if reskey=='aulalab' or reskey=='salacomputo':
                            nmiss+=10
                            d="\t"*7
                            if verbose4:print d,"This is not a special room and it is required. Mismatch:",nmiss
                    ntot+=1

                if not required:continue
                if ntot>0:
                    score5=conf.weight_matching*(ncoin-nmiss)/(1.*ntot)
                else:
                    score5=0
                d="\t"*5
                if verbose4:print d,"Scoring resource:",score5
                d="\t"*6
                if verbose4:print d,"Coincidences:",ncoin
                if verbose4:print d,"Missings:",nmiss
                if verbose4:print d,"Total:",ntot

                score+=score5
                #==================================================
                #CRITERIUM 6: SPECIAL CONDITIONS
                #==================================================

                #==================================================
                #TOTAL
                #==================================================
                d="\t"*5
                scores+=[score]
                roomsol+=[espacioid]
                capsol+=[int(capacidad)]
                if verbose4:print d,"TOTAL SCORE:",score

                if verbose4:
                    if not continuar:
                        continuar=raw_input()
                        try:
                            continuar=int(continuar)
                        except:
                            pass
                    else:
                        verbose4=0

                #raw_input()

            #****************************************
            #SOLUTION
            #****************************************
            d="\t"*4
            ibest=np.array(scores).argsort()[::-1][0]
            roombest=roomsol[ibest]
            scorebest=scores[ibest]
            capbest=capsol[ibest]
            cupbest=int(cupo)
            if verbose3:print 
            if verbose3:print d,"Solution Actividad %s (%s) Horario %s: %s (%.2f)"%(actividadid,nombre,horarioid,roombest,scorebest)
            if verbose3:print 

            #****************************************
            #STORE SOLUTION
            #****************************************
            horario['espacio_id']=roombest
            espacio['horario_ids']+='%s;'%horarioid
            scoresolution+=scorebest

            #****************************************
            #COMPUTE EFFICIENCY
            #****************************************
            seats_occupied+=cupbest
            seats_available+=capbest
            efficiency=min(100.,(100.*cupbest)/capbest)
            horario['eficiencia']=efficiency
            horario['puntaje']=scorebest
            average_efficiency+=efficiency

            #****************************************
            #COMPUTE COINCIDENCES
            #****************************************
            espacio=salomon_test['Espacios']['rows'][roombest]
            recursoid=espacio['recurso_id']
            resources=salomon_test['Recursos']['rows'][recursoid]
            reskeys=resources.keys()
            for reskey in reskeys:
                res=resources[reskey]
                req=requirements[reskey]
                if reskey=='recurso':continue
                elif reskey=='capacidad':
                    coincidencia[reskey]=int(res)-int(req)
                else:
                    try:req_int=int(req)
                    except:req_int=0
                    if req_int:
                        if req==res:coincidencia[reskey]='Si'
                        else:coincidencia[reskey]='No'
                    else:
                        if res==req:coincidencia[reskey]='Vacio'
                        else:coincidencia[reskey]='Sobrante'
            """
            print "Requerido:\n",requirements
            print "Recursos:\n",resources
            print "Coincidencia:\n",coincidencia
            exit(0)
            """

            if continuar:
                continuar=raw_input()
                try:
                    continuar=int(continuar)
                except:
                    continuar=1

                if continuar==0:
                    verbose4=True
                elif continuar==2:
                    continuar=False


        #END-COURSE

    d="\t"*2
    if verbose1:print d,"Number of activities:",actividad_count
    if verbose1:print d,"Solution Score:",scoresolution
    globalefficiency=(100.*seats_occupied)/seats_available
    if verbose1:print d,"Global Efficiency: %.1f"%(globalefficiency)
    averageefficiency=(average_efficiency)/horario_count
    if verbose1:print d,"Average Efficiency: %.1f"%(averageefficiency)

    """
    if not continuar and continuar!=3:
        continuar=raw_input()
        try:
            continuar=int(continuar)
        except:
            continuar=False
    else:
        verbose4=False
    #"""
        
    fsol.write("%05d %.3f %.2f %.2f\n"%(solution,scoresolution,globalefficiency,averageefficiency))
    
    pickleSalomon("soluciones/salomon-%05d.sal"%solution,salomon_test)
    del(salomon_test)
    #END-ACTIVIDADES

#END-SOLUTIONS
fsol.close()
