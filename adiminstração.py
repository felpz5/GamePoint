import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from datetime import datetime

# Inicializar banco de dados
conn = sqlite3.connect('loja_jogos.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (nome_usuario TEXT PRIMARY KEY, senha TEXT, cargo TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS jogos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, genero TEXT, preco REAL, estoque INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_usuario TEXT, id_jogo INTEGER, quantidade INTEGER, data_venda TEXT)''')
conn.commit()
cursor.execute("INSERT OR IGNORE INTO usuarios (nome_usuario, senha, cargo) VALUES (?, ?, ?)", ("admin", "123456", "admin"))
conn.commit()

class LojaJogos(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Loja de Jogos - Painel Administrador")
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

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        cursor.execute("SELECT cargo FROM usuarios WHERE nome_usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        if resultado:
            self.usuario_atual = {"nome_usuario": usuario, "cargo": resultado[0]}
            if self.usuario_atual["cargo"] == "admin":
                self.criar_tela_admin()
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
        if nome and genero and preco and estoque:
            cursor.execute("INSERT INTO jogos (nome, genero, preco, estoque) VALUES (?, ?, ?, ?)", 
                          (nome, genero, preco, estoque))
            conn.commit()
            messagebox.showinfo("Sucesso", "Jogo cadastrado com sucesso!")
            self.criar_tela_admin()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    def criar_tela_editar_excluir_jogo(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Editar/Excluir Jogo", font=("Arial", 14)).pack(pady=10)
        cursor.execute("SELECT id, nome, genero, preco, estoque FROM jogos")
        jogos = cursor.fetchall()
        for jogo in jogos:
            ctk.CTkButton(self, text=f"{jogo[1]} (ID: {jogo[0]})", 
                         command=lambda id=jogo[0]: self.editar_excluir_jogo(id)).pack(pady=2)
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
        if nome and genero and preco and estoque:
            cursor.execute("UPDATE jogos SET nome = ?, genero = ?, preco = ?, estoque = ? WHERE id = ?", 
                          (nome, genero, preco, estoque, id_jogo))
            conn.commit()
            messagebox.showinfo("Sucesso", "Jogo atualizado com sucesso!")
            self.criar_tela_editar_excluir_jogo()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    def excluir_jogo(self, id_jogo):
        cursor.execute("DELETE FROM jogos WHERE id = ?", (id_jogo,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Jogo excluído com sucesso!")
        self.criar_tela_editar_excluir_jogo()

    def gerar_relatorio_vendas(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Relatório de Vendas", font=("Arial", 14)).pack(pady=10)
        cursor.execute("SELECT v.id, j.nome, v.quantidade, v.data_venda FROM vendas v JOIN jogos j ON v.id_jogo = j.id")
        vendas = cursor.fetchall()
        for venda in vendas:
            ctk.CTkLabel(self, text=f"ID Venda: {venda[0]}, Jogo: {venda[1]}, Qtd: {venda[2]}, Data: {venda[3]}").pack(pady=2)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_admin).pack(pady=5)

    def sair(self):
        self.usuario_atual = None
        self.destroy()
        LojaJogos()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def rodar(self):
        self.mainloop()

if __name__ == "__main__":
    app = LojaJogos()
    app.rodar()