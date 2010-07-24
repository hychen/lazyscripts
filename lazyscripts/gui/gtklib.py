#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import time
import thread
import shutil

import pygtk
pygtk.require('2.0')
import gtk, gobject, vte
import os, sys
from lazyscripts import __VERSION__, __WEBURL__
from lazyscripts import env
from lazyscripts import pool as lzspool
from lazyscripts import runner as lzsrunner

#{{{
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
#}}}

#{{{
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
#}}}

#{{{def query(msg, msg_type, button_type, assert_res=None, parent=None):
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
#}}}

#{{{def show_error(msg, title=None, parent=None):
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
#}}}

#{{{def select_defaultpool(poollist):
def select_defaultpool(poollist):
    import re
    show_pools = ""
    for pool in poollist:
        show_pools += 'FALSE %s %s ' % (pool[0],re.escape(pool[1]))

    select_cmd = ' '.join(
                ["zenity",
                "--height=350",
                "--width=600",
                "--list",
                "--title=\"%s\"" % _('gui.gtklib.select_defaultpool.title'),
                "--radiolist",
                "--column \"\"",
                "--column \"%s\"" % _('gui.gtklib.select_defaultpool.poolname'),
                "--column \"%s\"" % _('gui.gtklib.select_default.desc'),
                "%s" % show_pools])
    select_pool = commands.getoutput(select_cmd)
    if not select_pool:
        print _('gui.gtklib.select_defaultpool.abort_with_empty_retrunvalue')
        exit()
    return select_pool
#}}}

#{{{def show_progress(cmd, title, text, percentage, width, autoclose, autokill):
def show_progress(cmd, title, text, percentage, width, autoclose, autokill):
    progress_dialog_cmd = [
        "zenity --progress --title='%s'" % title,
        "--text='%s'" % text,
        "--percentage=%s" % str(percentage),
        "--width=%s" % width]
    if autoclose:
        progress_dialog_cmd.append("--auto-close")
    if autokill:
        progress_dialog_cmd.append("--auto-kill")
    os.system("%s | %s" % (cmd, ' '.join(progress_dialog_cmd)))
#}}}

class Tool:
    #{{{def __init__ (self, script, used=True):
    def __init__ (self, script, used=True):
        self.used = used
        self.script = script
    #}}}
pass

class ToolPage:
    #{{{def __init__ (self):
    def __init__ (self):
        self.tools = []
    #}}}

    #{{{def get_widget (self):
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

        col = gtk.TreeViewColumn (_("gui.gtklib.toolpage.items"))
        render=gtk.CellRendererText ()
        col.pack_start (render)
        col.set_attributes (render, markup=1)
        view.append_column (col)

        for tool in self.tools:
            list.append ((tool.used,
            ("<b>%s</b>：\n%s" % \
            (tool.script.name, tool.script.desc)), tool))

        view.set_model (list)
        view.show ()
        return view
    #}}}

    #{{{def on_toggled (self, render, path, list):
    def on_toggled (self, render, path, list):
        it = list.get_iter_from_string(path)
        used, tool = list.get (it, 0, 2)
        tool.used = not used
        list.set (it, 0, not used)
    #}}}
    #{{{def get_command_lines(self):
    def get_command_lines(self):
        lines=[]
        for tool in self.tools:
            if tool.used == True and tool.command:
                lines.append("echo\necho '\x1b[1;33m%s\x1b[m'\necho\n" % tool.title)
                lines.append(tool.command+'\n')
        return lines
    #}}}
pass

class WelcomePage:
    #{{{def get_widget(self):
    def get_widget(self):
        view=gtk.Viewport()
        label=gtk.Label()
        label.set_markup(
            _('gui.gtklib.welcomepage.markup.desc\n') +
            _('gui.gtklib.welcomepage.markup.copyright\n') % '2010' +
            _('gui.gtklib.welcomepage.markup.project_web_prefix') +
              '<span color="blue">%s</span>' % __WEBURL__)

        view.add(label)
        view.show_all()
        return view
    #}}}
pass

class FinalPage:
    #{{{def get_widget(self):
    def get_widget(self):
        hbox=gtk.HBox(False, 0)
        term=vte.Terminal()
        term.set_scrollback_lines(65535)    # Will this value be too big?
        term.feed(_('gui.gtklib.finalpage.execute_action\n'))
        term.set_cursor_blinks(True)
        self.term=term
        scroll=gtk.VScrollbar( term.get_adjustment() )
        hbox.pack_start( term, True, True, 0 )
        hbox.pack_start( scroll, False, True, 0 )

        view=gtk.Viewport()
        view.add(hbox)
        view.show_all()
        return view
    #}}}
pass

class ToolListWidget:
    #{{{def __init__(self, win):
    def __init__(self, win):
        self.all_tools = []
        self.win = win
        self.recommands_list = win.recommands_list

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
    #}}}

    #{{{def download_scripts (self):
    def download_scripts (self):
        conf = env.resource('config')
        if not self.recommands_list:
            self.pool = env.resource('pool')
        else:
            path = os.path.join(env.resource_name('pools'), conf.get_default('pool'))
            self.pool = lzspool.GitScriptsPool(path, self.win.recommands_list)
    #}}}

    #{{{def load_tree(self, list_store):
    def load_tree(self, list_store):
        self.download_scripts()
        lzs_loc = env.get_local()
        for category in self.pool.categories():
            tool_page = ToolPage()
            tool_page.title = self.pool.get_i18n('category', category, lzs_loc)
            tool_page.img = self.pool.get_iconpath(category)

            for script in self.pool.scripts(category, lzs_loc):
                tool = Tool (script, self.pool.recommand_script(category, script.id))
                tool_page.tools.append(tool)

            tool_page.get_widget()
            list_store.append( (tool_page.img, tool_page.title, tool_page) )
            self.all_tools.append(tool_page)
    #}}}

    #{{{def get_widget(self):
    def get_widget(self):
        return self.hbox
    #}}}

    #{{{def on_category_changed(self, sel):
    def on_category_changed(self, sel):
        list, it=sel.get_selected()
        tool=list.get(it, 2)
        old=self.right_pane.get_child()
        if old != None:
            self.right_pane.remove(old)
        self.right_pane.add(tool[0].get_widget())
    #}}}
pass

class MainWin:
    #{{{def __init__(self):
    def __init__(self, recommands_list=None):
        win=gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.recommands_list = recommands_list
        win.maximize()
        win.set_title(_('gui.gtklib.mainwin.title'))
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
        tool_list.list.insert( 0, ('lazyscripts',
                                    _('gui.gtklib.mainwin.welcome'), WelcomePage()) )
        self.final_page=FinalPage()
        tool_list.list.append( ('gnome-app-install', _('gui.gtklib.mainwin.result'), self.final_page) )
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
    #}}}

    #{{{def confirm_close(self):
    def confirm_close(self):
        if self.complete or query_yes_no(_('gui.gtklib.mainwin.confrim_close'), self.win):
            if os.path.exists('/tmp/lzs_root/'): shutil.rmtree('/tmp/lzs_root/')
            gtk.main_quit()
            return True
        return False
    #}}}

    #{{{def on_close(self, w, evt):
    def on_close(self, w, evt):
        return self.confirm_close()
    #}}}

    #{{{
    def on_cancel(self, btn):
        self.confirm_close()
    #}}}

    #{{{def on_about(self, item ):
    def on_about(self, item ):
        dlg = gtk.AboutDialog()
        dlg.set_name(_('gui.gtklib.mainwin.about.name'))
        dlg.set_version(__VERSION__)
        dlg.set_website(__WEBURL__)
        if self.icon:
            dlg.set_logo(self.icon)
        dlg.set_authors(['洪任諭 (PCMan) <pcman.tw@gmail.com>',
                        '朱昱任 (Yuren Ju) <yurenju@gmail.com>',
                        '林哲瑋 (billy3321,雨蒼) <billy3321@gmail.com>',
                        '陳信屹 (Hychen) <ossug.hychen@gmail.com>',
                        '王綱民(Aminzai) <lagunawang@gmail.com>',
                        '張君平(mrmoneyc) <moneyc.net@gmail.com>'])
        dlg.set_copyright('Copyright (C) 2010 by Lazyscripts project')
        dlg.set_license('GNU General Public License V2')
        dlg.set_comments(_('gui.gtklib.mainwin.about.comments'))
        dlg.run()
        dlg.destroy()
    #}}}

    #{{{def on_apply(self, btn):
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

        runner = lzsrunner.ScriptsRunner(self)
        runner.select_pool(self.tool_list.pool)
        runner.set_scripts(selected_scripts)
        runner.run()
        self.final_page.term.connect('child-exited', self.on_complete)
    #}}}

    #{{{def on_complete(self, data):
    def on_complete(self, data):
        self.final_page.term.feed(_('\ngui.gtklib.mainwin.complete.finished-install\n'))
        if os.path.exists('/tmp/lzs_root/'): shutil.rmtree('/tmp/lzs_root/')

        self.cancel_btn.set_label(gtk.STOCK_CLOSE)
        self.complete=True
        self.pid=-1
    #}}}

    #{{{def on_clear(self, btn):
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
    #}}}
pass

#{{{def startgui(recommands_list=None):
def startgui(recommands_list=None):
    """
    launchs the application.
    """
    MainWin(recommands_list)
    gtk.main()
#}}}
