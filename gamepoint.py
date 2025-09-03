import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LojaJogos(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GamePoint")
        self.geometry("800x600")
        self.configure(fg_color="#1e1e2e")
        self.resizable(True, True)
        
        # Listas para gerenciar dados
        self.usuarios = [
            {"nome": "admin", "senha": "admin123", "cargo": "admin"},
            {"nome": "cliente", "senha": "cliente123", "cargo": "cliente"},
        ]
        self.jogos = [
            {"id": 1, "nome": "Pokémon Emerald", "genero": "RPG", "preco": 59.99, "estoque": 10},
            {"id": 2, "nome": "The Legend of Zelda", "genero": "Ação/Aventura", "preco": 49.99, "estoque": 8},
            {"id": 3, "nome": "Mario Kart", "genero": "Corrida", "preco": 39.99, "estoque": 15},
        ]
        self.vendas = []  # Lista de vendas
        self.carrinhos = []  # Lista de carrinhos, cada um com {"cliente": str, "itens": [{"jogo_id": int, "quantidade": int}]}
        self.usuario_atual = None
        self.criar_tela_principal()

    # ------------------- TELAS -------------------
    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def criar_tela_principal(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="🎮 GamePoint", font=("Arial", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        ctk.CTkButton(self, text="Ver Jogos", command=self.criar_tela_jogos).pack(pady=10)
        if not self.usuario_atual:
            ctk.CTkButton(self, text="Login / Cadastro", command=self.criar_tela_login).pack(pady=10)
        else:
            if self.usuario_atual["cargo"] == "admin":
                ctk.CTkButton(self, text="Área Admin", command=self.criar_tela_admin).pack(pady=10)
            else:
                ctk.CTkButton(self, text="Área Cliente", command=self.criar_tela_cliente).pack(pady=10)
        ctk.CTkButton(self, text="Sair", fg_color="#b83232", command=self.destroy).pack(pady=10)

    def criar_tela_login(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Login", font=("Arial", 24, "bold")).pack(pady=20)
        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entry_usuario.pack(pady=5)
        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_senha.pack(pady=5)
        ctk.CTkButton(self, text="Entrar", command=self.fazer_login).pack(pady=10)
        ctk.CTkButton(self, text="Cadastrar", command=self.criar_tela_cadastro).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_principal).pack(pady=10)

    def criar_tela_cadastro(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Cadastro", font=("Arial", 24, "bold")).pack(pady=20)
        self.entry_novo_usuario = ctk.CTkEntry(self, placeholder_text="Novo Usuário")
        self.entry_novo_usuario.pack(pady=5)
        self.entry_nova_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_nova_senha.pack(pady=5)
        ctk.CTkButton(self, text="Cadastrar", command=self.cadastrar_usuario).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_login).pack(pady=10)

    def criar_tela_jogos(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Catálogo de Jogos", font=("Arial", 24, "bold")).pack(pady=20)
        for jogo in self.jogos:
            texto = f"{jogo['nome']} ({jogo['genero']}) - R${jogo['preco']:.2f} (Estoque: {jogo['estoque']})"
            ctk.CTkButton(self, text=texto, command=lambda j=jogo: self.adicionar_ao_carrinho(j)).pack(pady=5)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_principal).pack(pady=15)

    def criar_tela_admin(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Área Admin", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkButton(self, text="Cadastrar Jogo", command=self.criar_tela_cadastrar_jogo).pack(pady=10)
        ctk.CTkButton(self, text="Ver Relatórios", command=self.criar_tela_relatorios).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_principal).pack(pady=10)

    def criar_tela_cliente(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Área do Cliente", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkButton(self, text="Ver Jogos", command=self.criar_tela_jogos).pack(pady=10)
        ctk.CTkButton(self, text="Ver Carrinho", command=self.criar_tela_carrinho).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_principal).pack(pady=10)

    def criar_tela_carrinho(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Carrinho de Compras", font=("Arial", 24, "bold")).pack(pady=20)
        
        if not self.usuario_atual:
            ctk.CTkLabel(self, text="Faça login para ver o carrinho.").pack(pady=10)
        else:
            carrinho_usuario = next((c for c in self.carrinhos if c["cliente"] == self.usuario_atual["nome"]), None)
            if not carrinho_usuario or not carrinho_usuario["itens"]:
                ctk.CTkLabel(self, text="Seu carrinho está vazio.").pack(pady=10)
            else:
                total = 0
                for item in carrinho_usuario["itens"]:
                    jogo = next(j for j in self.jogos if j["id"] == item["jogo_id"])
                    valor_item = jogo["preco"] * item["quantidade"]
                    total += valor_item
                    texto = f"{jogo['nome']} - {item['quantidade']} x R${jogo['preco']:.2f} = R${valor_item:.2f}"
                    ctk.CTkLabel(self, text=texto).pack(pady=5)
                ctk.CTkLabel(self, text=f"Total: R${total:.2f}", font=("Arial", 16, "bold")).pack(pady=10)
                ctk.CTkButton(self, text="Finalizar Compra", command=self.finalizar_compra).pack(pady=10)
        
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_cliente).pack(pady=10)

    def criar_tela_cadastrar_jogo(self):
        self.limpar_tela()
        ctk.CTkLabel(self, text="Cadastrar Jogo", font=("Arial", 24, "bold")).pack(pady=20)
        self.entry_nome_jogo = ctk.CTkEntry(self, placeholder_text="Nome do Jogo")
        self.entry_nome_jogo.pack(pady=5)
        self.entry_genero = ctk.CTkEntry(self, placeholder_text="Gênero")
        self.entry_genero.pack(pady=5)
        self.entry_preco = ctk.CTkEntry(self, placeholder_text="Preço")
        self.entry_preco.pack(pady=5)
        self.entry_estoque = ctk.CTkEntry(self, placeholder_text="Estoque")
        self.entry_estoque.pack(pady=5)
        ctk.CTkButton(self, text="Cadastrar Jogo", command=self.cadastrar_jogo).pack(pady=10)
        ctk.CTkButton(self, text="Voltar", command=self.criar_tela_admin).pack(pady=10)

    # ------------------- FUNÇÕES -------------------
    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        for u in self.usuarios:
            if u["nome"] == usuario and u["senha"] == senha:
                self.usuario_atual = u
                messagebox.showinfo("Sucesso", f"Bem-vindo {usuario}!")
                self.criar_tela_principal()
                return
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def cadastrar_usuario(self):
        usuario = self.entry_novo_usuario.get()
        senha = self.entry_nova_senha.get()
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        for u in self.usuarios:
            if u["nome"] == usuario:
                messagebox.showerror("Erro", "Usuário já existe!")
                return
        self.usuarios.append({"nome": usuario, "senha": senha, "cargo": "cliente"})
        messagebox.showinfo("Sucesso", "Usuário cadastrado!")
        self.criar_tela_login()

    def adicionar_ao_carrinho(self, jogo):
        if not self.usuario_atual:
            messagebox.showwarning("Atenção", "Faça login para adicionar ao carrinho.")
            return
        if jogo["estoque"] <= 0:
            messagebox.showinfo("Indisponível", "Sem estoque.")
            return
        
        # Encontrar ou criar carrinho do usuário
        carrinho_usuario = next((c for c in self.carrinhos if c["cliente"] == self.usuario_atual["nome"]), None)
        if not carrinho_usuario:
            carrinho_usuario = {"cliente": self.usuario_atual["nome"], "itens": []}
            self.carrinhos.append(carrinho_usuario)
        
        # Adicionar ou atualizar item no carrinho
        item_existente = next((item for item in carrinho_usuario["itens"] if item["jogo_id"] == jogo["id"]), None)
        if item_existente:
            item_existente["quantidade"] += 1
        else:
            carrinho_usuario["itens"].append({"jogo_id": jogo["id"], "quantidade": 1})
        
        messagebox.showinfo("Carrinho", f"{jogo['nome']} adicionado ao carrinho!")

    def finalizar_compra(self):
        if not self.usuario_atual:
            messagebox.showwarning("Atenção", "Faça login para finalizar a compra.")
            return
        
        carrinho_usuario = next((c for c in self.carrinhos if c["cliente"] == self.usuario_atual["nome"]), None)
        if not carrinho_usuario or not carrinho_usuario["itens"]:
            messagebox.showinfo("Carrinho", "Seu carrinho está vazio.")
            return
        
        total = 0
        for item in carrinho_usuario["itens"]:
            jogo = next(j for j in self.jogos if j["id"] == item["jogo_id"])
            if jogo["estoque"] < item["quantidade"]:
                messagebox.showerror("Erro", f"Estoque insuficiente para {jogo['nome']}.")
                return
            total += jogo["preco"] * item["quantidade"]
            jogo["estoque"] -= item["quantidade"]
            self.vendas.append({
                "cliente": self.usuario_atual["nome"],
                "jogo": jogo["nome"],
                "quantidade": item["quantidade"],
                "valor": jogo["preco"] * item["quantidade"],
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
        
        carrinho_usuario["itens"] = []  # Limpar carrinho após compra
        messagebox.showinfo("Compra", f"Compra finalizada! Total: R${total:.2f}")
        self.criar_tela_cliente()

    def cadastrar_jogo(self):
        nome = self.entry_nome_jogo.get()
        genero = self.entry_genero.get()
        try:
            preco = float(self.entry_preco.get())
            estoque = int(self.entry_estoque.get())
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números!")
            return
        if not nome or not genero or preco <= 0 or estoque < 0:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return
        novo_id = max(j["id"] for j in self.jogos) + 1 if self.jogos else 1
        self.jogos.append({"id": novo_id, "nome": nome, "genero": genero, "preco": preco, "estoque": estoque})
        messagebox.showinfo("Sucesso", "Jogo cadastrado com sucesso!")
        self.criar_tela_admin()

    def criar_tela_relatorios(self):
        total = sum(v["valor"] for v in self.vendas)
        vendas_texto = "\n".join([f"{v['jogo']} - {v['quantidade']} x R${v['valor']/v['quantidade']:.2f} = R${v['valor']:.2f} ({v['data']})" for v in self.vendas])
        messagebox.showinfo("Relatórios", f"Total de vendas: R${total:.2f}\n\nDetalhes:\n{vendas_texto if vendas_texto else 'Nenhuma venda.'}")

# ------------------- EXECUTAR -------------------
if __name__ == "__main__":
    app = LojaJogos()
    app.mainloop()