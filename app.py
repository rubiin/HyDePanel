import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class InfiniteScrollWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Scroll Pagination")
        self.set_default_size(400, 600)

        # Scrolled window
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC
        )
        self.add(self.scrolled_window)

        # ListBox
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.scrolled_window.add(self.list_box)

        # Pagination state
        self.items_loaded = 0
        self.batch_size = 20
        self.loading = False

        # Add some initial content
        self.load_more_items()

        # Connect scroll event after showing window
        self.connect("show", self.on_show)

    def on_show(self, widget):
        adjustment = self.scrolled_window.get_vadjustment()
        adjustment.connect("value-changed", self.on_scroll)

    def load_more_items(self):
        if self.loading:
            return
        self.loading = True

        for i in range(self.items_loaded, self.items_loaded + self.batch_size):
            # Create a tall box per row to ensure scrollable height
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            box.set_margin_top(10)
            box.set_margin_bottom(10)
            box.set_margin_start(10)
            box.set_margin_end(10)

            label = Gtk.Label(label=f"Item {i + 1}", xalign=0)
            box.pack_start(label, False, False, 0)

            row = Gtk.ListBoxRow()
            row.add(box)
            self.list_box.add(row)

        self.items_loaded += self.batch_size
        self.list_box.show_all()
        self.loading = False

    def on_scroll(self, adjustment):
        value = adjustment.get_value()
        upper = adjustment.get_upper()
        page_size = adjustment.get_page_size()

        if value + page_size >= upper - 50:  # Load more when near bottom
            self.load_more_items()


win = InfiniteScrollWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
