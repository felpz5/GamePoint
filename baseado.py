import customtkinter as ctk
from tkinter import messagebox, ttk, Canvas
from datetime import datetime, timedelta
import uuid
from PIL import Image, ImageTk
import json
import os

# Data storage with improved structure
class DataManager:
    def __init__(self):
        self.usuarios = {
            "admin": {"senha": "123", "cargo": "admin", "email": "admin@gamecafe.com", "telefone": "123456789"},
            "cliente": {"senha": "1234", "cargo": "cliente", "email": "cliente@gamecafe.com", "telefone": "987654321"}
        }
        self.mesas = [
            {"id": 1, "console": "PS5", "status": "livre", "tempo_inicio": None, "tempo_total": 0},
            {"id": 2, "console": "Xbox", "status": "livre", "tempo_inicio": None, "tempo_total": 0},
            {"id": 3, "console": "Nintendo Switch", "status": "livre", "tempo_inicio": None, "tempo_total": 0}
        ]
        self.consoles = [
            {"id": 1, "tipo": "PS5", "jogos": ["FIFA 23", "God of War"], "manutencao": []},
            {"id": 2, "tipo": "Xbox", "jogos": ["Mortal Kombat", "Forza Horizon"], "manutencao": []},
            {"id": 3, "tipo": "Nintendo Switch", "jogos": ["Nintendo Switch Sports"], "manutencao": []}
        ]
        self.cardapio = [
            {"id": 1, "nome": "Hambúrguer", "preco": 25.00, "tipo": "comida"},
            {"id": 2, "nome": "Refrigerante", "preco": 8.00, "tipo": "bebida"}
        ]
        self.pedidos = []
        self.reservas = []
        self.pagamentos = []
        self.feedbacks = []
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists("game_cafe_data.json"):
                with open("game_cafe_data.json", "r") as f:
                    data = json.load(f)
                    self.usuarios.update(data.get("usuarios", {}))
                    self.mesas = data.get("mesas", self.mesas)
                    self.consoles = data.get("consoles", self.consoles)
                    self.cardapio = data.get("cardapio", self.cardapio)
                    self.pedidos = data.get("pedidos", [])
                    self.reservas = data.get("reservas", [])
                    self.pagamentos = data.get("pagamentos", [])
                    self.feedbacks = data.get("feedbacks", [])
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def save_data(self):
        try:
            with open("game_cafe_data.json", "w") as f:
                json.dump({
                    "usuarios": self.usuarios,
                    "mesas": self.mesas,
                    "consoles": self.consoles,
                    "cardapio": self.cardapio,
                    "pedidos": self.pedidos,
                    "reservas": self.reservas,
                    "pagamentos": self.pagamentos,
                    "feedbacks": self.feedbacks
                }, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")

class GameCafeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("P.U.P. Game Café")
        self.geometry("1280x720")
        self.resizable(True, True)
        self.data = DataManager()
        self.usuario_atual = None
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Create canvas for background
        self.canvas = Canvas(self, highlightthickness=0, bg="#1a1a1a")
        self.canvas.pack(fill="both", expand=True)

        # Load and set background image
        try:
            self.bg_image = Image.open("content2.png")
        except FileNotFoundError:
            print("Warning: content2.png not found. Using default background.")
            self.bg_image = Image.new("RGB", (1280, 720), "#1a1a1a")
        
        self.bg_image_id = None
        self.update_background()
        self.bind("<Configure>", self.update_background)

        self.criar_tela_principal()

    def update_background(self, event=None):
        window_width = max(self.winfo_width(), 1)
        window_height = max(self.winfo_height(), 1)
        img_width, img_height = self.bg_image.size
        scale = max(window_width / img_width, window_height / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized_image = self.bg_image.resize((new_width, new_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        
        if self.bg_image_id is None:
            self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.itemconfig(self.bg_image_id, image=self.bg_photo)
        self.canvas.lower(self.bg_image_id)

    def limpar_tela(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()
        if self.bg_image_id is not None:
            self.canvas.lower(self.bg_image_id)

    def criar_tela_principal(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="transparent", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        # Placeholder for logo
        # logo_label = ctk.CTkLabel(frame, text="", image=your_logo_image)
        # logo_label.pack(pady=20)
        
        ctk.CTkLabel(frame, text="P.U.P. Game Café", font=("Roboto", 48, "bold"), text_color="#FFD700").pack(pady=30)
        btn_ver_mesas = ctk.CTkButton(
            frame, text="Ver Mesas", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#4CAF50", hover_color="#45A049",
            command=self.criar_tela_mesas
        )
        btn_ver_mesas.pack(pady=15)
        
        if not self.usuario_atual:
            btn_login = ctk.CTkButton(
                frame, text="Login / Cadastro", width=300, height=50, font=("Roboto", 18),
                corner_radius=15, fg_color="#2196F3", hover_color="#1976D2",
                command=self.criar_tela_login
            )
            btn_login.pack(pady=15)
        else:
            btn_perfil = ctk.CTkButton(
                frame, text="Área do Usuário", width=300, height=50, font=("Roboto", 18),
                corner_radius=15, fg_color="#FF9800", hover_color="#F57C00",
                command=self.criar_tela_usuario
            )
            btn_perfil.pack(pady=15)
        
        btn_sair = ctk.CTkButton(
            frame, text="Sair", width=200, height=40, font=("Roboto", 16),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.destroy
        )
        btn_sair.pack(pady=20)

    def criar_tela_login(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Login", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        form = ctk.CTkFrame(frame, fg_color="transparent")
        
        self.entry_usuario = ctk.CTkEntry(
            form, placeholder_text="Usuário", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_usuario.pack(pady=12)
        
        self.entry_senha = ctk.CTkEntry(
            form, placeholder_text="Senha", show="*", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_senha.pack(pady=12)
        
        btn_entrar = ctk.CTkButton(
            form, text="Entrar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#4CAF50", hover_color="#45A049",
            command=self.fazer_login
        )
        btn_entrar.pack(pady=15)
        
        btn_cadastrar = ctk.CTkButton(
            form, text="Cadastrar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#2196F3", hover_color="#1976D2",
            command=self.criar_tela_cadastro
        )
        btn_cadastrar.pack(pady=15)
        
        btn_voltar = ctk.CTkButton(
            form, text="Voltar", width=200, height=40, font=("Roboto", 16),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_principal
        )
        btn_voltar.pack(pady=15)
        form.pack(pady=10)

    def criar_tela_cadastro(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Cadastro", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        form = ctk.CTkFrame(frame, fg_color="transparent")
        
        self.entry_novo_usuario = ctk.CTkEntry(
            form, placeholder_text="Novo Usuário", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_novo_usuario.pack(pady=12)
        
        self.entry_nova_senha = ctk.CTkEntry(
            form, placeholder_text="Senha", show="*", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_nova_senha.pack(pady=12)
        
        self.entry_nova_email = ctk.CTkEntry(
            form, placeholder_text="Email", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_nova_email.pack(pady=12)
        
        self.entry_nova_telefone = ctk.CTkEntry(
            form, placeholder_text="Telefone", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_nova_telefone.pack(pady=12)
        
        btn_cadastrar = ctk.CTkButton(
            form, text="Cadastrar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#4CAF50", hover_color="#45A049",
            command=self.cadastrar_usuario
        )
        btn_cadastrar.pack(pady=15)
        
        btn_voltar = ctk.CTkButton(
            form, text="Voltar", width=200, height=40, font=("Roboto", 16),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_login
        )
        btn_voltar.pack(pady=15)
        form.pack(pady=10)

    def criar_tela_usuario(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Área do Usuário", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        menu = ctk.CTkFrame(frame, fg_color="transparent")
        
        buttons = []
        if self.usuario_atual["cargo"] == "admin":
            buttons = [
                ("Gerenciar Mesas", self.criar_tela_gerenciar_mesas, "#4CAF50"),
                ("Gerenciar Consoles", self.criar_tela_gerenciar_consoles, "#2196F3"),
                ("Gerenciar Pedidos", self.criar_tela_gerenciar_pedidos, "#FF9800"),
                ("Gerenciar Reservas", self.criar_tela_gerenciar_reservas, "#9C27B0"),
                ("Gerenciar Pagamentos", self.criar_tela_gerenciar_pagamentos, "#009688"),
                ("Relatórios", self.criar_tela_relatorios, "#FFC107")
            ]
        else:
            buttons = [
                ("Fazer Reserva", self.criar_tela_reservar, "#4CAF50"),
                ("Controle de Tempo", self.criar_tela_tempo_jogo, "#2196F3"),
                ("Cardápio e Pedidos", self.criar_tela_cardapio, "#FF9800"),
                ("Perfil do Jogador", self.criar_tela_perfil, "#9C27B0"),
                ("Pagamentos", self.criar_tela_pagamento_cliente, "#009688")
            ]
        
        for text, command, color in buttons:
            btn = ctk.CTkButton(
                menu, text=text, width=350, height=50, font=("Roboto", 18),
                corner_radius=15, fg_color=color, hover_color=f"#{(int(color[1:3], 16) - 20):02x}{(int(color[3:5], 16) - 20):02x}{(int(color[5:7], 16) - 20):02x}",
                command=command
            )
            btn.pack(pady=12)
        
        btn_deslogar = ctk.CTkButton(
            menu, text="Deslogar", width=350, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.deslogar
        )
        btn_deslogar.pack(pady=12)
        menu.pack(pady=10)

    def criar_tela_gerenciar_mesas(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Gerenciar Mesas", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        lista = ctk.CTkScrollableFrame(frame, width=900, height=450, corner_radius=12, fg_color="transparent")
        
        for mesa in self.data.mesas:
            card = ctk.CTkFrame(lista, fg_color="#3C3C3C", corner_radius=12)
            status_color = "#4CAF50" if mesa["status"] == "livre" else "#F44336" if mesa["status"] == "ocupada" else "#FFC107"
            info = f"Mesa {mesa['id']} | Console: {mesa['console'] or 'Nenhum'} | Status: {mesa['status'].capitalize()}"
            if mesa["tempo_inicio"]:
                tempo = (datetime.now() - mesa["tempo_inicio"]).seconds // 60
                info += f" | Tempo: {tempo} min"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), text_color=status_color).pack(side="left", padx=15, pady=10)
            btn_acao = ctk.CTkButton(
                card, text="Alterar Status", width=150, height=40, font=("Roboto", 14),
                corner_radius=10, fg_color="#2196F3", hover_color="#1976D2",
                command=lambda m=mesa: self.alterar_status_mesa(m)
            )
            btn_acao.pack(side="right", padx=10)
            card.pack(pady=8, padx=15, fill="x")
        
        lista.pack(pady=15, padx=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_gerenciar_consoles(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Gerenciar Consoles", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        lista = ctk.CTkScrollableFrame(frame, width=900, height=450, corner_radius=12, fg_color="transparent")
        
        for console in self.data.consoles:
            card = ctk.CTkFrame(lista, fg_color="#3C3C3C", corner_radius=12)
            info = f"Console {console['id']} | Tipo: {console['tipo']} | Jogos: {', '.join(console['jogos'])}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), text_color="#FFFFFF").pack(side="left", padx=15, pady=10)
            btn_manutencao = ctk.CTkButton(
                card, text="Registrar Manutenção", width=180, height=40, font=("Roboto", 14),
                corner_radius=10, fg_color="#FF9800", hover_color="#F57C00",
                command=lambda c=console: self.registrar_manutencao(c)
            )
            btn_manutencao.pack(side="right", padx=10)
            card.pack(pady=8, padx=15, fill="x")
        
        lista.pack(pady=15, padx=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_gerenciar_pedidos(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Gerenciar Pedidos", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        lista = ctk.CTkScrollableFrame(frame, width=900, height=450, corner_radius=12, fg_color="transparent")
        
        for pedido in self.data.pedidos:
            card = ctk.CTkFrame(lista, fg_color="#3C3C3C", corner_radius=12)
            status_color = "#FFC107" if pedido["status"] == "preparando" else "#4CAF50" if pedido["status"] == "pronto" else "#9C27B0"
            info = f"Pedido {pedido['id']} | Mesa {pedido['mesa']} | Item: {pedido['item']} | Status: {pedido['status'].capitalize()}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), text_color=status_color).pack(side="left", padx=15, pady=10)
            btn_status = ctk.CTkButton(
                card, text="Atualizar Status", width=150, height=40, font=("Roboto", 14),
                corner_radius=10, fg_color="#2196F3", hover_color="#1976D2",
                command=lambda p=pedido: self.atualizar_status_pedido(p)
            )
            btn_status.pack(side="right", padx=10)
            card.pack(pady=8, padx=15, fill="x")
        
        lista.pack(pady=15, padx=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_gerenciar_reservas(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Gerenciar Reservas", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        lista = ctk.CTkScrollableFrame(frame, width=900, height=450, corner_radius=12, fg_color="transparent")
        
        for reserva in self.data.reservas:
            card = ctk.CTkFrame(lista, fg_color="#3C3C3C", corner_radius=12)
            info = f"Reserva {reserva['id']} | Cliente: {reserva['cliente']} | Mesa {reserva['mesa']} | Data: {reserva['data']}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), text_color="#FFFFFF").pack(side="left", padx=15, pady=10)
            btn_cancelar = ctk.CTkButton(
                card, text="Cancelar", width=150, height=40, font=("Roboto", 14),
                corner_radius=10, fg_color="#F44336", hover_color="#D32F2F",
                command=lambda r=reserva: self.cancelar_reserva(r)
            )
            btn_cancelar.pack(side="right", padx=10)
            card.pack(pady=8, padx=15, fill="x")
        
        lista.pack(pady=15, padx=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_gerenciar_pagamentos(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Gerenciar Pagamentos", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        colunas = ("ID", "Cliente", "Valor", "Descrição", "Data")
        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 14), rowheight=30, background="#2B2B2B", foreground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Roboto", 16, "bold"), background="#4CAF50", foreground="#FFFFFF")
        
        tree = ttk.Treeview(frame, columns=colunas, show="headings", height=15)
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)
        
        for pagamento in self.data.pagamentos:
            tree.insert("", "end", values=(
                pagamento['id'], 
                pagamento['cliente'], 
                f"R${pagamento['valor']:.2f}",
                pagamento['descricao'], 
                pagamento['data']
            ))
        
        tree.pack(fill="both", expand=True, padx=15, pady=15)
        total = sum(p['valor'] for p in self.data.pagamentos)
        ctk.CTkLabel(frame, text=f"Total: R${total:.2f}", font=("Roboto", 20, "bold"), text_color="#FFD700").pack(pady=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_relatorios(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Relatórios", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        
        # Jogos mais populares
        jogos_pop = {}
        for reserva in self.data.reservas:
            mesa = next((m for m in self.data.mesas if m['id'] == reserva['mesa']), None)
            if mesa and mesa['console']:
                console = next((c for c in self.data.consoles if c['tipo'] == mesa['console']), None)
                if console:
                    for jogo in console['jogos']:
                        jogos_pop[jogo] = jogos_pop.get(jogo, 0) + 1
        
        ctk.CTkLabel(frame, text="Jogos Mais Populares:", font=("Roboto", 24, "bold"), text_color="#4CAF50").pack(pady=10)
        for jogo, count in sorted(jogos_pop.items(), key=lambda x: x[1], reverse=True)[:5]:
            ctk.CTkLabel(frame, text=f"{jogo}: {count} reservas", font=("Roboto", 18), text_color="#FFFFFF").pack()
        
        # Horários de pico
        horas = {}
        for reserva in self.data.reservas:
            hora = reserva['data'].split()[1][:2]
            horas[hora] = horas.get(hora, 0) + 1
        
        ctk.CTkLabel(frame, text="Horários de Pico:", font=("Roboto", 24, "bold"), text_color="#4CAF50").pack(pady=10)
        for hora, count in sorted(horas.items(), key=lambda x: x[1], reverse=True)[:5]:
            ctk.CTkLabel(frame, text=f"{hora}h: {count} reservas", font=("Roboto", 18), text_color="#FFFFFF").pack()
        
        # Feedbacks recentes
        ctk.CTkLabel(frame, text="Feedbacks Recentes:", font=("Roboto", 24, "bold"), text_color="#4CAF50").pack(pady=10)
        for feedback in self.data.feedbacks[-5:]:
            ctk.CTkLabel(frame, text=f"{feedback['cliente']}: {feedback['texto']}", font=("Roboto", 18), text_color="#FFFFFF").pack()
        
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_mesas(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Mesas Disponíveis", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        lista = ctk.CTkScrollableFrame(frame, width=900, height=450, corner_radius=12, fg_color="transparent")
        
        for mesa in self.data.mesas:
            card = ctk.CTkFrame(lista, fg_color="#3C3C3C", corner_radius=12)
            status_color = "#4CAF50" if mesa["status"] == "livre" else "#F44336" if mesa["status"] == "ocupada" else "#FFC107"
            info = f"Mesa {mesa['id']} | Console: {mesa['console'] or 'Nenhum'} | Status: {mesa['status'].capitalize()}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), text_color=status_color).pack(side="left", padx=15, pady=10)
            if self.usuario_atual and self.usuario_atual["cargo"] == "cliente":
                btn_reservar = ctk.CTkButton(
                    card, text="Reservar", width=150, height=40, font=("Roboto", 14),
                    corner_radius=10, fg_color="#4CAF50", hover_color="#45A049",
                    command=lambda m=mesa: self.reservar_mesa(m)
                )
                btn_reservar.pack(side="right", padx=10)
            card.pack(pady=8, padx=15, fill="x")
        
        lista.pack(pady=15, padx=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_principal
        )
        btn_voltar.pack(pady=15)

    def criar_tela_reservar(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Fazer Reserva", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        form = ctk.CTkFrame(frame, fg_color="transparent")
        
        self.entry_mesa = ctk.CTkEntry(
            form, placeholder_text="Número da Mesa", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_mesa.pack(pady=12)
        
        self.entry_tempo = ctk.CTkEntry(
            form, placeholder_text="Tempo (min)", width=400, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_tempo.pack(pady=12)
        
        btn_reservar = ctk.CTkButton(
            form, text="Confirmar Reserva", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#4CAF50", hover_color="#45A049",
            command=self.fazer_reserva
        )
        btn_reservar.pack(pady=15)
        
        btn_voltar = ctk.CTkButton(
            form, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)
        form.pack(pady=10)

    def criar_tela_tempo_jogo(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Controle de Tempo", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        lista = ctk.CTkScrollableFrame(frame, width=900, height=450, corner_radius=12, fg_color="transparent")
        
        username = self.usuario_atual["nome_usuario"]
        for reserva in [r for r in self.data.reservas if r['cliente'] == username]:
            mesa = next((m for m in self.data.mesas if m['id'] == reserva['mesa']), None)
            if mesa and mesa['tempo_inicio']:
                tempo = (datetime.now() - mesa['tempo_inicio']).seconds // 60
                info = f"Mesa {mesa['id']} | Tempo decorrido: {tempo} min"
                card = ctk.CTkFrame(lista, fg_color="#3C3C3C", corner_radius=12)
                ctk.CTkLabel(card, text=info, font=("Roboto", 16), text_color="#FFFFFF").pack(side="left", padx=15, pady=10)
                btn_extend = ctk.CTkButton(
                    card, text="Estender Tempo", width=150, height=40, font=("Roboto", 14),
                    corner_radius=10, fg_color="#FF9800", hover_color="#F57C00",
                    command=lambda m=mesa: self.estender_tempo(m)
                )
                btn_extend.pack(side="right", padx=10)
                card.pack(pady=8, padx=15, fill="x")
        
        lista.pack(pady=15, padx=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_cardapio(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Cardápio", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        lista = ctk.CTkScrollableFrame(frame, width=900, height=450, corner_radius=12, fg_color="transparent")
        
        for item in self.data.cardapio:
            card = ctk.CTkFrame(lista, fg_color="#3C3C3C", corner_radius=12)
            info = f"{item['nome']} ({item['tipo'].capitalize()}) | R${item['preco']:.2f}"
            ctk.CTkLabel(card, text=info, font=("Roboto", 16), text_color="#FFFFFF").pack(side="left", padx=15, pady=10)
            btn_pedir = ctk.CTkButton(
                card, text="Pedir", width=150, height=40, font=("Roboto", 14),
                corner_radius=10, fg_color="#4CAF50", hover_color="#45A049",
                command=lambda i=item: self.fazer_pedido(i)
            )
            btn_pedir.pack(side="right", padx=10)
            card.pack(pady=8, padx=15, fill="x")
        
        lista.pack(pady=15, padx=10)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_perfil(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Perfil do Jogador", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        username = self.usuario_atual["nome_usuario"]
        jogos_jogados = set()
        for reserva in self.data.reservas:
            if reserva['cliente'] == username:
                mesa = next((m for m in self.data.mesas if m['id'] == reserva['mesa']), None)
                if mesa and mesa['console']:
                    console = next((c for c in self.data.consoles if c['tipo'] == mesa['console']), None)
                    if console:
                        jogos_jogados.update(console['jogos'])
        
        ctk.CTkLabel(frame, text=f"Usuário: {username}", font=("Roboto", 24), text_color="#FFFFFF").pack(pady=10)
        ctk.CTkLabel(frame, text=f"Email: {self.data.usuarios[username]['email']}", font=("Roboto", 24), text_color="#FFFFFF").pack(pady=10)
        ctk.CTkLabel(frame, text=f"Telefone: {self.data.usuarios[username]['telefone']}", font=("Roboto", 24), text_color="#FFFFFF").pack(pady=10)
        ctk.CTkLabel(frame, text="Jogos Jogados:", font=("Roboto", 24, "bold"), text_color="#4CAF50").pack(pady=10)
        for jogo in jogos_jogados:
            ctk.CTkLabel(frame, text=jogo, font=("Roboto", 18), text_color="#FFFFFF").pack()
        
        ctk.CTkLabel(frame, text="Feedback:", font=("Roboto", 24, "bold"), text_color="#4CAF50").pack(pady=10)
        self.entry_feedback = ctk.CTkEntry(
            frame, placeholder_text="Deixe seu feedback", width=450, height=45, font=("Roboto", 16),
            corner_radius=10
        )
        self.entry_feedback.pack(pady=10)
        
        btn_enviar = ctk.CTkButton(
            frame, text="Enviar Feedback", width=250, height=45, font=("Roboto", 16),
            corner_radius=15, fg_color="#2196F3", hover_color="#1976D2",
            command=self.enviar_feedback
        )
        btn_enviar.pack(pady=10)
        
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def criar_tela_pagamento_cliente(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.canvas, fg_color="#2B2B2B", corner_radius=20)
        self.canvas.create_window(self.winfo_width() // 2, self.winfo_height() // 2, window=frame, anchor="center")
        
        ctk.CTkLabel(frame, text="Pagamentos", font=("Roboto", 32, "bold"), text_color="#FFD700").pack(pady=20)
        username = self.usuario_atual["nome_usuario"]
        total = sum(p['valor'] for p in self.data.pagamentos if p['cliente'] == username)
        ctk.CTkLabel(frame, text=f"Total Pago: R${total:.2f}", font=("Roboto", 24, "bold"), text_color="#4CAF50").pack(pady=10)
        
        colunas = ("ID", "Valor", "Descrição", "Data")
        style = ttk.Style()
        style.configure("Treeview", font=("Roboto", 14), rowheight=30, background="#2B2B2B", foreground="#FFFFFF")
        style.configure("Treeview.Heading", font=("Roboto", 16, "bold"), background="#4CAF50", foreground="#FFFFFF")
        
        tree = ttk.Treeview(frame, columns=colunas, show="headings", height=15)
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)
        
        for pagamento in [p for p in self.data.pagamentos if p['cliente'] == username]:
            tree.insert("", "end", values=(
                pagamento['id'], 
                f"R${pagamento['valor']:.2f}", 
                pagamento['descricao'], 
                pagamento['data']
            ))
        
        tree.pack(fill="both", expand=True, padx=15, pady=15)
        btn_voltar = ctk.CTkButton(
            frame, text="Voltar", width=300, height=50, font=("Roboto", 18),
            corner_radius=15, fg_color="#F44336", hover_color="#D32F2F",
            command=self.criar_tela_usuario
        )
        btn_voltar.pack(pady=15)

    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        if not usuario or not senha:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")
            return
        
        if usuario in self.data.usuarios and self.data.usuarios[usuario]["senha"] == senha:
            self.usuario_atual = {"nome_usuario": usuario, "cargo": self.data.usuarios[usuario]["cargo"]}
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.criar_tela_usuario()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def cadastrar_usuario(self):
        usuario = self.entry_novo_usuario.get().strip()
        senha = self.entry_nova_senha.get().strip()
        email = self.entry_nova_email.get().strip()
        telefone = self.entry_nova_telefone.get().strip()
        
        if not all([usuario, senha, email, telefone]):
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return
        
        if usuario in self.data.usuarios:
            messagebox.showerror("Erro", "Nome de usuário já existe!")
            return
        
        # Basic email validation
        if "@" not in email or "." not in email:
            messagebox.showerror("Erro", "Email inválido!")
            return
        
        # Basic phone validation
        if not telefone.replace(" ", "").isdigit():
            messagebox.showerror("Erro", "Telefone deve conter apenas números!")
            return
        
        self.data.usuarios[usuario] = {
            "senha": senha,
            "cargo": "cliente",
            "email": email,
            "telefone": telefone
        }
        self.data.save_data()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.criar_tela_login()

    def deslogar(self):
        self.data.save_data()
        self.usuario_atual = None
        messagebox.showinfo("Logout", "Saiu da conta com sucesso.")
        self.criar_tela_principal()

    def alterar_status_mesa(self, mesa):
        if mesa["status"] == "livre":
            mesa["status"] = "ocupada"
            mesa["tempo_inicio"] = datetime.now()
        elif mesa["status"] == "ocupada":
            mesa["status"] = "livre"
            tempo = (datetime.now() - mesa["tempo_inicio"]).seconds // 60
            mesa["tempo_total"] += tempo
            self.data.pagamentos.append({
                "id": str(uuid.uuid4())[:8],
                "cliente": self.usuario_atual["nome_usuario"],
                "valor": tempo * 10 / 60,  # R$10/hora
                "descricao": f"Uso da mesa {mesa['id']}",
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            mesa["tempo_inicio"] = None
        self.data.save_data()
        self.criar_tela_gerenciar_mesas()

    def registrar_manutencao(self, console):
        console["manutencao"].append({
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "detalhes": "Manutenção realizada"
        })
        self.data.save_data()
        messagebox.showinfo("Sucesso", "Manutenção registrada com sucesso!")
        self.criar_tela_gerenciar_consoles()

    def atualizar_status_pedido(self, pedido):
        if pedido["status"] == "preparando":
            pedido["status"] = "pronto"
        elif pedido["status"] == "pronto":
            pedido["status"] = "entregue"
            self.data.pagamentos.append({
                "id": str(uuid.uuid4())[:8],
                "cliente": pedido["cliente"],
                "valor": pedido["valor"],
                "descricao": f"Pedido {pedido['id']} - {pedido['item']}",
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
        self.data.save_data()
        self.criar_tela_gerenciar_pedidos()

    def cancelar_reserva(self, reserva):
        mesa = next((m for m in self.data.mesas if m['id'] == reserva['mesa']), None)
        if mesa:
            mesa["status"] = "livre"
        self.data.reservas.remove(reserva)
        self.data.save_data()
        messagebox.showinfo("Sucesso", "Reserva cancelada com sucesso!")
        self.criar_tela_gerenciar_reservas()

    def reservar_mesa(self, mesa):
        if mesa["status"] != "livre":
            messagebox.showerror("Erro", "Mesa não disponível!")
            return
        self.data.reservas.append({
            "id": str(uuid.uuid4())[:8],
            "cliente": self.usuario_atual["nome_usuario"],
            "mesa": mesa["id"],
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        mesa["status"] = "reservada"
        self.data.save_data()
        messagebox.showinfo("Sucesso", "Mesa reservada com sucesso!")
        self.criar_tela_mesas()

    def fazer_reserva(self):
        try:
            mesa_id = int(self.entry_mesa.get().strip())
            tempo = int(self.entry_tempo.get().strip())
            if tempo <= 0:
                messagebox.showerror("Erro", "O tempo deve ser maior que zero!")
                return
            
            mesa = next((m for m in self.data.mesas if m['id'] == mesa_id), None)
            if not mesa or mesa["status"] != "livre":
                messagebox.showerror("Erro", "Mesa inválida ou não disponível!")
                return
            
            self.data.reservas.append({
                "id": str(uuid.uuid4())[:8],
                "cliente": self.usuario_atual["nome_usuario"],
                "mesa": mesa_id,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tempo": tempo
            })
            mesa["status"] = "reservada"
            self.data.save_data()
            messagebox.showinfo("Sucesso", "Reserva realizada com sucesso!")
            self.criar_tela_usuario()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números válidos para mesa e tempo!")

    def estender_tempo(self, mesa):
        reservas_usuario = [r for r in self.data.reservas if r['cliente'] == self.usuario_atual["nome_usuario"] and r['mesa'] == mesa['id']]
        if reservas_usuario:
            reservas_usuario[0]["tempo"] += 30
            self.data.save_data()
            messagebox.showinfo("Sucesso", "Tempo estendido em 30 minutos!")
        self.criar_tela_tempo_jogo()

    def fazer_pedido(self, item):
        # Verificar se o usuário tem uma reserva ativa
        reservas_usuario = [r for r in self.data.reservas if r['cliente'] == self.usuario_atual["nome_usuario"]]
        if not reservas_usuario:
            messagebox.showerror("Erro", "Você precisa ter uma reserva ativa para fazer pedidos!")
            return
        
        mesa_id = reservas_usuario[0]["mesa"]
        self.data.pedidos.append({
            "id": str(uuid.uuid4())[:8],
            "cliente": self.usuario_atual["nome_usuario"],
            "mesa": mesa_id,
            "item": item["nome"],
            "valor": item["preco"],
            "status": "preparando",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        self.data.save_data()
        messagebox.showinfo("Sucesso", f"Pedido de {item['nome']} realizado com sucesso!")
        self.criar_tela_cardapio()

    def enviar_feedback(self):
        texto = self.entry_feedback.get().strip()
        if not texto:
            messagebox.showerror("Erro", "Por favor, escreva um feedback!")
            return
        
        self.data.feedbacks.append({
            "cliente": self.usuario_atual["nome_usuario"],
            "texto": texto,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        self.data.save_data()
        messagebox.showinfo("Sucesso", "Feedback enviado com sucesso!")
        self.entry_feedback.delete(0, "end")
        self.criar_tela_perfil()

    def rodar(self):
        self.mainloop()

if __name__ == "__main__":
    app = GameCafeApp()
    app.rodar()
