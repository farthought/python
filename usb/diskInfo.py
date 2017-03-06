#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio, GLib
import gettext
import subprocess
import sys

#gettext.install("diskInfo", "/usr/share/locale")

class DialogInfo:
    def __init__(self, msg, dtype):
        self.msg = msg
        self.dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
                dtype, Gtk.ButtonsType.OK, self.msg)
        self.dialog.set_title("外设连接通知")
        self.dialog.connect("destroy", Gtk.main_quit)
        self.button_ok = self.dialog.vbox.get_children()[1].get_children()[0].get_children()[0]
       # print self.button_ok
        self.button_ok.connect("clicked", Gtk.main_quit)
        self.dialog.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.dialog.show()
    
    def main(self):
        Gtk.main()

class MainProcess:
    def __init__(self):
        self.monitor = Gio.VolumeMonitor.get()
        self.monitor.connect("volume-changed", self._on_volume_changed)
        self.main_loop = GLib.MainLoop.new(None, True)

    def _on_volume_changed(self, widget, volume):
        volume_name = volume.get_name()
        msg = "\t设备 %s 已连接" % volume_name
        dialog = DialogInfo(msg, Gtk.MessageType.INFO)
        dialog.main()
        dialog.dialog.destroy()

if __name__ == "__main__":
    process = MainProcess()
#    Gtk.main()
    process.main_loop.run()



