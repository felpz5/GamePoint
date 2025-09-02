import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Dados em memória
usuarios = {"admin": {"senha": "1234", "cargo": "admin"}}
usuario_logado = [None]
jogos = []
vendas = []

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
    usuario, senha = usuario_entry.get(), senha_entry.get()
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        usuario_logado[0] = usuario
        cargo = usuarios[usuario].get("cargo", "cliente")
        messagebox.showinfo("Login", f"Bem-vindo, {usuario}!")
        mostrar_admin_menu() if cargo == "admin" else mostrar_principal()
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

def cadastrar():
    usuario, senha = entry_new_user.get(), entry_new_pass.get()
    if usuario and senha and usuario not in usuarios:
        usuarios[usuario] = {"senha": senha, "cargo": "cliente"}
        messagebox.showinfo("Sucesso", "Usuário cadastrado!")
        mostrar_login()
    else:
        messagebox.showerror("Erro", "Dados inválidos ou usuário já existe.")

def atualizar_jogos():
    for w in frame_lista.winfo_children(): w.destroy()
    for idx, jogo in enumerate(jogos):
        card = ctk.CTkFrame(frame_lista, fg_color="#2a2a44", corner_radius=8)
        card.pack(pady=5, padx=10, fill="x")
        info = f"{jogo['nome']} ({jogo['genero']}) — R${jogo['preco']:.2f} | Estoque: {jogo['estoque']}"
        ctk.CTkLabel(card, text=info, font=("Roboto", 14)).pack(side="left", padx=10)
        ctk.CTkButton(card, text="Comprar", width=80, command=lambda j=jogo: comprar(j)).pack(side="right", padx=5)

def comprar(jogo):
    if not usuario_logado[0]:
        messagebox.showwarning("Acesso negado", "Faça login para comprar.")
        return
    if jogo["estoque"] <= 0:
        messagebox.showinfo("Indisponível", "Jogo sem estoque.")
        return
    jogo["estoque"] -= 1
    vendas.append({
        "cliente": usuario_logado[0],
        "jogo": jogo["nome"],
        "quantidade": 1,
        "valor": jogo["preco"],
        "data": datetime.now().strftime("%d/%m/%Y %H:%M")
    })
    messagebox.showinfo("Compra", f"Você comprou {jogo['nome']} por R${jogo['preco']:.2f}")
    atualizar_jogos()

def mostrar_cadastro_jogo():
    limpar_tela()
    frame_add_jogo.pack(pady=20)

def salvar_jogo():
    try:
        nome = entry_jnome.get()
        genero = entry_genero.get()
        preco = float(entry_jpreco.get())
        estoque = int(entry_jestoque.get())
        jogos.append({"nome": nome, "genero": genero, "preco": preco, "estoque": estoque})
        messagebox.showinfo("Sucesso", f"{nome} cadastrado com sucesso.")
        mostrar_admin_menu()
    except ValueError:
        messagebox.showerror("Erro", "Preço ou estoque inválido.")

def mostrar_editar_excluir():
    limpar_tela()
    frame_editar_excluir.pack(pady=20)
    atualizar_lista_edicao()

def atualizar_lista_edicao():
    for widget in frame_lista_edicao.winfo_children():
        widget.destroy()
    for i, jogo in enumerate(jogos):
        ctk.CTkButton(frame_lista_edicao, text=f"{jogo['nome']} (ID: {i})", command=lambda idx=i: editar_jogo(idx)).pack(pady=4)

def editar_jogo(idx):
    limpar_tela()
    jogo = jogos[idx]
    entry_jnome_edit.delete(0, "end")
    entry_jpreco_edit.delete(0, "end")
    entry_jestoque_edit.delete(0, "end")
    entry_genero_edit.delete(0, "end")
    entry_jnome_edit.insert(0, jogo["nome"])
    entry_genero_edit.insert(0, jogo["genero"])
    entry_jpreco_edit.insert(0, jogo["preco"])
    entry_jestoque_edit.insert(0, jogo["estoque"])

    def salvar():
        try:
            jogo["nome"] = entry_jnome_edit.get()
            jogo["genero"] = entry_genero_edit.get()
            jogo["preco"] = float(entry_jpreco_edit.get())
            jogo["estoque"] = int(entry_jestoque_edit.get())
            messagebox.showinfo("Atualizado", "Jogo atualizado com sucesso.")
            mostrar_editar_excluir()
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos.")

    def excluir():
        jogos.pop(idx)
        messagebox.showinfo("Excluído", "Jogo removido com sucesso.")
        mostrar_editar_excluir()

    frame = ctk.CTkFrame(janela)
    frame.pack(pady=20)
    ctk.CTkLabel(frame, text=f"Editar Jogo (ID: {idx})", font=("Roboto", 16)).pack(pady=10)
    entry_jnome_edit.pack(pady=5)
    entry_genero_edit.pack(pady=5)
    entry_jpreco_edit.pack(pady=5)
    entry_jestoque_edit.pack(pady=5)
    ctk.CTkButton(frame, text="Salvar", command=salvar).pack(pady=5)
    ctk.CTkButton(frame, text="Excluir", command=excluir, fg_color="#b83232", hover_color="#ff4d4d").pack(pady=5)
    ctk.CTkButton(frame, text="Voltar", command=mostrar_editar_excluir).pack(pady=5)

def ver_relatorios():
    texto = "\n".join(f"{v['cliente']} comprou {v['jogo']} ({v['quantidade']}) por R${v['valor']:.2f} em {v['data']}" for v in vendas)
    messagebox.showinfo("Relatório de Vendas", texto or "Nenhuma venda ainda.")

def sair():
    janela.destroy()

# ---------- TELA INICIAL ----------
frame_inicio = ctk.CTkFrame(janela, fg_color="#2a2a3a", corner_radius=15)
ctk.CTkLabel(frame_inicio, text="Bem-vindo à Loja de Jogos", font=("Roboto", 28, "bold")).pack(pady=30)
button_frame_inicio = ctk.CTkFrame(frame_inicio, fg_color="transparent")
button_frame_inicio.pack(pady=20)
ctk.CTkButton(button_frame_inicio, text="Ver Jogos", width=220, height=45, font=("Roboto", 15),
corner_radius=12, hover_color="#3b82f6", command=mostrar_jogos).pack(pady=10)
ctk.CTkButton(button_frame_inicio, text="Login / Cadastro", width=220, height=45, font=("Roboto", 15),
corner_radius=12, hover_color="#3b82f6", command=mostrar_login).pack(pady=10)
ctk.CTkButton(frame_inicio, text="Sair", width=120, height=35, font=("Roboto", 14), corner_radius=10,
fg_color="#b83232", hover_color="#ff4d4d", command=sair).pack(side="bottom", pady=15)

# ---------- LOGIN ----------
frame_login = ctk.CTkFrame(janela, fg_color="#2a2a3a", corner_radius=15)
ctk.CTkLabel(frame_login, text="Login", font=("Roboto", 24, "bold")).pack(pady=20)
usuario_entry = ctk.CTkEntry(frame_login, placeholder_text="Usuário", width=300, font=("Roboto", 14))
usuario_entry.pack(pady=5)
senha_entry = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*", width=300, font=("Roboto", 14))
senha_entry.pack(pady=5)
ctk.CTkButton(frame_login, text="Entrar", command=entrar).pack(pady=10)
ctk.CTkButton(frame_login, text="Cadastrar", command=mostrar_cadastro).pack(pady=5)
ctk.CTkButton(frame_login, text="Voltar", command=mostrar_principal).pack(pady=5)

# ---------- CADASTRO ----------
frame_cadastro = ctk.CTkFrame(janela, fg_color="#2a2a3a", corner_radius=15)
ctk.CTkLabel(frame_cadastro, text="Cadastro", font=("Roboto", 24, "bold")).pack(pady=20)
entry_new_user = ctk.CTkEntry(frame_cadastro, placeholder_text="Novo Usuário", width=300, font=("Roboto", 14))
entry_new_user.pack(pady=5)
entry_new_pass = ctk.CTkEntry(frame_cadastro, placeholder_text="Senha", show="*", width=300, font=("Roboto", 14))
entry_new_pass.pack(pady=5)
ctk.CTkButton(frame_cadastro, text="Cadastrar", command=cadastrar).pack(pady=10)
ctk.CTkButton(frame_cadastro, text="Voltar", command=mostrar_login).pack(pady=5)

# ---------- JOGOS ----------
frame_jogos = ctk.CTkFrame(janela)
ctk.CTkLabel(frame_jogos, text="Jogos Disponíveis", font=("Roboto", 22)).pack(pady=10)
frame_lista = ctk.CTkScrollableFrame(frame_jogos, width=550, height=400)
frame_lista.pack(pady=10)
ctk.CTkButton(frame_jogos, text="Voltar", command=mostrar_principal).pack(pady=10)

# ---------- ADMIN MENU ----------
frame_admin = ctk.CTkFrame(janela)
ctk.CTkLabel(frame_admin, text="Área Admin", font=("Roboto", 22)).pack(pady=10)
ctk.CTkButton(frame_admin, text="Cadastrar Jogo", command=mostrar_cadastro_jogo).pack(pady=5)
ctk.CTkButton(frame_admin, text="Editar/Excluir Jogo", command=mostrar_editar_excluir).pack(pady=5)
ctk.CTkButton(frame_admin, text="Relatório de Vendas", command=ver_relatorios).pack(pady=5)
ctk.CTkButton(frame_admin, text="Voltar", command=mostrar_principal).pack(pady=10)

# ---------- CADASTRO JOGO ----------
frame_add_jogo = ctk.CTkFrame(janela)
entry_jnome = ctk.CTkEntry(frame_add_jogo, placeholder_text="Nome do Jogo"); entry_jnome.pack(pady=5)
entry_genero = ctk.CTkEntry(frame_add_jogo, placeholder_text="Gênero"); entry_genero.pack(pady=5)
entry_jpreco = ctk.CTkEntry(frame_add_jogo, placeholder_text="Preço"); entry_jpreco.pack(pady=5)
entry_jestoque = ctk.CTkEntry(frame_add_jogo, placeholder_text="Estoque"); entry_jestoque.pack(pady=5)
ctk.CTkButton(frame_add_jogo, text="Salvar", command=salvar_jogo).pack(pady=5)
ctk.CTkButton(frame_add_jogo, text="Voltar", command=mostrar_admin_menu).pack(pady=5)

# ---------- EDIÇÃO/EXCLUSÃO ----------
frame_editar_excluir = ctk.CTkFrame(janela)
ctk.CTkLabel(frame_editar_excluir, text="Editar ou Excluir Jogo", font=("Roboto", 20)).pack(pady=10)
frame_lista_edicao = ctk.CTkScrollableFrame(frame_editar_excluir, width=500, height=300)
frame_lista_edicao.pack(pady=10)
entry_jnome_edit = ctk.CTkEntry(janela, placeholder_text="Nome do Jogo")
entry_genero_edit = ctk.CTkEntry(janela, placeholder_text="Gênero")
entry_jpreco_edit = ctk.CTkEntry(janela, placeholder_text="Preço")
entry_jestoque_edit = ctk.CTkEntry(janela, placeholder_text="Estoque")

# Inicial
mostrar_principal()
janela.mainloop()
