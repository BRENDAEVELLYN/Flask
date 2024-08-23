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
    ra = request.form['ra']
    if ra == '12345678':
       
        return render_template('diariobordo.html',ra=ra)
    else:
        mensagem = "RA inválido."
        return render_template ('index.html',mensagem=mensagem)

@app.route('/diariobordo')
def abrir_diario():
   return render_template('diariobordo.html')


@app.route('/criaraluno', methods=['POST'])
def criar():
    ra = request.form['ra']
    Nome = request.form['Nome']
    Tempo_de_Estudo = int(request.form['Tempo_de_Estudo'])
    Renda_Media_Salarial_Familiar = float(request.form['Renda_Media_Salarial_Familiar'])

     # Verifica se o RA já existe no banco de dados
    aluno_existente = session.query(Aluno).filter_by(ra=ra).first()

    if aluno_existente:
        mensagem = "RA já cadastrado no sistema."
        return render_template('index.html', msgbanco=mensagem)

    aluno = Aluno(ra=ra,Nome=Nome,Tempo_de_Estudo = Tempo_de_Estudo, Renda_Media_Salarial_Familiar=Renda_Media_Salarial_Familiar)
    
    try:
      session.add(aluno) #  Adiciona um novo objeto aluno à sessão para ser inserido no banco de dados.
      session.commit() # Confirma a transação, salvando as mudanças no banco de dados.
    except:
      session.rollback() # Desfaz qualquer mudança feita na sessão durante a transação, revertendo o banco de dados ao estado anterior.
      raise # Relevanta a exceção original, permitindo que seja tratada em outro nível do código ou exibida como um erro
    finally:
       session.close() # Fecha a sessão, garantindo que os recursos sejam liberados, independentemente de a transação ter sido bem-sucedida ou não.
 
    return redirect(url_for('listar_alunos'))

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    try:
        # Busca todos os alunos cadastrados no banco de dados
        alunos = session.query(Aluno).all()
    except:
        session.rollback()
        mensagem = "Erro ao tentar recuperar a lista de alunos."
        return render_template('index.html', msgbanco=mensagem)
    finally:
        session.close()

    # Renderiza o template HTML passando a lista de alunos
    return render_template('lista_alunos.html', alunos=alunos)








if __name__ == '__main__':
    app.run(debug=True)