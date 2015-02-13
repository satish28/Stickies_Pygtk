#!/usr/bin/env python

import gtk
import os
import sys
import gobject
import pango
from save_function import save_sticky, get_project_directory
from icons import set_pin_image

class Window(object):

    def __init__(self):

        # window properties
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Stickies")
        self.window.set_size_request(250, 250)
        self.window.move(1100, 100)

        # intialize the filename as None
        self.filename = None

        # vertical box container
        self.vbox = gtk.VBox(False, 0)

        # create a menu bar
        self.menubar = gtk.MenuBar()

        # create a filemenu
        self.filemenu = gtk.Menu()
        self.filemenu_item = gtk.MenuItem("File")
        self.filemenu_item.set_submenu(self.filemenu)
        self.menubar.append(self.filemenu_item)

        # creating about menu
        self.aboutmenu = gtk.Menu()
        self.aboutmenu_item = gtk.MenuItem("About")
        self.aboutmenu_item.set_submenu(self.aboutmenu)
        self.menubar.append(self.aboutmenu_item)
        
        # Menu bar new
        self.new_file = gtk.MenuItem("New")
        self.new_file.connect('activate', self.on_new)
        self.filemenu.append(self.new_file)
        
        # Menu bar open 
        self.open_file = gtk.MenuItem("Open")
        self.open_file.connect('activate', self.on_open)
        self.filemenu.append(self.open_file)

        # Menu bar save
        self.save_file = gtk.MenuItem("Save")
        self.save_file.connect('activate', self.on_save)
        self.filemenu.append(self.save_file)
        
        # Menu bar quit
        self.quit_file = gtk.MenuItem("Quit")
        self.quit_file.connect('activate', self.on_quit)
        self.filemenu.append(self.quit_file)

        # Menu bar about us
        self.about_us = gtk.MenuItem("About Sticky")
        self.about_us.connect('activate', self.on_about)
        self.aboutmenu.append(self.about_us)
        
        # adding accelarator short cuts
        self.accelgroup = gtk.AccelGroup()
        self.window.add_accel_group(self.accelgroup)
        
        # new file short cut
        self.key_new, self.mod_new = gtk.accelerator_parse("<Control>N")
        self.new_file.add_accelerator('activate', self.accelgroup,
                                      self.key_new, self.mod_new, gtk.ACCEL_VISIBLE)
        
        # open file short cut
        self.key_open, self.mod_open = gtk.accelerator_parse("<Control>O")
        self.open_file.add_accelerator('activate', self.accelgroup, 
                                       self.key_open, self.mod_open, gtk.ACCEL_VISIBLE)

        # save file short cut
        self.key_save, self.mod_save = gtk.accelerator_parse("<Control>S")
        self.save_file.add_accelerator('activate', self.accelgroup, 
                                       self.key_save, self.mod_save, gtk.ACCEL_VISIBLE)

        # quit short cut
        self.key_quit, self.mod_quit = gtk.accelerator_parse("<Control>Q")
        self.quit_file.add_accelerator('activate', self.accelgroup, 
                                       self.key_quit, self.mod_quit, gtk.ACCEL_VISIBLE)
        
        #creating toolbar
        self.fixedbar = gtk.Fixed()

	
        # tool bar buttons
        self.new_button = gtk.ToolButton(gtk.STOCK_NEW)
        self.open_button = gtk.ToolButton(gtk.STOCK_OPEN)
        self.save_button = gtk.ToolButton(gtk.STOCK_SAVE)
        self.separator = gtk.SeparatorToolItem()
        self.quit_button = gtk.ToolButton(gtk.STOCK_CLOSE)
        self.about_button = gtk.ToolButton(gtk.STOCK_ABOUT)


	# toggle button 
	self.pin_toggle = gtk.ToggleButton()
	self.pin_toggle.add(set_pin_image())
        self.pin_toggle.connect("clicked", self.on_pin)
	
        # tool bar buttons connections
        self.new_button.connect("clicked", self.on_new)
        self.open_button.connect("clicked", self.on_open)
        self.quit_button.connect("clicked", self.on_quit)
        self.about_button.connect("clicked", self.on_about)
        
        # adding buttons to Toolbar
	self.fixedbar.put(self.new_button, 3, 1)
        self.fixedbar.put(self.open_button, 35 , 1)
 	self.fixedbar.put(self.quit_button, 70, 1)
	self.fixedbar.put(self.about_button, 105, 1)	
	self.fixedbar.put(self.pin_toggle, 140, 4)

        # set the font style.
        self.fontdesc = pango.FontDescription("Purisa 10")
        
        # set the font size
        self.fontdesc.set_size(1024*8)

        # create a scrollable
        self.scroll = gtk.ScrolledWindow()

        # Scroll vertically alone
        self.scroll.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)

        # create a text buffer 
        self.text_buffer = gtk.TextBuffer()
        
        # creating a text view and defining its properties
        self.textview = gtk.TextView(self.text_buffer)
        self.textview.modify_font(self.fontdesc)
        self.textview.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFB2"))
        self.textview.set_wrap_mode(gtk.WRAP_WORD)
        self.textview.set_cursor_visible(True)
        self.scroll.add(self.textview)
        
        # verticalbox container packing the toolbar
        self.vbox.pack_start(self.menubar, False, False, 0)
        self.vbox.pack_start(self.fixedbar, False, False, 0)
        self.vbox.pack_start(self.scroll, True, True, 0)

        # auto save function
        self.buffer_auto = self.textview.get_buffer()
        self.buffer_auto.connect("changed", self.on_save)

        #show window
        self.window.add(self.vbox)
        self.window.connect("destroy", gtk.main_quit)
        self.window.show_all()
    
    # set the icon for the window
    def set_image_as_icon_from_file(self, icon):
        try:
            self.window.set_icon_from_file(icon)
        except Exception, error:
            print error
            sys.exit(1)
    
    # text from the textview
    def get_text_data(self):
        buffer1 = self.textview.get_buffer()
        start, end = buffer1.get_bounds()
        notes = buffer1.get_text(start, end)
        return notes

    # new sticky
    def on_new(self, widget):
        Window().main()

    # open sticky
    def on_open(self, widget):
        open_dialog = gtk.FileChooserDialog("Open..",
                               None,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        open_dialog.set_default_response(gtk.RESPONSE_OK)
        open_dialog.set_current_folder(get_project_directory())
        open_dialog_response = open_dialog.run()
        if open_dialog_response == gtk.RESPONSE_OK:
            open_filename =  open_dialog.get_filename()
            with open(open_filename, "r") as open_file:
                self.filename = open_filename.split("/")[-1]
                data = open_file.read()
                self.text_buffer.set_text(data)
        open_dialog.destroy()

    # save notes
    def on_save(self, widget):
        notes = self.get_text_data()
        saved_file = save_sticky(notes, self.filename)
        self.filename = saved_file

    # pin sticky
    def on_pin(self, widget):
        if widget.get_active():
            self.window.set_keep_above(True)
            self.window.stick()
        else:
            self.window.set_keep_above(False)
            self.window.unstick()

    # Quit window
    def on_quit(self, widget):
        self.window.destroy()

    def on_about(self, widget):
        about_display = gtk.AboutDialog()
        about_display.set_program_name("Sticky Notes")
        about_display.set_version("0.1")
        about_display.set_copyright("(c) Satish")
        about_display.set_comments("Just a sticky note")
        about_display.set_logo_icon_name(None)
        about_display.run()
        about_display.destroy()

    def main(self):
        gtk.main()
        
if __name__ == "__main__":
    gui = Window()
    os.chdir("icons")
    gui.set_image_as_icon_from_file("icon.ico")
    os.chdir("..")
    gui.main()
