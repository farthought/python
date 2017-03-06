#!/usr/bin/python 
#-*- coding:utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject
import gettext, ConfigParser
from enum import Enum, unique
import list
import pdb

gettext.bindtextdomain('health', "./localedir")
gettext.textdomain('health')
_=gettext.gettext

@unique #装饰器可以帮助我们检查保证没有重复值
class Lock(Enum):
    LOCK_NONE = 0
    LOCK_CAPS = 1

Man = {'BASE':66.4730, 'H_RATIO':5.0033, 'W_RATIO':13.751, 'A_RATIO':6.7650}
Woman = {'BASE':65.0955, 'H_RATIO':1.8496, 'W_RATIO':9.463, 'A_RATIO':4.6756}

# 登录对话框，只有登录之后才能进行之后的操作

class LoginDialog(Gtk.Dialog):
    def __init__(self, title):
        super(LoginDialog, self).__init__()
        self.set_title(title)

        # 读取配置文件，里面存储用户名和密码，用于登录验证。
        self.conf = ConfigParser.ConfigParser()
        self.conf.read("./user.conf")

        table = DimmedTable()
        
        table.add_labels(0, 0, 3, [_("Welcome, please login first")])

        self.username_entry = Gtk.Entry.new()
        self.username_entry.connect("focus-in-event", self._on_entry_focus_in, None)
       
        self.password_entry = Gtk.Entry.new()
        self.password_entry.set_visibility(False)
        #设置caps-lock-warning属性可以关闭密码框后面的图标提示
        self.password_entry.set_property("caps-lock-warning",False)
        self.password_entry.connect("focus-in-event", self._on_entry_focus_in, None)

        table.add_labels(1, 0, 1, [_("Username"), ("Password")])
        table.add_controls(1, 1, 3, [self.username_entry, self.password_entry])
        self.password_label = table.label_list.GetData(2)
        self.password_label.set_text_with_mnemonic(_("_Password"))
        self.password_label.set_mnemonic_widget(table.control_list.GetData(1))

        self.login_fail_label = Gtk.Label()
        self.login_fail_label.set_justify(Gtk.Justification.LEFT)
        table.add_controls(3, 0, 3, [self.login_fail_label])

        self.capslock_label = Gtk.Label()
        self.capslock_label.set_justify(Gtk.Justification.LEFT)
        self.capslock_label.set_alignment(1, 0.5)
        table.add_controls(4, 0, 3, [self.capslock_label]) 

        self.button_login = Gtk.Button.new_with_label(_("login"))
        self.button_exit = Gtk.Button.new_with_label(_("exit"))
        self.button_login.connect("clicked", self._on_button_login_clicked)
        self.button_exit.connect("clicked", self._on_button_exit_clicked)
        table.attach(self.button_exit, 1, 2, 5, 6)
        table.attach(self.button_login, 2, 3, 5, 6)

        self.mode = Lock.LOCK_NONE
        self.keymap = Gdk.Keymap.get_for_display(self.get_display())
        self.keymap.connect("state-changed",self._on_keymap_state_changed)

        self.set_border_width(6)
        box = self.get_content_area()
        box.add(table)
        self.show_all()
    
    # 鉴别用户名和密码
    def _on_button_login_clicked(self, widget):
        user = self.conf.get("user", "1")
        password = self.conf.get("password","1")
        user_input = self.username_entry.get_text()
        password_input = self.password_entry.get_text()
        if((user == user_input) and (password == password_input)):
           self.destroy()
        else:
            self.login_fail_label.set_text(_("Your username or password is wrong, please try again"))

    def _on_button_exit_clicked(self,widget):
        self.destroy()

    def _on_keymap_state_changed(self, widget):
        self.get_kbd_lock_mode()
        self.kbd_lock_mode_update(self.mode.value)

    def get_kbd_lock_mode(self):
        self.mode = Lock.LOCK_NONE
        if(self.keymap.get_caps_lock_state()):
            self.mode = Lock.LOCK_CAPS

    def kbd_lock_mode_update(self, mode):
        if((mode & Lock.LOCK_CAPS.value) != 0):
            self.capslock_label.set_text(_("You have the Caps Lock key on."))
        else:
            self.capslock_label.set_text("")

    def _on_entry_focus_in(self, widget, event, userdata):
        self.login_fail_label.set_text("")
        
class PasswordDialog(Gtk.Dialog):
    def __init__(self):
        table = Gtk.Table(8, 4)
        table.set_border_width(6)
        table.set_row_spacings(8)                                                                                                 
        table.set_col_spacings(15)

class  metabolicDialog(Gtk.Dialog):
    pass

# DimmedTable继承自gtktable

class DimmedTable (Gtk.Table):
    def __init__ (self):
        super(DimmedTable, self).__init__()
        self.set_border_width(6)
        self.set_row_spacings(8)
        self.set_col_spacings(15)
        self.label_list = list.List()
        self.control_list = list.List()
    
    # add_labels向table容器中添加标签
    # row_n：添加标签的起始行
    # begin，end：标签所占的列
    # texts：列表，存储所有的标签
    def add_labels(self, row_n, begin, end, texts):
        row = row_n
        c_begin = begin
        c_end = end
        for text in texts:
            if text != None:
                label = Gtk.Label(text)
                self.label_list.Insert(label)
                label.set_alignment(1, 0.5)
                label.get_style_context().add_class("dim-label")
                self.attach(label, c_begin, c_end, row, row+1, xoptions=Gtk.AttachOptions.EXPAND|Gtk.AttachOptions.FILL)
            row = row + 1
    
    # add_controls相table中添加输入框等可以聚焦的插件
    # row_n：添加插件的起始行
    # begin，end：聚焦插件列位置
    # controls：列表，存储聚焦插件
    def add_controls(self, row_n, begin, end, controls):
        row = row_n
        c_begin = begin
        c_end = end
        for control in controls:
            self.control_list.Insert(control)
            self.attach(control, c_begin, c_end, row, row+1)
            row = row + 1

class EditableEntry (Gtk.Notebook):

    __gsignals__ = {
        'changed': (GObject.SIGNAL_RUN_FIRST, None,
                      (str,))
    }

    PAGE_BUTTON = 0
    PAGE_ENTRY = 1

    def __init__ (self):
        super(EditableEntry, self).__init__()

        self.label = Gtk.Label()
        self.entry = Gtk.Entry()
        self.button = Gtk.Button()

        self.button.set_alignment(0.0, 0.5)
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        self.append_page(self.button, None);
        self.append_page(self.entry, None);
        self.set_current_page(0)
        self.set_show_tabs(False)
        self.set_show_border(False)
        self.editable = False
        self.show_all()

        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY,  "gnome-run");
        self.entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, _("Change the name"))

        self.button.connect("released", self._on_button_clicked)
        self.button.connect("activate", self._on_button_clicked)
        self.entry.connect("activate", self._on_entry_validated)
        self.entry.connect("focus-out-event", self._on_entry_text_changed)
        self.entry.connect("icon-release", self._on_new_name_icon_released)
        self.entry.connect("changed", self._on_entry_changed)

    def _on_new_name_icon_released(self, widget, icon_pos, event):
        self.set_editable(False)
        self.entry.emit("activate")

    def _on_entry_text_changed(self, widget, event):
        self.set_editable(False)
        self.entry.emit("activate")

    def set_text(self, text):
        self.button.set_label(text)
        self.entry.set_text(text)

    def _on_button_clicked(self, button):
        self.set_editable(True)

    def _on_entry_validated(self, entry):
        self.set_editable(False)
        self.emit("changed", entry.get_text())

    def _on_entry_changed(self, entry):
        self.button.set_label(entry.get_text())

    def set_editable(self, editable):
        if (editable):
            self.set_current_page(EditableEntry.PAGE_ENTRY)
        else:
            self.set_current_page(EditableEntry.PAGE_BUTTON)
        self.editable = editable

    def set_tooltip_text(self, tooltip):
        self.button.set_tooltip_text(tooltip)

    def get_editable(self):
        return self.editable

    def get_text(self):
        return self.entry.get_text()

class MainWindow(Gtk.Window):
    def __init__ (self, title):
        super(MainWindow, self).__init__()
        self.set_title(title)
        self.connect("destroy", Gtk.main_quit)
        
        logindialog = LoginDialog(_("System login dialog"))
        logindialog.set_transient_for(self)
        
        self.set_default_size(400,300)
      #  self.set_accept_focus(False)

        self.frame = Gtk.Frame.new(_("Detail information")) 
        self.alignment = Gtk.Alignment.new(0, 0, 0, 0)
        fram_table = DimmedTable()
        fram_table.add_labels(0, 0, 1, [_("Username:"), _("Age:"),_("height(cm):")])
        fram_table.add_labels(0, 4, 5, [ _("sex:"), _("weight(kg):")])
        
        self.username_entry = Gtk.Entry.new()
        self.age_entry = Gtk.Entry.new()
        self.height_entry = Gtk.Entry.new()
        self.sex_entry = Gtk.Entry.new()
        self.weight_entry = Gtk.Entry.new()
        self.cacul_button = Gtk.Button.new_with_mnemonic(_("_Calculation"))
        self.cacul_button.connect("clicked", self._on_cacul_button_clicked)

        fram_table.add_controls(0, 1, 3, [self.username_entry, self.age_entry, self.height_entry])
        fram_table.add_controls(0, 5, 7, [self.sex_entry, self.weight_entry])
        fram_table.add_controls(2, 5, 7, [self.cacul_button])

        
        self.alignment.add(fram_table)
        self.frame.add(self.alignment)

        self.report = Gtk.Label.new()

        main_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 5)
        main_box.pack_start(self.frame,False, False, 5)
        main_box.pack_start(self.report, False, False, 5)
        #fram_hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 5)

        self.add(main_box)

        self.show_all()
    
    def _on_cacul_button_clicked(self, widget):
        flag = 0
        username = self.username_entry.get_text()
        age = float(self.age_entry.get_text())
        height = float(self.height_entry.get_text())
        sex = self.sex_entry.get_text()
        weight = float(self.weight_entry.get_text())
        man_list = ["man", "male", "boy", "男"]
        woman_list = ["woman", "female", "girl", "女"]
        
        for i in man_list:
            if(i == sex):
                basal = Man['BASE'] + Man['H_RATIO'] * height + Man['W_RATIO'] * weight - Man['A_RATIO'] * age
                flag = 1
                break
            else:
                continue
        if(flag == 0):
            for i in woman_list:
                if(i == sex):
                    basal = Woman['BASE'] + Woman['H_RATIO'] * height + Woman['W_RATIO'] * weight - Woman['A_RATIO'] * age
                    flag = 1
                    break
                else:
                    continue
        if(flag == 1):
            self.report.set_text(_("Hello ") + username + ", " +_("your basal metabolic calculation is ") + str(basal) + " Kcal")
        else:
            self.report.set_text(_("Hello ") + username + ", " + _("you input the wrong sex: ") + sex + _(" please check!"))
        
    def cacul_man_basal_metabolic(self, height, weight, age):
        h = height
        w = weight
        a = age 
        basal = Man.BASE.value + Man.H_RATIO.value * h + Man.W_RATIO.value * w - Man.A_RATIO * a
        return basal

if __name__ == "__main__":
    w = MainWindow(_("Basal metabolic calculation"))
    Gtk.main()
