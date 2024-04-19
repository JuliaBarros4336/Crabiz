from flask import Flask, render_template, request,jsonify,session
from usuario import Usuario
from chat import Chat
from contato import Contato

app = Flask(__name__)
app.secret_key = 'argamassa'

# Rota para a página de cadastro
@app.route('/')
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':

        nome = request.form['nome']
        telefone = request.form['telefone']
        senha = request.form['senha']
        # instanciar o usuario
        usuario = Usuario() 
        usuario.cadastrar(telefone,nome,senha)

        return render_template('index.html')
    
    
    return render_template('index.html')
    
# Rota para cadastro feito em requisição ajax
# @app.route('/')
# @app.route('/cadastro_ajax', methods=['GET', 'POST'])
# def cadastro_ajax():
#     if request.method == 'POST':

#     #  Recebendo os dados em json
#         dados_cadastro = request.get_json()

#         nome = dados_cadastro['nome']
#         telefone = dados_cadastro['telefone']
#         senha = dados_cadastro['senha']

#         # instanciando usuario
#         usuario = Usuario()

        

#         if usuario.cadastrar(telefone,nome,senha):
#             return jsonify({'mensagem':'Cadastro com sucesso'}), 200
#         else:
#             return jsonify({'mensagem':'Cadastro com erro'}), 500
        
#         return render_template('index-ajax.html')
    
#     return render_template('index-ajax.html')

#Rota do login 
@app.route('/login', methods=['GET', 'POST'])
def logar():
    if request.method == 'POST':

        telefone = request.form['telefone']
        senha = request.form['senha']
        usuario = Usuario()
        usuario.logar(telefone,senha)

        if usuario.logado == True:

            session['usuario_logado'] = {"nome":usuario.nome,
                                         "telefone":usuario.telefone}
            
            return render_template('chat.html')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    


# Rota da API usuario
@app.route('/get/usuarios')
def api_get_usuarios():
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario,telefone_usuario)
    contatos = chat.contato_retorno()
    return jsonify(contatos), 200

#Rota receber mensagem
@app.route('/get/mensagens/<tel_contato_selecionado>') 
def api_get_mensagens(tel_contato_selecionado):
    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    chat = Chat(nome_usuario,telefone_usuario)
    contato = Contato("",tel_contato_selecionado)
    lista_de_mensagens = chat.verificar_mensagem(0,contato)
    return jsonify(lista_de_mensagens), 200

#Rota enviar mensagem
@app.route('/post/envia_mensagem/',methods=['POST'])
def api_post_mensagem():
    #Pegando os dados que foram enviados
    dados = request.get_json()

    nome_usuario = session["usuario_logado"]["nome"]
    telefone_usuario = session["usuario_logado"]["telefone"]
    mensagem = dados['mensagem']
    destinatario = dados['telefone']
    chat = Chat(nome_usuario,telefone_usuario)
    chat.enviar_mensagem(mensagem,destinatario)
    
    return jsonify({}), 200

app.run(debug=True),