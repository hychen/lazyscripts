from lazyscript import info

def test_distro():
    "test to get the information about current distrobution."
    _info= info.get_distro() 
    assert _info == ('Ubuntu','intrepid'), _info
