import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from connect import connect_to_database


class AppAutores:
    def __init__(self, root):
        # Inicializa a janela principal do Tkinter.
        self.root = root
        self.root.title("Biblioteca - CRUD de Autores")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f2f5")

        # Abre a conexão com o banco de dados definido em connect.py.
        self.conn = connect_to_database()

        # Variáveis Tkinter usadas para ler e escrever valores dos campos.
        self.id_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.data_var = tk.StringVar()
        self.nac_var = tk.StringVar()

        # Cria os componentes visuais da interface.
        self.criar_interface()

    def criar_interface(self):
        # === Área esquerda: lista de autores ===
        left_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(left_frame, text="Autores", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

        # Treeview mostra os registros de autores em formato de tabela.
        colunas = ("ID", "Nome", "Nascimento", "Nacionalidade", "Cadastro")
        self.tree = ttk.Treeview(left_frame, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nome", width=280)
        self.tree.column("Nascimento", width=120, anchor="center")
        self.tree.column("Nacionalidade", width=160)
        self.tree.column("Cadastro", width=160, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões de ação para editar, excluir e atualizar a lista.
        btn_frame = tk.Frame(left_frame, bg="#ffffff")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Editar", bg="#f59e0b", fg="white",
                  command=self.editar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", bg="#ef4444", fg="white",
                  command=self.excluir).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Atualizar", bg="#3b82f6", fg="white",
                  command=self.carregar).pack(side="left", padx=5)

        # === Área direita: formulário de cadastro/edição ===
        right_frame = tk.Frame(self.root, bg="#f8fafc", width=420)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        right_frame.pack_propagate(False)

        form = tk.Frame(right_frame, bg="#f8fafc")
        form.pack(padx=20, pady=20, fill="both", expand=True)

        # Campo de nome do autor (obrigatório).
        tk.Label(form, text="Nome *", bg="#f8fafc").grid(row=0, column=0, sticky="w")
        tk.Entry(form, textvariable=self.nome_var, width=40).grid(row=1, column=0, sticky="w")

        # Campo de data de nascimento.
        tk.Label(form, text="Data de Nascimento", bg="#f8fafc").grid(row=2, column=0, sticky="w", pady=(10, 0))
        tk.Entry(form, textvariable=self.data_var, width=40).grid(row=3, column=0, sticky="w")

        # Campo de nacionalidade.
        tk.Label(form, text="Nacionalidade", bg="#f8fafc").grid(row=4, column=0, sticky="w", pady=(10, 0))
        tk.Entry(form, textvariable=self.nac_var, width=40).grid(row=5, column=0, sticky="w")

        # Campo de biografia usa um Text para texto maior.
        tk.Label(form, text="Biografia", bg="#f8fafc").grid(row=6, column=0, sticky="w", pady=(10, 0))
        self.biografia_text = tk.Text(form, width=40, height=8, wrap="word")
        self.biografia_text.grid(row=7, column=0, sticky="w")

        # Botões de salvar e limpar.
        btns = tk.Frame(right_frame, bg="#f8fafc")
        btns.pack(pady=20)

        tk.Button(btns, text="Salvar", bg="#22c55e", fg="white",
                  width=15, command=self.salvar).pack(side="left", padx=5)
        tk.Button(btns, text="Limpar", bg="#64748b", fg="white",
                  width=15, command=self.limpar).pack(side="left", padx=5)

        # Carrega os dados do banco assim que a interface estiver pronta.
        self.carregar()

    def carregar(self):
        # Limpa os itens existentes antes de carregar novamente.
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id_autor,
                   nome_autor,
                   DATE_FORMAT(data_nascimento, '%d/%m/%Y'),
                   nacionalidade,
                   DATE_FORMAT(data_cadastro, '%d/%m/%Y %H:%i')
            FROM autores
            ORDER BY nome_autor
        """)

        # Insere cada registro na tabela da interface.
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def parse_date(self, date_text):
        # Converte texto de data para objeto date.
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

        # Se nenhum formato bateu, mostra a mensagem correta ao usuário.
        raise ValueError("Data de nascimento deve estar no formato DD/MM/AAAA ou AAAA-MM-DD")

    def salvar(self):
        # Valida o nome do autor antes de gravar.
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showwarning("Atenção", "Nome do autor é obrigatório.")
            return

        # Tenta converter a data de nascimento para o formato do banco.
        try:
            data_nascimento = self.parse_date(self.data_var.get())
        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
            return

        biografia = self.biografia_text.get("1.0", "end").strip() or None
        dados = (
            nome,
            data_nascimento,
            self.nac_var.get() or None,
            biografia
        )

        cursor = self.conn.cursor()
        try:
            if self.id_var.get():
                # Atualiza o registro existente quando estiver no modo edição.
                cursor.execute("""
                    UPDATE autores
                    SET nome_autor=%s,
                        data_nascimento=%s,
                        nacionalidade=%s,
                        biografia=%s
                    WHERE id_autor=%s
                """, dados + (self.id_var.get(),))
            else:
                # Insere novo registro quando não há id definido.
                cursor.execute("""
                    INSERT INTO autores
                        (nome_autor, data_nascimento, nacionalidade, biografia)
                    VALUES (%s, %s, %s, %s)
                """, dados)

            self.conn.commit()
            self.carregar()
            self.limpar()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def editar(self):
        # Seleciona o item e carrega os dados para o formulário.
        sel = self.tree.selection()
        if not sel:
            return

        valores = self.tree.item(sel[0])['values']
        self.id_var.set(valores[0])
        self.nome_var.set(valores[1])
        self.data_var.set(valores[2] or "")
        self.nac_var.set(valores[3] or "")

        cursor = self.conn.cursor()
        cursor.execute("SELECT biografia FROM autores WHERE id_autor=%s", (valores[0],))
        dados = cursor.fetchone()

        self.biografia_text.delete("1.0", "end")
        if dados and dados[0]:
            self.biografia_text.insert("1.0", dados[0])

    def excluir(self):
        # Remove o autor selecionado do banco.
        sel = self.tree.selection()
        if not sel:
            return

        valores = self.tree.item(sel[0])['values']
        if messagebox.askyesno("Confirmar", "Excluir autor selecionado?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM autores WHERE id_autor=%s", (valores[0],))
            self.conn.commit()
            self.carregar()
            self.limpar()

    def limpar(self):
        # Limpa todos os campos do formulário e reseta o estado.
        self.id_var.set("")
        self.nome_var.set("")
        self.data_var.set("")
        self.nac_var.set("")
        self.biografia_text.delete("1.0", "end")

    def __del__(self):
        # Fecha a conexão automaticamente quando o objeto é destruído.
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Ponto de entrada do programa: cria a janela e inicia o loop do Tkinter.
    root = tk.Tk()
    app = AppAutores(root)
    root.mainloop()
