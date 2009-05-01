from lazyscripts import info

def test_distro():
    "test to get the information about current distrobution."
    _info= info.get_distro() 
    if _info[0] not in ('Debian',
                        'Ubuntu',
                        'SUSE LINUX',
                        'openSUSE'):
                        assert 1==0,"the distrobution name\
                                     is no supported by us yet."
