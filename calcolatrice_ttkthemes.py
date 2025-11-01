import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk

class Calcolatrice:
    def __init__(self, master):
        self.master = master
        master.title("Calcolatrice con ttkthemes")

        # Entry con stile ttk
        self.style = ttk.Style()
        self.style.configure('TEntry', font=('Arial', 24))
        
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(master, textvariable=self.entry_var, font=('Arial', 24), justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, sticky="we", padx=5, pady=5)
        self.entry.focus_set()

        # Menu contestuale per copia/incolla
        self.entry.bind("<Button-3><ButtonRelease-3>", self.popup_menu)
        self.create_menu()

        # Pulsanti (ttk.Button)
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '.', '+',
            '='
        ]

        row = 1
        col = 0
        for button in buttons:
            if button == '=':
                btn = ttk.Button(master, text=button, command=self.calcola)
                btn.grid(row=row, column=0, columnspan=4, sticky="we", padx=5,
 pady=5)
            else:
                btn = ttk.Button(master, text=button, command=lambda b=button
:self.aggiungi_carattere(b))
                btn.grid(row=row, column=col, sticky="we", padx=2, pady=2)
                col += 1
                if col > 3:
                    col = 0
                    row += 1

        # Rendi le colonne uniformi
        for i in range(4):
            master.grid_columnconfigure(i, weight=1)

        # Shortcut da tastiera
        master.bind('<Return>', lambda event: self.calcola())
        master.bind('<Control-c>', self.copia)
        master.bind('<Control-v>', self.incolla)

    def create_menu(self):
        self.menu = tk.Menu(self.master, tearoff=0)
        self.menu.add_command(label="Copia", command=self.copia)
        self.menu.add_command(label="Incolla", command=self.incolla)

    def popup_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def aggiungi_carattere(self, char):
        if char == 'C':
            self.entry_var.set("")
        else:
            self.entry_var.set(self.entry_var.get() + char)

    def calcola(self):
        espressione = self.entry_var.get()
        try:
            # Valutazione sicura dell'espressione
            risultato = eval(espressione, {"__builtins__": None}, {})
            self.entry_var.set(str(risultato))
        except Exception:
            messagebox.showerror("Errore", "Espressione non valida")

    def copia(self, event=None):
        try:
            self.master.clipboard_clear()
            testo = self.entry_var.get()
            self.master.clipboard_append(testo)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore copia: {e}")

    def incolla(self, event=None):
        try:
            testo = self.master.clipboard_get()
            self.entry_var.set(self.entry_var.get() + testo)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore incolla: {e}")

if __name__ == '__main__':
    # ThemedTk permette di scegliere un tema comodo
    root = ThemedTk(theme="keramik")  # puoi cambiare "arc" con altri temi es. "breeze", "plastik", "radiance"
    app = Calcolatrice(root)
    root.mainloop()
