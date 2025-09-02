import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import datetime

# Inicializar banco de dados
conn = sqlite3.connect('loja_jogos.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (nome_usuario TEXT PRIMARY KEY, senha TEXT, cargo TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS jogos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, genero TEXT, preco REAL, estoque INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS carrinho (nome_usuario TEXT, id_jogo INTEGER, quantidade INTEGER, PRIMARY KEY (nome_usuario, id_jogo))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_usuario TEXT, id_jogo INTEGER, quantidade INTEGER, data_venda TEXT)''')
conn.commit()
cursor.execute("INSERT OR IGNORE INTO usuarios (nome_usuario, senha, cargo) VALUES (?, ?, ?)", ("cliente", "12345", "cliente"))
conn.commit()

class LojaJogos(ctk.CTk): 
    def __init__(self):
        super().__init__()
        self.title("Loja de Jogos")
        self.geometry("800x700")
        self.usuario_atual = None
        self.criar_tela_login()

    def criar_tela_login(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Login", font=("Arial", 16)).pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Nome de Usuário")
        self.entry_usuario.pack(pady=5)
        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_senha.pack(pady=5)
        ctk.CTkButton(self, text="Entrar", command=self.fazer_login).pack(pady=10)
        ctk.CTkButton(self, text="Cadastrar", command=self.criar_tela_cadastro).pack(pady=5)

    def criar_tela_cadastro(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Cadastro de Cliente", font=("Arial", 16)).pack(pady=10)
        self.entry_novo_usuario = ctk.CTkEntry(self, placeholder_text="Nome de Usuário")
        self.entry_novo_usuario.pack(pady=5)
        self.entry_nova_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_nova_senha.pack(pady=5)
        ctk.CTkButton(self, text="Cadastrar", command=self.cadastrar_usuario).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_login).pack(pady=5)

    def cadastrar_usuario(self):
        usuario = self.entry_novo_usuario.get()
        senha = self.entry_nova_senha.get()
        if usuario and senha:
            try:
                cursor.execute("INSERT INTO usuarios (nome_usuario, senha, cargo) VALUES (?, ?, 'cliente')", (usuario, senha))
                conn.commit()
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.criar_tela_login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Nome de usuário já existe!")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        cursor.execute("SELECT cargo FROM usuarios WHERE nome_usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        if resultado:
            self.usuario_atual = {"nome_usuario": usuario, "cargo": resultado[0]}
            if self.usuario_atual["cargo"] == "admin":
                self.criar_tela_admin()
            elif self.usuario_atual["cargo"] == "cliente":
                self.criar_tela_cliente()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def criar_tela_admin(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Painel Administrador", font=("Arial", 16)).pack(pady=10)
        ctk.CTkButton(self, text="Cadastrar Jogo", command=self.criar_tela_cadastrar_jogo).pack(pady=5)
        ctk.CTkButton(self, text="Editar/Excluir Jogo", command=self.criar_tela_editar_excluir_jogo).pack(pady=5)
        ctk.CTkButton(self, text="Gerar Relatório de Vendas", command=self.gerar_relatorio_vendas).pack(pady=5)
        ctk.CTkButton(self, text="Sair", command=self.sair).pack(pady=10)

    def criar_tela_cadastrar_jogo(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Cadastrar Novo Jogo", font=("Arial", 14)).pack(pady=10)
        self.nome_var = ctk.StringVar()
        self.genero_var = ctk.StringVar()
        self.preco_var = ctk.DoubleVar()
        self.estoque_var = ctk.IntVar()
        ctk.CTkEntry(self, textvariable=self.nome_var, placeholder_text="Nome do Jogo").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.genero_var, placeholder_text="Gênero").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.preco_var, placeholder_text="Preço").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.estoque_var, placeholder_text="Estoque").pack(pady=5)
        ctk.CTkButton(self, text="Salvar Jogo", command=self.salvar_jogo).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_admin).pack(pady=5)

    def salvar_jogo(self):
        nome = self.nome_var.get()
        genero = self.genero_var.get()
        preco = self.preco_var.get()
        estoque = self.estoque_var.get()
        if nome and genero and preco > 0 and estoque > 0:
            cursor.execute("INSERT INTO jogos (nome, genero, preco, estoque) VALUES (?, ?, ?, ?)", 
                           (nome, genero, preco, estoque))
            conn.commit()
            messagebox.showinfo("Sucesso", "Jogo cadastrado com sucesso!")
            self.criar_tela_admin()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios e valores devem ser positivos!")

    def criar_tela_editar_excluir_jogo(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Editar/Excluir Jogo", font=("Arial", 14)).pack(pady=10)
        cursor.execute("SELECT id, nome, genero, preco, estoque FROM jogos")
        jogos = cursor.fetchall()
        scroll_frame = ctk.CTkScrollableFrame(self, height=300)
        scroll_frame.pack(fill="both", expand=True, pady=5)
        for jogo in jogos:
            btn = ctk.CTkButton(scroll_frame, text=f"{jogo[1]} (ID: {jogo[0]})", 
                                command=lambda id=jogo[0]: self.editar_excluir_jogo(id))
            btn.pack(pady=2)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_admin).pack(pady=5)

    def editar_excluir_jogo(self, id_jogo):
        self.limpar_tela()
        cursor.execute("SELECT nome, genero, preco, estoque FROM jogos WHERE id = ?", (id_jogo,))
        jogo = cursor.fetchone()
        self.nome_var = ctk.StringVar(value=jogo[0])
        self.genero_var = ctk.StringVar(value=jogo[1])
        self.preco_var = ctk.DoubleVar(value=jogo[2])
        self.estoque_var = ctk.IntVar(value=jogo[3])
        ctk.CTkLabel(self, text=f"Editar Jogo (ID: {id_jogo})", font=("Arial", 14)).pack(pady=10)
        ctk.CTkEntry(self, textvariable=self.nome_var, placeholder_text="Nome do Jogo").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.genero_var, placeholder_text="Gênero").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.preco_var, placeholder_text="Preço").pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.estoque_var, placeholder_text="Estoque").pack(pady=5)
        ctk.CTkButton(self, text="Atualizar", command=lambda: self.atualizar_jogo(id_jogo)).pack(pady=5)
        ctk.CTkButton(self, text="Excluir", command=lambda: self.excluir_jogo(id_jogo)).pack(pady=5)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_editar_excluir_jogo).pack(pady=5)

    def atualizar_jogo(self, id_jogo):
        nome = self.nome_var.get()
        genero = self.genero_var.get()
        preco = self.preco_var.get()
        estoque = self.estoque_var.get()
        if nome and genero and preco > 0 and estoque >= 0:
            cursor.execute("UPDATE jogos SET nome = ?, genero = ?, preco = ?, estoque = ? WHERE id = ?", 
                           (nome, genero, preco, estoque, id_jogo))
            conn.commit()
            messagebox.showinfo("Sucesso", "Jogo atualizado com sucesso!")
            self.criar_tela_editar_excluir_jogo()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios e valores devem ser positivos!")

    def excluir_jogo(self, id_jogo):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este jogo?"):
            cursor.execute("DELETE FROM jogos WHERE id = ?", (id_jogo,))
            conn.commit()
            messagebox.showinfo("Sucesso", "Jogo excluído com sucesso!")
            self.criar_tela_editar_excluir_jogo()

    def gerar_relatorio_vendas(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Relatório de Vendas", font=("Arial", 14)).pack(pady=10)
        scroll_frame = ctk.CTkScrollableFrame(self, height=400)
        scroll_frame.pack(fill="both", expand=True, pady=5)
        cursor.execute("SELECT v.id, j.nome, u.nome_usuario, v.quantidade, v.data_venda FROM vendas v JOIN jogos j ON v.id_jogo = j.id JOIN usuarios u ON v.nome_usuario = u.nome_usuario")
        vendas = cursor.fetchall()
        for venda in vendas:
            label = ctk.CTkLabel(scroll_frame, text=f"ID: {venda[0]} | Jogo: {venda[1]} | Cliente: {venda[2]} | Qtd: {venda[3]} | Data: {venda[4]}")
            label.pack(pady=2)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_admin).pack(pady=5)

    def criar_tela_cliente(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Painel do Cliente", font=("Arial", 16)).pack(pady=10)
        ctk.CTkButton(self, text="Visualizar Catálogo", command=self.visualizar_catalogo).pack(pady=5)
        ctk.CTkButton(self, text="Filtrar Jogos", command=self.filtrar_jogos).pack(pady=5)
        ctk.CTkButton(self, text="Ver Carrinho", command=self.ver_carrinho).pack(pady=5)
        ctk.CTkButton(self, text="Sair", command=self.sair).pack(pady=10)

    def visualizar_catalogo(self, jogos=None):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Catálogo de Jogos", font=("Arial", 14)).pack(pady=10)
        scroll_frame = ctk.CTkScrollableFrame(self, height=400)
        scroll_frame.pack(fill="both", expand=True, pady=5)
        if jogos is None:
            cursor.execute("SELECT id, nome, genero, preco, estoque FROM jogos WHERE estoque > 0")
            jogos = cursor.fetchall()
        for jogo in jogos:
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=f"{jogo[1]} | Gênero: {jogo[2]} | Preço: R${jogo[3]:.2f} | Estoque: {jogo[4]}").pack(side="left", padx=5)
            ctk.CTkButton(frame, text="Adicionar ao Carrinho", command=lambda id=jogo[0]: self.adicionar_ao_carrinho(id)).pack(side="right", padx=5)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_cliente).pack(pady=5)

    def filtrar_jogos(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Filtrar Jogos", font=("Arial", 14)).pack(pady=10)
        self.genero_filter = ctk.CTkEntry(self, placeholder_text="Gênero (opcional)")
        self.genero_filter.pack(pady=5)
        self.preco_max_filter = ctk.CTkEntry(self, placeholder_text="Preço Máximo (opcional)")
        self.preco_max_filter.pack(pady=5)
        ctk.CTkButton(self, text="Aplicar Filtro", command=self.aplicar_filtro).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_cliente).pack(pady=5)

    def aplicar_filtro(self):
        genero = self.genero_filter.get()
        preco_max_str = self.preco_max_filter.get()
        query = "SELECT id, nome, genero, preco, estoque FROM jogos WHERE estoque > 0"
        params = []
        if genero:
            query += " AND genero LIKE ?"
            params.append(f"%{genero}%")
        if preco_max_str:
            try:
                preco_max = float(preco_max_str)
                query += " AND preco <= ?"
                params.append(preco_max)
            except ValueError:
                messagebox.showerror("Erro", "Preço máximo deve ser um número válido!")
                return
        cursor.execute(query, params)
        jogos = cursor.fetchall()
        if jogos:
            self.visualizar_catalogo(jogos)
        else:
            messagebox.showinfo("Info", "Nenhum jogo encontrado com os filtros aplicados!")
            self.filtrar_jogos()

    def adicionar_ao_carrinho(self, id_jogo):
        cursor.execute("SELECT estoque FROM jogos WHERE id = ?", (id_jogo,))
        estoque = cursor.fetchone()[0]
        if estoque > 0:
            cursor.execute("INSERT OR REPLACE INTO carrinho (nome_usuario, id_jogo, quantidade) VALUES (?, ?, COALESCE((SELECT quantidade + 1 FROM carrinho WHERE nome_usuario = ? AND id_jogo = ?), 1))",
                           (self.usuario_atual["nome_usuario"], id_jogo, self.usuario_atual["nome_usuario"], id_jogo))
            conn.commit()
            messagebox.showinfo("Sucesso", "Jogo adicionado ao carrinho!")
        else:
            messagebox.showerror("Erro", "Estoque insuficiente!")

    def ver_carrinho(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Carrinho de Compras", font=("Arial", 14)).pack(pady=10)
        scroll_frame = ctk.CTkScrollableFrame(self, height=300)
        scroll_frame.pack(fill="both", expand=True, pady=5)
        cursor.execute("SELECT j.id, j.nome, j.preco, c.quantidade, (j.preco * c.quantidade) AS total FROM carrinho c JOIN jogos j ON c.id_jogo = j.id WHERE c.nome_usuario = ?",
                       (self.usuario_atual["nome_usuario"],))
        itens = cursor.fetchall()
        total_geral = 0
        for item in itens:
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=f"{item[1]} | Preço: R${item[2]:.2f} | Qtd: {item[3]} | Total: R${item[4]:.2f}").pack(side="left", padx=5)
            ctk.CTkButton(frame, text="Remover", command=lambda id=item[0]: self.remover_do_carrinho(id)).pack(side="right", padx=5)
            total_geral += item[4]
        ctk.CTkLabel(self, text=f"Total Geral: R${total_geral:.2f}", font=("Arial", 12)).pack(pady=5)
        ctk.CTkButton(self, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=5)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_cliente).pack(pady=5)

    def remover_do_carrinho(self, id_jogo):
        cursor.execute("DELETE FROM carrinho WHERE nome_usuario = ? AND id_jogo = ?", (self.usuario_atual["nome_usuario"], id_jogo))
        conn.commit()
        messagebox.showinfo("Sucesso", "Item removido do carrinho!")
        self.ver_carrinho()

    def finalizar_compra(self):
        cursor.execute("SELECT id_jogo, quantidade FROM carrinho WHERE nome_usuario = ?", (self.usuario_atual["nome_usuario"],))
        itens = cursor.fetchall()
        if not itens:
            messagebox.showerror("Erro", "Carrinho vazio!")
            return
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            for item in itens:
                id_jogo, qtd = item
                cursor.execute("SELECT estoque FROM jogos WHERE id = ?", (id_jogo,))
                estoque = cursor.fetchone()[0]
                if estoque < qtd:
                    raise ValueError(f"Estoque insuficiente para o jogo ID {id_jogo}!")
                cursor.execute("UPDATE jogos SET estoque = estoque - ? WHERE id = ?", (qtd, id_jogo))
                cursor.execute("INSERT INTO vendas (nome_usuario, id_jogo, quantidade, data_venda) VALUES (?, ?, ?, ?)",
                               (self.usuario_atual["nome_usuario"], id_jogo, qtd, data_atual))
            cursor.execute("DELETE FROM carrinho WHERE nome_usuario = ?", (self.usuario_atual["nome_usuario"],))
            conn.commit()
            messagebox.showinfo("Sucesso", "Compra finalizada com sucesso!")
            self.criar_tela_cliente()
        except ValueError as e:
            conn.rollback()
            messagebox.showerror("Erro", str(e))

    def sair(self):
        self.usuario_atual = None
        self.criar_tela_login()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def rodar(self):
        self.mainloop()

if __name__ == "__main__":
    app = LojaJogos()
    app.rodar()