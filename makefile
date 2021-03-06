clean:
	find . -name "*~" -exec rm -rf {} \;
	rm -rf *.log
	rm -rf *.txt
	rm -rf *.pyc

cleandata:
	rm -rf soluciones/*

cleanall:clean cleandata

commit:
	git commit -am "Commit"
	git push origin master

pull:
	git pull
	chown -R www-data.www-data .

create:
	mysql --user='root' -p < table.sql

populate:
	python salomon-populate.py
