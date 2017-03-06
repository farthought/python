#!/usr/bin/env python2

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class mywindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.button = Gtk.Button(label="Click Here")
        gag = Gtk.AccelGroup.new()
        #Gtk.Widget.add_accelerator(self.button,"clicked",gag,69, Gdk.ModifierType.MOD1_MASK,Gtk.AccelFlags.VISIBLE)
        Gtk.Widget.add_accelerator(self.button,"clicked",gag,Gdk.KEY_e, Gdk.ModifierType.MOD1_MASK,Gtk.AccelFlags.VISIBLE)
        self.button.connect("clicked",self.on_button_clicked)
        self.add(self.button)
        Gtk.Window.add_accel_group(self,gag)

    def on_button_clicked(self, widget):
        print("Hello World")

win = mywindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()
