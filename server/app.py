from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from models import db
from flask_cors import CORS
from datetime import timedelta


from routes.auth_route import init_auth_route
from routes.comment_route import init_comment_route
from routes.feed_route import init_feed_route
from routes.like_route import init_like_route
from routes.profile_route import init_profile_route
from routes.post_route import init_post_route

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'victoreslieh@gmail.com'
# app.config['MAIL_PASSWORD'] = 'drfx rbkz auvy sguh'
# app.config['MAIL_DEFAULT_SENDER'] = 'victoreslieh@gmail.com'

jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)



@app.route('/')
def index():
    return '<h1>Lively</h1>'

# Initialize routes
init_auth_route(app, bcrypt)
init_comment_route(app)
init_feed_route(app)
init_like_route(app)
init_profile_route(app)
init_post_route(app)
if __name__ == '__main__':
    app.run(port=5555, debug=True)
