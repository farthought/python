#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 中文编码支持“# -*- coding: utf-8 -*-”必须加到第一行或第二行

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class mywindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        str = "Gte(G)"
        format = "<span foreground=\"red\" style=\"italic\">%s</span>"
        strformat = format % str
        self.entry = Gtk.Entry()
        self.entry2 = Gtk.Entry()
        self.entry3 = Gtk.Entry()
        self.label = Gtk.Label()
        self.label.set_markup(strformat)
        self.label2 = Gtk.Label("Hte(H)") 
        #使用助记符给标签设置助记符，并设置关联插件
        self.label3 = Gtk.Label.new_with_mnemonic("_Ete(E)")
        self.label3.set_mnemonic_widget(self.entry3)
        self.button = Gtk.Button(label="button(e)")
        self.button2 = Gtk.Button(label="button2(f)")
        
        #使用助记符给按钮设置快捷键
        self.button3 = Gtk.Button.new_with_mnemonic("_Kick(k)")
        
        #使用组合器设置热键
        gag = Gtk.AccelGroup.new()
        #Gtk.Widget.add_accelerator(self.button,"clicked",gag,69, Gdk.ModifierType.MOD1_MASK,Gtk.AccelFlags.VISIBLE)
        self.button.add_accelerator("clicked",gag,Gdk.KEY_e, Gdk.ModifierType.MOD1_MASK,
                Gtk.AccelFlags.VISIBLE)
        self.button2.add_accelerator("clicked",gag,Gdk.KEY_f, Gdk.ModifierType.MOD1_MASK,Gtk.AccelFlags.VISIBLE)
        self.entry.add_accelerator("activate",gag,Gdk.KEY_g, Gdk.ModifierType.MOD1_MASK,Gtk.AccelFlags.VISIBLE)
        self.entry2.add_accelerator("activate",gag,Gdk.KEY_h, Gdk.ModifierType.MOD1_MASK,Gtk.AccelFlags.VISIBLE)
        self.button.connect("clicked",self.on_button_clicked)
        self.button2.connect("clicked",self.on_button_clicked2)
        self.button3.connect("clicked",self.on_button_clicked3)
        self.entry.connect("activate",self.on_entry_focus_in)
        self.entry2.connect("activate",self.on_entry2_focus_in)
        self.entry3.connect("focus-in-event", self.on_entry3_focus_in)

        self.box = Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        self.box2 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,0)
        self.box3 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,0)
        self.box4 = Gtk.Box.new(Gtk.Orientation.HORIZONTAL,0)

        self.box2.add(self.label)
        self.box2.add(self.entry)
        self.box3.add(self.label2)
        self.box3.add(self.entry2)
        self.box4.add(self.label3)
        self.box4.add(self.entry3)

        self.box.add(self.button)
        self.box.add(self.button2)
        self.box.add(self.button3)
        self.box.add(self.box2)
        self.box.add(self.box3)
        self.box.add(self.box4)

#        self.box.pack_start(self.button, True, True, 0)
#        self.box.pack_start(self.button2, True, True, 0)
#        self.box.pack_start(self.entry, True, True, 0)
#        self.box.pack_start(self.entry2, True, True, 0)
#        self.box.pack_start(self.button, True, True, 0)
#        self.box.pack_start(self.button, True, True, 0)

        self.add(self.box)
        self.add_accel_group(gag)

    def on_button_clicked(self, widget):
        print("button(e) is clicked")

    def on_button_clicked2(self, widget):
        print("button(f) is clicked")
    
    def on_button_clicked3(self, widget):
        print("Kick(k) is clicked")

    def on_entry_focus_in(self, widget):
        print("entry Gte(G) is select")
        Gtk.Widget.grab_focus(self.entry)

    def on_entry2_focus_in(self,widget):
        print("entry Hte(H) is select")
        Gtk.Widget.grab_focus(self.entry2)
    
    def on_entry3_focus_in(self, widget, event):
        print("entry Ete(E) is select")

win = mywindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
