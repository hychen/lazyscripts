test:
	nosetests -v --with-doctest t/
	make clean
devtest:
	nosetests -s -v --with-doctest t/
clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.*(.*)?.swp' -exec rm -f {} \;
