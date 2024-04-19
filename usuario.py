from conexao import Conexao
# import criptografia
from hashlib import sha256

class Usuario:
    def __init__(self):
        self.nome = None
        self.telefone = None
        self.senha = None
        self.logado = False

    def cadastrar(self,telefone,nome,senha):
        try:
            

            # Conectando ao banco de dados
            mydb = Conexao.conectar()

            #Criando o cursor 
            mycursor = mydb.cursor()
            
            # criptografia
            senha = sha256(senha.encode()).hexdigest()

            sql = f"INSERT INTO tb_usuario (tel,nome, senha) VALUES ('{telefone}', '{nome}','{senha}')"
            mycursor.execute(sql)
        
            mydb.commit()

            mydb.close()

            self.telefone = telefone
            self.senha = senha
            self.nome = nome
            self.logado = True


            return True
        
        except:
            return False
        
    def logar(self,telefone,senha):
        # criptografia
        senha = sha256(senha.encode()).hexdigest()

        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        # mycursor.execute("SELECT tel,nome FROM tb_usuario")

        # 1 FORMA
        # sql = f"SELECT tel,nome FROM tb_usuario WHERE tel='{telefone}' AND senha='{senha}';"
        # mycursor.execute(sql)

        #2 FORMA
        sql = "SELECT tel,nome,senha FROM tb_usuario WHERE tel=%s AND senha=%s;"
        valores = (telefone,senha)
        mycursor.execute(sql,valores)


        valor = mycursor.fetchone()

        if   not valor == None: 
             self.logado = True
             self.nome = valor[1]
             self.telefone = valor[0]
             self.senha = valor[2]

             print("Você está Cadastrado!")
        else:
             self.logado =False
             print("Você não tem Cadastro!")

