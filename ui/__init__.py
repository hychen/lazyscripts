#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gettext
import locale
import time
import thread

import pygtk
pygtk.require('2.0')
import gtk, gobject, vte
import os, sys
import xml.sax
from lazyscripts.script import ScriptsList, ScriptSet, ScriptsRunner
import lazyscripts.ui.utils
from lazyscripts import info

from lazyscripts.ui.gui import query_yes_no, show_error
from lazyscripts.util import detect
distro, codename = info.get_distro()

from lazyscripts.util import package_repository
from os import path as os_path

try:
    locale.setlocale (locale.LC_ALL, "")
except:
    locale.setlocale (locale.LC_ALL, "en_US.UTF-8")

APP_NAME = "lazyscripts"
APP_PATH = os.path.abspath (os_path.dirname (__file__) + '/../')
LOCALE_DIR = os.path.join (APP_PATH, 'locale')

gettext.textdomain(APP_NAME)
gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
_ = gettext.gettext

def create_network_dialog ():
    dlg = gtk.MessageDialog \
        (None, gtk.DIALOG_MODAL,  \
        gtk.MESSAGE_QUESTION, \
        gtk.BUTTONS_OK_CANCEL)

    dlg.set_markup (_('<b>Lazyscripts need internet connection to execute,') +
                    _('please select type of internet connection: </b>'))

    other_btn = \
        gtk.RadioButton (None, 
            _('Open netowrk manager to connect to internet'))
    dlg.vbox.pack_start (other_btn, False, True, 2)

    no_btn = gtk.RadioButton (other_btn, 
        _('I already connect to internet') +
        _(', i don\'t need any other configuration \n'))

    no_btn.set_active (True)
    dlg.vbox.pack_start (no_btn, False, True, 2)
    dlg.vbox.show_all ()
    return dlg, other_btn

def ensure_network ():
    ''' test availibility of network connection '''
    distro, codename = info.get_distro()

    if detect.test_network () == True:
        return True;

    dlg, other_btn = create_network_dialog ()
    ret = dlg.run ()
    use_other = other_btn.get_active ()
    dlg.destroy ()

    if ret != gtk.RESPONSE_OK:
        return False

    # update GUI
    while gtk.events_pending ():
       gtk.main_iteration ()

    if use_other:
        os.system('/usr/bin/nm-connection-editor')

    return detect.test_network ()   # test again after settings

def ensure_apt_sources():
    msg =_("""
we need to modify your software sources,
do you want to let lazyscripts modify your software sources?
""")
    if query_yes_no (msg):
        package_repository.add_official_repos ()
        #os.system ('scripts/add_official_repos.py');
    else:
        show_error (_('Lazyscripts will not change your settings') +
                    _('please ensure your software sources right\n\n') +
                    _('comment: please enable main, universe, ') +
                    _('multiverse and restricted section'))

        # update GUI
        while gtk.events_pending ():
           gtk.main_iteration ()
        os.system ('software-properties-gtk');

class Tool:
    def __init__ (self, script, used=True):
        self.used = used
        self.script = script

class ToolPage:
    def __init__ (self):
        self.tools = []

    def get_widget (self):
        # columns: used or not, description, tool object
        self.list = gtk.ListStore \
                    (gobject.TYPE_BOOLEAN, gobject.TYPE_STRING, \
                    gobject.TYPE_PYOBJECT)

        list = self.list
        view = gtk.TreeView ()
        view.set_rules_hint (True)
        view.get_selection().set_mode(gtk.SELECTION_NONE)

        render = gtk.CellRendererToggle ()
        render.set_property ('activatable', True)
        render.set_property ('width', 20)
        render.connect ('toggled', self.on_toggled, list)
        col = gtk.TreeViewColumn ()
        col.pack_start (render)
        col.set_attributes (render, active=0)
        view.append_column (col)

        col = gtk.TreeViewColumn (_("items"))
        render=gtk.CellRendererText ()
        col.pack_start (render)
        col.set_attributes (render, markup=1)
        view.append_column (col)

        for tool in self.tools:
            list.append ((tool.used, ("<b>%s</b>：\n%s" % (tool.script.name, tool.script.desc)), tool))

        view.set_model (list)
        view.show ()
        return view

    def on_toggled (self, render, path, list):
        it = list.get_iter_from_string(path)
        used, tool = list.get (it, 0, 2)
        tool.used = not used
        list.set (it, 0, not used)

    def get_command_lines(self):
        lines=[]
        for tool in self.tools:
            if tool.used == True and tool.command:
                lines.append("echo\necho '\x1b[1;33m%s\x1b[m'\necho\n" % tool.title)
                lines.append(tool.command+'\n')
        return lines

class WelcomePage:
    def get_widget(self):
        view=gtk.Viewport()
        label=gtk.Label()
        label.set_markup(
            _('<b><big>Lazyscripts - Linux lazy pack') +
            _(', Linux end user\'s good friend</big></b>\n\n\n') +
            _('Copyright (C) 2007, Design and developed by PCMan, Yuren Ju, hychen and billy\n\n') +
            _('Project Lazyscripts - ') +
            _('<span color="blue">http://sites.google.com/site/lazyscripts/</span>'))

        view.add(label)
        view.show_all()
        return view


class FinalPage:
    def get_widget(self):
        hbox=gtk.HBox(False, 0)
        term=vte.Terminal()
        term.set_scrollback_lines(65535)    # Will this value be too big?
        term.feed(_('execute action: \n'))
        term.set_cursor_blinks(True)
        self.term=term
        scroll=gtk.VScrollbar( term.get_adjustment() )
        hbox.pack_start( term, True, True, 0 )
        hbox.pack_start( scroll, False, True, 0 )

        view=gtk.Viewport()
        view.add(hbox)
        view.show_all()
        return view

class ToolListWidget:
    def __init__(self, win):
        self.all_tools = []
        self.win = win

        hbox = gtk.HBox(False, 2)
        self.hbox = hbox

        # left pane
        tree = gtk.TreeView()
        self.left_pane = tree
        scroll = gtk.ScrolledWindow()
        scroll.add(tree)
        scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        hbox.pack_start(scroll, False, True, 2)

        render=gtk.CellRendererPixbuf()
        render.set_property('stock-size', gtk.ICON_SIZE_LARGE_TOOLBAR)
        col=gtk.TreeViewColumn(None, render, icon_name=0)
        render=gtk.CellRendererText()
        col.pack_start(render)
        col.set_attributes(render, text=1)
        tree.append_column(col)
        tree.set_headers_visible(False)

        list = gtk.ListStore \
            (gobject.TYPE_STRING, gobject.TYPE_STRING, \
            gobject.TYPE_PYOBJECT)
        self.list=list
        self.load_tree(list)

        tree.set_model(list)

        sel=tree.get_selection()
        sel.connect('changed', self.on_category_changed)

        # right pane
        scroll=gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scroll.set_shadow_type(gtk.SHADOW_IN)
        hbox.pack_start(scroll, True, True, 2)
        self.right_pane=scroll

        hbox.show_all()

    def download_scripts (self, lock):
        scripts_list = ScriptsList.get_by_detect()
        scripts_list.update()
        self.script_set = ScriptSet.from_scriptslist(scripts_list)
        lock.release ()

    def load_tree(self, list_store):
        loc = locale.getlocale (locale.LC_ALL)
        lzs_loc = ""
        if (loc[0] == None):
            lzs_loc = "enUS"
        else:
            lzs_loc = loc[0].replace ("_", "")

        dlg = gtk.MessageDialog \
                (None, gtk.DIALOG_MODAL, \
                gtk.MESSAGE_INFO, \
                gtk.BUTTONS_NONE)
        dlg.set_markup ( _("Please waiting for download scripts."))
        dlg_progress = gtk.ProgressBar ()
        dlg_progress.grab_focus ()
        dlg.vbox.pack_start (dlg_progress, False, True, 2)
        dlg.show_all ()

        lock = thread.allocate_lock ()
        lock.acquire ()
        t = thread.start_new_thread (self.download_scripts, (lock,))

        while lock.locked ():
            while gtk.events_pending ():
                gtk.main_iteration ()
            time.sleep (0.15)
            dlg_progress.pulse ()
        while gtk.events_pending ():
            gtk.main_iteration ()

        dlg.destroy ()

        for category in self.script_set.categories():
            category.lang = lzs_loc
            tool_page = ToolPage()
            tool_page.title = category.name
            tool_page.img = category._icon_name

            for script in category.items():
                tool = Tool (script, script.selected)
                tool_page.tools.append(tool)

            tool_page.get_widget()
            list_store.append( (tool_page.img, tool_page.title, tool_page) )
            self.all_tools.append(tool_page)

    def get_widget(self):
        return self.hbox

    def on_category_changed(self, sel):
        list, it=sel.get_selected()
        tool=list.get(it, 2)
        old=self.right_pane.get_child()
        if old != None:
            self.right_pane.remove(old)
        self.right_pane.add(tool[0].get_widget())

class MainWin:
    def __init__(self):

        win=gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_title(_('Lazyscripts - Linux lazy pack'))
        try:
            self.icon=gtk.icon_theme_get_default().load_icon('gnome-app-install', 48,0)
        except:
            # print "No gnome-app-install icon"
            self.icon = None
        if self.icon:
            win.set_icon(self.icon)
        win.connect('delete_event', self.on_close)

        vbox=gtk.VBox(False, 2)
        win.add(vbox)

        # upper parts: main GUI
        self.tool_list=tool_list=ToolListWidget(win)
        tool_list.list.insert( 0, ('lazyscripts', _('Welcome'), WelcomePage()) )
        self.final_page=FinalPage()
        tool_list.list.append( ('gnome-app-install', _('fininsh'), self.final_page) )
        sel=tool_list.left_pane.get_selection()
        sel.select_path('0')

        vbox.pack_start(tool_list.get_widget(), True, True, 2)

        # buttons at bottom
        hbox=gtk.HBox(False,2)
        btn=gtk.Button(stock=gtk.STOCK_ABOUT)
        btn.connect('clicked', self.on_about)
        hbox.pack_start(btn, False, True, 2)

        btn=gtk.Button(stock=gtk.STOCK_APPLY)
        btn.connect('clicked', self.on_apply)
        hbox.pack_end(btn, False, True, 8)
        self.apply_btn=btn

        btn=gtk.Button(stock=gtk.STOCK_CANCEL)
        self.cancel_btn=btn
        btn.connect('clicked', self.on_cancel)
        hbox.pack_end(btn, False, True, 8)

        btn=gtk.Button(stock=gtk.STOCK_CLEAR)
        self.clear_btn=btn
        btn.connect('clicked', self.on_clear)
        hbox.pack_end(btn, False, True, 8)

        vbox.pack_start(hbox, False, True, 2)

        win.set_default_size( 720, 540 )
        win.show_all()
        self.win=win

        self.pid=-1
        self.complete=False

    def confirm_close(self):
        if self.complete or query_yes_no(_('do you want to quit lazyscripts?'), self.win):
            gtk.main_quit()
            return True
        return False

    def on_close(self, w, evt):
        return self.confirm_close()

    def on_cancel(self, btn):
        self.confirm_close()

    def on_about(self, item ):
        dlg = gtk.AboutDialog()
        dlg.set_name('Lazyscripts')
        dlg.set_version("0.1")
        dlg.set_website('http://TBD/')
        if self.icon:
            dlg.set_logo(self.icon)
        dlg.set_authors(['洪任諭 (PCMan) <pcman.tw@gmail.com>', '朱昱任 (Yuren Ju) <yurenju@gmail.com>', '林哲瑋 (billy3321,雨蒼) <billy3321@gmail.com>', '陳信屹 (Hychen) <ossug.hychen@gmail.com>'])
        dlg.set_copyright('Copyright (C) 2007 by Lazyscripts project')
        dlg.set_license('GNU General Public License')
        dlg.set_comments(_('Linux Lazy pack'))
        dlg.run()
        dlg.destroy()

    def on_apply(self, btn):
        sel=self.tool_list.left_pane.get_selection()
        list=self.tool_list.left_pane.get_model()
        it=list.iter_nth_child( None, list.iter_n_children(None)-1 )
        sel.select_iter(it)
        self.tool_list.left_pane.set_sensitive(False)
        self.apply_btn.set_sensitive(False)
        self.clear_btn.set_sensitive(False)

        selected_scripts = []
        for page in self.tool_list.all_tools:
            for (used, path, tool) in page.list:
                if used == True:
                    selected_scripts.append(tool.script)

        runner = ScriptsRunner(self)
        runner.run_scripts(selected_scripts)
        self.final_page.term.connect('child-exited', self.on_complete)

    def on_complete(self, data):
        self.final_page.term.feed(_('\n\x1b[1;36mLazyscripts - linux lazy pack run finish!\x1b[1;32m   have fun for linux!\x1b[m\n'))

        self.cancel_btn.set_label(gtk.STOCK_CLOSE)
        self.complete=True
        self.pid=-1

    def on_clear(self, btn):
        for (id, name, category) in self.tool_list.list:
            if category.__class__.__name__ != 'ToolPage':
                continue
            it = category.list.get_iter_first()
            while True:
                if it == None:
                    break
                app = category.list.get(it, 2)
                app[0].used = False
                category.list.set(it, 0, False)
                it = category.list.iter_next(it)
	
class GUI:
	def start(self):
		"""
		launchs the application.
		"""
        if not ensure_network ():
            show_error (_("no avalible internet connection, lazyscripts cannot execute."), _("error"))
            exit(1)

        ensure_apt_sources ()
        MainWin()
        gtk.main()

if __name__ == '__main__':
	GUI().start()
