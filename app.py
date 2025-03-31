from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from db import db
from auth import auth
from models import User
from flask_migrate import Migrate

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = "g6KYa5PZx9yGR9nFp9WMvtHG8IXPT3z5kqxnAvSrTYc"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ADMIN@localhost/authdb'
app.config['JWT_SECRET_KEY'] = 'AyjjR3dWJGOXTOFjOuBZd7xN_3iBBZbwIoQ3WiYz_q8'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies', 'json']

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(auth)

@app.route('/')
@jwt_required(optional=True)
def home():
    current_user = get_jwt_identity()
    return render_template('index.html', current_user=current_user)

@app.route('/user-info')
@jwt_required()
def user_info():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    return {'name': user.name, 'email': user.email}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)