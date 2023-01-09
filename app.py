from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user , login_required, current_user
from flask_session import Session
from werkzeug.utils import secure_filename
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


   
@app.route("/show/<int:show_id>")
def show(show_id):
   serie=dao.get_show_by_id(show_id)
   episodi=dao.get_episodes_by_show_id(show_id)
   commenti=dao.get_comments_by_show_id(show_id)
   return render_template('show.html', serie=serie, episodi=episodi, commenti=commenti)
   
#TODO Validare campi
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
            flash('Registrazione effettuata correttamente, effettua il login', 'success')
            return redirect(url_for('home'))
         else:
            flash('Errore nella registrazione, riprova!', 'danger')

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
      
@app.route('/logout')
@login_required
def logout():
   logout_user()
   return redirect(url_for('home'))
   
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
   serie_seguite=dao.get_followed_shows(current_user.id)
   if current_user.type=='creatore':
      mie_serie=dao.get_my_shows(current_user.id)
      return render_template('profile.html',mie_serie=mie_serie, serie_seguite=serie_seguite)            
   else:
      return render_template('profile.html', serie_seguite=serie_seguite)            
      

@app.route('/follow-show/<int:show_id>')
@login_required
def follow_a_show(show_id):
   success=dao.add_followed_show(show_id, current_user.id)
   if success:
      flash('Serie seguita correttamente','success')
      return redirect(url_for('show', show_id=show_id))
   else:
      flash('Errore nel seguire la serie', 'danger')
      return redirect(url_for('show', show_id=show_id))


@app.route('/unfollow-show/<int:show_id>')
@login_required
def unfollow_a_show(show_id):
   success=dao.remove_followed_show(show_id, current_user.id)
   if success:
      flash('Hai smesso di seguire la serie','success')
      return redirect(url_for('show', show_id=show_id))
   else:
      flash('Si è verificato un problema ', 'danger')
      return redirect(url_for('show', show_id=show_id))

#CREARE, MODIFICARE SERIE
#TODO valida campi
@app.route('/new-show',methods=["POST"])
@login_required
def newshow():
   if current_user.type != 'creatore':
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('profile'))
   if request.method=='POST':
      titolo=request.form.get('title')
      categoria=request.form.get('category')
      description=request.form.get('description')
      image=request.files['image']
      filename = secure_filename(image.filename)
      if image:
         image.save('static/' + filename)
      
      new_show={ 'title':titolo, 
                'category': categoria,
                'description': description,
                'image':filename,
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

#TODO valida campi
@app.route('/show/edit-show/<int:show_id>', methods=['POST'])
@login_required
def edit_show(show_id):
   if current_user.type != 'creatore':
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('show', show_id=show_id))
   
   if request.method=='POST':
      old_show=dao.get_show_by_id(show_id)
      nuovo_titolo=request.form.get('title')
      nuovo_categoria=request.form.get('category')
      nuova_descrizione=request.form.get('description')
      nuova_immagine=request.files['image']
      filename=old_show['image']
      if nuova_immagine:
         filename = secure_filename(nuova_immagine.filename)
         nuova_immagine.save('static/' + filename)
      
      new_show={'id': old_show['id'], 
                'title':nuovo_titolo, 
                'category': nuovo_categoria,
                'description': nuova_descrizione,
                'image':filename,
                'creator_id': current_user.id,
                'creator_name': current_user.name + " " +current_user.surname
      }
      
      success=dao.edit_show(new_show)
      
      if success:
         flash('Modifica della serie avvenuta correttamente','success')
         return redirect(url_for('show', show_id=show_id))
      else:
         flash('Errore nella modifica della serie', 'danger')
         return redirect(url_for('show', show_id=show_id))

@app.route('/delete-show/<int:show_id>')
@login_required
def delete_show(show_id):
   if current_user.type != 'creatore':
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('profile'))
   success=dao.delete_show(show_id)
   if success:
      flash('Eliminazione della serie avvenuta correttamente','success')
      return redirect(url_for('profile'))
   else:
      flash('Errore nell\'eliminazione della serie','danger')
      return redirect(url_for('profile'))

#AGGIUNGI, ELIMINA EPISODI
#TODO valida campi
@app.route('/new-episode/<int:show_id>', methods=["POST"])
@login_required
def add_episode(show_id):
   if current_user.type != 'creatore':
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('profile'))
   if request.method=='POST':
      titolo=request.form.get('title')
      descrizione=request.form.get('description')
      data=request.form.get('date')
      audio=request.files['audio']
      filename=secure_filename(audio.filename)
      if audio:
         audio.save('static/'+ filename)
         
      new_episode={
         'show_id':show_id,
         'title':titolo,
         'description': descrizione,
         'date': data,
         'audio': filename
      }
      
      success=dao.add_new_episode(new_episode,show_id)
      
      if success:
         flash('Episodio caricato correttamente', 'success')
         return redirect(url_for('show', show_id=show_id))
      else:
         flash('Errore nel caricamento dell\'episodio', 'danger')
         return redirect(url_for('show', show_id=show_id))

@app.route('/delete-episode/<int:show_id>_<int:episode_id>')
@login_required
def delete_episode(show_id, episode_id):
   if current_user.type!='creatore':
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('show', show_id=show_id))
   
   success=dao.delete_episode_by_id(episode_id)
   
   if success:
      flash('Elimazione dell\'episodio avvenuta correttamente', 'success')
      return redirect(url_for('show', show_id=show_id))
   else:
      flash('Errore nell\'eliminazione dell\'episodio', 'danger')
      return redirect(url_for('show', show_id=show_id))

#COMMENTI
@app.route('/new-comment/<int:show_id>_<int:episode_id>', methods=["POST"])
@login_required
def add_comment(show_id,episode_id):
   return redirect(url_for('show', show_id=show_id))
   
   
   
app.run(port=5000, debug=True)