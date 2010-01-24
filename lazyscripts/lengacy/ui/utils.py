import gtk, gobject

class Progress:
    def __init__ (self, text):
        self.finished = False
        self.dialog = gtk.Dialog (text)
        vbox = gtk.VBox (False, 2);
        self.progress = gtk.ProgressBar ()
        self.progress.set_text (text)
        self.progress.set_fraction(0.0)
        self.progress.pulse ()
        vbox.add (self.progress)
        timer = gobject.timeout_add \
                (100, self.progress_timeout)
        self.progress.show ()
        vbox.show ()
        self.dialog.show ()

    def progress_timeout(self):
        if self.finished == False:
            self.progress.pulse()
        else:
            gtk.Widget.destroy (self.dialog)
        return True
    def set_finish (self):
        self.finished = True
