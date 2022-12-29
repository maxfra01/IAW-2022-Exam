from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user 
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import dao
from models.User import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mistero'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
   db_user = dao.get_user_by_id(user_id)
   user = User(id=db_user['id'],
   name=db_user['nome'],
   email=db_user['email'],
   password=db_user['password'])
   return user

@app.route("/")
def home():
   categorie=dao.get_all_categories()  
   serie=dao.get_all_shows()
   return render_template('home.html', categorie=categorie, serie=serie)


@app.route("/signup", methods=["POST"])
def signup():
   if request.method=="POST":
      name = request.form.get('name')
      email = request.form.get('email')
      tipo=request.form.get('type')
      password = request.form.get("password")
      print(name,email, tipo, password)

      user_in_db = dao.get_user_by_email(email,tipo)

      if user_in_db:
         flash('C\'è già un utente registrato con questa email', 'danger')
         return redirect(url_for('home'))
      else:
         new_user = {
            "name": name,
            "email": email,
            "tipo": tipo,
            "password": generate_password_hash(password,method="pbkdf2:sha256")
         }

         success = dao.add_user(new_user)

         if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('home'))
         else:
            flash('Errore nella creazione del utente: riprova!', 'danger')

   return redirect(url_for('home'))



@app.route("/login", methods=["POST"])
def login():
   if request.method=="POST":
      email=request.form.get("email")
      password=request.form.get("password")
      tipo=request.form.get("type")
      
      print(email, password, tipo)
      
      user_in_db=dao.get_user_by_email(email,tipo)
      if not user_in_db or not check_password_hash(user_in_db["password"], password):
         flash("Credenziali non valide", 'error')
         return redirect(url_for('home'))
      else:
         new_user=User()
         
         login_user(new_user)
      
   return redirect(url_for('home'))
            

      
   
   
   
   
   
   
app.run(port=5000, debug=True)