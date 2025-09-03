import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

usuarios = {
    "admin": {"senha": "admin123", "cargo": "admin"},
    "cliente": {"senha": "cliente123", "cargo": "cliente"}
}
jogos = [
    {"id": 1, "nome": "Pokémon Emerald", "genero": "RPG", "preco": 59.99, "estoque": 10},
    {"id": 2, "nome": "The Legend of Zelda: The Minish Cap", "genero": "Ação/Aventura", "preco": 49.99, "estoque": 8},
    {"id": 3, "nome": "Metroid Fusion", "genero": "Ação/Aventura", "preco": 44.99, "estoque": 12},
    {"id": 4, "nome": "Mario Kart: Super Circuit", "genero": "Corrida", "preco": 39.99, "estoque": 15},
    {"id": 5, "nome": "Fire Emblem: The Sacred Stones", "genero": "RPG/Estratégia", "preco": 54.99, "estoque": 7}
]
vendas = []
carrinhos = {}

class LojaJogos(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GamePoint")
        self.geometry("800x650")
        self.configure(fg_color="#1e1e2e")
        self.resizable(True, True)
        self.usuario_atual = None
        self.criar_tela_principal()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    def criar_tela_principal(self):
        self.limpar_tela()
        self.frame_inicio = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_inicio, text=" GamePoint", font=("Roboto", 32, "bold"), text_color="#4CAF50").pack(pady=40)
        botao_ver_jogos = ctk.CTkButton(self.frame_inicio, text="Ver Jogos", width=250, height=48, font=("Roboto", 16),
                                        corner_radius=10, command=self.criar_tela_jogos)
        botao_ver_jogos.pack(pady=12)
        if not self.usuario_atual:
            botao_login = ctk.CTkButton(self.frame_inicio, text="Login / Cadastro", width=250, height=48, font=("Roboto", 16),
                                        corner_radius=10, command=self.criar_tela_login)
            botao_login.pack(pady=12)
        botao_sair = ctk.CTkButton(self.frame_inicio, text="Sair", width=150, height=40, font=("Roboto", 14),
                                   fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10, command=self.destroy)
        botao_sair.pack(pady=20)
        self.frame_inicio.pack(expand=True, fill="both", padx=20, pady=20)

    def criar_tela_login(self):
        self.limpar_tela()
        self.frame_login = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_login, text=" Login", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=30)
        form_login = ctk.CTkFrame(self.frame_login, fg_color="transparent")
        form_login.pack(pady=10)
        self.entry_usuario = ctk.CTkEntry(form_login, placeholder_text="Usuário", width=350, height=40, font=("Roboto", 14))
        self.entry_usuario.pack(pady=10)
        self.entry_senha = ctk.CTkEntry(form_login, placeholder_text="Senha", show="*", width=350, height=40, font=("Roboto", 14))
        self.entry_senha.pack(pady=10)
        botao_entrar = ctk.CTkButton(form_login, text="Entrar", width=250, height=48, font=("Roboto", 16),
                                     corner_radius=10, command=self.fazer_login)
        botao_entrar.pack(pady=15)
        botao_cadastrar = ctk.CTkButton(form_login, text="Cadastrar", width=250, height=48, font=("Roboto", 16),
                                        corner_radius=10, command=self.criar_tela_cadastro)
        botao_cadastrar.pack(pady=10)
        botao_voltar = ctk.CTkButton(form_login, text="Voltar", width=150, height=40, font=("Roboto", 14),
                                     fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10, command=self.criar_tela_principal)
        botao_voltar.pack(pady=15)
        self.frame_login.pack(expand=True, fill="both", padx=20, pady=20)

    def criar_tela_cadastro(self):
        self.limpar_tela()
        self.frame_cadastro = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_cadastro, text=" Cadastro", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=30)
        form_cadastro = ctk.CTkFrame(self.frame_cadastro, fg_color="transparent")
        form_cadastro.pack(pady=10)
        self.entry_novo_usuario = ctk.CTkEntry(form_cadastro, placeholder_text="Novo Usuário", width=350, height=40, font=("Roboto", 14))
        self.entry_novo_usuario.pack(pady=10)
        self.entry_nova_senha = ctk.CTkEntry(form_cadastro, placeholder_text="Senha", show="*", width=350, height=40, font=("Roboto", 14))
        self.entry_nova_senha.pack(pady=10)
        botao_cadastrar = ctk.CTkButton(form_cadastro, text="Cadastrar", width=250, height=48, font=("Roboto", 16),
                                        corner_radius=10, command=self.cadastrar_usuario)
        botao_cadastrar.pack(pady=15)
        botao_voltar = ctk.CTkButton(form_cadastro, text="Voltar", width=150, height=40, font=("Roboto", 14),
                                     fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10, command=self.criar_tela_login)
        botao_voltar.pack(pady=15)
        self.frame_cadastro.pack(expand=True, fill="both", padx=20, pady=20)

    def criar_tela_jogos(self):
        self.limpar_tela()
        self.frame_jogos = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_jogos, text=" Jogos", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        search_frame = ctk.CTkFrame(self.frame_jogos, fg_color="transparent")
        search_frame.pack(pady=10)
        self.entry_busca = ctk.CTkEntry(search_frame, placeholder_text="Buscar por nome ou gênero", width=400, height=40, font=("Roboto", 14))
        self.entry_busca.pack(side="left", padx=10)
        botao_buscar = ctk.CTkButton(search_frame, text="Buscar", width=100, height=40, font=("Roboto", 14),
                                     corner_radius=10, command=self.atualizar_jogos)
        botao_buscar.pack(side="left")
        self.frame_lista = ctk.CTkScrollableFrame(self.frame_jogos, width=650, height=400, corner_radius=12)
        self.frame_lista.pack(pady=15, padx=10)
        botoes_jogos = ctk.CTkFrame(self.frame_jogos, fg_color="transparent")
        botoes_jogos.pack(pady=15)
        botao_voltar = ctk.CTkButton(botoes_jogos, text="Voltar", width=200, height=48, font=("Roboto", 16),
                                     fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10,
                                     command=self.voltar_da_tela_jogos)
        botao_voltar.pack(side="left", padx=10)
        self.frame_jogos.pack(expand=True, fill="both", padx=20, pady=20)
        self.atualizar_jogos()

    def criar_tela_admin(self):
        self.limpar_tela()
        self.frame_admin = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_admin, text=" Área Admin", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        admin_menu = ctk.CTkFrame(self.frame_admin, fg_color="transparent")
        admin_menu.pack(pady=10)
        botao_cadastrar_jogo = ctk.CTkButton(admin_menu, text="Cadastrar Jogo", width=300, height=48, font=("Roboto", 16),
                                             corner_radius=10, command=self.criar_tela_cadastrar_jogo)
        botao_cadastrar_jogo.pack(pady=12)
        botao_editar_excluir = ctk.CTkButton(admin_menu, text="Editar/Excluir Jogo", width=300, height=48, font=("Roboto", 16),
                                             corner_radius=10, command=self.criar_tela_editar_excluir_jogo)
        botao_editar_excluir.pack(pady=12)
        botao_relatorios = ctk.CTkButton(admin_menu, text="Relatório de Vendas", width=300, height=48, font=("Roboto", 16),
                                         corner_radius=10, command=self.criar_tela_relatorios)
        botao_relatorios.pack(pady=12)
        botao_gerenciar_usuarios = ctk.CTkButton(admin_menu, text="Gerenciar Usuários", width=300, height=48, font=("Roboto", 16),
                                                 corner_radius=10, command=self.criar_tela_gerenciar_usuarios)
        botao_gerenciar_usuarios.pack(pady=12)
        botao_deslogar = ctk.CTkButton(admin_menu, text="Deslogar", width=300, height=48, font=("Roboto", 16),
                                       fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10, command=self.deslogar)
        botao_deslogar.pack(pady=12)
        self.frame_admin.pack(expand=True, fill="both", padx=20, pady=20)

    def criar_tela_gerenciar_usuarios(self):
        self.limpar_tela()
        self.frame_usuarios = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_usuarios, text=" Gerenciar Usuários", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        self.frame_lista_usuarios = ctk.CTkScrollableFrame(self.frame_usuarios, width=600, height=400, corner_radius=12)
        self.frame_lista_usuarios.pack(pady=15, padx=10)
        botao_voltar = ctk.CTkButton(self.frame_usuarios, text="Voltar", width=250, height=48, font=("Roboto", 16),
                                     corner_radius=10, command=self.criar_tela_admin)
        botao_voltar.pack(pady=15)
        self.frame_usuarios.pack(expand=True, fill="both", padx=20, pady=20)
        self.atualizar_lista_usuarios()

    def atualizar_lista_usuarios(self):
        for widget in self.frame_lista_usuarios.winfo_children():
            widget.destroy()
        for user, data in usuarios.items():
            if user == "admin":
                continue
            card = ctk.CTkFrame(self.frame_lista_usuarios, fg_color="#2a2a44", corner_radius=12)
            card.pack(pady=8, padx=15, fill="x")
            info = f"Usuário: {user} | Cargo: {data['cargo']}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), anchor="w").pack(side="left", padx=15, pady=10)
            botao_excluir = ctk.CTkButton(card, text="Excluir", width=100, height=36, font=("Roboto", 14),
                                          fg_color="#b83232", hover_color="#ff4d4d", corner_radius=8,
                                          command=lambda u=user: self.excluir_usuario(u))
            botao_excluir.pack(side="right", padx=10)

    def excluir_usuario(self, user):
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o usuário {user}?"):
            del usuarios[user]
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
            self.atualizar_lista_usuarios()

    def criar_tela_cadastrar_jogo(self):
        self.limpar_tela()
        self.frame_add_jogo = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_add_jogo, text=" Cadastrar Jogo", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        form_add_jogo = ctk.CTkFrame(self.frame_add_jogo, fg_color="transparent")
        form_add_jogo.pack(pady=10)
        self.nome_var = ctk.StringVar()
        self.genero_var = ctk.StringVar()
        self.preco_var = ctk.DoubleVar()
        self.estoque_var = ctk.IntVar()
        ctk.CTkEntry(form_add_jogo, textvariable=self.nome_var, placeholder_text="Nome do Jogo", width=350, height=40, font=("Roboto", 14)).pack(pady=8)
        ctk.CTkEntry(form_add_jogo, textvariable=self.genero_var, placeholder_text="Gênero", width=350, height=40, font=("Roboto", 14)).pack(pady=8)
        ctk.CTkEntry(form_add_jogo, textvariable=self.preco_var, placeholder_text="Preço", width=350, height=40, font=("Roboto", 14)).pack(pady=8)
        ctk.CTkEntry(form_add_jogo, textvariable=self.estoque_var, placeholder_text="Estoque", width=350, height=40, font=("Roboto", 14)).pack(pady=8)
        botoes_add_jogo = ctk.CTkFrame(self.frame_add_jogo, fg_color="transparent")
        botoes_add_jogo.pack(pady=15)
        botao_salvar = ctk.CTkButton(botoes_add_jogo, text="Salvar", width=200, height=48, font=("Roboto", 16),
                                     corner_radius=10, command=self.salvar_jogo)
        botao_salvar.pack(side="left", padx=10)
        botao_voltar = ctk.CTkButton(botoes_add_jogo, text="Voltar", width=200, height=48, font=("Roboto", 16),
                                     corner_radius=10, command=self.criar_tela_admin)
        botao_voltar.pack(side="left", padx=10)
        self.frame_add_jogo.pack(expand=True, fill="both", padx=20, pady=20)

    def criar_tela_editar_excluir_jogo(self):
        self.limpar_tela()
        self.frame_editar_excluir = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_editar_excluir, text=" Editar ou Excluir Jogo", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        self.frame_lista_edicao = ctk.CTkScrollableFrame(self.frame_editar_excluir, width=600, height=300, corner_radius=12)
        self.frame_lista_edicao.pack(pady=15, padx=10)
        form_editar = ctk.CTkFrame(self.frame_editar_excluir, fg_color="transparent")
        form_editar.pack(pady=10)
        self.entry_jnome_edit = ctk.CTkEntry(form_editar, placeholder_text="Nome do Jogo", width=350, height=40, font=("Roboto", 14))
        self.entry_jnome_edit.pack(pady=8)
        self.entry_genero_edit = ctk.CTkEntry(form_editar, placeholder_text="Gênero", width=350, height=40, font=("Roboto", 14))
        self.entry_genero_edit.pack(pady=8)
        self.entry_jpreco_edit = ctk.CTkEntry(form_editar, placeholder_text="Preço", width=350, height=40, font=("Roboto", 14))
        self.entry_jpreco_edit.pack(pady=8)
        self.entry_jestoque_edit = ctk.CTkEntry(form_editar, placeholder_text="Estoque", width=350, height=40, font=("Roboto", 14))
        self.entry_jestoque_edit.pack(pady=8)
        botao_voltar = ctk.CTkButton(self.frame_editar_excluir, text="Voltar", width=250, height=48, font=("Roboto", 16),
                                     corner_radius=10, command=self.criar_tela_admin)
        botao_voltar.pack(pady=15)
        self.frame_editar_excluir.pack(expand=True, fill="both", padx=20, pady=20)
        self.atualizar_lista_edicao()

    def criar_tela_relatorios(self):
        self.limpar_tela()
        self.frame_relatorios = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_relatorios, text=" Relatório de Vendas", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        colunas = ("Id", "Cliente", "Jogo", "Qtd", "Valor", "Data")
        self.tree = ttk.Treeview(self.frame_relatorios, columns=colunas, show="headings", height=15)
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, padx=15, pady=15)
        total_vendas = sum(venda['valor'] for venda in vendas)
        ctk.CTkLabel(self.frame_relatorios, text=f"Total de Vendas: R${total_vendas:.2f}", font=("Roboto", 18, "bold"), text_color="#4CAF50").pack(pady=10)
        botoes_relatorio = ctk.CTkFrame(self.frame_relatorios, fg_color="transparent")
        botoes_relatorio.pack(pady=15)
        botao_remover = ctk.CTkButton(botoes_relatorio, text="Remover Selecionados", width=200, height=40, font=("Roboto", 14),
                                      fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10, command=self.excluir_selecionados)
        botao_remover.pack(side="left", padx=10)
        botao_voltar = ctk.CTkButton(botoes_relatorio, text="Voltar", width=200, height=40, font=("Roboto", 14),
                                     corner_radius=10, command=self.criar_tela_admin)
        botao_voltar.pack(side="left", padx=10)
        self.frame_relatorios.pack(expand=True, fill="both", padx=20, pady=20)
        self.atualizar_relatorio()

    def criar_tela_cliente(self):
        self.limpar_tela()
        self.frame_cliente = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_cliente, text=" Área do Cliente", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        botao_ver_jogos = ctk.CTkButton(self.frame_cliente, text="Ver Jogos", width=250, height=48, font=("Roboto", 16),
                                        corner_radius=10, command=self.criar_tela_jogos)
        botao_ver_jogos.pack(pady=12)
        botao_ver_carrinho = ctk.CTkButton(self.frame_cliente, text="Ver Carrinho", width=250, height=48, font=("Roboto", 16),
                                           corner_radius=10, command=self.criar_tela_carrinho)
        botao_ver_carrinho.pack(pady=12)
        botao_ver_compras = ctk.CTkButton(self.frame_cliente, text="Ver Minhas Compras", width=250, height=48, font=("Roboto", 16),
                                          corner_radius=10, command=self.criar_tela_minhas_compras)
        botao_ver_compras.pack(pady=12)
        botao_deslogar = ctk.CTkButton(self.frame_cliente, text="Deslogar", width=250, height=48, font=("Roboto", 16),
                                       fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10, command=self.deslogar)
        botao_deslogar.pack(pady=12)
        self.frame_cliente.pack(expand=True, fill="both", padx=20, pady=20)

    def criar_tela_minhas_compras(self):
        self.limpar_tela()
        self.frame_compras = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_compras, text=" Minhas Compras", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        colunas = ("Id", "Jogo", "Qtd", "Valor", "Data")
        self.tree_compras = ttk.Treeview(self.frame_compras, columns=colunas, show="headings", height=15)
        for col in colunas:
            self.tree_compras.heading(col, text=col)
            self.tree_compras.column(col, anchor="center", width=150)
        self.tree_compras.pack(fill="both", expand=True, padx=15, pady=15)
        total_compras = sum(venda['valor'] for venda in vendas if venda['cliente'] == self.usuario_atual["nome_usuario"])
        ctk.CTkLabel(self.frame_compras, text=f"Total Gasto: R${total_compras:.2f}", font=("Roboto", 18, "bold"), text_color="#4CAF50").pack(pady=10)
        botao_voltar = ctk.CTkButton(self.frame_compras, text="Voltar", width=200, height=40, font=("Roboto", 14),
                                     corner_radius=10, command=self.criar_tela_cliente)
        botao_voltar.pack(pady=15)
        self.frame_compras.pack(expand=True, fill="both", padx=20, pady=20)
        self.atualizar_minhas_compras()

    def atualizar_minhas_compras(self):
        for i in self.tree_compras.get_children():
            self.tree_compras.delete(i)
        username = self.usuario_atual["nome_usuario"]
        for idx, venda in enumerate([v for v in vendas if v['cliente'] == username], start=1):
            self.tree_compras.insert("", "end", values=(idx, venda['jogo'], venda['quantidade'], f"R${venda['valor']:.2f}", venda['data']))

    def criar_tela_carrinho(self):
        self.limpar_tela()
        self.frame_carrinho = ctk.CTkFrame(self, fg_color="#2a2a3a", corner_radius=20)
        ctk.CTkLabel(self.frame_carrinho, text="Carrinho", font=("Roboto", 28, "bold"), text_color="#4CAF50").pack(pady=20)
        self.frame_lista_carrinho = ctk.CTkScrollableFrame(self.frame_carrinho, width=650, height=500, corner_radius=12)
        self.frame_lista_carrinho.pack(pady=15, padx=10)
        botoes_carrinho = ctk.CTkFrame(self.frame_carrinho, fg_color="transparent")
        botoes_carrinho.pack(pady=15)
        botao_finalizar = ctk.CTkButton(botoes_carrinho, text="Finalizar Compra", width=200, height=48, font=("Roboto", 16),
                                        corner_radius=10, command=self.finalizar_compra)
        botao_finalizar.pack(side="left", padx=10)
        botao_voltar = ctk.CTkButton(botoes_carrinho, text="Voltar", width=200, height=48, font=("Roboto", 16),
                                     fg_color="#b83232", hover_color="#ff4d4d", corner_radius=10,
                                     command=self.voltar_da_tela_carrinho)
        botao_voltar.pack(side="left", padx=10)
        self.frame_carrinho.pack(expand=True, fill="both", padx=20, pady=20)
        self.atualizar_carrinho()

    def voltar_da_tela_carrinho(self):
        if self.usuario_atual and self.usuario_atual["cargo"] == "cliente":
            self.criar_tela_cliente()
        else:
            self.criar_tela_principal()

    def fazer_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        if usuario in usuarios and usuarios[usuario]["senha"] == senha:
            self.usuario_atual = {"nome_usuario": usuario, "cargo": usuarios[usuario]["cargo"]}
            if self.usuario_atual["cargo"] == "admin":
                self.criar_tela_admin()
            else:
                self.criar_tela_cliente()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def cadastrar_usuario(self):
        usuario = self.entry_novo_usuario.get()
        senha = self.entry_nova_senha.get()
        if usuario and senha:
            if usuario in usuarios:
                messagebox.showerror("Erro", "Nome de usuário já existe!")
            else:
                usuarios[usuario] = {"senha": senha, "cargo": "cliente"}
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                self.criar_tela_login()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    def atualizar_jogos(self):
        for w in self.frame_lista.winfo_children():
            w.destroy()
        busca = self.entry_busca.get().lower() if hasattr(self, 'entry_busca') else ""
        jogos_filtrados = [j for j in jogos if busca in j['nome'].lower() or busca in j['genero'].lower()]
        for jogo in jogos_filtrados:
            card = ctk.CTkFrame(self.frame_lista, fg_color="#2a2a44", corner_radius=12)
            card.pack(pady=8, padx=15, fill="x")
            if self.usuario_atual and self.usuario_atual["cargo"] == "admin":
                info = f"{jogo['nome']} ({jogo['genero']}) — R${jogo['preco']:.2f} | Estoque: {jogo['estoque']}"
            else:
                info = f"{jogo['nome']} ({jogo['genero']}) — R${jogo['preco']:.2f}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), anchor="w").pack(side="left", padx=15, pady=10)
            botao_comprar = ctk.CTkButton(card, text="Comprar", width=100, height=36, font=("Roboto", 14),
                                          corner_radius=8, command=lambda j=jogo: self.comprar(j))
            botao_comprar.pack(side="right", padx=5)
            botao_carrinho = ctk.CTkButton(card, text="Adicionar ao Carrinho", width=150, height=36, font=("Roboto", 14),
                                           corner_radius=8, command=lambda j=jogo: self.adicionar_ao_carrinho(j))
            botao_carrinho.pack(side="right", padx=5)

    def comprar(self, jogo):
        if not self.usuario_atual:
            messagebox.showwarning("Acesso negado", "Faça login para comprar.")
            return
        if jogo["estoque"] <= 0:
            messagebox.showinfo("Indisponível", "Sem estoque.")
            return
        jogo["estoque"] -= 1
        vendas.append({
            "cliente": self.usuario_atual["nome_usuario"],
            "jogo": jogo["nome"],
            "quantidade": 1,
            "valor": jogo["preco"],
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        messagebox.showinfo("Compra", f"Você comprou {jogo['nome']} por R${jogo['preco']:.2f}")
        self.atualizar_jogos()

    def adicionar_ao_carrinho(self, jogo):
        if not self.usuario_atual:
            messagebox.showwarning("Acesso negado", "Faça login para adicionar ao carrinho.")
            return
        if jogo["estoque"] <= 0:
            messagebox.showinfo("Indisponível", "Sem estoque.")
            return
        username = self.usuario_atual["nome_usuario"]
        if username not in carrinhos:
            carrinhos[username] = []
        for item in carrinhos[username]:
            if item["jogo"]["id"] == jogo["id"]:
                if item["quantidade"] < jogo["estoque"]:
                    item["quantidade"] += 1
                else:
                    messagebox.showinfo("Limite", "Quantidade máxima em estoque atingida.")
                self.atualizar_carrinho()
                return
        carrinhos[username].append({"jogo": jogo, "quantidade": 1})
        messagebox.showinfo("Sucesso", f"{jogo['nome']} adicionado ao carrinho!")
        self.atualizar_carrinho()

    def atualizar_carrinho(self):
        for w in self.frame_lista_carrinho.winfo_children():
            w.destroy()
        if not self.usuario_atual or self.usuario_atual["nome_usuario"] not in carrinhos or not carrinhos[self.usuario_atual["nome_usuario"]]:
            ctk.CTkLabel(self.frame_lista_carrinho, text="Carrinho vazio", font=("Roboto", 16)).pack(pady=20)
            return
        total = 0
        for item in carrinhos[self.usuario_atual["nome_usuario"]]:
            card = ctk.CTkFrame(self.frame_lista_carrinho, fg_color="#2a2a44", corner_radius=12)
            card.pack(pady=8, padx=15, fill="x")
            info = f"{item['jogo']['nome']} ({item['jogo']['genero']}) — R${item['jogo']['preco']:.2f} x {item['quantidade']} = R${item['jogo']['preco'] * item['quantidade']:.2f}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), anchor="w").pack(side="left", padx=15, pady=10)
            botao_remover = ctk.CTkButton(card, text="Remover", width=100, height=36, font=("Roboto", 14),
                                          fg_color="#b83232", hover_color="#ff4d4d", corner_radius=8,
                                          command=lambda i=item: self.remover_do_carrinho(i))
            botao_remover.pack(side="right", padx=10)
            total += item["jogo"]["preco"] * item["quantidade"]
        ctk.CTkLabel(self.frame_lista_carrinho, text=f"Total: R${total:.2f}", font=("Roboto", 18, "bold"), text_color="#4CAF50").pack(pady=20)

    def remover_do_carrinho(self, item):
        username = self.usuario_atual["nome_usuario"]
        carrinhos[username].remove(item)
        if not carrinhos[username]:
            del carrinhos[username]
        self.atualizar_carrinho()
        messagebox.showinfo("Sucesso", f"{item['jogo']['nome']} removido do carrinho!")

    def finalizar_compra(self):
        if not self.usuario_atual or self.usuario_atual["nome_usuario"] not in carrinhos or not carrinhos[self.usuario_atual["nome_usuario"]]:
            messagebox.showinfo("Carrinho vazio", "Adicione itens ao carrinho antes de finalizar a compra.")
            return
        username = self.usuario_atual["nome_usuario"]
        for item in carrinhos[username]:
            jogo = item["jogo"]
            quantidade = item["quantidade"]
            if jogo["estoque"] < quantidade:
                messagebox.showerror("Erro", f"Estoque insuficiente para {jogo['nome']}.")
                return
            jogo["estoque"] -= quantidade
            vendas.append({
                "cliente": username,
                "jogo": jogo["nome"],
                "quantidade": quantidade,
                "valor": jogo["preco"] * quantidade,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
        del carrinhos[username]
        messagebox.showinfo("Compra", "Compra finalizada com sucesso!")
        self.criar_tela_cliente()

    def salvar_jogo(self):
        try:
            nome = self.nome_var.get()
            genero = self.genero_var.get()
            preco = self.preco_var.get()
            estoque = self.estoque_var.get()
            if nome and genero and preco > 0 and estoque > 0:
                jogo_id = max([j['id'] for j in jogos], default=0) + 1
                jogos.append({"id": jogo_id, "nome": nome, "genero": genero, "preco": preco, "estoque": estoque})
                messagebox.showinfo("Sucesso", "Jogo cadastrado com sucesso!")
                self.criar_tela_admin()
            else:
                messagebox.showerror("Erro", "Todos os campos são obrigatórios e valores devem ser positivos!")
        except ValueError:
            messagebox.showerror("Erro", "Preço ou estoque inválido.")

    def atualizar_lista_edicao(self):
        for widget in self.frame_lista_edicao.winfo_children():
            widget.destroy()
        for jogo in jogos:
            botao_jogo = ctk.CTkButton(self.frame_lista_edicao, text=f"{jogo['nome']} (ID: {jogo['id']})",
                                       width=300, height=48, font=("Roboto", 14),
                                       corner_radius=8, command=lambda j=jogo: self.editar_excluir_jogo(j))
            botao_jogo.pack(pady=6)

    def editar_excluir_jogo(self, jogo):
        self.entry_jnome_edit.delete(0, "end")
        self.entry_genero_edit.delete(0, "end")
        self.entry_jpreco_edit.delete(0, "end")
        self.entry_jestoque_edit.delete(0, "end")
        self.entry_jnome_edit.insert(0, jogo["nome"])
        self.entry_genero_edit.insert(0, jogo["genero"])
        self.entry_jpreco_edit.insert(0, jogo["preco"])
        self.entry_jestoque_edit.insert(0, jogo["estoque"])
        def atualizar():
            try:
                nome = self.entry_jnome_edit.get()
                genero = self.entry_genero_edit.get()
                preco = float(self.entry_jpreco_edit.get())
                estoque = int(self.entry_jestoque_edit.get())
                if nome and genero and preco > 0 and estoque >= 0:
                    jogo.update({"nome": nome, "genero": genero, "preco": preco, "estoque": estoque})
                    messagebox.showinfo("Sucesso", "Jogo atualizado com sucesso!")
                    self.criar_tela_editar_excluir_jogo()
                else:
                    messagebox.showerror("Erro", "Todos os campos são obrigatórios e valores devem ser positivos!")
            except ValueError:
                messagebox.showerror("Erro", "Dados inválidos.")
        def excluir():
            if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este jogo?"):
                jogos.remove(jogo)
                messagebox.showinfo("Sucesso", "Jogo excluído com sucesso!")
                self.criar_tela_editar_excluir_jogo()
        botoes = ctk.CTkFrame(self.frame_lista_edicao, fg_color="transparent")
        botoes.pack(pady=15)
        botao_atualizar = ctk.CTkButton(botoes, text="Atualizar", width=120, height=40, font=("Roboto", 14),
                                        corner_radius=8, command=atualizar)
        botao_atualizar.pack(side="left", padx=8)
        botao_excluir = ctk.CTkButton(botoes, text="Excluir", width=120, height=40, font=("Roboto", 14),
                                      fg_color="#b83232", hover_color="#ff4d4d", corner_radius=8, command=excluir)
        botao_excluir.pack(side="left", padx=8)
        botao_voltar = ctk.CTkButton(botoes, text="Voltar", width=120, height=40, font=("Roboto", 14),
                                     corner_radius=8, command=self.criar_tela_editar_excluir_jogo)
        botao_voltar.pack(side="left", padx=8)

    def atualizar_relatorio(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, venda in enumerate(vendas, start=1):
            self.tree.insert("", "end", values=(idx, venda['cliente'], venda['jogo'], venda['quantidade'], f"R${venda['valor']:.2f}", venda['data']))

    def excluir_selecionados(self):
        selecionados = self.tree.selection()
        for item in selecionados:
            idx = int(self.tree.item(item, "values")[0]) - 1
            if 0 <= idx < len(vendas):
                vendas.pop(idx)
        self.atualizar_relatorio()
        messagebox.showinfo("Removido", "Venda(s) removida(s).")

    def deslogar(self):
        self.usuario_atual = None
        messagebox.showinfo("Logout", "Saiu da conta.")
        self.criar_tela_principal()

    def voltar_da_tela_jogos(self):
        if self.usuario_atual and self.usuario_atual["cargo"] == "cliente":
            self.criar_tela_cliente()
        else:
            self.criar_tela_principal()

    def rodar(self):
        self.mainloop()

if __name__ == "__main__":
    app = LojaJogos()
    app.rodar()