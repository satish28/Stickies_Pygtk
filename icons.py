#!/usr/bin/env python

import gtk
import os

# adding the pin icon to the a factory
def insert_factory():
    factory = gtk.IconFactory()
    os.chdir("icons")
    pin_pixbuf = gtk.gdk.pixbuf_new_from_file("pin.png")
    pin_iconset = gtk.IconSet(pin_pixbuf)
    factory.add('pin-icon', pin_iconset)
    factory.add_default()
    os.chdir("..")

#setting the pin image
def set_pin_image():
        pin_image = gtk.Image()
        pin_image.set_from_stock('pin-icon', gtk.ICON_SIZE_MENU) 
        return pin_image
        
    
insert_factory()
