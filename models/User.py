from flask_login import UserMixin
class User(UserMixin):
   def __init__(self, id, name, surname, email, tipo,  password):
      self.id = id
      self.surname=surname
      self.name = name
      self.email = email
      self.type=tipo
      self.password = password