import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Calcolatrice(Gtk.Window):
    def __init__(self):
        super().__init__(title="Calcolatrice PyGTK")
        self.set_border_width(10)
        self.set_default_size(300, 400)

        # Layout verticale
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Entry per l'input e i risultati
        self.entry = Gtk.Entry()
        self.entry.set_alignment(1)  # testo allineato a destra
        self.entry.set_placeholder_text("0")
        self.entry.set_hexpand(True)
        self.entry.set_margin_bottom(10)
        vbox.pack_start(self.entry, False, False, 0)

        # Griglia per i pulsanti
        grid = Gtk.Grid(column_spacing=5, row_spacing=5)
        vbox.pack_start(grid, True, True, 0)

        buttons = [
            ('7', 0, 0), ('8', 1, 0), ('9', 2, 0), ('/', 3, 0),
            ('4', 0, 1), ('5', 1, 1), ('6', 2, 1), ('*', 3, 1),
            ('1', 0, 2), ('2', 1, 2), ('3', 2, 2), ('-', 3, 2),
            ('C', 0, 3), ('0', 1, 3), ('.', 2, 3), ('+', 3, 3),
            ('=', 0, 4, 4, 1)
        ]

        for label, col, row, *span in buttons:
            colspan = span[0] if span else 1
            rowspan = span[1] if len(span) > 1 else 1
            button = Gtk.Button(label=label)
            button.set_hexpand(True)
            button.set_vexpand(True)
            grid.attach(button, col, row, colspan, rowspan)
            button.connect("clicked", self.on_button_clicked)

        # Menu per copia/incolla sulla Entry
        self.entry.connect("popup-menu", self.on_popup_menu)

        # Aggiungo gestori per copia/incolla da tastiera
        self.entry.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.entry.connect("key-press-event", self.on_key_press)

        self.show_all()

    def on_button_clicked(self, button):
        label = button.get_label()
        if label == "C":
            self.entry.set_text("")
        elif label == "=":
            self.calcola()
        else:
            self.entry.set_text(self.entry.get_text() + label)

    def calcola(self):
        espressione = self.entry.get_text()
        try:
            risultato = eval(espressione, {"__builtins__": None}, {})
            self.entry.set_text(str(risultato))
        except Exception:
            dialog = Gtk.MessageDialog(
                transient_for=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Espressione non valida",
            )
            dialog.format_secondary_text("Controlla la sintassi e riprova.")
            dialog.run()
            dialog.destroy()

    def on_popup_menu(self, entry, menu):
        # elemento menu standard di Gtk.Entry include già Copia/Incolla
        # se vuoi personalizzarlo puoi implementare qui
        return False  # Usa menu di default

    def on_key_press(self, widget, event):
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
        keyval = event.keyval

        if ctrl and (keyval == Gdk.KEY_c or keyval == Gdk.KEY_C):
            # Copia
            self.entry.copy_clipboard()
            return True
        elif ctrl and (keyval == Gdk.KEY_v or keyval == Gdk.KEY_V):
            # Incolla
            self.entry.paste_clipboard()
            return True
        elif keyval == Gdk.KEY_Return or keyval == Gdk.KEY_KP_Enter:
            # Invio per calcola
            self.calcola()
            return True

        return False

def main():
    win = Calcolatrice()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

if __name__ == "__main__":
    main()