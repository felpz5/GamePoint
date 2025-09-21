# Importar bibliotecas necessárias
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random
import time
import sys
from pathlib import Path
from PIL import Image, ImageTk
import threading  # Para carregamento assíncrono de imagens

# Forçar o diretório de trabalho para a pasta do script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Configurar modo de aparência e tema
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Definir esquema de cores
PRIMARY_PURPLE = "#8B5CF6"  # Roxo suave para acentos
SECONDARY_ORANGE = "#F59E0B"  # Laranja suave para destaques
GOLDEN_YELLOW = "#EAB308"  # Amarelo dourado para texto
RED_BUTTON = "#EF4444"  # Vermelho suave para botões
BLUE_BUTTON = "#3B82F6"  # Azul suave para botões
BACKGROUND_LIGHT = "#F3E8FF"  # Fundo roxo claro (original)
PANEL_BG = "#DDD6FE"  # Roxo mais claro para painéis

# Caminhos para arquivos de dados
DATA_DIR = Path("data")
TABLES_FILE = DATA_DIR / "tables.json"
MENU_FILE = DATA_DIR / "menu.json"
ORDERS_FILE = DATA_DIR / "orders.json"
SALES_FILE = DATA_DIR / "sales.json"
FEEDBACK_FILE = DATA_DIR / "feedback.json"
EMPLOYEES_FILE = DATA_DIR / "employees.json"
GAMES_FILE = DATA_DIR / "games.json"
COSTS_FILE = DATA_DIR / "costs.json"
DEVICES_FILE = DATA_DIR / "devices.json"
IMAGES_DIR = Path("images")

# Garantir que diretórios existam
DATA_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

# Dados padrão para mesas (20 mesas)
CONSOLE_TYPES = ["PS5", "Xbox Series X", "PC Gamer", "Nintendo Switch"]
DEFAULT_TABLES = [
    {"id": i, "status": "livre", "time_left": 0, "code": None, "orders": [], "start_time": None, "games_played": [], "console": CONSOLE_TYPES[(i-1) % len(CONSOLE_TYPES)]}
    for i in range(1, 21)
]

# Dados padrão para menu
DEFAULT_MENU = [
    {"nome": "Pizza Margherita", "preco": 25.00},
    {"nome": "Pizza Pepperoni", "preco": 28.00},
    {"nome": "Pizza Quatro Queijos", "preco": 30.00},
    {"nome": "Pizza Calabresa", "preco": 27.00},
    {"nome": "Pizza Frango com Catupiry", "preco": 29.00},
    {"nome": "Burger Clássico", "preco": 15.00},
    {"nome": "Burger Vegetariano", "preco": 14.00},
    {"nome": "Burger Duplo", "preco": 20.00},
    {"nome": "Burger Bacon", "preco": 18.00},
    {"nome": "Burger Cheddar", "preco": 17.00},
    {"nome": "Refrigerante Lata", "preco": 5.00},
    {"nome": "Suco Natural", "preco": 7.00},
    {"nome": "Água Mineral", "preco": 3.00},
    {"nome": "Água com Gás", "preco": 4.00},
    {"nome": "Chá Gelado", "preco": 5.00},
    {"nome": "Batata Frita", "preco": 10.00},
    {"nome": "Onion Rings", "preco": 12.00},
    {"nome": "Batata Doce Frita", "preco": 11.00},
    {"nome": "Batata Rústica", "preco": 12.00},
    {"nome": "Mandioquinha Frita", "preco": 11.00},
    {"nome": "Salada Caesar", "preco": 18.00},
    {"nome": "Salada Grega", "preco": 16.00},
    {"nome": "Salada Caprese", "preco": 17.00},
    {"nome": "Salada Tropical", "preco": 15.00},
    {"nome": "Pasta Carbonara", "preco": 22.00},
    {"nome": "Pasta Bolognese", "preco": 20.00},
    {"nome": "Pasta Alfredo", "preco": 21.00},
    {"nome": "Pasta Primavera", "preco": 23.00},
    {"nome": "Sanduíche de Frango", "preco": 13.00},
    {"nome": "Hot Dog", "preco": 8.00},
    {"nome": "Sanduíche Vegano", "preco": 12.00},
    {"nome": "Sanduíche de Carne", "preco": 14.00},
    {"nome": "Nachos", "preco": 15.00},
    {"nome": "Quesadilla", "preco": 16.00},
    {"nome": "Taco", "preco": 10.00},
]

# Dados padrão para funcionários
DEFAULT_EMPLOYEES = [
    {"id": 1, "nome": "Funcionário Teste 1", "email": "teste1@example.com", "cargo": "Atendente", "data_admissao": "2023-01-01"},
    {"id": 2, "nome": "Funcionário Teste 2", "email": "teste2@example.com", "cargo": "Gerente", "data_admissao": "2023-02-01"},
    {"id": 3, "nome": "Funcionário Teste 3", "email": "teste3@example.com", "cargo": "Técnico", "data_admissao": "2023-03-01"},
]

# Dados padrão para jogos
DEFAULT_GAMES = [
    {"nome": "Fortnite", "jogadas": 10},
    {"nome": "Minecraft", "jogadas": 15},
    {"nome": "Call of Duty", "jogadas": 8},
    {"nome": "Among Us", "jogadas": 12},
    {"nome": "FIFA", "jogadas": 9},
]

# Dados padrão para custos
DEFAULT_COSTS = [
    {"data": "2023-09-01", "valor": 500.00},
    {"data": "2023-09-08", "valor": 600.00},
]

# Dados padrão para dispositivos
DEFAULT_DEVICES = [
    {"id": 1, "tipo": "PS5", "quantidade": 5, "status": "disponivel"},
    {"id": 2, "tipo": "Xbox Series X", "quantidade": 5, "status": "disponivel"},
    {"id": 3, "tipo": "PC Gamer", "quantidade": 5, "status": "disponivel"},
    {"id": 4, "tipo": "Nintendo Switch", "quantidade": 5, "status": "disponivel"},
]

# Funções auxiliares para JSON
def safe_load_json(caminho_arquivo, dados_padrao=None):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        if caminho_arquivo.name == "tables.json" and len(dados) < 20:
            print("Atualizando mesas para 20.")
            mesas_adicionais = DEFAULT_TABLES[len(dados):]
            dados.extend(mesas_adicionais)
            safe_save_json(caminho_arquivo, dados)
        return dados
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erro no JSON em {caminho_arquivo}: {e}. Recriando com padrões.")
        if dados_padrao is not None:
            safe_save_json(caminho_arquivo, dados_padrao)
        return dados_padrao or []

def safe_save_json(caminho_arquivo, dados):
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar {caminho_arquivo}: {e}")
        messagebox.showerror("Erro", f"Falha ao salvar dados: {e}")

# Inicializar arquivos JSON com dados padrão
safe_save_json(TABLES_FILE, DEFAULT_TABLES)
safe_save_json(MENU_FILE, DEFAULT_MENU)
safe_save_json(ORDERS_FILE, [])
safe_save_json(SALES_FILE, [])
safe_save_json(FEEDBACK_FILE, [])
safe_save_json(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)
safe_save_json(GAMES_FILE, DEFAULT_GAMES)
safe_save_json(COSTS_FILE, DEFAULT_COSTS)
safe_save_json(DEVICES_FILE, DEFAULT_DEVICES)

# Classe principal da aplicação
class GameCafeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("P.U.P. - The Power-Up Palace")
        self.geometry("1000x700")

        # Logo principal
        # Comentário: Coloque a imagem do logo em 'images/content-Photoroom.png'
        try:
            caminho_logo = IMAGES_DIR / "content-Photoroom.png"
            print(f"Tentando carregar logo: {caminho_logo}")
            imagem_logo = Image.open(caminho_logo).resize((200, 200), Image.LANCZOS)
            foto_logo = ctk.CTkImage(light_image=imagem_logo, size=(250, 250))
            self.logo_label = ctk.CTkLabel(self, image=foto_logo, text="")
        except Exception as e:
            print(f"Erro ao carregar logo {caminho_logo}: {e}")
            self.logo_label = ctk.CTkLabel(self, text="Logo não encontrada", font=("Arial", 16), text_color="red")
        self.logo_label.pack(pady=20)

        self.welcome_label = ctk.CTkLabel(self, text="Bem-vindo ao P.U.P.!", font=("Arial", 36, "bold"), text_color=SECONDARY_ORANGE)
        self.welcome_label.pack(pady=30)

        self.client_button = ctk.CTkButton(self, text="Área do Cliente", command=self.abrir_area_cliente, fg_color=PRIMARY_PURPLE, hover_color=BLUE_BUTTON, text_color=GOLDEN_YELLOW, corner_radius=20, font=("Arial", 18), width=400, height=60)
        self.client_button.pack(pady=15, padx=200)

        self.employee_button = ctk.CTkButton(self, text="Área do Funcionário", command=self.abrir_area_funcionario, fg_color=PRIMARY_PURPLE, hover_color=RED_BUTTON, text_color=GOLDEN_YELLOW, corner_radius=20, font=("Arial", 18), width=400, height=60)
        self.employee_button.pack(pady=15, padx=200)

        self.admin_button = ctk.CTkButton(self, text="Área do Admin", command=self.abrir_area_admin, fg_color=PRIMARY_PURPLE, hover_color=SECONDARY_ORANGE, text_color=GOLDEN_YELLOW, corner_radius=20, font=("Arial", 18), width=400, height=60)
        self.admin_button.pack(pady=15, padx=200)

        # Variáveis de frames
        self.client_frame = None
        self.employee_frame = None
        self.admin_frame = None
        self.mesa_atual = None
        self.timer_id = None
        self.mesa_selecionada = None
        self.imagens_pre_carregadas = {}  # Para pré-carregamento de imagens

        # Pré-carregar imagens em thread separada
        threading.Thread(target=self.pre_carregar_imagens, daemon=True).start()

    def pre_carregar_imagens(self):
        """Pré-carregar imagens do menu."""
        menu = safe_load_json(MENU_FILE, DEFAULT_MENU)
        for item in menu:
            caminho_imagem = IMAGES_DIR / f"{item['nome'].replace(' ', '_').replace('ç', 'c').replace('ã', 'a').replace('é', 'e').replace('ô', 'o')}.jpg"
            try:
                imagem_item = Image.open(caminho_imagem).resize((120, 120), Image.LANCZOS)
                foto_item = ctk.CTkImage(light_image=imagem_item, size=(120, 120))
                self.imagens_pre_carregadas[item['nome']] = foto_item
            except Exception as e:
                print(f"Erro ao pré-carregar {caminho_imagem}: {e}")

    def mostrar_frame(self, frame):
        """Esconder menu principal e mostrar frame com transição."""
        self.logo_label.pack_forget()
        self.welcome_label.pack_forget()
        self.client_button.pack_forget()
        self.employee_button.pack_forget()
        self.admin_button.pack_forget()
        self.after(100, lambda: frame.pack(fill="both", expand=True))

    def voltar_ao_menu_principal(self):
        """Retornar ao menu principal com transição."""
        if self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
        if self.client_frame:
            self.client_frame.pack_forget()
        if self.employee_frame:
            self.employee_frame.pack_forget()
        if self.admin_frame:
            self.admin_frame.pack_forget()
        self.after(100, self._empacotar_elementos_principais)

    def _empacotar_elementos_principais(self):
        """Empacotar elementos do menu principal."""
        self.logo_label.pack(pady=20)
        self.welcome_label.pack(pady=30)
        self.client_button.pack(pady=15, padx=200)
        self.employee_button.pack(pady=15, padx=200)
        self.admin_button.pack(pady=15, padx=200)

    # Métodos para Área do Cliente
    def abrir_area_cliente(self):
        if self.client_frame is None:
            self.client_frame = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND_LIGHT, corner_radius=0, width=980, height=680)

            botao_voltar = ctk.CTkButton(self.client_frame, text="Voltar", command=self.voltar_ao_menu_principal, fg_color=RED_BUTTON, text_color="white", corner_radius=10, width=100)
            botao_voltar.pack(anchor="nw", padx=10, pady=10)

            titulo_cliente = ctk.CTkLabel(self.client_frame, text="Área do Cliente", font=("Arial", 24, "bold"), text_color=SECONDARY_ORANGE)
            titulo_cliente.pack(pady=10)

            frame_codigo = ctk.CTkFrame(self.client_frame, fg_color=PANEL_BG, corner_radius=15)
            frame_codigo.pack(pady=10, padx=300, fill="x")
            rotulo_codigo = ctk.CTkLabel(frame_codigo, text="Insira o Código da Mesa:", text_color=GOLDEN_YELLOW, font=("Arial", 16))
            rotulo_codigo.pack(side="left", padx=15, pady=10)
            self.campo_codigo = ctk.CTkEntry(frame_codigo, width=250, height=40, font=("Arial", 16))
            self.campo_codigo.pack(side="left", padx=15, pady=10)
            botao_enviar = ctk.CTkButton(frame_codigo, text="Entrar", command=self.login_cliente, fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=150, height=40, font=("Arial", 16))
            botao_enviar.pack(side="left", padx=15, pady=10)

            self.rotulo_tempo = ctk.CTkLabel(self.client_frame, text="", font=("Arial", 20, "bold"), text_color=RED_BUTTON)
            self.rotulo_tempo.pack(pady=10)

            titulo_menu = ctk.CTkLabel(self.client_frame, text="Cardápio", font=("Arial", 18, "bold"), text_color=GOLDEN_YELLOW)
            titulo_menu.pack(pady=10)

            frame_grade_menu = ctk.CTkFrame(self.client_frame, fg_color=BACKGROUND_LIGHT)
            frame_grade_menu.pack(pady=5, padx=50, fill="x")

            menu = safe_load_json(MENU_FILE, DEFAULT_MENU)
            self.carrinho = []
            for idx, item in enumerate(menu):
                frame_item = ctk.CTkFrame(frame_grade_menu, fg_color=PANEL_BG, corner_radius=20, width=180, height=250)
                frame_item.grid(row=idx//5, column=idx%5, padx=10, pady=10, sticky="nsew")

                if item['nome'] in self.imagens_pre_carregadas:
                    rotulo_imagem = ctk.CTkLabel(frame_item, image=self.imagens_pre_carregadas[item['nome']], text="")
                else:
                    caminho_imagem = IMAGES_DIR / f"{item['nome'].replace(' ', '_').replace('ç', 'c').replace('ã', 'a').replace('é', 'e').replace('ô', 'o')}.jpg"
                    try:
                        imagem_item = Image.open(caminho_imagem).resize((120, 120), Image.LANCZOS)
                        foto_item = ctk.CTkImage(light_image=imagem_item, size=(120, 120))
                        rotulo_imagem = ctk.CTkLabel(frame_item, image=foto_item, text="")
                    except Exception as e:
                        print(f"Erro ao carregar {caminho_imagem}: {e}")
                        rotulo_imagem = ctk.CTkLabel(frame_item, text="Sem imagem", font=("Arial", 12), text_color="gray")
                rotulo_imagem.pack(pady=5)

                rotulo_nome = ctk.CTkLabel(frame_item, text=f"{item['nome']} - R${item['preco']:.2f}", text_color="black", font=("Arial", 14), wraplength=160)
                rotulo_nome.pack(pady=5)

                botao_adicionar = ctk.CTkButton(frame_item, text="Adicionar ao Carrinho", command=lambda i=item: self.adicionar_ao_carrinho(i), fg_color=SECONDARY_ORANGE, text_color="white", width=150, corner_radius=10)
                botao_adicionar.pack(pady=5)

            frame_grade_menu.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            titulo_carrinho = ctk.CTkLabel(self.client_frame, text="Carrinho", font=("Arial", 16, "bold"), text_color=GOLDEN_YELLOW)
            titulo_carrinho.pack(pady=10)
            self.lista_carrinho = tk.Listbox(self.client_frame, bg=PANEL_BG, fg="black", font=("Arial", 12), height=5)
            self.lista_carrinho.pack(fill="x", padx=20, pady=5)

            botao_pedido = ctk.CTkButton(self.client_frame, text="Fazer Pedido do Carrinho", command=self.fazer_pedido, fg_color=BLUE_BUTTON, text_color="white", corner_radius=10)
            botao_pedido.pack(pady=10)

            rotulo_feedback = ctk.CTkLabel(self.client_frame, text="Deixe seu Feedback:", text_color=GOLDEN_YELLOW, font=("Arial", 14))
            rotulo_feedback.pack(pady=10)
            self.campo_feedback = ctk.CTkEntry(self.client_frame, width=400)
            self.campo_feedback.pack(pady=5)
            botao_feedback = ctk.CTkButton(self.client_frame, text="Enviar Feedback", command=self.enviar_feedback, fg_color=SECONDARY_ORANGE, text_color="white", corner_radius=10)
            botao_feedback.pack(pady=10)

        self.mostrar_frame(self.client_frame)

    def adicionar_ao_carrinho(self, item):
        self.carrinho.append(item)
        self.lista_carrinho.insert(tk.END, f"{item['nome']} - R${item['preco']:.2f}")

    def fazer_pedido(self):
        if not self.carrinho:
            messagebox.showwarning("Carrinho", "Carrinho vazio.")
            return
        total = sum(item['preco'] for item in self.carrinho)
        try:
            pedidos = safe_load_json(ORDERS_FILE, [])
            pedidos.append({"mesa": self.mesa_atual['id'] if self.mesa_atual else "desconhecido", "itens": [i['nome'] for i in self.carrinho], "total": total})
            safe_save_json(ORDERS_FILE, pedidos)

            vendas = safe_load_json(SALES_FILE, [])
            vendas.append({"data": time.strftime("%Y-%m-%d"), "valor": total})
            safe_save_json(SALES_FILE, vendas)

            messagebox.showinfo("Pedido", f"Pedido realizado! Total: R${total:.2f}")
            self.carrinho = []
            self.lista_carrinho.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar pedido: {e}")

    def enviar_feedback(self):
        feedback = self.campo_feedback.get().strip()
        if feedback:
            try:
                feedbacks = safe_load_json(FEEDBACK_FILE, [])
                feedbacks.append({"mesa": self.mesa_atual['id'] if self.mesa_atual else "desconhecido", "feedback": feedback})
                safe_save_json(FEEDBACK_FILE, feedbacks)
                messagebox.showinfo("Feedback", "Obrigado pelo feedback!")
                self.campo_feedback.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar feedback: {e}")

    def login_cliente(self):
        codigo = self.campo_codigo.get().strip()
        try:
            mesas = safe_load_json(TABLES_FILE, DEFAULT_TABLES)
            for mesa in mesas:
                if mesa["code"] == codigo and mesa["status"] == "ocupada":
                    self.mesa_atual = mesa
                    mesa["start_time"] = time.time()
                    safe_save_json(TABLES_FILE, mesas)
                    self.atualizar_timer()
                    return
            messagebox.showerror("Erro", "Código inválido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao validar código: {e}")

    def atualizar_timer(self):
        if self.mesa_atual:
            tempo_decorrido = time.time() - self.mesa_atual["start_time"]
            tempo_restante = self.mesa_atual["time_left"] * 60 - tempo_decorrido
            if tempo_restante > 0:
                mins, secs = divmod(tempo_restante, 60)
                self.rotulo_tempo.configure(text=f"Tempo Restante: {int(mins):02d}:{int(secs):02d}")
                self.timer_id = self.after(1000, self.atualizar_timer)
            else:
                self.rotulo_tempo.configure(text="Tempo Esgotado!")
                if self.timer_id:
                    self.after_cancel(self.timer_id)
                    self.timer_id = None

    # Métodos para Área do Funcionário
    def abrir_area_funcionario(self):
        if self.employee_frame is None:
            self.employee_frame = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND_LIGHT, corner_radius=0, width=980, height=680)

            botao_voltar = ctk.CTkButton(self.employee_frame, text="Voltar", command=self.voltar_ao_menu_principal, fg_color=RED_BUTTON, text_color="white", corner_radius=10, width=100)
            botao_voltar.pack(anchor="nw", padx=10, pady=10)

            titulo_funcionario = ctk.CTkLabel(self.employee_frame, text="Área do Funcionário", font=("Arial", 24, "bold"), text_color=SECONDARY_ORANGE)
            titulo_funcionario.pack(pady=10)

            titulo_mesas = ctk.CTkLabel(self.employee_frame, text="Status das Mesas", text_color=GOLDEN_YELLOW, font=("Arial", 18))
            titulo_mesas.pack(pady=10)
            self.scroll_mesas = ctk.CTkScrollableFrame(self.employee_frame, fg_color=PANEL_BG, corner_radius=15, height=300)
            self.scroll_mesas.pack(fill="x", padx=20, pady=5)
            self.botoes_mesa = []
            self.carregar_botoes_mesa()

            botao_atualizar = ctk.CTkButton(self.employee_frame, text="Atualizar Status", command=self.atualizar_mesas, fg_color=BLUE_BUTTON, text_color="white", corner_radius=10)
            botao_atualizar.pack(pady=10)

            self.frame_detalhes = ctk.CTkFrame(self.employee_frame, fg_color=PANEL_BG, corner_radius=15)
            self.frame_detalhes.pack(fill="x", padx=20, pady=10)
            self.rotulo_detalhes = ctk.CTkLabel(self.frame_detalhes, text="Clique em uma mesa para ver detalhes", font=("Arial", 16), text_color="black")
            self.rotulo_detalhes.pack(pady=10)
            self.botao_desocupar = ctk.CTkButton(self.frame_detalhes, text="Desocupar Mesa", command=self.desocupar_mesa, fg_color=RED_BUTTON, text_color="white", corner_radius=10)
            self.botao_desocupar.pack(pady=10)
            self.botao_desocupar.pack_forget()

            titulo_gerar = ctk.CTkLabel(self.employee_frame, text="Gerar Código para Mesa", font=("Arial", 18), text_color=GOLDEN_YELLOW)
            titulo_gerar.pack(pady=10)
            frame_gerar = ctk.CTkFrame(self.employee_frame, fg_color=PANEL_BG, corner_radius=15)
            frame_gerar.pack(pady=5, padx=300, fill="x")
            rotulo_id = ctk.CTkLabel(frame_gerar, text="ID da Mesa:", text_color=GOLDEN_YELLOW, font=("Arial", 16))
            rotulo_id.grid(row=0, column=0, padx=15, pady=10)
            self.campo_id_mesa = ctk.CTkEntry(frame_gerar, width=150, height=40, font=("Arial", 16))
            self.campo_id_mesa.grid(row=0, column=1, padx=15, pady=10)
            rotulo_tempo = ctk.CTkLabel(frame_gerar, text="Tempo (minutos):", text_color=GOLDEN_YELLOW, font=("Arial", 16))
            rotulo_tempo.grid(row=1, column=0, padx=15, pady=10)
            self.campo_tempo = ctk.CTkEntry(frame_gerar, width=150, height=40, font=("Arial", 16))
            self.campo_tempo.grid(row=1, column=1, padx=15, pady=10)
            botao_gerar = ctk.CTkButton(frame_gerar, text="Gerar Código", command=self.gerar_codigo, fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=200, height=40, font=("Arial", 16))
            botao_gerar.grid(row=2, column=0, columnspan=2, pady=10)

            self.atualizar_exibicao_mesas()

        self.mostrar_frame(self.employee_frame)

    def carregar_botoes_mesa(self):
        for widget in self.scroll_mesas.winfo_children():
            widget.destroy()
        self.botoes_mesa = []
        try:
            mesas = safe_load_json(TABLES_FILE, DEFAULT_TABLES)
            for i, mesa in enumerate(mesas):
                cor = "#22C55E" if mesa["status"] == "livre" else "#EF4444" if mesa["status"] == "ocupada" else "#EAB308"
                btn = ctk.CTkButton(self.scroll_mesas, text=f"Mesa {mesa['id']}\nStatus: {mesa['status'].capitalize()}\nTempo: 00:00", fg_color=cor, text_color="white", command=lambda m=mesa: self.mostrar_detalhes_mesa(m), width=150, height=80, corner_radius=15, font=("Arial", 12))
                btn.grid(row=i//5, column=i%5, padx=5, pady=10)
                self.botoes_mesa.append(btn)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar mesas: {e}")

    def atualizar_mesas(self):
        self.carregar_botoes_mesa()

    def mostrar_detalhes_mesa(self, mesa):
        self.mesa_selecionada = mesa
        try:
            todos_pedidos = safe_load_json(ORDERS_FILE, [])
            pedidos = []
            total_gasto = 0
            for pedido in todos_pedidos:
                if pedido.get("mesa") == mesa["id"]:
                    pedidos.extend(pedido["itens"])
                    total_gasto += pedido["total"]
            detalhes = f"Mesa {mesa['id']} Detalhes:\nStatus: {mesa['status'].capitalize()}\nConsole: {mesa['console']}\nTempo Restante: {mesa['time_left']} min\nPedidos: {', '.join(set(pedidos)) or 'Nenhum'}\nValor Total Gasto: R${total_gasto:.2f}"
            self.rotulo_detalhes.configure(text=detalhes)
            self.botao_desocupar.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar detalhes: {e}")

    def desocupar_mesa(self):
        if hasattr(self, 'mesa_selecionada'):
            try:
                mesas = safe_load_json(TABLES_FILE, DEFAULT_TABLES)
                for m in mesas:
                    if m["id"] == self.mesa_selecionada["id"]:
                        m["status"] = "livre"
                        m["time_left"] = 0
                        m["code"] = None
                        m["start_time"] = None
                        m["orders"] = []
                        break
                safe_save_json(TABLES_FILE, mesas)
                messagebox.showinfo("Mesa", "Mesa desocupada!")
                self.atualizar_mesas()
                self.rotulo_detalhes.configure(text="Clique em uma mesa para ver detalhes")
                self.botao_desocupar.pack_forget()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao desocupar mesa: {e}")

    def gerar_codigo(self):
        try:
            id_mesa = int(self.campo_id_mesa.get())
            tempo_min = int(self.campo_tempo.get())
            codigo = str(random.randint(1000, 9999))
            mesas = safe_load_json(TABLES_FILE, DEFAULT_TABLES)
            for mesa in mesas:
                if mesa["id"] == id_mesa and mesa["status"] == "livre":
                    mesa["code"] = codigo
                    mesa["time_left"] = tempo_min
                    mesa["status"] = "ocupada"
                    mesa["start_time"] = time.time()
                    break
            else:
                messagebox.showerror("Erro", "Mesa inválida ou já ocupada.")
                return
            safe_save_json(TABLES_FILE, mesas)
            messagebox.showinfo("Código", f"Código gerado: {codigo}")
            self.atualizar_mesas()
        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar código: {e}")

    def atualizar_exibicao_mesas(self):
        try:
            mesas = safe_load_json(TABLES_FILE, DEFAULT_TABLES)
            if len(self.botoes_mesa) != len(mesas):
                self.carregar_botoes_mesa()
                return
            for btn, mesa in zip(self.botoes_mesa, mesas):
                status = mesa["status"]
                cor = "#22C55E" if status == "livre" else "#EF4444" if status == "ocupada" else "#EAB308"
                btn.configure(fg_color=cor)
                if status == "ocupada" and mesa["start_time"]:
                    tempo_decorrido = time.time() - mesa["start_time"]
                    tempo_restante = mesa["time_left"] * 60 - tempo_decorrido
                    if tempo_restante > 0:
                        mins, secs = divmod(tempo_restante, 60)
                        texto_tempo = f"{int(mins):02d}:{int(secs):02d}"
                    else:
                        texto_tempo = "00:00"
                else:
                    texto_tempo = "00:00"
                btn.configure(text=f"Mesa {mesa['id']}\nStatus: {status.capitalize()}\nTempo: {texto_tempo}")
            self.after(1000, self.atualizar_exibicao_mesas)
        except Exception as e:
            print(f"Erro ao atualizar exibição das mesas: {e}")
            self.after(5000, self.atualizar_exibicao_mesas)

    # Métodos para Área do Admin
    def abrir_area_admin(self):
        if self.admin_frame is None:
            self.admin_frame = ctk.CTkScrollableFrame(self, fg_color=BACKGROUND_LIGHT, corner_radius=0, width=980, height=680)

            botao_voltar = ctk.CTkButton(self.admin_frame, text="Voltar", command=self.voltar_ao_menu_principal, fg_color=RED_BUTTON, text_color="white", corner_radius=10, width=100)
            botao_voltar.pack(anchor="nw", padx=10, pady=10)

            titulo_admin = ctk.CTkLabel(self.admin_frame, text="Área do Admin", font=("Arial", 24, "bold"), text_color=SECONDARY_ORANGE)
            titulo_admin.pack(pady=10)

            frame_secoes = ctk.CTkFrame(self.admin_frame, fg_color=PANEL_BG, corner_radius=15)
            frame_secoes.pack(fill="x", padx=20, pady=10)

            botao_vendas = ctk.CTkButton(frame_secoes, text="Vendas Semanais", command=lambda: self.mostrar_subvista_admin("vendas"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_vendas.grid(row=0, column=0, padx=20, pady=10)

            botao_jogos = ctk.CTkButton(frame_secoes, text="Jogos Mais Jogados", command=lambda: self.mostrar_subvista_admin("jogos"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_jogos.grid(row=0, column=1, padx=20, pady=10)

            botao_comidas = ctk.CTkButton(frame_secoes, text="Comidas Mais Compradas", command=lambda: self.mostrar_subvista_admin("comidas"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_comidas.grid(row=1, column=0, padx=20, pady=10)

            botao_ganhos = ctk.CTkButton(frame_secoes, text="Ganhos e Custos Semanais/Mensais", command=lambda: self.mostrar_subvista_admin("ganhos"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_ganhos.grid(row=1, column=1, padx=20, pady=10)

            botao_funcionarios = ctk.CTkButton(frame_secoes, text="Funcionários", command=lambda: self.mostrar_subvista_admin("funcionarios"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_funcionarios.grid(row=2, column=0, padx=20, pady=10)

            botao_feedback = ctk.CTkButton(frame_secoes, text="Feedbacks", command=lambda: self.mostrar_subvista_admin("feedback"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_feedback.grid(row=2, column=1, padx=20, pady=10)

            botao_adicionar_jogos = ctk.CTkButton(frame_secoes, text="Adicionar Jogos", command=lambda: self.mostrar_subvista_admin("adicionar_jogos"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_adicionar_jogos.grid(row=3, column=0, padx=20, pady=10)

            botao_dispositivos = ctk.CTkButton(frame_secoes, text="Dispositivos", command=lambda: self.mostrar_subvista_admin("dispositivos"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_dispositivos.grid(row=3, column=1, padx=20, pady=10)

            botao_adicionar_mesas = ctk.CTkButton(frame_secoes, text="Adicionar Mesas", command=lambda: self.mostrar_subvista_admin("adicionar_mesas"), fg_color=BLUE_BUTTON, text_color="white", corner_radius=10, width=300)
            botao_adicionar_mesas.grid(row=4, column=0, padx=20, pady=10)

            self.frame_conteudo_admin = ctk.CTkFrame(self.admin_frame, fg_color=BACKGROUND_LIGHT)
            self.frame_conteudo_admin.pack(fill="both", expand=True, pady=10)

        self.mostrar_frame(self.admin_frame)

    def mostrar_subvista_admin(self, secao):
        for widget in self.frame_conteudo_admin.winfo_children():
            widget.destroy()

        try:
            if secao == "vendas":
                titulo_vendas = ctk.CTkLabel(self.frame_conteudo_admin, text="Vendas Semanais", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_vendas.pack(pady=5)
                self.arvore_vendas = ttk.Treeview(self.frame_conteudo_admin, columns=("Data", "Valor"), show="headings", height=10)
                self.arvore_vendas.heading("Data", text="Data")
                self.arvore_vendas.heading("Valor", text="Valor")
                self.arvore_vendas.column("Data", anchor="center", width=200)
                self.arvore_vendas.column("Valor", anchor="center", width=200)
                self.arvore_vendas.pack(fill="x", padx=20, pady=5)
                self.carregar_relatorio_vendas()

            elif secao == "jogos":
                titulo_jogos = ctk.CTkLabel(self.frame_conteudo_admin, text="Jogos Mais Jogados", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_jogos.pack(pady=5)
                self.arvore_jogos = ttk.Treeview(self.frame_conteudo_admin, columns=("Jogo", "Jogadas"), show="headings", height=10)
                self.arvore_jogos.heading("Jogo", text="Jogo")
                self.arvore_jogos.heading("Jogadas", text="Jogadas")
                self.arvore_jogos.column("Jogo", anchor="center", width=200)
                self.arvore_jogos.column("Jogadas", anchor="center", width=200)
                self.arvore_jogos.pack(fill="x", padx=20, pady=5)
                self.carregar_relatorio_jogos()

            elif secao == "adicionar_jogos":
                titulo_adicionar_jogos = ctk.CTkLabel(self.frame_conteudo_admin, text="Adicionar Jogos", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_adicionar_jogos.pack(pady=5)

                frame_adicionar = ctk.CTkFrame(self.frame_conteudo_admin, fg_color=PANEL_BG, corner_radius=15)
                frame_adicionar.pack(pady=10, padx=20, fill="x")
                rotulo_nome = ctk.CTkLabel(frame_adicionar, text="Nome do Jogo:", text_color=GOLDEN_YELLOW, font=("Arial", 14))
                rotulo_nome.pack(side="left", padx=10)
                self.campo_nome_jogo = ctk.CTkEntry(frame_adicionar, width=300)
                self.campo_nome_jogo.pack(side="left", padx=10)
                rotulo_jogadas = ctk.CTkLabel(frame_adicionar, text="Jogadas:", text_color=GOLDEN_YELLOW, font=("Arial", 14))
                rotulo_jogadas.pack(side="left", padx=10)
                self.campo_jogadas = ctk.CTkEntry(frame_adicionar, width=100)
                self.campo_jogadas.pack(side="left", padx=10)
                botao_adicionar = ctk.CTkButton(frame_adicionar, text="Adicionar", command=self.adicionar_jogo, fg_color=BLUE_BUTTON, text_color="white", corner_radius=10)
                botao_adicionar.pack(side="left", padx=10)

            elif secao == "dispositivos":
                titulo_dispositivos = ctk.CTkLabel(self.frame_conteudo_admin, text="Dispositivos Disponíveis", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_dispositivos.pack(pady=5)
                self.arvore_dispositivos = ttk.Treeview(self.frame_conteudo_admin, columns=("ID", "Tipo", "Quantidade", "Status"), show="headings", height=10)
                self.arvore_dispositivos.heading("ID", text="ID")
                self.arvore_dispositivos.heading("Tipo", text="Tipo")
                self.arvore_dispositivos.heading("Quantidade", text="Quantidade")
                self.arvore_dispositivos.heading("Status", text="Status")
                self.arvore_dispositivos.column("ID", anchor="center", width=50)
                self.arvore_dispositivos.column("Tipo", anchor="center", width=150)
                self.arvore_dispositivos.column("Quantidade", anchor="center", width=100)
                self.arvore_dispositivos.column("Status", anchor="center", width=100)
                self.arvore_dispositivos.pack(fill="x", padx=20, pady=5)
                self.carregar_arvore_dispositivos()

            elif secao == "adicionar_mesas":
                titulo_adicionar_mesas = ctk.CTkLabel(self.frame_conteudo_admin, text="Adicionar Mesas", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_adicionar_mesas.pack(pady=5)

                frame_adicionar = ctk.CTkFrame(self.frame_conteudo_admin, fg_color=PANEL_BG, corner_radius=15)
                frame_adicionar.pack(pady=10, padx=20, fill="x")
                rotulo_console = ctk.CTkLabel(frame_adicionar, text="Console:", text_color=GOLDEN_YELLOW, font=("Arial", 14))
                rotulo_console.pack(side="left", padx=10)
                self.campo_console_mesa = ctk.CTkEntry(frame_adicionar, width=300)
                self.campo_console_mesa.pack(side="left", padx=10)
                botao_adicionar = ctk.CTkButton(frame_adicionar, text="Adicionar", command=self.adicionar_mesa, fg_color=BLUE_BUTTON, text_color="white", corner_radius=10)
                botao_adicionar.pack(side="left", padx=10)

            elif secao == "comidas":
                titulo_comidas = ctk.CTkLabel(self.frame_conteudo_admin, text="Comidas Mais Compradas", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_comidas.pack(pady=5)
                self.arvore_comidas = ttk.Treeview(self.frame_conteudo_admin, columns=("Item", "Quantidade"), show="headings", height=10)
                self.arvore_comidas.heading("Item", text="Item")
                self.arvore_comidas.heading("Quantidade", text="Quantidade")
                self.arvore_comidas.column("Item", anchor="center", width=200)
                self.arvore_comidas.column("Quantidade", anchor="center", width=200)
                self.arvore_comidas.pack(fill="x", padx=20, pady=5)
                self.carregar_relatorio_comidas()

            elif secao == "ganhos":
                titulo_ganhos = ctk.CTkLabel(self.frame_conteudo_admin, text="Ganhos e Custos", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_ganhos.pack(pady=5)
                self.rotulo_ganhos = ctk.CTkLabel(self.frame_conteudo_admin, text="", font=("Arial", 14), text_color="black")
                self.rotulo_ganhos.pack(pady=5)
                self.calcular_ganhos()

            elif secao == "funcionarios":
                titulo_funcionarios = ctk.CTkLabel(self.frame_conteudo_admin, text="Funcionários", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_funcionarios.pack(pady=5)

                self.arvore_funcionarios = ttk.Treeview(self.frame_conteudo_admin, columns=("ID", "Nome", "Email", "Cargo", "Data Admissão"), show="headings", height=10)
                self.arvore_funcionarios.heading("ID", text="ID")
                self.arvore_funcionarios.heading("Nome", text="Nome")
                self.arvore_funcionarios.heading("Email", text="Email")
                self.arvore_funcionarios.heading("Cargo", text="Cargo")
                self.arvore_funcionarios.heading("Data Admissão", text="Data Admissão")
                self.arvore_funcionarios.column("ID", anchor="center", width=50)
                self.arvore_funcionarios.column("Nome", anchor="center", width=150)
                self.arvore_funcionarios.column("Email", anchor="center", width=200)
                self.arvore_funcionarios.column("Cargo", anchor="center", width=100)
                self.arvore_funcionarios.column("Data Admissão", anchor="center", width=150)
                self.arvore_funcionarios.pack(fill="x", padx=20, pady=5)
                self.carregar_arvore_funcionarios()

                frame_adicionar = ctk.CTkFrame(self.frame_conteudo_admin, fg_color=PANEL_BG, corner_radius=15)
                frame_adicionar.pack(pady=10, padx=20, fill="x")
                rotulo_nome = ctk.CTkLabel(frame_adicionar, text="Nome:", text_color=GOLDEN_YELLOW, font=("Arial", 14))
                rotulo_nome.grid(row=0, column=0, padx=10, pady=5)
                self.campo_nome_func = ctk.CTkEntry(frame_adicionar, width=200)
                self.campo_nome_func.grid(row=0, column=1, padx=10, pady=5)
                rotulo_email = ctk.CTkLabel(frame_adicionar, text="Email:", text_color=GOLDEN_YELLOW, font=("Arial", 14))
                rotulo_email.grid(row=1, column=0, padx=10, pady=5)
                self.campo_email_func = ctk.CTkEntry(frame_adicionar, width=200)
                self.campo_email_func.grid(row=1, column=1, padx=10, pady=5)
                rotulo_cargo = ctk.CTkLabel(frame_adicionar, text="Cargo:", text_color=GOLDEN_YELLOW, font=("Arial", 14))
                rotulo_cargo.grid(row=2, column=0, padx=10, pady=5)
                self.campo_cargo_func = ctk.CTkEntry(frame_adicionar, width=200)
                self.campo_cargo_func.grid(row=2, column=1, padx=10, pady=5)
                rotulo_data = ctk.CTkLabel(frame_adicionar, text="Data Admissão (YYYY-MM-DD):", text_color=GOLDEN_YELLOW, font=("Arial", 14))
                rotulo_data.grid(row=3, column=0, padx=10, pady=5)
                self.campo_data_func = ctk.CTkEntry(frame_adicionar, width=200)
                self.campo_data_func.grid(row=3, column=1, padx=10, pady=5)
                botao_adicionar = ctk.CTkButton(frame_adicionar, text="Adicionar", command=self.adicionar_funcionario, fg_color=BLUE_BUTTON, text_color="white", corner_radius=10)
                botao_adicionar.grid(row=4, column=0, columnspan=2, pady=10)

                botao_excluir = ctk.CTkButton(self.frame_conteudo_admin, text="Excluir Selecionado", command=self.excluir_funcionario, fg_color=RED_BUTTON, text_color="white", corner_radius=10)
                botao_excluir.pack(pady=10)

            elif secao == "feedback":
                titulo_feedback = ctk.CTkLabel(self.frame_conteudo_admin, text="Feedbacks dos Clientes", font=("Arial", 18), text_color=GOLDEN_YELLOW)
                titulo_feedback.pack(pady=5)

                self.arvore_feedback = ttk.Treeview(self.frame_conteudo_admin, columns=("Mesa", "Feedback"), show="headings", height=10)
                self.arvore_feedback.heading("Mesa", text="Mesa")
                self.arvore_feedback.heading("Feedback", text="Feedback")
                self.arvore_feedback.column("Mesa", anchor="center", width=100)
                self.arvore_feedback.column("Feedback", anchor="w", width=400)
                self.arvore_feedback.pack(fill="x", padx=20, pady=5)
                self.carregar_arvore_feedbacks()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar seção: {e}")

    def carregar_arvore_dispositivos(self):
        self.arvore_dispositivos.delete(*self.arvore_dispositivos.get_children())
        dispositivos = safe_load_json(DEVICES_FILE, DEFAULT_DEVICES)
        for dispositivo in dispositivos:
            self.arvore_dispositivos.insert("", "end", values=(dispositivo['id'], dispositivo['tipo'], dispositivo['quantidade'], dispositivo['status']))

    def adicionar_jogo(self):
        nome = self.campo_nome_jogo.get().strip()
        jogadas = self.campo_jogadas.get().strip()
        if nome and jogadas.isdigit():
            try:
                jogos = safe_load_json(GAMES_FILE, DEFAULT_GAMES)
                jogos.append({"nome": nome, "jogadas": int(jogadas)})
                safe_save_json(GAMES_FILE, jogos)
                messagebox.showinfo("Jogo", "Jogo adicionado!")
                self.campo_nome_jogo.delete(0, tk.END)
                self.campo_jogadas.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao adicionar jogo: {e}")
        else:
            messagebox.showwarning("Entrada", "Insira valores válidos.")

    def adicionar_mesa(self):
        console = self.campo_console_mesa.get().strip()
        if console:
            try:
                mesas = safe_load_json(TABLES_FILE, DEFAULT_TABLES)
                proximo_id = max((m['id'] for m in mesas), default=0) + 1
                mesas.append({"id": proximo_id, "status": "livre", "time_left": 0, "code": None, "orders": [], "start_time": None, "games_played": [], "console": console})
                safe_save_json(TABLES_FILE, mesas)
                messagebox.showinfo("Mesa", "Mesa adicionada!")
                self.campo_console_mesa.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao adicionar mesa: {e}")
        else:
            messagebox.showwarning("Entrada", "Insira um console válido.")

    def carregar_arvore_funcionarios(self):
        self.arvore_funcionarios.delete(*self.arvore_funcionarios.get_children())
        funcionarios = safe_load_json(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)
        for func in funcionarios:
            self.arvore_funcionarios.insert("", "end", values=(func['id'], func['nome'], func['email'], func['cargo'], func['data_admissao']))

    def adicionar_funcionario(self):
        nome = self.campo_nome_func.get().strip()
        email = self.campo_email_func.get().strip()
        cargo = self.campo_cargo_func.get().strip()
        data = self.campo_data_func.get().strip()
        if nome and email and cargo and data:
            try:
                funcionarios = safe_load_json(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)
                proximo_id = max((func['id'] for func in funcionarios), default=0) + 1
                funcionarios.append({"id": proximo_id, "nome": nome, "email": email, "cargo": cargo, "data_admissao": data})
                safe_save_json(EMPLOYEES_FILE, funcionarios)
                self.carregar_arvore_funcionarios()
                self.campo_nome_func.delete(0, tk.END)
                self.campo_email_func.delete(0, tk.END)
                self.campo_cargo_func.delete(0, tk.END)
                self.campo_data_func.delete(0, tk.END)
                messagebox.showinfo("Funcionário", "Funcionário adicionado!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao adicionar funcionário: {e}")
        else:
            messagebox.showwarning("Entrada", "Preencha todos os campos.")

    def excluir_funcionario(self):
        selecao = self.arvore_funcionarios.selection()
        if selecao:
            try:
                funcionarios = safe_load_json(EMPLOYEES_FILE, DEFAULT_EMPLOYEES)
                id_selecionado = self.arvore_funcionarios.item(selecao[0])['values'][0]
                funcionarios = [func for func in funcionarios if func['id'] != id_selecionado]
                safe_save_json(EMPLOYEES_FILE, funcionarios)
                self.carregar_arvore_funcionarios()
                messagebox.showinfo("Funcionário", "Funcionário excluído!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir funcionário: {e}")
        else:
            messagebox.showwarning("Seleção", "Selecione um funcionário para excluir.")

    def carregar_arvore_feedbacks(self):
        self.arvore_feedback.delete(*self.arvore_feedback.get_children())
        feedbacks = safe_load_json(FEEDBACK_FILE, [])
        for fb in feedbacks:
            self.arvore_feedback.insert("", "end", values=(fb['mesa'], fb['feedback']))

    def carregar_relatorio_vendas(self):
        try:
            self.arvore_vendas.delete(*self.arvore_vendas.get_children())
            vendas = safe_load_json(SALES_FILE, [])
            for venda in vendas[-7:]:
                self.arvore_vendas.insert("", "end", values=(venda["data"], f"R${venda['valor']:.2f}"))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar vendas: {e}")

    def carregar_relatorio_comidas(self):
        try:
            self.arvore_comidas.delete(*self.arvore_comidas.get_children())
            contagem_comidas = {}
            pedidos = safe_load_json(ORDERS_FILE, [])
            for pedido in pedidos:
                for item in pedido["itens"]:
                    contagem_comidas[item] = contagem_comidas.get(item, 0) + 1
            comidas_ordenadas = sorted(contagem_comidas.items(), key=lambda x: x[1], reverse=True)[:10]
            for item, contagem in comidas_ordenadas:
                self.arvore_comidas.insert("", "end", values=(item, contagem))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar relatório de comidas: {e}")

    def carregar_relatorio_jogos(self):
        try:
            self.arvore_jogos.delete(*self.arvore_jogos.get_children())
            jogos = safe_load_json(GAMES_FILE, DEFAULT_GAMES)
            jogos_ordenados = sorted(jogos, key=lambda x: x["jogadas"], reverse=True)
            for jogo in jogos_ordenados:
                self.arvore_jogos.insert("", "end", values=(jogo["nome"], jogo["jogadas"]))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar relatório de jogos: {e}")

    def calcular_ganhos(self):
        try:
            vendas = safe_load_json(SALES_FILE, [])
            vendas_semanais = sum(v["valor"] for v in vendas if "data" in v and time.time() - time.mktime(time.strptime(v["data"], "%Y-%m-%d")) < 7*86400)
            vendas_mensais = sum(v["valor"] for v in vendas if "data" in v and time.time() - time.mktime(time.strptime(v["data"], "%Y-%m-%d")) < 30*86400)

            custos = safe_load_json(COSTS_FILE, DEFAULT_COSTS)
            custos_semanais = sum(c["valor"] for c in custos if "data" in c and time.time() - time.mktime(time.strptime(c["data"], "%Y-%m-%d")) < 7*86400)
            custos_mensais = sum(c["valor"] for c in custos if "data" in c and time.time() - time.mktime(time.strptime(c["data"], "%Y-%m-%d")) < 30*86400)

            texto = f"Ganhos Semanais: R${vendas_semanais:.2f} | Custos Semanais: R${custos_semanais:.2f}\nGanhos Mensais: R${vendas_mensais:.2f} | Custos Mensais: R${custos_mensais:.2f}"
            self.rotulo_ganhos.configure(text=texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao calcular ganhos: {e}")

# Executar a aplicação
if __name__ == "__main__":
    try:
        app = GameCafeApp()
        app.mainloop()
    except Exception as e:
        print(f"Erro na aplicação: {e}")
        sys.exit(1)