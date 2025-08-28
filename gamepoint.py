import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

usuarios = {"admin": "1234"}
usuario_logado = [None]

jogos = []
vendas = []
carrinho = []

janela = ctk.CTk()
janela.title("GamePoint")
janela.geometry("700x800")
janela.configure(fg_color="#1e1e2e")

def limpar_tela():
    for widget in janela.winfo_children():
        widget.pack_forget()

def mostrar_principal():
    limpar_tela()
    frame_inicio.pack(expand=True)

def mostrar_login():
    limpar_tela()
    frame_login.pack(pady=50)

def mostrar_cadastro():
    limpar_tela()
    frame_cadastro.pack(pady=50)

def mostrar_jogos():
    limpar_tela()
    frame_jogos.pack(pady=20)
    atualizar_jogos()

def mostrar_admin_menu():
    limpar_tela()
    frame_admin.pack(pady=20)

def entrar():
    usuario = usuario_entry.get()
    senha = senha_entry.get()
    if usuarios.get(usuario) == senha:
        usuario_logado[0] = usuario
        messagebox.showinfo("Login", f"Bem-vindo, {usuario}!")
        if usuario == "admin":
            mostrar_admin_menu()
        else:
            mostrar_principal()
    else:
        messagebox.showerror("Erro", "Credenciais inválidas.")

def cadastrar():
    usuario = entry_new_user.get()
    senha = entry_new_pass.get()
    if usuario and senha and usuario not in usuarios:
        usuarios[usuario] = senha
        messagebox.showinfo("Sucesso", "Usuário cadastrado!")
        mostrar_login()
    else:
        messagebox.showerror("Erro", "Dados inválidos ou usuário já existe.")

def atualizar_jogos():
    for widget in frame_lista.winfo_children():
        widget.destroy()
    for jogo in jogos:
        card = ctk.CTkFrame(frame_lista, fg_color="#2a2a44")
        card.pack(pady=5, padx=10, fill="x")

        nome_preco = f"{jogo['nome']} — R${jogo['preco']:.2f} | Estoque: {jogo['estoque']}"
        ctk.CTkLabel(card, text=nome_preco, font=("Roboto", 14)).pack(side="left", padx=10)

        btn_comprar = ctk.CTkButton(card, text="Comprar", width=80, command=lambda j=jogo: comprar(j))
        btn_comprar.pack(side="right", padx=5)

        btn_carrinho = ctk.CTkButton(card, text="Carrinho", width=80, command=lambda j=jogo: add_carrinho(j))
        btn_carrinho.pack(side="right")

def comprar(jogo):
    if not usuario_logado[0]:
        messagebox.showwarning("Acesso negado", "Faça login para comprar.")
    elif jogo["estoque"] <= 0:
        messagebox.showinfo("Indisponível", "Jogo sem estoque.")
    else:
        jogo["estoque"] -= 1
        vendas.append({"cliente": usuario_logado[0], "jogo": jogo["nome"], "valor": jogo["preco"]})
        messagebox.showinfo("Compra", f"Você comprou {jogo['nome']} por R${jogo['preco']:.2f}")
        atualizar_jogos()

def add_carrinho(jogo):
    if not usuario_logado[0]:
        messagebox.showwarning("Acesso negado", "Faça login para adicionar ao carrinho.")
    else:
        carrinho.append(jogo)
        messagebox.showinfo("Carrinho", f"{jogo['nome']} adicionado!")

def cadastrar_jogo():
    nome = entry_jnome.get()
    preco_texto = entry_jpreco.get()
    estoque_texto = entry_jestoque.get()

    try:
        preco = float(preco_texto)
        estoque = int(estoque_texto)
    except ValueError:
        messagebox.showerror("Erro", "Preço ou estoque inválido.")
        return

    jogos.append({"nome": nome, "preco": preco, "estoque": estoque})
    messagebox.showinfo("Adicionado", f"{nome} cadastrado com sucesso.")
    atualizar_jogos()

def excluir_jogo(jogo):
    jogos.remove(jogo)
    atualizar_jogos()

def ver_relatorios():
    if vendas:
        texto = "\n".join(f"{v['cliente']} comprou {v['jogo']} por R${v['valor']:.2f}" for v in vendas)
    else:
        texto = "Nenhuma venda ainda."
    messagebox.showinfo("Relatório de Vendas", texto)


# Tela inicial
frame_inicio = ctk.CTkFrame(janela, fg_color="#2a2a3a", corner_radius=15)
ctk.CTkLabel(frame_inicio, text="Bem-vindo à Loja de Jogos", font=("Roboto", 24, "bold")).pack(pady=20)

button_frame_inicio = ctk.CTkFrame(frame_inicio, fg_color="transparent")
button_frame_inicio.pack(pady=10)

btn_ver_jogos = ctk.CTkButton(button_frame_inicio, text="Ver Jogos", width=200, height=40,
font=("Roboto", 14), corner_radius=10, hover_color="#3b82f6",
command=mostrar_jogos)
btn_ver_jogos.pack(pady=10)

btn_login_cadastro = ctk.CTkButton(button_frame_inicio, text="Login / Cadastro", width=200, height=40,
font=("Roboto", 14), corner_radius=10, hover_color="#3b82f6",
command=mostrar_login)
btn_login_cadastro.pack(pady=10)


# Tela de login
frame_login = ctk.CTkFrame(janela, fg_color="#2a2a3a", corner_radius=15)

ctk.CTkLabel(frame_login, text="Login", font=("Roboto", 24, "bold")).pack(pady=20)

login_frame = ctk.CTkFrame(frame_login, fg_color="transparent")
login_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(login_frame, text="Usuário", font=("Roboto", 14)).pack(pady=5)
usuario_entry = ctk.CTkEntry(login_frame, placeholder_text="Digite seu usuário", width=300, font=("Roboto", 14))
usuario_entry.pack(pady=5)

ctk.CTkLabel(login_frame, text="Senha", font=("Roboto", 14)).pack(pady=5)
senha_entry = ctk.CTkEntry(login_frame, placeholder_text="Digite sua senha", show="*", width=300, font=("Roboto", 14))
senha_entry.pack(pady=5)

button_frame_login = ctk.CTkFrame(frame_login, fg_color="transparent")
button_frame_login.pack(pady=20)

btn_entrar = ctk.CTkButton(button_frame_login, text="Entrar", command=entrar, width=150, height=40,
font=("Roboto", 14), corner_radius=10, hover_color="#3b82f6")
btn_entrar.pack(side="left", padx=10)

btn_cadastrar = ctk.CTkButton(button_frame_login, text="Cadastrar", command=mostrar_cadastro, width=150, height=40,
font=("Roboto", 14), corner_radius=10, hover_color="#3b82f6")
btn_cadastrar.pack(side="left", padx=10)

btn_voltar_login = ctk.CTkButton(button_frame_login, text="Voltar", command=mostrar_principal, width=150, height=40,
font=("Roboto", 14), corner_radius=10, hover_color="#3b82f6")
btn_voltar_login.pack(side="left", padx=10)


# Tela de cadastro
frame_cadastro = ctk.CTkFrame(janela, fg_color="#2a2a3a", corner_radius=15)

ctk.CTkLabel(frame_cadastro, text="Cadastro", font=("Roboto", 24, "bold")).pack(pady=20)

cadastro_frame = ctk.CTkFrame(frame_cadastro, fg_color="transparent")
cadastro_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(cadastro_frame, text="Novo usuário", font=("Roboto", 14)).pack(pady=5)
entry_new_user = ctk.CTkEntry(cadastro_frame, placeholder_text="Digite seu username", width=300, font=("Roboto", 14))
entry_new_user.pack(pady=5)

ctk.CTkLabel(cadastro_frame, text="Senha", font=("Roboto", 14)).pack(pady=5)
entry_new_pass = ctk.CTkEntry(cadastro_frame, placeholder_text="Digite sua senha", show="*", width=300, font=("Roboto", 14))
entry_new_pass.pack(pady=5)

button_frame_cadastro = ctk.CTkFrame(frame_cadastro, fg_color="transparent")
button_frame_cadastro.pack(pady=20)

btn_cadastrar_usuario = ctk.CTkButton(button_frame_cadastro, text="Cadastrar", command=cadastrar, width=150, height=40,
font=("Roboto", 14), corner_radius=10, hover_color="#3b82f6")
btn_cadastrar_usuario.pack(side="left", padx=10)

btn_voltar_cadastro = ctk.CTkButton(button_frame_cadastro, text="Voltar", command=mostrar_login, width=150, height=40,
 font=("Roboto", 14), corner_radius=10, hover_color="#3b82f6")
btn_voltar_cadastro.pack(side="left", padx=10)


# Tela de jogos
frame_jogos = ctk.CTkFrame(janela)
ctk.CTkLabel(frame_jogos, text="Jogos Disponíveis", font=("Roboto", 22)).pack(pady=10)

frame_lista = ctk.CTkScrollableFrame(frame_jogos, width=550, height=400)
frame_lista.pack(pady=10)

btn_voltar_jogos = ctk.CTkButton(frame_jogos, text="Voltar", command=mostrar_principal)
btn_voltar_jogos.pack(pady=10)


# Tela admin
frame_admin = ctk.CTkFrame(janela)
ctk.CTkLabel(frame_admin, text="Área Admin", font=("Roboto", 22)).pack(pady=10)

btn_cadastrar_jogo = ctk.CTkButton(frame_admin, text="Cadastrar Jogo",
                                  command=lambda: [limpar_tela(), frame_add_jogo.pack(pady=20)])
btn_cadastrar_jogo.pack(pady=5)

btn_relatorios = ctk.CTkButton(frame_admin, text="Relatório de Vendas", command=ver_relatorios)
btn_relatorios.pack(pady=5)

btn_ver_jogos_admin = ctk.CTkButton(frame_admin, text="Ver Jogos", command=mostrar_jogos)
btn_ver_jogos_admin.pack(pady=5)

btn_logout = ctk.CTkButton(frame_admin, text="Logout",
                          command=lambda: [usuario_logado.__setitem__(0, None), mostrar_principal()])
btn_logout.pack(pady=5)


# Tela de adicionar jogo
frame_add_jogo = ctk.CTkFrame(janela)
ctk.CTkLabel(frame_add_jogo, text="Cadastrar Novo Jogo", font=("Roboto", 20)).pack(pady=10)

entry_jnome = ctk.CTkEntry(frame_add_jogo, placeholder_text="Nome do Jogo")
entry_jnome.pack(pady=5)

entry_jpreco = ctk.CTkEntry(frame_add_jogo, placeholder_text="Preço")
entry_jpreco.pack(pady=5)

entry_jestoque = ctk.CTkEntry(frame_add_jogo, placeholder_text="Estoque")
entry_jestoque.pack(pady=5)

btn_salvar_jogo = ctk.CTkButton(frame_add_jogo, text="Salvar", command=cadastrar_jogo)
btn_salvar_jogo.pack(pady=5)

btn_voltar_add_jogo = ctk.CTkButton(frame_add_jogo, text="Voltar", command=mostrar_admin_menu)
btn_voltar_add_jogo.pack(pady=5)


mostrar_principal()
janela.mainloop()
