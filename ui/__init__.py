#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2007 洪任諭 Hong Jen Yee (PCMan) <pcman.tw@gmail.com>
# Released under GNU General Public License

import pygtk
pygtk.require('2.0')
import gtk, gobject, vte
import os, sys
import xml.sax
from lazyscript.script import ScriptsList, ScriptSet
#from lazyscript.script import ScriptsRunner

from lazyscript.ui.gui import query_yes_no, show_error
from lazyscript.util import detect

def connect_test ():    # Dirty trick used to test if the network connection is available
    ''' test availibility of network connection '''
    zenity_cmd = "zenity --progress --text='測試網路中' --pulsate --auto-close"
    websites=['http://www.google.com/', 'http://tw.archive.ubuntu.com/']
    for website in websites:
        if os.system ("wget --tries=2 --timeout=120 -O -" +
                        "%s >/dev/null 2>&1 | %s" % (website, zenity_cmd)) == 0:
            return True
    return False

def ensure_network ():
    ''' test availibility of network connection '''
    distro, codename = detect.get_distro()

    if connect_test () == True:
        return True;
    elif distro == 'Debian':
        return False;

    dlg = gtk.MessageDialog \
        (None, gtk.DIALOG_MODAL,  \
        gtk.MESSAGE_QUESTION, \
        gtk.BUTTONS_OK_CANCEL)

    dlg.set_markup ('<b>Lazyscript 需要網路才能執行，' +
                    '請選擇你使用的網路種類：</b>')

    adsl_btn=gtk.RadioButton (None, 
        '使用需要使用者名稱與密碼的寬頻連線來連線\n' +
        ' (需要帳號密碼的 ADSL 請選擇此項，' + 
        '例如浮動 IP 的 Hinet ADSL)')

    if codename != "hardy" and codename != 'intrepid':
        dlg.vbox.pack_start (adsl_btn, False, True, 2)

    other_btn = \
        gtk.RadioButton (adsl_btn, 
            '透過其他方式' +
            '- DHCP 自動取得、固定 IP、' +
            '或是數據機電話撥接...\n' +
            '( 固定 IP 的 ADSL，視服務業者' +
            '，有可能需要使用此項，例如 Hinet, So-net)')

    dlg.vbox.pack_start (other_btn, False, True, 2)

    no_btn = gtk.RadioButton (adsl_btn, 
        '我已連接到網際網路，' +
        '不需要額外設定\n ' +
        '(使用無線網路，' +
        '請點選螢幕右上角工作列中' + 
        '的無線網路圖示，即可連線)')

    no_btn.set_active (True)
    dlg.vbox.pack_start (no_btn, False, True, 2)
    dlg.vbox.show_all ()

    ret = dlg.run ()
    use_adsl = adsl_btn.get_active ()
    use_other = other_btn.get_active ()
    dlg.destroy ()

    if ret != gtk.RESPONSE_OK:
        return False

    # update GUI
    while gtk.events_pending ():
       gtk.main_iteration ()

    if use_adsl:
        os.system('scripts/pppoeconf')
        os.system('pon dsl-provider')
    elif use_other:
        os.system('network-admin')

    return connect_test()    # test again after settings


def ensure_apt_sources():
    msg ="""
使用 Lazyscript，需要正確設定系統上的 APT 軟體套件來源，
才有辦法正確從網路上安裝各種軟體。
Lazyscript 將會嘗試加入你的國家/地區的區域性伺服器。\n
你是否願意讓 Lazybuntu 修改你的套件庫設定？
"""
    if query_yes_no (msg):
        os.system ('scripts/add_official_repos.py');
    else:
        show_error ('Lazybuntu 不會變更你的設定，' +
                    '請自行妥善設定你的套件庫。\n\n' +
                    '提示：請開啟 main, universe, ' +
                    'multiverse, 及 restricted')

        # update GUI
        while gtk.events_pending ():
           gtk.main_iteration ()
        os.system ('software-properties-gtk');

class Tool:
    def __init__ (self, title, command, used=True):
        self.title = title
        self.desc = ''
        self.command = command
        self.used = used

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
        render.connect ('toggled', self.on_toggled, list)
        col = gtk.TreeViewColumn ('可選用的項目')
        col.pack_start (render)
        col.set_attributes (render, active=0)

        render=gtk.CellRendererText ()
        col.pack_start (render)
        col.set_attributes (render, markup=1)
        view.append_column (col)

        for tool in self.tools:
            list.append ((False, ("<b>%s</b>：\n%s" % (tool.name, tool.desc)), tool))

        view.set_model (list)
        view.show ()
        return view

    def on_toggled (self, render, path, list):
        # print "toggled"
        it=list.get_iter_from_string(path)
        used, tool=list.get(it, 0, 2)
        #tool.used = not used
        list.set( it, 0, not used )

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
            '<b><big>Lazybuntu - Ubuntu 懶人包' +
            '，Linux 新手的好朋友</big></b>\n\n' +
            '幫你解決安裝後煩人的小設定，安裝一些好用軟體，\n' +
            '省去在茫茫網海中搜尋的時間。\n\n' +
            '請從左邊的清單中，點選各個分類，選擇你要套用的項目。\n\n\n' +
            'Copyright (C) 2007, Design and developed by PCMan and Yuren Ju\n' +
            'Powered by Ubuntu Taiwan Community\n\n' +
            'Project Lazybuntu - ' +
            '<span color="blue">http://lazybuntu.openfoundry.org/</span>')

        view.add(label)
        view.show_all()
        return view


class FinalPage:
    def get_widget(self):
        hbox=gtk.HBox(False, 0)
        term=vte.Terminal()
        term.set_scrollback_lines(65535)    # Will this value be too big?
        term.feed('要執行的動作：\r\n')
        term.set_cursor_blinks(True)
        self.term=term
        scroll=gtk.VScrollbar( term.get_adjustment() )
        hbox.pack_start( term, True, True, 0 )
        hbox.pack_start( scroll, False, True, 0 )

        view=gtk.Viewport()
        view.add(hbox)
        view.show_all()
        return view


class XmlLoader(xml.sax.ContentHandler):
    def __init__(self, list):
        self.cur_cat=None
        self.cur_tool=-1
        self.list=list

    def startElement(self, name, attrs):
        if name=='category':
            self.cur_cat = ToolPage()
            self.cur_cat.title=attrs['title']
            self.cur_cat.img=attrs['image']
        elif name=='tool':
            tool=Tool(attrs['title'], attrs['command'], attrs['used']=='1' )
            self.cur_cat.tools.append(tool)
            self.cur_tool=len(self.cur_cat.tools)-1

    def endElement(self, name):
        if name=='category':
            self.list.append(self.cur_cat)
        elif name=='tool':
            self.cur_cat.tools[self.cur_tool].desc=self.cur_cat.tools[self.cur_tool].desc.strip()
            self.cur_tool=-1

    def characters(self, text):
        if self.cur_tool != -1:
            self.cur_cat.tools[self.cur_tool].desc +=text


class ToolListWidget:
    def __init__(self, scripts_list_file):
        self.all_tools = []

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

        list=gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
        self.list=list
        self.load_tree(list, scripts_list_file)

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

    def load_tree(self, list_store, scripts_list_file):
        scripts_list = ScriptsList(scripts_list_file)
        scripts_list.update()
        script_set = ScriptSet.from_scriptslist(scripts_list)
        for category in script_set.categories():
            tool_page = ToolPage()
            tool_page.title = category.name
            tool_page.img = None

            for script in category.items():
                tool_page.tools.append(script)

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


class GamesPage(ToolListWidget):
    def __init__(self):
        ToolListWidget.__init__(self, 'ui/games.xml')
        view=gtk.Viewport()
        widget=ToolListWidget.get_widget(self)
        sel=self.left_pane.get_selection()
        sel.select_path("0")
        view.add(widget)
        view.show_all()

        # We need to keep the object to hold a reference;
        # otherwise, this widget will be destroyed
        # when removed from scrolled window.
        self.view_port=view

    def get_widget(self):
        return self.view_port


class MainWin:
    def __init__(self):

        win=gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_title('Lazybuntu - Ubuntu 懶人包')
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
        self.tool_list=tool_list=ToolListWidget('scripts.list')
        tool_list.list.insert( 0, ('ubuntu', '歡迎使用', WelcomePage()) )
        #self.games_page=GamesPage()
        #tool_list.list.append( ('applications-games', '各種遊戲', self.games_page) )
        self.final_page=FinalPage()
        tool_list.list.append( ('gnome-app-install', '完成', self.final_page) )
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
        if self.complete or query_yes_no('確定要結束程式？', self.win):
            gtk.main_quit()
            return True
        return False

    def on_close(self, w, evt):
        return self.confirm_close()

    def on_cancel(self, btn):
        self.confirm_close()

    def on_about(self, item ):
        dlg = gtk.AboutDialog()
        dlg.set_name('Lazybuntu')
        dlg.set_version(VERSION)
        dlg.set_website('http://lazybuntu.openfoundry.org/')
        if self.icon:
            dlg.set_logo(self.icon)
        dlg.set_authors(['洪任諭 (PCMan) <pcman.tw@gmail.com>', '朱昱任 (Yuren Ju) <yurenju@gmail.com>', '林哲瑋 (billy3321,雨蒼) <billy3321@gmail.com>'])
        dlg.set_copyright('Copyright (C) 2007 by Lazybuntu project')
        dlg.set_license('GNU General Public License')
        dlg.set_comments('台灣社群專用 Ubuntu 懶人包')
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
            for (used, path, script) in page.list:
                if used == True:
                    selected_scripts.append(script)

        #ScriptsRunner.run_scripts(self.final_page.term, selected_scripts)
        # hychen! here is your block!! start
        # temp dir
        """
        tmpdir='temp'
        if not os.path.exists(tmpdir):
            os.mkdir(tmpdir, 0777)

        script_name="%s/lazybuntu_apply.sh" % tmpdir
        f=open(script_name, 'w')

        # FIXME: working network should be available before this line
        f.write ("#!/bin/bash\n\n")
        f.write( "apt-get update\n" )    # This is required
        f.write( ". temp/env-export.sh\n" )    # This is required

        for page in self.tool_list.all_tools:
            f.writelines( page.get_command_lines() )
        for page in self.games_page.all_tools:
            f.writelines( page.get_command_lines() )
        # Dirty hack: fix permission problems of unknown cause...
        f.write( "echo '\x1b[1;33m正在修正檔案權限問題，請稍候...\x1b[m'\nscripts/fix-perms\n" )
        f.write( "update-desktop-database\n" )
        f.close()
        os.chmod(script_name, 0775)

        self.pid = self.final_page.term.fork_command( "%s/%s" % (os.getcwd(), script_name) )
        """
        #hychen!! here is your block!! end
        self.final_page.term.connect('child-exited', self.on_complete)

    def on_complete(self, data):
        self.final_page.term.feed('\r\n\x1b[1;36mLazyscripts - Linux 究極懶人包，執行完畢！ 你的系統現在應該很好用了！\r\n\r\n某些設定可能不會馬上有效，建議重新開機。\x1b[1;32m   祝玩 Linux 愉快！\x1b[m\r\n')

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
		MainWin()
		gtk.main()

if __name__ == '__main__':
	GUI().start()
