from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app) #associa o banco de dados ao app

class User(db.Model):
    nome = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    idade_do_usuario = db.Column(db.Integer, nullable = False)

with app.app_context(): #Comando necessário para o próximo comando  "db.create_all()"
    db.create_all() #Cria o banco de dados se não existir um 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users_list():
    users = db.session.execute(db.select(User).order_by(User.nome)).scalars() #db.session.execute(db.select(...)) usado para selecionar dados do database
    
    return render_template('users_list.html', users=users)                    #o método scalars gera uma lista de resultado, o scalar gera apenas um único resultado

@app.route('/users/create', methods=['POST', 'GET'])
def user_create():
    if request.method == 'POST':
        user=User(nome=request.form['username'], idade_do_usuario=request.form['age'])
        db.session.add(user) #.add adiciona o objeto entre parênteses ao database
        db.session.commit()#o commit salva as alterações no database 
        
    return render_template('user_create.html')

@app.route('/users/delete', methods=['POST', 'GET'])
def user_delete():
    if request.method == 'POST':
        user_nome = request.form['user_nome']
        user = db.session.execute(db.select(User).filter_by(nome=user_nome)).scalar()
        db.session.delete(user)
        db.session.commit()    
        return redirect(url_for('users_list'))
    
    return render_template('user_delete.html')
 
@app.route('/users/update', methods=['POST', 'GET'])
def users_update():
   #fornece uma lista com os usuários do database
    if request.method == 'POST':
        nm = request.form['user_nome']
        users = db.session.execute(db.select(User).filter_by(nome= nm)).scalar()
        users.nome = request.form['new_nome']
        users.idade_do_usuario = request.form['new_age']
        db.session.commit()

        redirect(url_for('users_list'))  

    return render_template('user_update.html')



if __name__ == '__main__':
    app.run(debug=True)