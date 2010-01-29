#!/usr/bin/python

# Copyright (c) 2010 Inderjit Gill
# 
# Released under an MIT license.
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import pygtk
pygtk.require('2.0')
import gtk
import subprocess

class ToggleFullScreen:

  def __init__(self):
    self.statusIcon = gtk.StatusIcon()
    self.statusIcon.set_from_stock(gtk.STOCK_ZOOM_FIT)
    self.statusIcon.set_visible(True)
    self.statusIcon.set_tooltip("Toggle max-screen")

    self.statusIcon.connect('popup-menu', self._on_activate) # right click
    self.statusIcon.connect('activate', self._on_activate)     # left  click
    self.statusIcon.set_visible(True)

    gtk.main()

  def _on_activate(self, *args):
    self.menu = gtk.Menu()

    self.list_windows(self.menu)

    self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
    self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
    self.menu.append(self.menuItem)
    self.menu.show_all()

    self.menu.popup(None, None, gtk.status_icon_position_menu, 3, gtk.get_current_event_time(), self.statusIcon)

  def get_all_window_titles(self):
    process = subprocess.Popen(['wmctrl', '-l'], shell=False, stdout=subprocess.PIPE)
    res = process.communicate()
    windows = res[0].split("\n")[0:-1]
    valid_win = [w for w in windows if w.split(" ")[1] != "-1"]
    titles = [" ".join(w.split(" ")[4:]) for w in valid_win]
    return titles

  def list_windows(self, menu):
    for t in self.get_all_window_titles():
      self.menuItem = gtk.MenuItem(t)
      self.menuItem.connect('activate', self.execute_fullscreen_toggle, t)
      self.menu.append(self.menuItem)

  def execute_fullscreen_toggle(self, widget, title):
    process = subprocess.Popen(['wmctrl', '-r', title, "-btoggle,fullscreen"], shell=False)

  def quit_cb(self, widget, data = None):
    gtk.main_quit()

if __name__ == "__main__":
  helloWord = ToggleFullScreen()
