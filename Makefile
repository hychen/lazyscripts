TESTDIR='t/'
SCRIPTS_REPO	?= git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git

test:
	nosetests -v --with-doctest ${TESTDIR}
	make clean
devtest:
	nosetests -s -v --with-doctest ${TESTDIR}

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.*(.*)?.swp' -exec rm -f {} \;

fetch:
	git clone ${SCRIPTS_REPO} ./scriptspoll/`./lzs repo sign ${SCRIPTS_REPO}` 

init_devenv:
	# clone lazybuntu scripts for testing.
	git clone ${SCRIPTS_REPO} ${TESTDIR}datas/scriptspoll/`./lzs repo sign ${SCRIPTS_REPO}`
