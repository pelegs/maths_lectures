#!/usr/bin/env python3.6
# -*- coding: iso-8859-15 -*-

import numpy as np

try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk, GObject, GLib
	settings = Gtk.Settings.get_default()
	settings.props.gtk_button_images = True
except:
	raise SystemError('Gtk not availble!')
	sys.exit(1)


class Window:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('gui_trans2d.glade')
        self.builder.connect_signals(self)

        self.main_window = self.builder.get_object('main_window')
        self.main_window.show_all()

        self.a11_sp = self.builder.get_object('a11_spinbutton')
        self.a12_sp = self.builder.get_object('a12_spinbutton')
        self.a21_sp = self.builder.get_object('a21_spinbutton')
        self.a22_sp = self.builder.get_object('a22_spinbutton')

        self.A = None

    def quit(self, widget):
        Gtk.main_quit()

    def apply_button_clicked(self, menuitem, data=None):
        a11 = self.a11_sp.get_value()
        a12 = self.a12_sp.get_value()
        a21 = self.a21_sp.get_value()
        a22 = self.a22_sp.get_value()
        self.A = np.array([[a11, a12], [a21, a22]])

    def reset_button_clicked(self, menuitem, data=None):
        self.a11_sp.set_value(1.0)
        self.a12_sp.set_value(0.0)
        self.a21_sp.set_value(0.0)
        self.a22_sp.set_value(1.0)


if __name__ == '__main__':
    main = Window()
    Gtk.main()
