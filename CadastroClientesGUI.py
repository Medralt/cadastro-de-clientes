from tkinter import Tk, Label, Entry, Button, Text, messagebox
from PIL import ImageTk, Image
import pandas as pd
import re


class Cliente:
    def __init__(self, nome, idade, email, telefone):
        self.nome = nome
        self.idade = idade
        self.email = email
        self.telefone = telefone


class CadastroClientes:
    def __init__(self):
        self.clientes = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.salvar_dados()
        print("Cliente cadastrado com sucesso!")

    def listar_clientes(self):
        return self.clientes

    def carregar_clientes(self, arquivo):
        try:
            df = pd.read_excel(arquivo)
            for _, row in df.iterrows():
                nome = row['Nome']
                idade = row['Idade']
                email = row['Email']
                telefone = row['Telefone']
                cliente = Cliente(nome, idade, email, telefone)
                self.clientes.append(cliente)
            print("Dados carregados com sucesso!")
        except FileNotFoundError:
            print(f"Arquivo {arquivo} não encontrado.")


class CadastroClientesGUI:
    def __init__(self):
        self.cadastro = CadastroClientes()
        self.window = Tk()
        self.window.title("Cadastro de Clientes")
        self.window.state("zoomed")

        # Logo
        image = Image.open("logo.jpg")
        logo = ImageTk.PhotoImage(image)
        logo_label = Label(self.window, image=logo)
        logo_label.image = logo
        logo_label.pack(anchor="nw", padx=5, pady=10)

        # Frame para os campos de entrada
        entry_frame = Label(self.window)
        entry_frame.pack(anchor="nw", padx=10, pady=10)

        # Labels
        Label(entry_frame, text="Nome:", justify="left").grid(row=0, column=0, padx=10, pady=5)
        Label(entry_frame, text="Idade:", justify="left").grid(row=1, column=0, padx=10, pady=5)
        Label(entry_frame, text="Email:", justify="left").grid(row=2, column=0, padx=10, pady=5)
        Label(entry_frame, text="Telefone:", justify="left").grid(row=3, column=0, padx=10, pady=5)

        # Entry fields
        self.nome_entry = Entry(entry_frame)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        self.idade_entry = Entry(entry_frame)
        self.idade_entry.grid(row=1, column=1, padx=10, pady=5)
        self.email_entry = Entry(entry_frame)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)
        self.telefone_entry = Entry(entry_frame)
        self.telefone_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        button_frame = Label(self.window)
        button_frame.pack(anchor="w", padx=10, pady=10)

        adicionar_button = Button(button_frame, text="Adicionar", command=self.adicionar_cliente)
        adicionar_button.pack(side="left", padx=10)

        listar_button = Button(button_frame, text="Listar", command=self.listar_clientes)
        listar_button.pack(side="left", padx=10)
        
        novo_button = Button(button_frame, text="Novo", command=self.novo_cliente)
        novo_button.pack(side="left", padx=10)

        # Lista de Clientes
        self.lista_clientes = Text(self.window, height=10, width=50)
        self.lista_clientes.pack(anchor="ne", padx=30, pady=10)

        # Caminho do arquivo de saída
        self.caminho_arquivo = "clientes.xlsx"

        # Carregar clientes do arquivo
        self.cadastro.carregar_clientes(self.caminho_arquivo)

    def adicionar_cliente(self):
        nome = self.nome_entry.get()
        idade = self.idade_entry.get()
        email = self.email_entry.get()
        telefone = self.telefone_entry.get()

        if not self.validar_data(idade):
            messagebox.showerror("Erro", "O campo Idade deve estar no formato dd/mm/aaaa.")
            return

        if not self.validar_email(email):
            messagebox.showerror("Erro", "O campo Email está em um formato inválido.")
            return

        novo_cliente = Cliente(nome, idade, email, telefone)
        self.cadastro.adicionar_cliente(novo_cliente)

        self.nome_entry.delete(0, "end")
        self.idade_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.telefone_entry.delete(0, "end")

    def listar_clientes(self):
        clientes = self.cadastro.listar_clientes()
        self.lista_clientes.config(state="normal")
        self.lista_clientes.delete("1.0", "end")
        self.lista_clientes.insert("end", "Lista de Clientes:\n")
        for cliente in clientes:
            self.lista_clientes.insert("end", f"Nome: {cliente.nome}, Idade: {cliente.idade}, Email: {cliente.email}\n")
        self.lista_clientes.config(state="disabled")
        
    def novo_cliente(self):
        self.nome_entry.delete(0, "end")
        self.idade_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.telefone_entry.delete(0, "end")

    def salvar_dados(self):
        dados = []
        for cliente in self.cadastro.clientes:
            dados.append([cliente.nome, cliente.idade, cliente.email, cliente.telefone])

        df = pd.DataFrame(dados, columns=["Nome", "Idade", "Email", "Telefone"])
        df.to_excel(self.caminho_arquivo, index=False)
        print("Dados salvos com sucesso!")

    def validar_data(self, data):
        pattern = r"\d{2}/\d{2}/\d{4}"
        if re.match(pattern, data):
            return True
        return False

    def validar_email(self, email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        if re.match(pattern, email):
            return True
        return False

    def iniciar(self):
        self.window.mainloop()


cadastro_gui = CadastroClientesGUI()
cadastro_gui.iniciar()
