from usuario import Usuario
from mensagem import Mensagem
from conexao import Conexao
from contato import Contato

class Chat:
    
    def __init__(self, nome:str,telefone:str):
        self.nome_usuario = nome
        self.telefone_usuario = telefone
        

    def enviar_mensagem(self,conteudo:str,tel_destinatario:str): #-> bool
        try:
         # Conectando ao banco de dados
            mydb = Conexao.conectar()

            #Criando o cursor 
            mycursor = mydb.cursor()

            sql = f"INSERT INTO tb_mensagem (tel_remetente,tel_destinatario,mensagem) VALUES ('{self.telefone_usuario}','{tel_destinatario}','{conteudo}')"
            mycursor.execute(sql)
        
            mydb.commit()

            mydb.close()

            return True
        except:
                return False
        
    def verificar_mensagem(self,quantidade:int,contato_selecionado:Contato) -> bool:
         mydb =Conexao.conectar()
        # criando o cursor
         mycursor = mydb.cursor()

         sql = f"""select u.nome,m.mensagem from tb_mensagem m
         INNER JOIN tb_usuario u
         on m.tel_remetente = u.tel 
         where tel_remetente = '{contato_selecionado.telefone}' 
         and tel_destinatario = '{self.telefone_usuario}' or 
         tel_destinatario = '{contato_selecionado.telefone}' and tel_remetente = '{self.telefone_usuario}'"""

         mycursor.execute(sql)
         resultado = mycursor.fetchall()
         mensagens=[]

         for linha in resultado:
               mensagem = {'nome':linha[0],'mensagem':linha[1]}
               mensagens.append(mensagem)
         return (mensagens)

        # return (Mensagem("Testonildo","Testando o teste!"),
        #         Mensagem("Odivaldo","Faz o pix!"))

    def contato_retorno(self):
        mydb =Conexao.conectar()
        mycursor = mydb.cursor()
        sql="SELECT nome,tel FROM tb_usuario order by nome"
        mycursor.execute(sql)
        resultado= mycursor.fetchall()
        contatos=[]

        # inserindo o contato TODOS
        contatos.append({"nome":"TODOS","telefone":""})

        
        for linha in resultado:
              #Criando a mensagem primeiro e incluindo na lista
              contato = ({"nome":linha[0],"telefone":linha[1]})
              contatos.append(contato)
        
        return (contatos)
