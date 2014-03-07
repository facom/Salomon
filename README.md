Salomon
=======

Asignacion de Espacios

Quick start
-----------

Get a copy of from https://github.com/facom/Salomon:

        $ git clone http://github.com/facom/Salomon.git


For contributors
----------------

Generate a public key of your account at the server where you will
develop contributions:
	
	$ ssh-keygen -t rsa -C "user@email"

Upload public key to the github project site
(https://github.com/facom/Salomon). You will need access to the
account where the repository was created.

Configure git:

	$ git config --global user.name "Your Name"
	$ git config --global user.email "your@email"

Get an authorized clone of the master trunk:

        $ git clone git@github.com:facom/Salomon.git

How to use it
-------------

1) Configure and create user "salomon":
   
	$ mysql -u root -p"***" < user.sql
	
   Where "***" is the mysql root password.

2) Choose name for database (e.g. salomon_1401) and grant permissions
   to user "salomon":

   	$ mysql -u root -p"***" < database.sql

3) Change name for database (e.g. salomon_1401) in tables.sql and
   create tables:
   
        $ mysql -u salomon -p"###" < tables.sql

   Where "###" is the mysql salomon user password.

4) Configure user, password, database and CSV source location at
   "salomon.py":

	CSVLOCATION="tmp/EspaciosFacultad/BaseDatos/"
	BASENAME="Salomon"
	DATABASE="salomon_1401"
	USER="salomon"
	PASSWORD="123"   

5) Configure user, password and database at "salomon-configuration.php":

	$DATABASE="salomon_1401";
	$USER="salomon";
	$PASSWORD="123";  

5) Populate tables from csv source data:

   	$ python salomon-populate.py

6) Find solutions:

   	$ python salomon-solucion.py 20
 
   where 20 is the number of solutions searched.

7) Find the best solution checking file
   "soluciones/salomon-soluciones.txt"

8) Load a given solution:

   	$ python salomon-carga.py soluciones/salomon-00001.sal

   where salomon-00001.sal is the solution to load.

9) Navigate in salomon database in a browser with "salomon.php".
