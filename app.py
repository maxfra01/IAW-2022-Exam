from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_login import LoginManager, login_user
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import dao
import model

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mistero'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

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
   #categorie=dao.get_all_categories()  
   #serie=dao.get_all_shows()
   return render_template('home.html')

@app.route("/login")
def login():
   return render_template('login.html')


@app.route("/login", methods=["POST"])
def login_post():
   if request.method=="POST":
      email=request.form.get("email")
      password=request.form.get("password")
      tipo=request.form.get("tipo")
      user_in_db=dao.get_user_by_email(email)
      if not user_in_db or not check_password_hash(user_in_db["password"], password):
         flash("Credenziali non valide", 'danger')
         return redirect(url_for('login'))
      else:
         login_user()
         
   return
            
@app.route("/signup")
def signup():
   return render_template('signup.html')

@app.route("/signup", methods=["POST"])
def signup_post():
   if request.method=="POST":
      new_user=request.form.to_dict()
      
   
   
   
   
   
   
app.run(port=5000, debug=True)