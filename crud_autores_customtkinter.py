import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from connect import connect_to_database
from style import COLORS, FONT_TITLE, FONT_LABEL, FONT_INPUT, card, primary_button, danger_button, success_button


class AppAutores:
    def __init__(self, root):
        self.root = root
        self.root.title("Biblioteca")
        self.root.geometry("1200x700")
        self.root.configure(fg_color=COLORS["bg_main"])

        self.conn = connect_to_database()

        # Variáveis
        self.id_var = ctk.StringVar()
        self.nome_var = ctk.StringVar()
        self.data_var = ctk.StringVar()
        self.nac_var = ctk.StringVar()

        self.build_ui()
        self.carregar()

    def build_ui(self):
        # ===== CONTAINER =====
        container = ctk.CTkFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # ===== LEFT (LISTA) =====
        left = card(container)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(left, text="Autores", font=FONT_TITLE, text_color=COLORS["text"]).pack(pady=15)

        # Treeview (mantido)
        columns = ("ID", "Nome", "Nascimento", "Nacionalidade")
        self.tree = ttk.Treeview(left, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões
        btns = ctk.CTkFrame(left, fg_color="transparent")
        btns.pack(pady=10)

        primary_button(btns, "Atualizar", self.carregar).pack(side="left", padx=5)
        primary_button(btns, "Editar", self.editar).pack(side="left", padx=5)
        danger_button(btns, "Excluir", self.excluir).pack(side="left", padx=5)

        # ===== RIGHT (FORM) =====
        right = card(container)
        right.pack(side="right", fill="y", padx=(10, 0))

        ctk.CTkLabel(right, text="Cadastro de Autor", font=FONT_TITLE).pack(pady=15)

        form = ctk.CTkFrame(right, fg_color="transparent")
        form.pack(padx=20, pady=10)

        # Nome
        ctk.CTkLabel(form, text="Nome", font=FONT_LABEL).pack(anchor="w")
        ctk.CTkEntry(form, textvariable=self.nome_var, width=300).pack(pady=5)

        # Data
        ctk.CTkLabel(form, text="Nascimento", font=FONT_LABEL).pack(anchor="w", pady=(10, 0))
        ctk.CTkEntry(form, textvariable=self.data_var).pack(pady=5)

        # Nacionalidade
        ctk.CTkLabel(form, text="Nacionalidade", font=FONT_LABEL).pack(anchor="w", pady=(10, 0))
        ctk.CTkEntry(form, textvariable=self.nac_var).pack(pady=5)

        # Botões
        actions = ctk.CTkFrame(right, fg_color="transparent")
        actions.pack(pady=20)

        success_button(actions, "Salvar", self.salvar).pack(side="left", padx=5)
        primary_button(actions, "Limpar", self.limpar).pack(side="left", padx=5)

    # ===== CRUD =====

    def carregar(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id_autor,
                   nome_autor,
                   DATE_FORMAT(data_nascimento, '%d/%m/%Y'),
                   nacionalidade
            FROM autores
            ORDER BY nome_autor
        """)

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def parse_date(self, date_text):
        # Aceita datas em DD/MM/AAAA ou AAAA-MM-DD.
        if not date_text:
            return None

        date_text = date_text.strip()
        if not date_text:
            return None

        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(date_text, fmt).date()
            except ValueError:
                continue

        raise ValueError("Data de nascimento deve estar no formato DD/MM/AAAA ou AAAA-MM-DD")

    def salvar(self):
        nome = self.nome_var.get().strip()

        if not nome:
            messagebox.showwarning("Atenção", "Nome obrigatório")
            return

        try:
            data_nascimento = self.parse_date(self.data_var.get())
        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
            return

        dados = (
            nome,
            data_nascimento,
            self.nac_var.get() or None
        )

        cursor = self.conn.cursor()

        if self.id_var.get():
            cursor.execute("""
                UPDATE autores
                SET nome_autor=%s, data_nascimento=%s, nacionalidade=%s
                WHERE id_autor=%s
            """, dados + (self.id_var.get(),))
        else:
            cursor.execute("""
                INSERT INTO autores (nome_autor, data_nascimento, nacionalidade)
                VALUES (%s, %s, %s)
            """, dados)

        self.conn.commit()
        self.carregar()
        self.limpar()

    def editar(self):
        sel = self.tree.selection()
        if not sel:
            return

        valores = self.tree.item(sel[0])['values']

        self.id_var.set(valores[0])
        self.nome_var.set(valores[1])
        self.data_var.set(valores[2] or "")
        self.nac_var.set(valores[3] or "")

    def excluir(self):
        sel = self.tree.selection()
        if not sel:
            return

        valores = self.tree.item(sel[0])['values']

        if messagebox.askyesno("Confirmar", "Excluir autor?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM autores WHERE id_autor=%s", (valores[0],))
            self.conn.commit()
            self.carregar()
            self.limpar()

    def limpar(self):
        self.id_var.set("")
        self.nome_var.set("")
        self.data_var.set("")
        self.nac_var.set("")


if __name__ == "__main__":
    root = ctk.CTk()
    app = AppAutores(root)
    root.mainloop()
