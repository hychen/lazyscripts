from lazyscript import info

def test_distro():
	_info= info.get_distro() 
	assert _info == ('Ubuntu','intrepid'), _info
