from lazyscripts import get_version

class BaseUI:

    '''
    A command line interface, can be used to debug without
    network connections

    @param engine object BaseBot
    '''
    def __init__(self, engine=None):
        self._engine = engine

    def use(self, engine):
        """
        set engine engine.

        @param engine BaseBot
        """
        self._engine = engine

class CLI(BaseUI):

    def start(self):
        """
        """
        self._show_header()

        from os import getlogin
        while 1:
            msgd = MsgDelta(raw_input('>>> '), author=getlogin())
            response = self._engine.reply(msgd)
            # skip if no respone.
            if response is None:	continue
            # confirm the respone is a message delta always.
            if 'str' == type(response).__name__:
                msgd.set_msg(response)
                msgd.author = self._engine.name
                response = msgd

            self.tell(response)

    def _show_header(self):
        print """Lazyscript TestConsole%s
Type "help" for more information.""" % get_version()

    def quit(self):
        print "stop console interface." 
        from sys import exit
        exit()
