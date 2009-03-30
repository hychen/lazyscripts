TESTDIR='t/'

test:
	nosetests -v --with-doctest ${TESTDIR}
	make clean
devtest:
	nosetests -s -v --with-doctest ${TESTDIR}

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '.*(.*)?.swp' -exec rm -f {} \;

fetch:
	git clone git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git ./scriptspoll/`./lzs repo sign git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git` 

init_devenv:
	# clone lazybuntu scripts for testing.
	git clone git://github.com/billy3321/lazyscripts_pool_debian_ubuntu.git ${TESTDIR}datas/scriptspoll/`./lzs repo sign git://github.com/billy3321/lazyscripts_pool_debian_ubuntu`
