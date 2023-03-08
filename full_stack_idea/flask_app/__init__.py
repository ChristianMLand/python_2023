from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
app.secret_key = 'itsasecret'
bcrypt = Bcrypt(app)

DB = "wall_db_new"