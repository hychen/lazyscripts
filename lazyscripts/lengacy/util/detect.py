from commands import getoutput
import os

def run_asroot():
    """
    checks if the program runs as root.

    @return True if run as root.
    """
    if 'root' == getoutput("whoami"):
        return True

def test_network():
    """
    test availibility of network connection 

    @return True if netwrok is avaliable.
    """
    websites=['http://www.google.com/', 'http://tw.archive.ubuntu.com/']
    for website in websites:
        if os.system ("wget --tries=2 --timeout=120 -O - %s >/dev/null 2>&1" % website) == 0:
            return True
    return False
