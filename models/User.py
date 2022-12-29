from flask_login import UserMixin
class User(UserMixin):
   def __init__(self, id, name, email, password):
      self.id = id
      self.name = name
      self.email = email
      self.password = password