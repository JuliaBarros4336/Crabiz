import mysql.connector

class Conexao:
    def conectar():
        mydb = mysql.connector.connect(
                host="10.110.140.166",
                # projetochat2.mysql.database.azure.com
                user="equipe",
                password="123456789",
                database="crabiz",
            )
        return mydb