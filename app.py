from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from routes import blueprint

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


@app.route('/api/hello')
def index_page():
    return "Hello word"

# app.register_blueprint(blueprint)

