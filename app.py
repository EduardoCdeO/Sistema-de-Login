import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox


class BackEnd():
    def conectar_db(self):
        self.conn = sqlite3.connect("Sistema_Login.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado com sucesso")

    def desconectar_db(self):
        self.conn.close()
        print("Banco de dados desconectado")

    def criar_tabela(self):
        self.conectar_db()
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios(
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Email TEXT NOT NULL,
                Senha TEXT NOT NULL,
                Confirmar_Senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
        self.desconectar_db()

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirmar_senha_cadastro = self.confirmar_senha_entry.get()

        self.conectar_db()

        self.cursor.execute("""
            INSERT INTO Usuarios (Username, Email, Senha, Confirmar_Senha)
            VALUES (?, ?, ?, ?)""", (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirmar_senha_cadastro))
        
        try:
            if (self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirmar_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de Login", message="Erro!\nPor favor, preencha todos os campos!")
            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="O nome de usuário deve ter pelo menos 4 caracteres.")
            elif (len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="A senha deve ter pelo menos 4 caracteres.")
            elif (self.senha_cadastro != self.confirmar_senha_cadastro):
                messagebox.showerror(title="Sistema de Login", message="Erro!\nSenha e Confirmar Senha precisam ser iguais.")
            elif ("@" not in self.email_cadastro):
                messagebox.showerror(title="Sistema de Login", message="E-mail Inválido!")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema de Login", message=f"Usuário: {self.username_cadastro}\nCadastrado com sucesso!")
                self.desconectar_db()
                self.limpar_entry_cadastro()
        except:
            messagebox.showerror(title="Sistema de Login", message="Erro no cadastro. \nPor favor, tente novamente!")
            self.desconectar_db()

    def verificar_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        self.conectar_db()

        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)""", (self.username_login, self.senha_login))

        self.verificar_dados = self.cursor.fetchone()

        try:
            if (self.username_login == "" or self.senha_login == ""):
                messagebox.showwarning(title="Sistema de Login", message="Preencha todos os campos!")
            elif (self.username_login in self.verificar_dados and self.senha_login in self.verificar_dados):
                messagebox.showinfo(title="Sistema de Login", message=f"Iniciando sessão!\nUsuário: {self.username_login}")
                self.desconectar_db()
                self.limpar_entry_login()
        except:
            messagebox.showerror(title="Sistema de Login", message="Erro!\nUsuário ou Senha incorreto.\nTente novamente!")
            self.desconectar_db()


class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.configuracao_da_janela_inicial()
        self.tela_de_login()
        self.criar_tabela()

    # Configurando a Janela Principal
    def configuracao_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.resizable(False, False)

    def show_pass(self, frame):
        if frame == "login":
            if self.senha_login_entry.cget("show") == "*":
                self.senha_login_entry.configure(show="")
            else:
                self.senha_login_entry.configure(show="*")
        elif frame == "cadastro":
            if self.senha_cadastro_entry.cget("show") == "*":
                self.senha_cadastro_entry.configure(show="")
                self.confirmar_senha_entry.configure(show="")
            else:
                self.senha_cadastro_entry.configure(show="*")
                self.confirmar_senha_entry.configure(show="*")

    def tela_de_login(self):     
        # Trabalhando com as imagens
        self.img = PhotoImage(file="To the stars.png")
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10)

        # Título da plataforma
        self.title = ctk.CTkLabel(self, text="Faça o seu login ou Cadastre-se \nna nossa plataforma para acessar \nos nossos serviços!", font=("Arial Rounded MT Bold", 14))
        self.title.grid(row=0, column=0, pady=10, padx=10)

        # Criar o frame do formulário de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)

        # Colocando widgets dentro do frame(formulário de login)
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Arial Rounded MT Bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Nome de usuário...", font=("Arial Rounded MT Bold", 16), corner_radius=15, border_color="white")
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha...", font=("Arial Rounded MT Bold", 16), corner_radius=15, border_color="white", show="*")
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha", command=lambda: self.show_pass("login"),font=("Arial Rounded MT Bold", 14), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Entrar".upper(), font=("Arial Rounded MT Bold", 14), corner_radius=15, command=self.verificar_login)
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

        self.span = ctk.CTkLabel(self.frame_login, text="Ainda não possui uma conta no nosso sistema? \nCadastre-se clicando no botão abaixo", font=("Arial Rounded MT Bold", 10))
        self.span.grid(row=5, column=0, padx=10, pady=10)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050", text="Cadastrar-se".upper(), font=("Arial Rounded MT Bold", 14), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, padx=10, pady=10)


    def tela_de_cadastro(self):
        # Remover a tela de login
        self.frame_login.place_forget()

        # Criando frame de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)

        # Criar os widgets da tela de cadastro
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça o cadastro", font=("Arial Rounded MT Bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Nome de usuário...", font=("Arial Rounded MT Bold", 16), corner_radius=15, border_color="white")
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="E-mail...", font=("Arial Rounded MT Bold", 16), corner_radius=15, border_color="white")
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha...", font=("Arial Rounded MT Bold", 16), corner_radius=15, border_color="white", show="*")
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)

        self.confirmar_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirmar senha...", font=("Arial Rounded MT Bold", 16), corner_radius=15, border_color="white", show="*")
        self.confirmar_senha_entry.grid(row=4, column=0, padx=10, pady=5)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", command=lambda: self.show_pass("cadastro"),font=("Arial Rounded MT Bold", 14), corner_radius=20)
        self.ver_senha.grid(row=5, column=0, pady=5)

        self.btn_cadastrar = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", hover_color="#050", text="Cadastrar-se".upper(), font=("Arial Rounded MT Bold", 14), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar.grid(row=6, column=0, padx=10, pady=10)
    
        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar".upper(), font=("Arial Rounded MT Bold", 14), corner_radius=15, fg_color="#444", hover_color="#333", command=self.tela_de_login)
        self.btn_login_back.grid(row=7, column=0, padx=10, pady=10)


    def limpar_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirmar_senha_entry.delete(0, END)

    def limpar_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)


if __name__ == "__main__":
    app = App()
    app.mainloop()