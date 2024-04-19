import sqlite3
from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)

app.secret_key ="abelinha"

conexao=sqlite3.connect("banco.sqlite")
cursor=conexao.cursor()

conexao.commit()
conexao.close()

# rota do Index
@app.route("/",methods= ["GET","POST"])
def pagina_index():
        if request.method == "GET":
                filtro= request.args.get("filtro")
                # conexao com o arquivo sqlite
                conexao = sqlite3.connect("banco.sqlite")
                # Manda informaçoes para o banco de dados
                cursor = conexao.cursor()
                if filtro == "Todos" or filtro == None:
                        cursor.execute("SELECT *, rowid FROM tb_produtos WHERE ativo == 'Sim'")
                else:
                        cursor.execute(f"SELECT *, rowid FROM tb_produtos WHERE categoria = '{filtro}' and ativo == 'Sim' ")
                produto=cursor.fetchall()
                conexao.close()

                return render_template("index.html",show_produto = (produto))


# rota do cadrasto
@app.route("/cadastro",methods= ["GET","POST"])
def pagina_cadastro():
      

    if request.method == "GET":
        if session.get("usuario","ERRO") == "Autenticado":
                conexao = sqlite3.connect("banco.sqlite")
                cursor = conexao.cursor()
                cursor.execute(f"SELECT *, rowid FROM tb_produtos")
                dados=cursor.fetchall()
                conexao.close()

                return render_template("cadastrar.html", listagem = (dados))
        else:
               return redirect("/senha")
        
    else:
        #nomes dos inputs VARIAVEIS
        nome = request.form["nome"]
        descricao= request.form["descricao"]
        categoria = request.form["categoria"]
        foto = request.form["foto"]
        preco =  request.form["preco"]
        ativo = request.form["ativo"]
        #salvamento dos dados
        conexao=sqlite3.connect("banco.sqlite")
        #envia os comando (criar tabela, deletar, etc)
        cursor=conexao.cursor()
        #inserçao dos dados na tabela
        cursor.execute(f"INSERT INTO tb_produtos VALUES ('{nome}','{descricao}','{categoria}','{foto}','{preco}','{ativo}')")
        #salva a conexao
        conexao.commit()
       
        
         #fecha a conexao
        conexao.close()

        return render_template("cadastrar.html")

# rota dos produtos1
@app.route("/produto/<rowid>")
def pagina_produto(rowid):

        conexao=sqlite3.connect("banco.sqlite")
        cursor=conexao.cursor()
        cursor.execute(f"SELECT * FROM tb_produtos WHERE rowid = {rowid}")
        produto=cursor.fetchone()
        conexao.close()
       


        return render_template("produtos.html", item = produto)

# deleta dados do banco de dados  
@app.route("/delete/<rowid>")
def delete(rowid):

    conexao=sqlite3.connect("banco.sqlite")

    cursor=conexao.cursor()


    cursor.execute(f"DELETE FROM tb_produtos WHERE rowid = {rowid}")

    conexao.commit()

    conexao.close()

    return redirect("/cadastro")

# aciona o botão ativar e o botao desativar do banco de dados
@app.route("/produto/<acao>/<rowid>")
def pagina_(acao,rowid):
        conexao = sqlite3.connect("banco.sqlite")
        cursor = conexao.cursor()
        if acao == 'ativar':
                cursor.execute(f"update tb_produtos set ativo = 'Sim' where rowid = {rowid}")
        else:  
                cursor.execute(f"update tb_produtos set ativo = 'Não' where rowid = {rowid}")
        conexao.commit()
        conexao.close()

        return redirect("/cadastro")
      
@app.route("/senha", methods=["GET","POST"])
def pagina_login():
        if request.method == 'GET':
                if session.get("usuario","ERRO") == "Autenticado":
                       return redirect("/cadastro")
                else:
                        return render_template("senha.html")
        if request.method == 'POST':
                login = request.form["usuario"]
                senha = request.form["senha"]
                conexao = sqlite3.connect("banco.sqlite")
                cursor = conexao.cursor()
                cursor.execute(f"SELECT *, rowid FROM tb_usuarios WHERE login = '{login}' and senha = '{senha}'")
                dados = cursor.fetchall()
                conexao.close()

                if len (dados) > 0:
                       session["usuario"] = "Autenticado"
                       return redirect("/cadastro")
                else:
                       return redirect("/senha")
        
@app.route("/logoff")
def pagina_logoff():
       session.clear()
       return redirect("/login")
               
                


app.run(debug=True)
