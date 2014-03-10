from salomon import *

salomon_file=argv[1]

#############################################################
#LOAD DATABASE
#############################################################
salomon,connection=loadDatabase(server='localhost',
                                user='salomon',
                                password='123',
                                database='salomon_1401')

#############################################################
#LOAD DATA
#############################################################
print "Unpackaging Salomon database in file '%s'..."%salomon_file
salomon_load=unpickleSalomon(salomon_file)

#############################################################
#SAVE DATABASE
#############################################################
print "Updating database..."
updateDatabase(salomon_load,connection)
