
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

# Variável global que irá armazenar a coleção "Pessoas" do MongoDB
pessoas = None

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    global pessoas  # Acessa a variável global 'pessoas'
    if request.method == 'POST':
        usuario = request.form['login']  # Pega o valor do campo 'login'
        senha = request.form['senha']    # Pega o valor do campo 'senha'
        try:
            uri = f'mongodb+srv://{usuario}:{senha}@n703.dfo9g.mongodb.net/?retryWrites=true&w=majority&appName=N703'
            # print(f'{usuario}, {senha}')
            usuario = None
            senha = None
            client = MongoClient(uri)
            db = client['N703-WEB-SERVICE']
            db.list_collection_names()
            pessoas = db['Pessoas']  # Inicializa a variável global 'pessoas' com a coleção 'Pessoas'
            return redirect(url_for('index'))
        except Exception as e:
            print(f'Erro: {e}')

    return render_template('login.html')  # Retorna o formulário de login

# Rota principal (index)
@app.route('/')
def index():
    global pessoas  # Acessa a variável global 'pessoas'
    if pessoas is not None:
        todos = pessoas.find()  # Busca todos os documentos da coleção
        return render_template('index.html', pessoas=todos)
    return redirect(url_for('login'))  # Redireciona para login caso a variável 'pessoas' seja None

# Rota para adicionar um novo registro
@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    global pessoas  # Acessa a variável global 'pessoas'
    if request.method == 'POST':
        nome = request.form['Nome']
        idade = request.form['Idade']
        contato = request.form['Contato']
        rua = request.form['Rua']
        bairro= request.form['Bairro']
        cidade = request.form['Cidade']
        pessoa = {
            'Nome': nome,
            'Idade': idade,
            'Contato': contato,
            'Rua': rua,
            'Bairro': bairro,
            'Cidade': cidade
        }
        pessoas.insert_one(pessoa)  # Inserir no MongoDB
        return redirect(url_for('index'))
    return render_template('adicionar.html')

# Rota para editar um registro
@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    global pessoas  # Acessa a variável global 'pessoas'
    try:
        pessoa = pessoas.find_one({'_id': ObjectId(id)})
    except InvalidId:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form['Nome']
        idade = request.form['Idade']
        contato = request.form['Contato']
        rua = request.form['Rua']
        bairro = request.form['Bairro']
        cidade = request.form['Cidade']
        pessoas.update_one({'_id': ObjectId(id)}, {'$set': {
            'Nome': nome,
            'Idade': idade,
            'Contato': contato,
            'Rua': rua,
            'Bairro': bairro,
            'Cidade': cidade
        }})
        return redirect(url_for('index'))
    
    return render_template('editar.html', pessoa=pessoa)

# Rota para deletar um registro
@app.route('/deletar/<id>', methods=['GET'])
def deletar(id):
    global pessoas  # Acessa a variável global 'pessoas'
    try:
        pessoas.delete_one({'_id': ObjectId(id)})
    except InvalidId:
        return redirect(url_for('index'))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
