# -*- Mode: Python; py-indent-offset: 4 -*-
# vim: tabstop=4 shiftwidth=4 expandtab

import unittest

import sys
sys.path.insert(0, "../")

from gi.repository import Gdk
from gi.repository import Gtk

import gi.pygtkcompat

gi.pygtkcompat.enable()
gi.pygtkcompat.enable_gtk(version='3.0')

import atk
import pango
import pangocairo
import gtk
import gtk.gdk


class TestATKCompat(unittest.TestCase):
    def testObject(self):
        self.assertTrue(hasattr(atk, 'Object'))


class TestPangoCompat(unittest.TestCase):
    def testLayout(self):
        self.assertTrue(hasattr(pango, 'Layout'))


class TestPangoCairoCompat(unittest.TestCase):
    def testErrorUnderlinePath(self):
        self.assertTrue(hasattr(pangocairo, 'error_underline_path'))


class TestGTKCompat(unittest.TestCase):
    def testButtons(self):
        self.assertEqual(Gdk._2BUTTON_PRESS, 5)
        self.assertEqual(Gdk.BUTTON_PRESS, 4)

    def testEnums(self):
        self.assertEqual(gtk.WINDOW_TOPLEVEL, Gtk.WindowType.TOPLEVEL)
        self.assertEqual(gtk.PACK_START, Gtk.PackType.START)

    def testFlags(self):
        self.assertEqual(gtk.EXPAND, Gtk.AttachOptions.EXPAND)
        self.assertEqual(gtk.gdk.SHIFT_MASK, Gdk.ModifierType.SHIFT_MASK)

    def testKeysyms(self):
        import gtk.keysyms
        self.assertEqual(gtk.keysyms.Escape, Gdk.KEY_Escape)
        self.assertTrue(gtk.keysyms._0, Gdk.KEY_0)

    def testStyle(self):
        widget = gtk.Button()
        self.assertTrue(isinstance(widget.style.base[gtk.STATE_NORMAL],
                                   gtk.gdk.Color))

    def testAlignment(self):
        a = gtk.Alignment()
        self.assertEqual(a.props.xalign, 0.0)
        self.assertEqual(a.props.yalign, 0.0)
        self.assertEqual(a.props.xscale, 0.0)
        self.assertEqual(a.props.yscale, 0.0)

    def testBox(self):
        box = gtk.Box()
        child = gtk.Button()

        box.pack_start(child)
        expand, fill, padding, pack_type = box.query_child_packing(child)
        self.assertTrue(expand)
        self.assertTrue(fill)
        self.assertEqual(padding, 0)
        self.assertEqual(pack_type, gtk.PACK_START)

        child = gtk.Button()
        box.pack_end(child)
        expand, fill, padding, pack_type = box.query_child_packing(child)
        self.assertTrue(expand)
        self.assertTrue(fill)
        self.assertEqual(padding, 0)
        self.assertEqual(pack_type, gtk.PACK_END)

    def testComboBoxEntry(self):
        liststore = gtk.ListStore(int, str)
        liststore.append((1, 'One'))
        liststore.append((2, 'Two'))
        liststore.append((3, 'Three'))
        combo = gtk.ComboBoxEntry(model=liststore)
        combo.set_text_column(1)
        combo.set_active(0)
        self.assertEqual(combo.get_text_column(), 1)
        self.assertEqual(combo.get_child().get_text(), 'One')
        combo = gtk.combo_box_entry_new()
        combo.set_model(liststore)
        combo.set_text_column(1)
        combo.set_active(0)
        self.assertEqual(combo.get_text_column(), 1)
        self.assertEqual(combo.get_child().get_text(), 'One')
        combo = gtk.combo_box_entry_new_with_model(liststore)
        combo.set_text_column(1)
        combo.set_active(0)
        self.assertEqual(combo.get_text_column(), 1)
        self.assertEqual(combo.get_child().get_text(), 'One')

    def testSizeRequest(self):
        box = gtk.Box()
        self.assertEqual(box.size_request(), [0, 0])

    def testPixbuf(self):
        gtk.gdk.Pixbuf()

    def testPixbufLoader(self):
        loader = gtk.gdk.PixbufLoader('png')
        loader.close()

    def testPixbufFormats(self):
        formats = gtk.gdk.pixbuf_get_formats()
        self.assertEqual(type(formats[0]), dict)
        self.assertTrue('name' in formats[0])
        self.assertTrue('description' in formats[0])
        self.assertTrue('mime_types' in formats[0])
        self.assertEqual(type(formats[0]['extensions']), list)

    def testGdkWindow(self):
        w = gtk.Window()
        w.realize()
        self.assertEqual(w.get_window().get_origin(), (0, 0))
