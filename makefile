clean:
	find . -name "*~" -exec rm -rf {} \;

cleandata:
	rm -rf soluciones/*

commit:
	git commit -am "Commit"
	git push origin master

create:
	mysql --user='root' -p < spasig.sql

