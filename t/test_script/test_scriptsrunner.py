from lazyscripts.script import ScriptsRunner

class Term:

    def fork_command(self):
        pass

class Page:

    def __init__(self):

        self.term = Term()

class Console:
  
    def __init__(self):
        self.final_page = Page()

class MonkScript:

    def __init__(self, name, data):
        self.name = name
        self.id = name
        self.data = data

    def get_subscripts(self):
        pass

    def save(self,path):
        pass

def test_checkout_scripts():
    scs = []
    for i in range(0,5):
        scs.append(MonkScript('ddd'+str(i),"echo "+str(i)))

    runner = ScriptsRunner(ui=Console())
    runner.checkout_scripts(scs)
