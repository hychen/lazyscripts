TESTDIR='t/'

test:
	nosetests -v --with-doctest ${TESTDIR}
	make clean
devtest:
	nosetests -s -v --with-doctest ${TESTDIR}
clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.*(.*)?.swp' -exec rm -f {} \;

init_testenv:
	# clone lazybuntu scripts for testing.
	git svn clone http://svn.openfoundry.org/lazybuntu/trunk/scripts `./lsc repo sign http://svn.openfoundry.org/lazybuntu/trunk/scripts ${TESTDIR}datas/scriptpoll/`
