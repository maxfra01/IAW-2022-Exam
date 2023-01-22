from flask import Flask, render_template, request, session, redirect, flash, url_for, abort
from flask_login import LoginManager, login_user, logout_user , login_required, current_user
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import dao
from datetime import datetime
import re
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

def check_name(name):
   pattern = '[^a-zA-Z0-9\s]'
   match = re.search(pattern, name)
   if match:
      return False
   else:
      return True

def check_email(email):
   regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
   if re.fullmatch(regex, email):
      return True
   return False


#404
@app.errorhandler(404)
def error_page(e):
   return render_template('error.html'),404

#HOME E SERIE
@app.route("/")
def home():
   categorie=dao.get_all_categories()  
   serie=dao.get_all_shows()
   return render_template('home.html', categorie=categorie, serie=serie,active_category='all')

@app.route('/<category>')
def home_by_category(category):
   if category=='all':
      return redirect(url_for('home'))
   categorie=dao.get_all_categories()
   serie=dao.get_shows_by_category(category)
   if not serie:
      abort(404)
   return render_template('home.html', categorie=categorie, serie=serie, active_category=category)

   
@app.route("/show/<int:show_id>")
def show(show_id):
   serie=dao.get_show_by_id(show_id)
   if not serie:
      abort(404)
   episodi=dao.get_episodes_by_show_id(show_id)
   commenti=dao.get_comments_by_show_id(show_id)
   seguita=0
   if current_user.is_authenticated:
      seguita= dao.check_followed_show(current_user.id,show_id)
   return render_template('show.html', serie=serie, episodi=episodi, commenti=commenti, follow=seguita)

#LOGIN
@app.route("/signup", methods=["POST"])
def signup():
   success=True
   if request.method=="POST":
      name = request.form.get('name')
      if not check_name(name) or len(name.strip())==0:
         flash('Errore, il nome non può contenere carattere speciali o essere vuoto', 'danger')
         return redirect(url_for('home'))
      surname=request.form.get('surname')
      if not check_name(surname) or len(surname.strip())==0:
         flash('Errore, il cognome non può contenere carattere speciali o essere vuoto', 'danger')
         return redirect(url_for('home'))
      email = request.form.get('email')
      if not check_email(email):
         flash('Errore, email non valida', 'danger')
         return redirect(url_for('home'))
      tipo=request.form.get('type')
      password = request.form.get("password")

      user_in_db = dao.get_user_by_email(email)

      if user_in_db:
         flash('Errore, C\'è già un utente registrato con questa email', 'danger')
         return redirect(url_for('home'))
      else:
         new_user = {
            "name": name.lstrip().rstrip(),
            "surname": surname.lstrip().rstrip(),
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
      if not check_email(email):
         flash('Errore, inserisci una mail valida', 'danger')
         return redirect(url_for('home'))
      password=request.form.get("password")
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
         login_user(new,False)
         return redirect(url_for('home'))
      
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
      
#SEGUIRE
@app.route('/follow-show/<int:show_id>')
@login_required
def follow_a_show(show_id):
   if not current_user.is_authenticated:
      flash('Per effettuare questa operazione devi essere registrato','danger')
      return redirect(url_for('show', show_id=show_id))
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
   if not current_user.is_authenticated:
      flash('Per effettuare questa operazione devi essere registrato','danger')
      return redirect(url_for('show', show_id=show_id))
   success=dao.remove_followed_show(show_id, current_user.id)
   if success:
      flash('Hai smesso di seguire la serie','success')
      return redirect(url_for('show', show_id=show_id))
   else:
      flash('Si è verificato un problema ', 'danger')
      return redirect(url_for('show', show_id=show_id))

#SERIE

@app.route('/new-show',methods=["POST"])
@login_required
def newshow():
   if current_user.type != 'creatore':
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('profile'))
   if request.method=='POST':
      titolo=request.form.get('title')
      if not titolo.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('profile'))
      categoria=request.form.get('category')
      if not categoria.strip() or not check_name(categoria):
         flash('Errore, la categoria non può essere vuota o contenere caratteri speciali', 'danger')
         return redirect(url_for('profile'))
      description=request.form.get('description')
      if not description.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('profile'))
      image=request.files['image']
      filename = secure_filename(image.filename)
      if not filename.endswith('.jpg') :
         flash('Errore, carica un\'immagine .jpg valida', 'danger')
         return redirect(url_for('profile'))
      if image:
         image.save('static/' + filename)
      
      new_show={ 'title':titolo.lstrip().rstrip(), 
                'category': categoria.lstrip().rstrip(),
                'description': description.lstrip().rstrip(),
                'image':filename,
                'creator_id': current_user.id,
                'creator_name': current_user.name + " " +current_user.surname
      }
      
      success=dao.add_show(new_show)
      
      if success:
         
         flash('Creazione della serie avvenuta correttamente','success')
         return redirect(url_for('profile'))
      else:
         flash('Errore nella creazione della serie', 'danger')
         return redirect(url_for('profile'))


@app.route('/show/edit-show/<int:show_id>', methods=['POST'])
@login_required
def edit_show(show_id):
   if current_user.type != 'creatore' or not dao.check_show_author(show_id, current_user.id):
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('show', show_id=show_id))
   
   if request.method=='POST':
      old_show=dao.get_show_by_id(show_id)
      
      nuovo_titolo=request.form.get('title')
      if not nuovo_titolo.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))
      
      nuovo_categoria=request.form.get('category')
      if not nuovo_categoria.strip() or not check_name(nuovo_categoria):
         flash('Errore, la categoria non può essere vuota o contenere caratteri speciali', 'danger')
         return redirect(url_for('show', show_id=show_id))
      
      nuova_descrizione=request.form.get('description')
      if not nuova_descrizione.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))
      
      nuova_immagine=request.files['image']
      filename=old_show['image']
      if nuova_immagine:
         filename = secure_filename(nuova_immagine.filename)
         if not filename.endswith('.jpg'):
            flash('Errore, carica un\'immagine valida','danger')
            return redirect(url_for('show', show_id=show_id))

         nuova_immagine.save('static/' + filename)
      
      new_show={'id': old_show['id'], 
                'title':nuovo_titolo.lstrip().rstrip(), 
                'category': nuovo_categoria.lstrip().rstrip(),
                'description': nuova_descrizione.lstrip().rstrip(),
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

@app.route('/delete-show/<int:show_id>', methods=["POST"])
@login_required
def delete_show(show_id):
   if current_user.type != 'creatore' or not dao.check_show_author(show_id,current_user.id):
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('profile'))
   success=dao.delete_show(show_id)
   if success:
      flash('Eliminazione della serie avvenuta correttamente','success')
      return redirect(url_for('profile'))
   else:
      flash('Errore nell\'eliminazione della serie','danger')
      return redirect(url_for('profile'))

#EPISODI
@app.route('/new-episode/<int:show_id>', methods=["POST"])
@login_required
def add_episode(show_id):
   if current_user.type != 'creatore' or not dao.check_show_author(show_id, current_user.id):
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('profile'))
   if request.method=='POST':
      titolo=request.form.get('title')
      if not titolo.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))
      descrizione=request.form.get('description')
      if not descrizione.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))
      data=request.form.get('date')
      
      if not data:
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))
        
      today=datetime.now()
      if datetime.strptime(data,'%Y-%m-%d') > today:
         flash('Errore, non puoi inserire date oltre quella odierna','danger')
         return redirect(url_for('show', show_id=show_id))
      
      audio=request.files['audio']
      filename=secure_filename(audio.filename)
      if audio:
         if not filename.endswith('.mp3'):
            flash('Errore, carica un file valido', 'danger')
            return redirect(url_for('show', show_id=show_id))
         audio.save('static/'+ filename)
      else:
         flash('Errore, carica un file valido', 'danger')
         return redirect(url_for('show', show_id=show_id))
      new_episode={
         'show_id':show_id,
         'title':titolo.lstrip().rstrip(),
         'description': descrizione.lstrip().rstrip(),
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

@app.route('/edit-episode/<int:show_id>_<int:episode_id>', methods=["POST"])
@login_required
def edit_episode(show_id, episode_id):
   if current_user.type != 'creatore' or not dao.check_show_author(show_id, current_user.id):
      flash('Non disponi dei privilegi necessari per eseguire ques\'azione', 'danger')
      return redirect(url_for('show', show_id=show_id))
   
   old_episode=dao.get_episode_by_id(episode_id)
   
   if request.method=='POST':
      titolo=request.form.get('title')
      if not titolo.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))
      descrizione=request.form.get('description')
      if not descrizione.strip():
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))
      data=request.form.get('date')
      if not data:
         flash('Errore, i campi non possono essere vuoti', 'danger')
         return redirect(url_for('show', show_id=show_id))

      today=datetime.now()
      if datetime.strptime(data,'%Y-%m-%d') > today:
         flash('Errore, non puoi inserire date oltre quella odierna','danger')
         return redirect(url_for('show', show_id=show_id))

      audio=request.files['audio']
      filename=old_episode['audio']
      if audio:
         filename=secure_filename(audio.filename)
         if not filename.endswith('.mp3'):
            flash('Errore, carica un file valido', 'danger')
            return redirect(url_for('show', show_id=show_id))
         audio.save('static/'+ filename)
      
      new_episode={
         'show_id':show_id,
         'title':titolo.lstrip().rstrip(),
         'description': descrizione.lstrip().rstrip(),
         'date': data,
         'audio': filename
      }
      
      success=dao.edit_episode_by_id(new_episode,episode_id)
      
      if success:
         flash('Episodio modificato correttamente', 'success')
         return redirect(url_for('show', show_id=show_id))
      else:
         flash('Errore nela modifica dell\'episodio', 'danger')
         return redirect(url_for('show', show_id=show_id))

@app.route('/delete-episode/<int:show_id>_<int:episode_id>', methods=["POST"])
@login_required
def delete_episode(show_id, episode_id):
   if current_user.type!='creatore' or not dao.check_show_author(show_id, current_user.id):
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
   if not current_user.is_authenticated:
      flash('Per effettuare questa operazione devi essere registrato','danger')
      return redirect(url_for('show', show_id=show_id))
   if request.method=="POST":
      commento=request.form.get('comment') 
      if not commento.strip():
         flash('Errore, inserisci un commento valido', 'danger')
         return redirect(url_for('show', show_id=show_id))  
      new_comment={
         'text': commento,
         'episode_id': episode_id,
         'user_id': current_user.id,
         'show_id': show_id,
         'author': current_user.name +' ' + current_user.surname
      }
      
      success=dao.add_comment(new_comment)
      if success:
         flash('Commento inserito correttamente','success')
         return redirect(url_for('show', show_id=show_id))
      else:
         flash('Errore nell\'inserimento del commento, riprovare','danger')
         return redirect(url_for('show', show_id=show_id))

@app.route('/edit-comment/<int:show_id>_<int:comment_id>', methods=["POST"])
@login_required
def edit_comment(show_id, comment_id):
   if not current_user.is_authenticated:
      flash('Per effettuare questa operazione devi essere registrato','danger')
      return redirect(url_for('show', show_id=show_id))
   if not dao.check_comment_author(comment_id, current_user.id):
      flash('Non disponi dei privilegi necessari per effettuare questa operazione','danger')
      return redirect(url_for('show', show_id=show_id))
   if request.method=="POST":
      commento=request.form.get('comment') 
      if not commento.strip():
         flash('Errore, inserisci un commento valido', 'danger')
         return redirect(url_for('show', show_id=show_id))    
      success=dao.edit_comment_by_id(commento, comment_id)
      if success:
         flash('Commento modificato correttamente','success')
         return redirect(url_for('show', show_id=show_id))
      else:
         flash('Errore nella modifica del commento, riprovare','danger')
         return redirect(url_for('show', show_id=show_id))

@app.route('/delete-comment/<int:show_id>_<int:comment_id>', methods=["POST"])
def delete_comment(show_id, comment_id):
   if not current_user.is_authenticated:
      flash('Per effettuare questa operazione devi essere registrato')
      return redirect(url_for('show', show_id=show_id))
   if not dao.check_comment_author(comment_id, current_user.id):
      flash('Non disponi dei privilegi necessari per effettuare questa operazione','danger')
   success=dao.delete_comment_by_id(comment_id)
   
   if success:
      flash('Commento eliminato correttamente', 'success')
      return redirect(url_for('show', show_id=show_id))
   else:
      flash('Errore nell\'eliminazione del commento, riprovare', 'danger')
      return redirect(url_for('show', show_id=show_id))
      
app.run(port=5000, debug=True)
