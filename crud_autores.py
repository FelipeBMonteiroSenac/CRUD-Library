import tkinter as tk
from tkinter import ttk, messagebox
from connect import connect_to_database


class AppPublicadoras:
    def __init__(self, root):
        # Recebe a janela principal (root) e configura o título,
        # tamanho e cor de fundo da aplicação.
        self.root = root
        self.root.title("Biblioteca - CRUD de Publicadoras")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f2f5")

        # Abre a conexão com o banco de dados MySQL.
        self.conn = connect_to_database()

        # Variáveis Tkinter que armazenam os valores dos campos do formulário.
        self.id_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.endereco_var = tk.StringVar()
        self.telefone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.website_var = tk.StringVar()

        # Gera toda a interface gráfica da aplicação.
        self.criar_interface()

    def criar_interface(self):
        # Frame da esquerda contém a lista de publicadoras e botões de ação.
        left_frame = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(left_frame, text="Publicadoras", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

        # Treeview exibe as publicadoras cadastradas em formato de tabela.
        colunas = ("ID", "Nome", "Telefone", "Email", "Data Cadastro")
        self.tree = ttk.Treeview(left_frame, columns=colunas, show="headings")

        for col in colunas:
            self.tree.heading(col, text=col)

        # Define largura e alinhamento das colunas da tabela.
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nome", width=250)
        self.tree.column("Telefone", width=120)
        self.tree.column("Email", width=200)
        self.tree.column("Data Cadastro", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Botões para editar, excluir e atualizar registros.
        btn_frame = tk.Frame(left_frame, bg="#ffffff")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Editar", bg="#f59e0b", fg="white",
                  command=self.editar).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Excluir", bg="#ef4444", fg="white",
                  command=self.excluir).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Atualizar", bg="#3b82f6", fg="white",
                  command=self.carregar).pack(side="left", padx=5)

        # Frame da direita contém o formulário para inserir/editar dados.
        right_frame = tk.Frame(self.root, bg="#f8fafc", width=400)
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        right_frame.pack_propagate(False)

        form = tk.Frame(right_frame, bg="#f8fafc")
        form.pack(padx=20, pady=20)

        # Campo de nome (obrigatório).
        tk.Label(form, text="Nome *", bg="#f8fafc").grid(row=0, column=0, sticky="w")
        tk.Entry(form, textvariable=self.nome_var, width=40).grid(row=1, column=0)

        # Campo de endereço.
        tk.Label(form, text="Endereço", bg="#f8fafc").grid(row=2, column=0, sticky="w", pady=(10,0))
        tk.Entry(form, textvariable=self.endereco_var, width=40).grid(row=3, column=0)

        # Campo de telefone.
        tk.Label(form, text="Telefone", bg="#f8fafc").grid(row=4, column=0, sticky="w", pady=(10,0))
        tk.Entry(form, textvariable=self.telefone_var, width=40).grid(row=5, column=0)

        # Campo de email.
        tk.Label(form, text="Email", bg="#f8fafc").grid(row=6, column=0, sticky="w", pady=(10,0))
        tk.Entry(form, textvariable=self.email_var, width=40).grid(row=7, column=0)

        # Campo de website.
        tk.Label(form, text="Website", bg="#f8fafc").grid(row=8, column=0, sticky="w", pady=(10,0))
        tk.Entry(form, textvariable=self.website_var, width=40).grid(row=9, column=0)

        # Botões salvar e limpar no formulário.
        btns = tk.Frame(right_frame, bg="#f8fafc")
        btns.pack(pady=20)

        tk.Button(btns, text="Salvar", bg="#22c55e", fg="white",
                  width=15, command=self.salvar).pack(side="left", padx=5)

        tk.Button(btns, text="Limpar", bg="#64748b", fg="white",
                  width=15, command=self.limpar).pack(side="left", padx=5)

        # Carrega os dados já existentes ao iniciar a aplicação.
        self.carregar()

    # ===== CRUD =====

    def carregar(self):
        # Limpa a lista antes de recarregar os dados do banco.
        for item in self.tree.get_children():
            self.tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id_publicadora, nome_publicadora, telefone, email,
                   DATE_FORMAT(data_cadastro, '%d/%m/%Y %H:%i')
            FROM publicadoras
            ORDER BY nome_publicadora
        """)

        # Insere cada registro retornado no Treeview.
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def salvar(self):
        # Recupera o nome do campo e remove espaços em branco extras.
        nome = self.nome_var.get().strip()

        if not nome:
            # Nome é obrigatório para salvar o registro.
            messagebox.showwarning("Atenção", "Nome é obrigatório!")
            return

        # Prepara os dados para o INSERT ou UPDATE.
        dados = (
            nome,
            self.endereco_var.get() or None,
            self.telefone_var.get() or None,
            self.email_var.get() or None,
            self.website_var.get() or None
        )

        cursor = self.conn.cursor()

        try:
            if self.id_var.get():
                # Se existe id_var, atualiza o registro existente.
                cursor.execute("""
                    UPDATE publicadoras
                    SET nome_publicadora=%s, endereco=%s, telefone=%s,
                        email=%s, website=%s
                    WHERE id_publicadora=%s
                """, dados + (self.id_var.get(),))
            else:
                # Caso contrário, insere um novo registro.
                cursor.execute("""
                    INSERT INTO publicadoras
                    (nome_publicadora, endereco, telefone, email, website)
                    VALUES (%s, %s, %s, %s, %s)
                """, dados)

            # Confirma a alteração no banco e atualiza a interface.
            self.conn.commit()
            self.carregar()
            self.limpar()

        except Exception as e:
            # Mostra mensagem de erro se algo der errado.
            messagebox.showerror("Erro", str(e))

    def editar(self):
        # Verifica se algum item está selecionado na tabela.
        sel = self.tree.selection()
        if not sel:
            return

        # Recupera os valores da linha selecionada.
        valores = self.tree.item(sel[0])['values']

        # Preenche as variáveis do formulário com os dados selecionados.
        self.id_var.set(valores[0])
        self.nome_var.set(valores[1])
        self.telefone_var.set(valores[2] or "")
        self.email_var.set(valores[3] or "")

        # Busca os campos restantes (endereço e website) no banco.
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT endereco, website
            FROM publicadoras
            WHERE id_publicadora=%s
        """, (valores[0],))

        dados = cursor.fetchone()
        if dados:
            self.endereco_var.set(dados[0] or "")
            self.website_var.set(dados[1] or "")

    def excluir(self):
        sel = self.tree.selection()
        if not sel:
            return

        valores = self.tree.item(sel[0])['values']

        # Pergunta ao usuário se ele realmente deseja excluir o registro.
        if messagebox.askyesno("Confirmar", "Excluir registro?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM publicadoras WHERE id_publicadora=%s", (valores[0],))
            self.conn.commit()
            self.carregar()
            self.limpar()

    def limpar(self):
        # Limpa todos os campos do formulário e reseta o modo de edição.
        self.id_var.set("")
        self.nome_var.set("")
        self.endereco_var.set("")
        self.telefone_var.set("")
        self.email_var.set("")
        self.website_var.set("")

    def __del__(self):
        # Fecha a conexão com o banco quando a instância for destruída.
        self.conn.close()


if __name__ == "__main__":
    # Inicia a aplicação Tkinter.
    root = tk.Tk()
    app = AppPublicadoras(root)
    root.mainloop()
