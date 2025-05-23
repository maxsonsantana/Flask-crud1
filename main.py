from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://flask:flask123@NOTE_MAXSON\\SQLEXPRESS/max1?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&Encrypt=no'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Cria a tabela caso não exista
class Pessoa(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NOME = db.Column(db.String(100), nullable=False)
    SOBRENOME = db.Column(db.String(100), nullable=False)
    IDADE = db.Column(db.String(100), nullable=True)
    ID_PROFISSAO = db.Column(db.String(100), nullable=True)

#Retorna os dados da tabela
@app.route('/')
def index():
    pessoa = Pessoa.query.all()
    return render_template('index.html', pess=pessoa)

#Adiciona uma nova pessoa
@app.route('/addperson', methods=['POST'])  
def addPerson():
    # Verifica se existe o campo nome e sobrenome
    existeDados = Pessoa.query.filter_by(NOME=request.form["nome"], SOBRENOME=request.form["sobrenome"]).first()
    if existeDados:
        return 'Erro ao efetuar o cadastro, já existe uma pessoa com esse nome e sobrenome'
    
    nome = request.form["nome"]
    sobrenome = request.form["sobrenome"]
    new_pessoa = Pessoa(NOME=nome, SOBRENOME=sobrenome)
    db.session.add(new_pessoa)
    db.session.commit()
    return redirect('/')

#Deleta uma pessoa
@app.route('/delPerson/<int:ID>', methods=['POST'])
def delPerson(ID):
    pessoa = Pessoa.query.get(ID)
    if pessoa:
        db.session.delete(pessoa)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)