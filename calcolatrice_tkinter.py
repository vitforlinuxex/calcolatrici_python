import tkinter as tk
from tkinter import messagebox

class Calcolatrice:
    def __init__(self, master):
        self.master = master
        master.title("Calcolatrice")

        self.entry = tk.Entry(master, width=16, font=('Arial', 24), bd=2, relief
='ridge', justify='right')
        self.entry.grid(row=0, column=0, columnspan=4, sticky="we", padx=5, pady
=5)
        self.entry.focus_set()

        # Abilita copia/incolla tramite menu contestuale
        self.entry.bind("<Button-3><ButtonRelease-3>", self.popup_menu)  # Tasto destro mouse
        self.create_menu()

        # Pulsanti
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
                btn = tk.Button(master, text=button, width=34, height=2, command
=self.calcola)
                btn.grid(row=row, column=0, columnspan=4, padx=5, pady=5)
            else:
                btn = tk.Button(master, text=button, width=8, height=2, command
=lambda b=button:self.aggiungi_carattere(b))
                btn.grid(row=row, column=col, padx=2, pady=2)
                col += 1
                if col > 3:
                    col = 0
                    row += 1

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
            self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, char)

    def calcola(self):
        espressione = self.entry.get()
        try:
            # Valuta l'espressione con eval
            risultato = eval(espressione, {"__builtins__":None}, {})
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(risultato))
        except Exception:
            messagebox.showerror("Errore", "Espressione non valida")

    def copia(self, event=None):
        try:
            self.master.clipboard_clear()
            testo = self.entry.get()
            self.master.clipboard_append(testo)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore copia: {e}")

    def incolla(self, event=None):
        try:
            testo = self.master.clipboard_get()
            self.entry.insert(tk.END, testo)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore incolla: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = Calcolatrice(root)
    root.mainloop()
