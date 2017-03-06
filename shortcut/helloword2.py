#!/usr/bin/env python2

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class mywindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.button = Gtk.Button.new_with_mnemonic("_Clicked here")
        self.button.connect("clicked",self.on_button_clicked)
        self.add(self.button)
    
    def on_button_clicked(self, widget):
        print("Hello World")

win = mywindow()
win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()

