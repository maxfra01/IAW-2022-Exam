from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user , login_required, current_user
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import dao
from models.User import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mistero'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_manager=LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Accedi per visualizzare questa pagina'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@app.route("/")
def home():
   categorie=dao.get_all_categories()  
   serie=dao.get_all_shows()
   return render_template('home.html', categorie=categorie, serie=serie)


@app.route("/signup", methods=["POST"])
def signup():
   if request.method=="POST":
      name = request.form.get('name')
      surname=request.form.get('surname')
      email = request.form.get('email')
      tipo=request.form.get('type')
      password = request.form.get("password")

      user_in_db = dao.get_user_by_email(email)

      if user_in_db:
         flash('C\'è già un utente registrato con questa email', 'danger')
         return redirect(url_for('home'))
      else:
         new_user = {
            "name": name,
            "surname": surname,
            "email": email,
            "type": tipo,
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
      user_in_db=dao.get_user_by_email(email)
      if not user_in_db or not check_password_hash(user_in_db["password"], password):
         flash("Credenziali non valide", 'danger')
         return redirect(url_for('home'))
      else:
         new=User(id=user_in_db['id'],
            name=user_in_db['name'],
            surname=user_in_db['surname'],
            email=user_in_db['email'],
            password=user_in_db['password'],
            tipo=user_in_db['type'])
         login_user(new,)
         return redirect(url_for('profile'))
      
      
@login_manager.user_loader
def load_user(user_id):
   db_user = dao.get_user_by_id(user_id)
   user = User(id=db_user['id'],
   name=db_user['name'],
   surname=db_user['surname'],
   email=db_user['email'],
   password=db_user['password'],
   tipo=db_user['type'])
   return user

      

@app.route('/profile')
@login_required
def profile():
   if current_user.type=='creatore':
      mie_serie=dao.get_my_show(current_user.id)
   else:
      mie_serie=dao.get_followed_show(current_user.id)
   return render_template('profile.html',mie_serie=mie_serie)            


@app.route('/new-show',methods=["POST"])
@login_required
def newshow():
   if request.method=='POST':
      titolo=request.form.get('title')
      categoria=request.form.get('category')
      description=request.form.get('description')
      image=request.files['image']
      if image:
         image.save('static/' + titolo.lower() + '.jpg')
      
      new_show={ 'title':titolo, 
                'category': categoria,
                'description': description,
                'image':image,
                'creator_id': current_user.id,
                'creator_name': current_user.name + " " +current_user.surname
      }
      
      success=dao.add_show(new_show)
      
      if success:
         
         flash('Creazione della serie avvenuta correttamente','success')
         return redirect(url_for('home'))
      else:
         flash('Errore nella creazione della serie', 'danger')
         return redirect(url_for('profile'))
         

@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('home'))
   
   
@app.route("/show/<int:show_id>")
def show(show_id):
   serie=dao.get_show_by_id(show_id)
   episodi=dao.get_episodes_by_showid(show_id)
   return render_template('show.html', serie=serie, episodi=episodi)
   
   
app.run(port=5000, debug=True)