#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path as python_path
from os import path as os_path

# Initial python_path
def init_python_path ():
    dir = os_path.dirname(__file__)+'/../'
    root= os_path.abspath(dir)
    python_path.insert(0, root)

init_python_path ()

import gettext
import locale
import pygtk
pygtk.require('2.0')
import gtk, gobject
import os, sys
from lazyscripts.script import ScriptsList, ScriptSet, ScriptsRunner

def get_root():
	dir = os_path.dirname(__file__)+'/../'
	root= os_path.abspath(dir)
	return root

class Editor:
    def __init__ (self):
        # Model
        self.scripts_liststore = gtk.ListStore \
            (gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)

        self.scripts_list = ScriptsList (get_root()+"/scripts.list")
        self.scripts_list.update ()

        for entry in self.scripts_list.items():
            if not entry.has_key ("selected"):
                entry['selected'] = False
            self.scripts_liststore.append((entry['selected'], entry['name'], entry))

        # View
        self.window = gtk.Window ()
        self.window.set_title ("scripts.list editor")
        self.window.set_size_request (400, 400)

        self.scroll = gtk.ScrolledWindow ()
        self.scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        self.treeview = gtk.TreeView ()
        self.vbox = gtk.VBox (False, 10)

        self.ok_button = gtk.Button ("OK")
        self.ok_button.connect ("clicked", self.on_press_ok, None)

        self.scroll.add (self.treeview)
        self.vbox.pack_start (self.scroll, True, True, 0)
        self.vbox.pack_start (self.ok_button, False, False, 0)
        self.window.add (self.vbox)

        # first column
        render = gtk.CellRendererToggle ()
        render.set_property ('activatable', True)
        render.set_property ('width', 20)
        render.connect ('toggled', self.on_toggled, self.scripts_liststore)
        col = gtk.TreeViewColumn ()
        col.pack_start (render)
        col.set_attributes (render, active=0)
        self.treeview.append_column (col)

        # second column
        col = gtk.TreeViewColumn ("items")
        render=gtk.CellRendererText ()
        col.pack_start (render)
        col.set_attributes (render, markup=1)
        self.treeview.append_column (col)

        self.treeview.set_model (self.scripts_liststore)

        self.treeview.show ()
        self.scroll.show ()
        self.window.show_all ()

        # Controller
        self.window.connect ("destroy", gtk.main_quit)

    def on_toggled (self, render, path, list):
        it = list.get_iter_from_string(path)
        used, entry = list.get (it, 0, 2)
        entry['selected'] = not used
        list.set (it, 0, not used)

    def on_press_ok (self, button, data):
        self.scripts_list.save ()
        gtk.main_quit ()



if __name__ == '__main__':
    editor = Editor ()
    gtk.main ()
