from tkinter import LEFT
from tkinter.font import BOLD, ITALIC
from turtle import color
from PIL import ImageTk, Image
import customtkinter as ctk
import os
from Liza import AI

class Janela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configuracao_janela()
        self.tela_login()
        
    def configuracao_janela(self):
        self.geometry("1200x620")
        self.title("Liza")
        self.resizable(False, False)
    
    def tela_login(self):
        
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.liza = ctk.CTkImage(Image.open(self.file_path + "/liza.png"), size=(500,500))

        self.frameT = ctk.CTkFrame(self, width=350, height=380)
        self.frameT.place(x=0, y=0)
        
        self.lb_img = ctk.CTkLabel(self.frameT,text="", image=self.liza)
        self.lb_img.grid(row=1, column=0, padx=20, pady=50)
       
        self.titleB = ctk.CTkLabel(self.frameT, text="Faça o Login ou Cadastre-se\n em nosso site para\n acessar os serviços de Liza!", font=("Roboto", 24, BOLD), )
        self.titleB.grid(row=0, column=0, padx=10, pady=10)
        
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=800, y=190)
        
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o login!", font=("Roboto", 22, BOLD))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.usuario_login_entry = ctk.CTkEntry(self.frame_login,width=300, placeholder_text="Usuario", font=("Roboto", 16, BOLD))
        self.usuario_login_entry.grid(row=1, column=0, padx=10, pady=10)
                
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", width=300,font=("Roboto", 16, BOLD), corner_radius=10, show="*")
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)
        
        self.btn_login = ctk.CTkButton(self.frame_login,width=300, text="Fazer Login", font=("Roboto", 16, BOLD), corner_radius=10, command=lambda:self.tela_home())
        self.btn_login.grid(row=3, column=0, padx=10, pady=10)

   
                    
    def tela_home(self): 
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.lizaimg = ctk.CTkImage(Image.open(self.file_path + "/liza.png"), size=(200,200))
        
        self.frame_login.place_forget()
        self.frameT.place_forget()
        self.navbar = ctk.CTkFrame(self)
        self.navbar.place(x=150, y=100)
        
        self.titleB = ctk.CTkLabel(self.navbar, text="Sua Liza já está preparada! Aperte o botão ou pressione a tecla F1\n em seu computador e tudo será controlado por voz!", font=("Roboto", 24, BOLD))
        self.titleB.grid(row=0, column=0, padx=10, pady=10)
        
        self.btn_login = ctk.CTkButton(self.navbar,width=30, image=self.lizaimg,text="", font=("Roboto", 16, BOLD), corner_radius=200, command=lambda:self.lizaEscute())
        self.btn_login.grid(row=3, column=0, padx=10, pady=10)
        self.bind("<F1>", lambda event: self.lizaEscute())
             
    def lizaEscute(self):
        self.Liza=AI()
        self.Liza.listen()
        
        
          
    def limpa_cadastro(self):
        self.usuario_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirm_senha_cadastro_entry.delete(0, END)
        self.nascimento_entry.delete(0, END)
        self.email_entry.delete(0, END)

        
if __name__ == "__main__":
    janela = Janela()
    janela.mainloop()