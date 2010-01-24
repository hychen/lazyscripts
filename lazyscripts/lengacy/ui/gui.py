import pygtk
pygtk.require('2.0')
import gtk, gobject, vte
import os, sys

def query_yes_no(msg, parent=None):
    """
    ask for yes or no.

    @param msg str message string.
    @param parent
    @return True if the respone is yes.
    """
    return query(msg, \
                gtk.MESSAGE_QUESTION, \
                gtk.BUTTONS_YES_NO,\
                 gtk.RESPONSE_YES)

def query_confirm(msg, parent=None):
    """
    ask for cofirm.

    @param msg str message string.
    @param parent
    @return True if the respone is ok.
    """
    return query(msg,\
                gtk.MESSAGE_QUESTION, \
                gtk.BUTTONS_OK_CANCEL,\
                 gtk.RESPONSE_YES)

def query(msg, msg_type, button_type, assert_res=None, parent=None):
    dlg = gtk.MessageDialog \
        (parent, gtk.DIALOG_MODAL, \
         msg_type, button_type, msg)

    ret = dlg.run ()
    dlg.destroy ()

    if assert_res is None:
        return ret
    else:
        return ret == assert_res

def show_error(msg, title=None, parent=None):
    """
    display error message.

    @param title str the title in dialog.
    @parant
    """
    dlg = gtk.MessageDialog \
            (parent, gtk.DIALOG_MODAL, \
            gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, msg)

    if title:
        dlg.set_title (title)

    dlg.run ()
    dlg.destroy ()

if __name__ == '__main__':
    #query_yes_no('hi')
    #query_confirm('hi')
    pass
