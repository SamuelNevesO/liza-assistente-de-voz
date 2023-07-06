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

        self.liza = AI()

           
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.liza = ctk.CTkImage(Image.open(self.file_path + "/liza.png"), size=(500,500))
       
        self.lb_img = ctk.CTkLabel(self,text="", image=self.liza)
        self.lb_img.grid(row=1, column=0, padx=20, pady=50)
       
        self.titleB = ctk.CTkLabel(self, text="Faça o Login ou Cadastre-se\n em nossa plataforma para\n acessar os serviços de Liza!", font=("Roboto", 24, BOLD), )
        self.titleB.grid(row=0, column=0, padx=10, pady=10)
        
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=800, y=100)
        
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o login!", font=("Roboto", 22, BOLD))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        self.usuario_login_entry = ctk.CTkEntry(self.frame_login,width=300, placeholder_text="Usuario", font=("Roboto", 16, BOLD))
        self.usuario_login_entry.grid(row=1, column=0, padx=10, pady=10)
                
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", width=300,font=("Roboto", 16, BOLD), corner_radius=10, show="*")
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)
        
        self.btn_login = ctk.CTkButton(self.frame_login,width=300, text="Fazer Login", font=("Roboto", 16, BOLD), corner_radius=10)
        self.btn_login.grid(row=3, column=0, padx=10, pady=10)
        
        self.spam= ctk.CTkLabel(self.frame_login, text="Se ainda não possui conta, clique no botão\n abaixo para se cadastrar", font=("Roboto", 10))
        self.spam.grid(row=4, column=0, padx=10, pady=10)
        
        self.btn_cadastro = ctk.CTkButton(self.frame_login,fg_color="green", hover_color="#050" ,width=300, text="Cadastrar-se", font=("Roboto", 16, BOLD), corner_radius=10, command=lambda:self.tela_cadastro())
        
        self.btn_cadastro.grid(row=5, column=0, padx=10, pady=17)         
        
    def tela_cadastro(self):
        
        self.frame_login.place_forget()
        
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=800, y=100)
        
                
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Cadastre-se", font=("Roboto", 22, BOLD))
        self.lb_title.grid(row=0, column=0, padx=10, pady=5)
        
        self.usuario_cadastro_entry = ctk.CTkEntry(self.frame_cadastro,width=300, placeholder_text="Usuario", font=("Roboto", 16, BOLD))
        self.usuario_cadastro_entry.grid(row=1, column=0, padx=10, pady=5)
                
        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Senha", width=300,font=("Roboto", 16, BOLD), corner_radius=10, show="*")
        self.senha_cadastro_entry.grid(row=2, column=0, padx=10, pady=5)
        
        self.confirm_senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Confirme sua senha", width=300,font=("Roboto", 16, BOLD), corner_radius=10, show="*")
        self.confirm_senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=5)
        
        self.nascimento_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Data de nascimento", width=300,font=("Roboto", 16, BOLD), corner_radius=10, show="*")
        self.nascimento_entry.grid(row=4, column=0, padx=10, pady=5)        
     
        self.email_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="Email", width=300,font=("Roboto", 16, BOLD), corner_radius=10, show="*")
        self.email_entry.grid(row=5, column=0, padx=10, pady=5)        
     
        self.btn_cadastrar = ctk.CTkButton(self.frame_cadastro ,width=300, text="Cadastrar-se", font=("Roboto", 16, BOLD), corner_radius=10, command=self.limpa_cadastro)
        self.btn_cadastrar.grid(row=6, column=0, padx=10, pady=5)    
            
        self.btn_voltar_login = ctk.CTkButton(self.frame_cadastro ,width=300,fg_color="green", hover_color="#050" ,text="Voltar ao login", font=("Roboto", 16, BOLD), corner_radius=10, command=lambda:self.tela_login())
        self.btn_voltar_login.grid(row=7, column=0, padx=10, pady=5)        
                    
    def tela_home(self): 
        
      
      
             
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