import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from SyntaxHighlighter import SyntaxHighlighter
from compiler.lexer import tokenize

class CompilerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JAMP COMPILER")
        self.root.config(bg="#000000")

        main_frame = tk.Frame(root, bg="#000000")
        main_frame.pack(fill='both', expand=True)

        button_frame = tk.Frame(main_frame, bg="#000000")
        button_frame.pack(side='top', padx=10, pady=10)

        tk.Button(button_frame, text="Nuevo Archivo", command=self.new_file, bg="#4CAF50", fg="white", height=2, width=15).pack(side='left', padx=5)
        tk.Button(button_frame, text="Guardar Archivo", command=self.save_file, bg="#008CBA", fg="white", height=2, width=15).pack(side='left', padx=5)
        tk.Button(button_frame, text="Compilar", command=self.compile_code, bg="#f44336", fg="white", height=2, width=15).pack(side='left', padx=5)

        self.text_area = tk.Text(main_frame, wrap='word', undo=True, bg="#FFFFFF")
        self.text_area.pack(side='left', expand='yes', fill='both', padx=10, pady=(0, 5))

        border_frame = tk.Frame(main_frame, height=1, bg="#FFFFFF")
        border_frame.pack(side='bottom', fill='x')

        columns = ("Token", "Lexema", "Línea", "Columna")
        self.table = ttk.Treeview(main_frame, columns=columns, show='headings', height=10)
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, minwidth=50, width=100)
        self.table.pack(side='right', fill='y', padx=10, pady=(5, 10))

        for child in self.table.get_children():
            self.table.item(child, tags=('evenrow',))
        self.table.tag_configure('evenrow', background='#FFFFFF')

        self.highlighter = SyntaxHighlighter(self.text_area)
        self.text_area.bind("<KeyRelease>", self.highlighter.highlight_syntax)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jp", filetypes=[("JAMP Files", "*.jp")])
        if file_path:
            with open(file_path, 'w') as file:
                code = self.text_area.get(1.0, tk.END)
                file.write(code)

    def compile_code(self):
        self.table.delete(*self.table.get_children())
        code = self.text_area.get(1.0, tk.END)
        try:
            tokens = tokenize(code)
            for token in tokens:
                self.table.insert("", "end", values=token)
            messagebox.showinfo("Éxito", "Código compilado correctamente", parent=self.root)
        except RuntimeError as e:
            messagebox.showerror("Error", str(e), parent=self.root)