TESTDIR='t/'

test:
	nosetests -v --with-doctest ${TESTDIR}
	make clean
devtest:
	nosetests -s -v --with-doctest ${TESTDIR}
clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.*(.*)?.swp' -exec rm -f {} \;

init_devenv:
	# clone lazybuntu scripts for testing.
	git clone git://github.com/hychen/scriptpoll.git `./lzs repo sign git://github.com/hychen/scriptpoll.git ${TESTDIR}datas/scriptspoll/`
	git clone git://github.com/billy3321/lazyscript_pool.git `./lzs repo sign git://github.com/billy3321/lazyscript_pool.git ${TESTDIR}datas/scriptspoll/`
