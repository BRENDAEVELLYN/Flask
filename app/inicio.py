from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Importa a função `sessionmaker`, que é usada para criar uma nova sessão para interagir com o banco de dados
from sqlalchemy.orm import sessionmaker

# Importa as funções `create_engine` para estabelecer uma conexão com o banco de dados e `MetaData` para trabalhar com metadados do banco de dados
from sqlalchemy import create_engine, MetaData

# Importa a função `automap_base`, que é usada para refletir um banco de dados existente em classes ORM automaticamente
from sqlalchemy.ext.automap import automap_base

from aluno import Aluno

app = Flask(__name__)

# Criando a configuração do banco de dados
# Configuração do Banco de Dados
# biblioteca para converter e resolver problema do @
import urllib.parse

# Qual o usuário do banco e a senha?

user = 'root'
password = urllib.parse.quote_plus('senai@123')

host = 'localhost'
database = 'projetodiario1'
connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# Criar a engine e refletir o banco de dados existente
engine = create_engine(connection_string)
metadata = MetaData()
metadata.reflect(engine)

# Mapeamento automático das tabelas para classes Python
Base = automap_base(metadata=metadata)
Base.prepare()

# Acessando a tabela 'aluno' mapeada
Aluno = Base.classes.aluno



# Criar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novoaluno')
def cadastrar_aluno():
    return render_template('novoaluno.html')

@app.route('/logar', methods=['POST'])
def logar_ra():
    ra = request.form.get('ra')
    if ra == '12345678':
       
        return redirect(url_for('diariobordo', ra=ra))
    else:
        mensagem = "RA inválido."
        return render_template ('index.html',mensagem=mensagem)

@app.route('/diariobordo')
def diariobordo():
    ra = request.args.get('ra')
    return render_template('diariobordo.html', ra=ra)


@app.route('/criaraluno', methods=['POST'])
def criar():
    ra = request.form['ra']
    Nome = request.form['Nome']
    Tempo_de_Estudo = int(request.form['Tempo_de_Estudo'])
    Renda_Media_Salarial_Familiar = float(request.form['Renda_Media_Salarial_Familiar'])
    aluno = Aluno(ra=ra,Nome=Nome,Tempo_de_Estudo=Tempo_de_Estudo,Renda_Media_Salarial_Familiar=Renda_Media_Salarial_Familiar)
    session.add(aluno)
    session.commit()
    mensagem = "cadastro efetuado com sucesso"
    return render_template('index.html',msgbanco = mensagem)

if __name__ == '__main__':
    app.run(debug=True)